#!/usr/bin/env python
# coding: utf-8

import os
import json
import base64
import hashlib
from getpass import getpass

from cryptography.fernet import Fernet, InvalidToken

# Optional: clipboard support (for auto-copy of passwords)
try:
    import pyperclip
except ImportError:
    pyperclip = None

# Try to import your quote-based password generator
try:
    # Make sure your generator file is named password_generator.py
    from password_generator import generate_password as quote_generate_password, SHOW_QUOTES
    USE_QUOTE_GENERATOR = True
except ImportError:
    USE_QUOTE_GENERATOR = False
    SHOW_QUOTES = {}

    import secrets
    import string

    def quote_generate_password(show=None):
        """
        Fallback generator if quote-based module isn't available.
        """
        chars = string.ascii_letters + string.digits
        base = "".join(secrets.choice(chars) for _ in range(14))
        base = base[0].upper() + base[1:]
        return base + "2!"


VAULT_FILE = "vault.dat"
SALT_FILE = "vault.salt"


# ========== CRYPTO HELPERS ==========

def derive_key(master_password: str, salt: bytes) -> bytes:
    """
    Derive a 32-byte key from the master password + salt using PBKDF2-HMAC-SHA256,
    then base64-encode it to be used with Fernet.
    """
    dk = hashlib.pbkdf2_hmac(
        "sha256",
        master_password.encode("utf-8"),
        salt,
        200_000,
    )
    return base64.urlsafe_b64encode(dk)


def get_fernet(master_password: str) -> Fernet:
    """
    Load or create a salt, and return a Fernet encryptor using the master password.
    """
    if os.path.exists(SALT_FILE):
        with open(SALT_FILE, "rb") as f:
            salt = f.read()
    else:
        # create new salt
        salt = os.urandom(16)
        with open(SALT_FILE, "wb") as f:
            f.write(salt)

    key = derive_key(master_password, salt)
    return Fernet(key)


# ========== VAULT HELPERS ==========

def load_vault(fernet: Fernet) -> dict:
    """
    Decrypt and load the vault from disk.
    If no vault exists yet, return an empty one.
    """
    if not os.path.exists(VAULT_FILE):
        return {"entries": []}

    with open(VAULT_FILE, "rb") as f:
        ciphertext = f.read()

    try:
        plaintext = fernet.decrypt(ciphertext)
    except InvalidToken:
        raise ValueError("Invalid master password (could not decrypt vault).")

    data = json.loads(plaintext.decode("utf-8"))
    if "entries" not in data:
        data["entries"] = []
    return data


def save_vault(fernet: Fernet, vault: dict) -> None:
    """
    Encrypt and write the vault to disk.
    """
    plaintext = json.dumps(vault, indent=2).encode("utf-8")
    ciphertext = fernet.encrypt(plaintext)
    with open(VAULT_FILE, "wb") as f:
        f.write(ciphertext)


# ========== CORE OPERATIONS ==========

def list_entries(vault: dict):
    entries = vault.get("entries", [])
    if not entries:
        print("No entries yet.\n")
        return

    print("\nSaved entries:")
    for idx, entry in enumerate(entries, start=1):
        svc = entry.get("service", "")
        usr = entry.get("username", "")
        email = entry.get("email", "")
        label = f"{svc}"
        if usr:
            label += f" | {usr}"
        if email:
            label += f" | {email}"
        print(f"  {idx}. {label}")
    print()


def find_entries_by_service(vault: dict, service_name: str):
    service_name = service_name.lower()
    return [
        entry for entry in vault.get("entries", [])
        if entry.get("service", "").lower() == service_name
    ]


