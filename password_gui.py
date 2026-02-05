#!/usr/bin/env python
# coding: utf-8

import os
import json
import base64
import hashlib
from getpass import getpass  # only used if you want CLI fallback

import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk

from cryptography.fernet import Fernet, InvalidToken

# Optional clipboard
try:
    import pyperclip
except ImportError:
    pyperclip = None

# Try to import your quote-based password generator
try:
    from password_generator import generate_password as quote_generate_password, SHOW_QUOTES
    USE_QUOTE_GENERATOR = True
except ImportError:
    USE_QUOTE_GENERATOR = False
    SHOW_QUOTES = {}

    import secrets
    import string

    def quote_generate_password(show=None):
        chars = string.ascii_letters + string.digits
        base = "".join(secrets.choice(chars) for _ in range(14))
        base = base[0].upper() + base[1:]
        return base + "2!"


VAULT_FILE = "vault.dat"
SALT_FILE = "vault.salt"


# ========== CRYPTO HELPERS ==========

def derive_key(master_password: str, salt: bytes) -> bytes:
    dk = hashlib.pbkdf2_hmac(
        "sha256",
        master_password.encode("utf-8"),
        salt,
        200_000,
    )
    return base64.urlsafe_b64encode(dk)


def get_fernet(master_password: str) -> Fernet:
    if os.path.exists(SALT_FILE):
        with open(SALT_FILE, "rb") as f:
            salt = f.read()
    else:
        salt = os.urandom(16)
        with open(SALT_FILE, "wb") as f:
            f.write(salt)

    key = derive_key(master_password, salt)
    return Fernet(key)


def load_vault(fernet: Fernet) -> dict:
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
    plaintext = json.dumps(vault, indent=2).encode("utf-8")
    ciphertext = fernet.encrypt(plaintext)
    with open(VAULT_FILE, "wb") as f:
        f.write(ciphertext)


# ========== IMPORT FROM RAW TEXT FILE ==========

def import_from_raw_file(file_path, vault: dict, fernet: Fernet):
    if not os.path.exists(file_path):
        messagebox.showerror("Import Error", f"File not found:\n{file_path}")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    current_service = None
    block = []

    def flush_block():
        nonlocal block, current_service, vault
        if current_service is None or len(block) == 0:
            block = []
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

        if line == "":
            flush_block()
            continue

        if line.endswith(":") and "@" not in line and "Username" not in line and "Password" not in line:
            flush_block()
            current_service = line.rstrip(":").strip()
            continue

        block.append(line)

    flush_block()
    save_vault(fernet, vault)
    messagebox.showinfo("Import", "Import complete.\nCheck entries for accuracy.")


# ========== PASSWORD STRENGTH SCORING ==========

def score_password(pw: str) -> str:
    length = len(pw)
    classes = 0
    if any(c.islower() for c in pw):
        classes += 1
    if any(c.isupper() for c in pw):
        classes += 1
    if any(c.isdigit() for c in pw):
        classes += 1
    if any(not c.isalnum() for c in pw):
        classes += 1

    score = length + classes * 2

    if score < 10:
        return "Weak"
    elif score < 18:
        return "Medium"
    elif score < 26:
        return "Strong"
    else:
        return "Very Strong"


# ========== GUI APP CLASS ==========

class PasswordManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title("Password Manager")
        self.geometry("900x600")

        self.fernet = None
        self.vault = {"entries": []}
        self.filtered_entries = []
        self.current_index = None  # index in filtered list

        self._build_login_screen()

    # ----- Login Screen -----

    def _build_login_screen(self):
        self.login_frame = ctk.CTkFrame(self)
        self.login_frame.pack(expand=True, fill="both", padx=40, pady=40)

        has_vault = os.path.exists(VAULT_FILE)

        title = "Unlock Vault" if has_vault else "Create Vault"
        label = ctk.CTkLabel(self.login_frame, text=title, font=ctk.CTkFont(size=24, weight="bold"))
        label.pack(pady=20)

        self.master_pw_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Master password", show="*",
                                            width=300)
        self.master_pw_entry.pack(pady=10)

        if not has_vault:
            self.master_pw_confirm_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Confirm password",
                                                        show="*", width=300)
            self.master_pw_confirm_entry.pack(pady=10)
        else:
            self.master_pw_confirm_entry = None

        btn = ctk.CTkButton(self.login_frame, text="Continue", command=self._handle_login)
        btn.pack(pady=20)

    def _handle_login(self):
        pw = self.master_pw_entry.get().strip()

        if os.path.exists(VAULT_FILE):
            # Unlock
            self.fernet = get_fernet(pw)
            try:
                self.vault = load_vault(self.fernet)
            except ValueError:
                messagebox.showerror("Error", "Invalid master password.")
                return
        else:
            # Create
            if self.master_pw_confirm_entry is None:
                messagebox.showerror("Error", "Internal error.")
                return
            pw2 = self.master_pw_confirm_entry.get().strip()
            if pw != pw2:
                messagebox.showerror("Error", "Passwords do not match.")
                return
            if len(pw) < 6:
                messagebox.showerror("Error", "Master password too short (min 6 characters).")
                return
            self.fernet = get_fernet(pw)
            self.vault = {"entries": []}
            save_vault(self.fernet, self.vault)

        self.login_frame.destroy()
        self._build_main_ui()

    # ----- Main UI -----

    def _build_main_ui(self):
        # Top frame for search and buttons
        top_frame = ctk.CTkFrame(self)
        top_frame.pack(fill="x", padx=10, pady=5)

        self.search_entry = ctk.CTkEntry(top_frame, placeholder_text="Search (service, username, email, tags)...")
        self.search_entry.pack(side="left", padx=5, pady=5, fill="x", expand=True)
        self.search_entry.bind("<KeyRelease>", lambda e: self.apply_search_filter())

        search_clear_btn = ctk.CTkButton(top_frame, text="Clear", width=80, command=self.clear_search)
        search_clear_btn.pack(side="left", padx=5)

        import_btn = ctk.CTkButton(top_frame, text="Import Raw", width=100, command=self.import_raw_dialog)
        import_btn.pack(side="right", padx=5)

        gen_btn = ctk.CTkButton(top_frame, text="Generate Password", width=150, command=self.generate_password_only)
        gen_btn.pack(side="right", padx=5)

        # Middle split frame
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Left: list of entries
        left_frame = ctk.CTkFrame(main_frame, width=250)
        left_frame.pack(side="left", fill="y", padx=5, pady=5)
        left_frame.pack_propagate(False)

        label = ctk.CTkLabel(left_frame, text="Entries", font=ctk.CTkFont(size=18, weight="bold"))
        label.pack(pady=5)

        self.listbox = tk.Listbox(left_frame, height=25)
        self.listbox.pack(fill="both", expand=True, padx=5, pady=5)
        self.listbox.bind("<<ListboxSelect>>", self.on_select_entry)

        # Buttons under list
        btn_frame = ctk.CTkFrame(left_frame)
        btn_frame.pack(fill="x", pady=5)

        add_btn = ctk.CTkButton(btn_frame, text="Add / Edit", command=self.open_add_edit_window)
        add_btn.pack(side="left", expand=True, fill="x", padx=2)

        del_btn = ctk.CTkButton(btn_frame, text="Delete", command=self.delete_selected_entry)
        del_btn.pack(side="left", expand=True, fill="x", padx=2)

        # Right: details
        right_frame = ctk.CTkFrame(main_frame)
        right_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        self.detail_service = ctk.CTkLabel(right_frame, text="Service:", anchor="w")
        self.detail_service.pack(fill="x", padx=5, pady=2)

        self.detail_username = ctk.CTkLabel(right_frame, text="Username:", anchor="w")
        self.detail_username.pack(fill="x", padx=5, pady=2)

        self.detail_email = ctk.CTkLabel(right_frame, text="Email:", anchor="w")
        self.detail_email.pack(fill="x", padx=5, pady=2)

        self.detail_phone = ctk.CTkLabel(right_frame, text="Phone:", anchor="w")
        self.detail_phone.pack(fill="x", padx=5, pady=2)

        # Password row with show/copy
        pw_row = ctk.CTkFrame(right_frame)
        pw_row.pack(fill="x", padx=5, pady=2)

        self.detail_password = ctk.CTkLabel(pw_row, text="Password:", anchor="w")
        self.detail_password.pack(side="left", fill="x", expand=True)

        self.show_pw = False
        self.current_pw_value = ""
        self.pw_show_btn = ctk.CTkButton(pw_row, text="Show", width=70, command=self.toggle_show_password)
        self.pw_show_btn.pack(side="left", padx=3)

        self.pw_copy_btn = ctk.CTkButton(pw_row, text="Copy", width=70, command=self.copy_password_to_clipboard)
        self.pw_copy_btn.pack(side="left", padx=3)

        self.detail_strength = ctk.CTkLabel(right_frame, text="Strength: ", anchor="w")
        self.detail_strength.pack(fill="x", padx=5, pady=2)

        self.detail_tags = ctk.CTkLabel(right_frame, text="Tags:", anchor="w")
        self.detail_tags.pack(fill="x", padx=5, pady=2)

        self.detail_note_label = ctk.CTkLabel(right_frame, text="Notes:", anchor="w")
        self.detail_note_label.pack(fill="x", padx=5, pady=(8, 0))

        self.detail_note = ctk.CTkTextbox(right_frame, height=120)
        self.detail_note.pack(fill="both", expand=True, padx=5, pady=2)

        self.detail_custom1 = ctk.CTkLabel(right_frame, text="Custom 1:", anchor="w")
        self.detail_custom1.pack(fill="x", padx=5, pady=2)

        self.detail_custom2 = ctk.CTkLabel(right_frame, text="Custom 2:", anchor="w")
        self.detail_custom2.pack(fill="x", padx=5, pady=2)

        self.refresh_entry_list()

    # ----- Helper Methods -----

    def refresh_entry_list(self):
        self.filtered_entries = self.apply_filter_internal(self.search_entry.get().strip())
        self.listbox.delete(0, tk.END)
        for entry in self.filtered_entries:
            svc = entry.get("service", "")
            usr = entry.get("username", "")
            email = entry.get("email", "")
            label = svc
            if usr:
                label += f" | {usr}"
            if email:
                label += f" | {email}"
            self.listbox.insert(tk.END, label)
        self.current_index = None
        self.clear_details()

    def apply_filter_internal(self, query: str):
        entries = self.vault.get("entries", [])
        if not query:
            return entries
        q = query.lower()
        results = []
        for e in entries:
            svc = e.get("service", "").lower()
            usr = e.get("username", "").lower()
            email = e.get("email", "").lower()
            tags = ",".join(e.get("tags", [])).lower()
            # simple fuzzy-like: any substring match in fields
            if q in svc or q in usr or q in email or q in tags:
                results.append(e)
        return results

    def apply_search_filter(self):
        self.refresh_entry_list()

    def clear_search(self):
        self.search_entry.delete(0, tk.END)
        self.refresh_entry_list()

    def on_select_entry(self, event=None):
        sel = self.listbox.curselection()
        if not sel:
            self.current_index = None
            self.clear_details()
            return
        idx = sel[0]
        self.current_index = idx
        entry = self.filtered_entries[idx]
        self.show_entry_details(entry)

    def clear_details(self):
        self.detail_service.configure(text="Service:")
        self.detail_username.configure(text="Username:")
        self.detail_email.configure(text="Email:")
        self.detail_phone.configure(text="Phone:")
        self.detail_password.configure(text="Password: ********")
        self.current_pw_value = ""
        self.show_pw = False
        self.pw_show_btn.configure(text="Show")
        self.detail_strength.configure(text="Strength:")
        self.detail_tags.configure(text="Tags:")
        self.detail_note.delete("1.0", tk.END)
        self.detail_custom1.configure(text="Custom 1:")
        self.detail_custom2.configure(text="Custom 2:")

    def show_entry_details(self, entry: dict):
        self.detail_service.configure(text=f"Service: {entry.get('service', '')}")
        self.detail_username.configure(text=f"Username: {entry.get('username', '')}")
        self.detail_email.configure(text=f"Email: {entry.get('email', '')}")
        self.detail_phone.configure(text=f"Phone: {entry.get('phone', '')}")

        pw = entry.get("password", "")
        self.current_pw_value = pw
        masked = "*" * len(pw) if pw else ""
        self.detail_password.configure(text=f"Password: {masked}")

        strength = score_password(pw) if pw else "N/A"
        self.detail_strength.configure(text=f"Strength: {strength}")

        tags = entry.get("tags", [])
        self.detail_tags.configure(text=f"Tags: {', '.join(tags) if tags else ''}")

        self.detail_note.delete("1.0", tk.END)
        if entry.get("note"):
            self.detail_note.insert("1.0", entry["note"])

        self.detail_custom1.configure(text=f"Custom 1: {entry.get('custom1', '')}")
        self.detail_custom2.configure(text=f"Custom 2: {entry.get('custom2', '')}")

    def toggle_show_password(self):
        if not self.current_pw_value:
            return
        self.show_pw = not self.show_pw
        if self.show_pw:
            self.detail_password.configure(text=f"Password: {self.current_pw_value}")
            self.pw_show_btn.configure(text="Hide")
        else:
            masked = "*" * len(self.current_pw_value)
            self.detail_password.configure(text=f"Password: {masked}")
            self.pw_show_btn.configure(text="Show")

    def copy_password_to_clipboard(self):
        if not self.current_pw_value:
            return
        if pyperclip is not None:
            try:
                pyperclip.copy(self.current_pw_value)
                messagebox.showinfo("Copied", "Password copied to clipboard.")
            except Exception:
                messagebox.showwarning("Clipboard", "Could not copy to clipboard.")
        else:
            self.clipboard_clear()
            self.clipboard_append(self.current_pw_value)
            messagebox.showinfo("Copied", "Password copied to clipboard (tkinter clipboard).")

    # ----- Add/Edit/Delete -----

    def open_add_edit_window(self):
        # if something selected, edit that entry; else new
        entry_to_edit = None
        if self.current_index is not None and self.filtered_entries:
            entry_to_edit = self.filtered_entries[self.current_index]

        win = ctk.CTkToplevel(self)
        win.title("Add / Edit Entry")
        win.geometry("400x500")
        win.grab_set()

        def get_val(key, default=""):
            return entry_to_edit.get(key, default) if entry_to_edit else default

        svc_entry = ctk.CTkEntry(win, placeholder_text="Service / Site", width=300)
        svc_entry.insert(0, get_val("service"))
        svc_entry.pack(pady=5)

        user_entry = ctk.CTkEntry(win, placeholder_text="Username", width=300)
        user_entry.insert(0, get_val("username"))
        user_entry.pack(pady=5)

        email_entry = ctk.CTkEntry(win, placeholder_text="Email", width=300)
        email_entry.insert(0, get_val("email"))
        email_entry.pack(pady=5)

        phone_entry = ctk.CTkEntry(win, placeholder_text="Phone", width=300)
        phone_entry.insert(0, get_val("phone"))
        phone_entry.pack(pady=5)

        pw_entry = ctk.CTkEntry(win, placeholder_text="Password (leave blank to keep / generate)", show="*", width=300)
        pw_entry.pack(pady=5)

        tags_entry = ctk.CTkEntry(win, placeholder_text="Tags (comma-separated)", width=300)
        existing_tags = get_val("tags", [])
        if existing_tags:
            tags_entry.insert(0, ", ".join(existing_tags))
        tags_entry.pack(pady=5)

        custom1_entry = ctk.CTkEntry(win, placeholder_text="Custom field 1", width=300)
        custom1_entry.insert(0, get_val("custom1"))
        custom1_entry.pack(pady=5)

        custom2_entry = ctk.CTkEntry(win, placeholder_text="Custom field 2", width=300)
        custom2_entry.insert(0, get_val("custom2"))
        custom2_entry.pack(pady=5)

        note_label = ctk.CTkLabel(win, text="Notes:")
        note_label.pack()
        note_text = ctk.CTkTextbox(win, height=90, width=340)
        if get_val("note"):
            note_text.insert("1.0", get_val("note"))
        note_text.pack(pady=5)

        # Generator controls
        gen_frame = ctk.CTkFrame(win)
        gen_frame.pack(fill="x", pady=5)

        gen_var = tk.BooleanVar(value=False)
        gen_check = ctk.CTkCheckBox(gen_frame, text="Generate from quote", variable=gen_var)
        gen_check.pack(side="left", padx=5)

        show_entry = ctk.CTkEntry(gen_frame, placeholder_text="Show (blank=random)", width=150)
        show_entry.pack(side="left", padx=5)

        def save_entry():
            service = svc_entry.get().strip()
            username = user_entry.get().strip()
            email = email_entry.get().strip()
            phone = phone_entry.get().strip()
            tags_raw = tags_entry.get().strip()
            tags = [t.strip() for t in tags_raw.split(",")] if tags_raw else []

            # Determine password
            pw_existing = entry_to_edit.get("password", "") if entry_to_edit else ""
            if gen_var.get():
                show_name = show_entry.get().strip() or None
                password = quote_generate_password(show_name)
            else:
                typed = pw_entry.get()
                if typed:
                    password = typed
                else:
                    password = pw_existing

            note_val = note_text.get("1.0", tk.END).strip()
            custom1 = custom1_entry.get().strip()
            custom2 = custom2_entry.get().strip()

            if not service:
                messagebox.showerror("Error", "Service name is required.")
                return

            if "entries" not in self.vault:
                self.vault["entries"] = []

            if entry_to_edit is not None:
                # Update existing
                entry_to_edit["service"] = service
                entry_to_edit["username"] = username
                entry_to_edit["email"] = email
                entry_to_edit["phone"] = phone
                entry_to_edit["password"] = password
                entry_to_edit["tags"] = tags
                entry_to_edit["note"] = note_val
                entry_to_edit["custom1"] = custom1
                entry_to_edit["custom2"] = custom2
            else:
                self.vault["entries"].append(
                    {
                        "service": service,
                        "username": username,
                        "email": email,
                        "phone": phone,
                        "password": password,
                        "tags": tags,
                        "note": note_val,
                        "custom1": custom1,
                        "custom2": custom2,
                    }
                )

            save_vault(self.fernet, self.vault)
            self.refresh_entry_list()
            win.destroy()

        save_btn = ctk.CTkButton(win, text="Save", command=save_entry)
        save_btn.pack(pady=10)

    def delete_selected_entry(self):
        if self.current_index is None or not self.filtered_entries:
            messagebox.showinfo("Delete", "No entry selected.")
            return
        entry = self.filtered_entries[self.current_index]
        svc = entry.get("service", "")
        usr = entry.get("username", "")
        if not messagebox.askyesno("Delete", f"Delete entry for:\n{svc} ({usr})?"):
            return

        # Remove from vault entries
        self.vault["entries"] = [e for e in self.vault["entries"] if e is not entry]
        save_vault(self.fernet, self.vault)
        self.refresh_entry_list()

    # ----- Generate Password Only -----

    def generate_password_only(self):
        show = None
        if USE_QUOTE_GENERATOR and SHOW_QUOTES:
            # Small dialog to ask for show
            top = ctk.CTkToplevel(self)
            top.title("Generate Password")
            top.geometry("360x160")
            top.grab_set()

            lbl = ctk.CTkLabel(top, text="Show name (blank = random):")
            lbl.pack(pady=10)

            show_entry = ctk.CTkEntry(top, width=250)
            show_entry.pack(pady=5)

            result_label = ctk.CTkLabel(top, text="")
            result_label.pack(pady=5)

            def do_gen():
                name = show_entry.get().strip() or None
                pw = quote_generate_password(name)
                result_label.configure(text=pw)
                if pyperclip is not None:
                    try:
                        pyperclip.copy(pw)
                    except Exception:
                        pass

            btn = ctk.CTkButton(top, text="Generate", command=do_gen)
            btn.pack(pady=5)
        else:
            pw = quote_generate_password(None)
            if pyperclip is not None:
                try:
                    pyperclip.copy(pw)
                except Exception:
                    pass
            messagebox.showinfo("Generated Password", f"{pw}\n\nCopied to clipboard (if available).")

    # ----- Import Dialog -----

    def import_raw_dialog(self):
        # Simple prompt; you can enhance with file dialog if you want
        path = ctk.CTkInputDialog(title="Import Raw File", text="Path to raw text file:")
        file_path = path.get_input()
        if not file_path:
            return
        import_from_raw_file(file_path, self.vault, self.fernet)
        self.refresh_entry_list()


if __name__ == "__main__":
    app = PasswordManagerApp()
    app.mainloop()
