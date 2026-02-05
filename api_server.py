# api_server.py
import os
import time
import json
import secrets
from functools import wraps
from flask import Flask, request, jsonify, send_from_directory

import password_manager as pm  # your existing file

APP_DIR = os.path.dirname(os.path.abspath(__file__))

# Simple in-memory sessions: token -> fernet
SESSIONS = {}
SESSION_TTL_SECONDS = 60 * 30  # 30 minutes
SESSION_EXP = {}              # token -> epoch seconds

VAULT_VERSION_FILE = os.path.join(APP_DIR, "vault.version")

def _get_version() -> int:
    try:
        with open(VAULT_VERSION_FILE, "r", encoding="utf-8") as f:
            return int(f.read().strip() or "1")
    except FileNotFoundError:
        return 1
    except Exception:
        return 1

def _bump_version() -> int:
    v = _get_version() + 1
    with open(VAULT_VERSION_FILE, "w", encoding="utf-8") as f:
        f.write(str(v))
    return v

def _normalize_entry(entry: dict) -> dict:
    # Ensure all keys exist and types are sane
    tags = entry.get("tags", [])
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",") if t.strip()]

    return {
        "service": (entry.get("service") or "").strip(),
        "username": (entry.get("username") or "").strip(),
        "email": (entry.get("email") or "").strip(),
        "phone": (entry.get("phone") or "").strip(),
        "tags": tags,
        "password": (entry.get("password") or ""),
        "note": (entry.get("note") or "").strip(),
        "custom1": (entry.get("custom1") or "").strip(),
        "custom2": (entry.get("custom2") or "").strip(),
    }

def _entry_key(e: dict) -> tuple:
    # Your unique key: service + username (case-insensitive)
    return (e.get("service", "").lower(), e.get("username", "").lower())

def require_auth(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization", "").replace("Bearer ", "").strip()
        if not token:
            return jsonify({"error": "missing token"}), 401

        exp = SESSION_EXP.get(token)
        if not exp or exp < time.time():
            # expired or unknown
            SESSIONS.pop(token, None)
            SESSION_EXP.pop(token, None)
            return jsonify({"error": "token expired"}), 401

        fernet = SESSIONS.get(token)
        if not fernet:
            return jsonify({"error": "invalid token"}), 401

        # refresh sliding TTL
        SESSION_EXP[token] = time.time() + SESSION_TTL_SECONDS
        return fn(fernet, *args, **kwargs)
    return wrapper

app = Flask(__name__, static_folder="pwa", static_url_path="/")

# --------------------
# PWA static hosting
# Put your PWA files inside ./pwa (index.html, app.js, sw.js, manifest.json, icons...)
# --------------------
@app.get("/")
def serve_index():
    return send_from_directory(os.path.join(APP_DIR, "pwa"), "index.html")

@app.get("/<path:path>")
def serve_static(path):
    return send_from_directory(os.path.join(APP_DIR, "pwa"), path)

# --------------------
# API
# --------------------
@app.post("/api/login")
def login():
    data = request.get_json(force=True) or {}
    master_password = data.get("master_password", "")

    try:
        fernet = pm.get_fernet(master_password)
        # prove it can decrypt vault (or create empty)
        vault = pm.load_vault(fernet)
    except Exception:
        return jsonify({"error": "invalid password"}), 401

    token = secrets.token_urlsafe(32)
    SESSIONS[token] = fernet
    SESSION_EXP[token] = time.time() + SESSION_TTL_SECONDS

    return jsonify({
        "token": token,
        "version": _get_version(),
        "count": len(vault.get("entries", [])),
    })

@app.get("/api/snapshot")
@require_auth
def snapshot(fernet):
    vault = pm.load_vault(fernet)
    entries = vault.get("entries", [])
    # IMPORTANT: this returns decrypted entries (includes passwords)
    # Use HTTPS.
    return jsonify({
        "version": _get_version(),
        "entries": entries
    })

@app.post("/api/apply-ops")
@require_auth
def apply_ops(fernet):
    data = request.get_json(force=True) or {}
    ops = data.get("ops", [])

    vault = pm.load_vault(fernet)
    entries = vault.setdefault("entries", [])

    # Build an index for quick upsert/delete
    idx = { _entry_key(e): i for i, e in enumerate(entries) }

    for op in ops:
        op_type = (op.get("type") or "").lower()
        payload = _normalize_entry(op.get("payload") or {})
        k = _entry_key(payload)

        if op_type in ("add", "upsert", "update"):
            if not payload["service"] or not payload["username"]:
                return jsonify({"error": "service and username required"}), 400

            if k in idx:
                entries[idx[k]] = payload
            else:
                entries.append(payload)
                idx[k] = len(entries) - 1

        elif op_type == "delete":
            # delete by service+username
            if k in idx:
                del entries[idx[k]]
                # rebuild index after delete
                idx = { _entry_key(e): i for i, e in enumerate(entries) }
        else:
            return jsonify({"error": f"unknown op type: {op_type}"}), 400

    pm.save_vault(fernet, vault)
    new_version = _bump_version()

    return jsonify({"ok": True, "version": new_version, "count": len(entries)})

@app.get("/api/metadata")
@require_auth
def metadata(fernet):
    return jsonify({"version": _get_version(), "server_time": int(time.time())})

if __name__ == "__main__":
    # Run with HTTPS in real usage (recommended for iPhone PWAs).
    # Example once you have cert.pem/key.pem:
    # app.run(host="0.0.0.0", port=5443, ssl_context=("cert.pem", "key.pem"))
    app.run(host="0.0.0.0", port=5000, debug=True)