def add_or_update_entry(vault: dict, fernet: Fernet):
    service = input("Service / Site name: ").strip()
    username = input("Username: ").strip()
    email = input("Email (optional): ").strip()
    phone = input("Phone (optional): ").strip()
    tags_raw = input("Tags (comma-separated, optional): ").strip()
    tags = [t.strip() for t in tags_raw.split(",")] if tags_raw else []

    use_generator = input("Generate password from quote-based generator? (y/n): ").strip().lower()
    if use_generator == "y":
        show = None
        if USE_QUOTE_GENERATOR and SHOW_QUOTES:
            # Let user pick show if they want
            choose_show = input("Use a specific show? (leave blank for random): ").strip()
            show = choose_show if choose_show else None
        password = quote_generate_password(show)
        print(f"Generated password: {password}")
    else:
        password = getpass("Password (typed, hidden): ").strip()

    note = input("Notes (optional): ").strip()
    custom1 = input("Custom field 1 (optional): ").strip()
    custom2 = input("Custom field 2 (optional): ").strip()

    # Check for existing entries with same service + username
    entries = vault.setdefault("entries", [])
    existing_indices = [
        i for i, e in enumerate(entries)
        if e.get("service", "").lower() == service.lower()
        and e.get("username", "").lower() == username.lower()
    ]

    if existing_indices:
        print(f"Found {len(existing_indices)} existing entry(ies) for this service/username.")
        overwrite = input("Overwrite the first match? (y/n): ").strip().lower()
        if overwrite == "y":
            idx = existing_indices[0]
            entries[idx] = {
                "service": service,
                "username": username,
                "email": email,
                "phone": phone,
                "password": password,
                "tags": tags,
                "note": note,
                "custom1": custom1,
                "custom2": custom2,
            }
        else:
            print("Canceled.\n")
            return
    else:
        entries.append(
            {
                "service": service,
                "username": username,
                "email": email,
                "phone": phone,
                "password": password,
                "tags": tags,
                "note": note,
                "custom1": custom1,
                "custom2": custom2,
            }
        )

    save_vault(fernet, vault)
    print("Entry saved.\n")


def view_entry(vault: dict):
    service = input("Service name to view: ").strip()
    matches = find_entries_by_service(vault, service)

    if not matches:
        print("No entry found with that name.\n")
        return

    if len(matches) > 1:
        print(f"Found {len(matches)} entries for '{service}':")
        for i, e in enumerate(matches, start=1):
            print(f"  {i}. {e.get('username', '')} | {e.get('email', '')}")
        sel = input("Choose entry number: ").strip()
        try:
            idx = int(sel) - 1
            entry = matches[idx]
        except Exception:
            print("Invalid choice.\n")
            return
    else:
        entry = matches[0]

    print("\n--- Entry ---")
    print(f"Service:  {entry.get('service', '')}")
    print(f"Username: {entry.get('username', '')}")
    print(f"Email:    {entry.get('email', '')}")
    print(f"Phone:    {entry.get('phone', '')}")
    print(f"Password: {entry.get('password', '')}")
    if entry.get("tags"):
        print(f"Tags:     {', '.join(entry['tags'])}")
    if entry.get("note"):
        print(f"Note:     {entry['note']}")
    if entry.get("custom1"):
        print(f"Custom1:  {entry['custom1']}")
    if entry.get("custom2"):
        print(f"Custom2:  {entry['custom2']}")
    print("------------\n")

    # Auto-copy to clipboard if available
    if pyperclip is not None:
        try:
            pyperclip.copy(entry.get("password", ""))
            print("(Password copied to clipboard.)\n")
        except Exception:
            pass


def delete_entry(vault: dict, fernet: Fernet):
    service = input("Service name to delete from: ").strip()
    matches = find_entries_by_service(vault, service)

    if not matches:
        print("No entries found.\n")
        return

    print(f"Found {len(matches)} entries:")
    for i, e in enumerate(matches, start=1):
        print(f"  {i}. {e.get('username', '')} | {e.get('email', '')}")

    sel = input("Choose entry number to delete (or blank to cancel): ").strip()
    if not sel:
        print("Canceled.\n")
        return

    try:
        idx = int(sel) - 1
        to_delete = matches[idx]
    except Exception:
        print("Invalid selection.\n")
        return

    confirm = input(f"Are you sure you want to delete '{to_delete.get('service')}' entry? (y/n): ").strip().lower()
    if confirm != "y":
        print("Canceled.\n")
        return

    vault["entries"] = [e for e in vault["entries"] if e is not to_delete]
    save_vault(fernet, vault)
    print("Entry deleted.\n")


def generate_password_only():
    show = None
    if USE_QUOTE_GENERATOR and SHOW_QUOTES:
        choose_show = input("Use specific show? (leave blank for random): ").strip()
        show = choose_show if choose_show else None
    pwd = quote_generate_password(show)
    print(f"Generated password: {pwd}\n")
    if pyperclip is not None:
        try:
            pyperclip.copy(pwd)
            print("(Password copied to clipboard.)\n")
        except Exception:
            pass


# ========== IMPORT FROM RAW TEXT FILE ==========

def import_from_raw_file(file_path, vault, fernet):
    """
    Import entries from a loosely formatted text file.

    Expected rough structure:

        ServiceName:
        username_or_email
        password
        optional extra info...

        (blank line)

        NextService:
        username_or_email
        password
        ...

    For each non-empty block under a service, we create an entry:
      - service  = last seen header ending with ':'
      - username = first line of block
      - password = second line of block (if exists)
      - note     = any remaining lines joined
    """
    if not os.path.exists(file_path):
        print(f"Import file not found: {file_path}\n")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    current_service = None
    block = []

    def flush_block():
        nonlocal block, current_service, vault
        if current_service is None:
            block = []
            return
        if len(block) == 0:
            return

        username = block[0].strip()
        password = block[1].strip() if len(block) >= 2 else ""
        note = "\n".join(line.strip() for line in block[2:]) if len(block) > 2 else ""

        if not username and not password:
            block = []
            return

        entry = {
            "service": current_service,
            "username": username,
            "email": "",
            "phone": "",
            "password": password,
            "tags": [],
            "note": note,
            "custom1": "",
            "custom2": "",
        }
        vault.setdefault("entries", []).append(entry)
        block = []

    for raw in lines:
        line = raw.strip()

        # Blank line separates blocks
        if line == "":
            flush_block()
            continue

        # Service header (e.g., "Google:", "Steam:", etc.)
        if line.endswith(":") and "@" not in line and "Username" not in line and "Password" not in line:
            flush_block()
            current_service = line.rstrip(":").strip()
            continue

        # Otherwise, treat as part of the current block
        block.append(line)

    # Flush last block if any
    flush_block()

    save_vault(fernet, vault)
    print("Import complete. Check entries for accuracy.\n")


# ========== MAIN LOOP ==========

def main():
    print("=== Password Manager ===")

    if os.path.exists(VAULT_FILE):
        print("Vault found. Please enter your master password.")
        master = getpass("Master password: ")
    else:
        print("No vault found. Creating a new one.")
        while True:
            pw1 = getpass("Create master password: ")
            pw2 = getpass("Confirm master password: ")
            if pw1 != pw2:
                print("Passwords do not match. Try again.\n")
            elif len(pw1) < 6:
                print("Master password too short. Use at least 6 characters.\n")
            else:
                master = pw1
                break

    fernet = get_fernet(master)

    try:
        vault = load_vault(fernet)
    except ValueError as e:
        print(f"Error: {e}")
        return

    while True:
        print("Choose an option:")
        print("  1) List entries")
        print("  2) Add / update entry")
        print("  3) View entry")
        print("  4) Delete entry")
        print("  5) Generate password only")
        print("  6) Import from raw text file")
        print("  0) Quit")

        choice = input("> ").strip()

        if choice == "1":
            list_entries(vault)
        elif choice == "2":
            add_or_update_entry(vault, fernet)
        elif choice == "3":
            view_entry(vault)
        elif choice == "4":
            delete_entry(vault, fernet)
        elif choice == "5":
            generate_password_only()
        elif choice == "6":
            path = input("Path to raw text file (default: raw_passwords.txt): ").strip()
            if not path:
                path = "raw_passwords.txt"
            import_from_raw_file(path, vault, fernet)
        elif choice == "0":
            print("Goodbye.")
            break
        else:
            print("Invalid choice, try again.\n")


if __name__ == "__main__":
    main()
