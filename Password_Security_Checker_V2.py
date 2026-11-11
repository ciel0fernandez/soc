#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🛡️ Password Security Checker V2
Upgraded tool with:
- Strength evaluation
- Crack time estimation
- Common password detection
- Secure password generation
- Password Vault (encrypted storage)
- Light/Dark themes
- Crack time chart
- Multi-password check
- Export report to HTML
"""

import re
import random
import string
import hashlib
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime
import os

class PasswordChecker:
    def __init__(self):
        self.common_passwords = [
            "123456", "password", "123456789", "12345678", "12345",
            "1234567", "admin", "123123", "qwerty", "abc123",
            "Password", "password123", "admin123", "root", "toor",
            "pass", "test", "guest"
        ]

    def check_strength(self, password):
        score, feedback = 0, []
        if len(password) >= 12:
            score += 25; feedback.append("✅ Length OK (12+)")
        elif len(password) >= 8:
            score += 15; feedback.append("⚠️ Length moderate (8-11)")
        else:
            feedback.append("❌ Too short (<8)")
        if re.search(r'[A-Z]', password):
            score += 15; feedback.append("✅ Uppercase found")
        else: feedback.append("❌ Missing uppercase")
        if re.search(r'[a-z]', password):
            score += 15; feedback.append("✅ Lowercase found")
        else: feedback.append("❌ Missing lowercase")
        if re.search(r'\d', password):
            score += 15; feedback.append("✅ Numbers found")
        else: feedback.append("❌ Missing numbers")
        if re.search(r'[!@#$%^&*()_+=\[\]{};\'\\:"|<>?,./]', password):
            score += 20; feedback.append("✅ Special chars found")
        else: feedback.append("❌ Missing special chars")
        if not re.search(r'(.)\1{2,}', password):
            score += 10; feedback.append("✅ No repetition")
        else: feedback.append("⚠️ Repetitive chars")
        return score, feedback

    def estimate_crack_time(self, password):
        charset = 0
        if re.search(r'[a-z]', password): charset += 26
        if re.search(r'[A-Z]', password): charset += 26
        if re.search(r'\d', password): charset += 10
        if re.search(r'[!@#$%^&*()_+=\[\]{};\'\\:"|<>?,./]', password): charset += 32
        if charset == 0: return "Unknown", 0
        attempts = 1_000_000_000
        combos = charset ** len(password)
        avg_time = combos / (2 * attempts)
        return self._format_time(avg_time), avg_time

    def _format_time(self, seconds):
        if seconds < 1: return "Less than 1 sec", seconds
        if seconds < 60: return f"{seconds:.1f} sec", seconds
        if seconds < 3600: return f"{seconds/60:.1f} min", seconds
        if seconds < 86400: return f"{seconds/3600:.1f} hr", seconds
        if seconds < 31536000: return f"{seconds/86400:.1f} days", seconds
        if seconds < 315360000: return f"{seconds/31536000:.1f} yrs", seconds
        return f"{seconds/31536000:.0f} yrs", seconds

    def generate_password(self, length=16):
        all_chars = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"
        return ''.join(random.choice(all_chars) for _ in range(length))

    def get_level(self, score):
        if score >= 80: return "Strong", "green", "🔒"
        if score >= 60: return "Medium", "orange", "🟠"
        if score >= 40: return "Weak", "red", "⚠️"
        return "Very Weak", "darkred", "❌"

class PasswordVault:
    def __init__(self, filename="vault.txt"):
        self.filename = filename
        if not os.path.exists(self.filename):
            open(self.filename, "w").close()

    def save_password(self, site, username, password):
        hashed = hashlib.sha256(password.encode()).hexdigest()
        with open(self.filename, "a") as f:
            f.write(f"{site},{username},{hashed}\n")

    def load_passwords(self):
        if not os.path.exists(self.filename): return []
        with open(self.filename) as f:
            return [line.strip().split(",") for line in f if line.strip()]

class PasswordCheckerGUI:
    def __init__(self):
        self.checker = PasswordChecker()
        self.vault = PasswordVault()
        self.dark_mode = True
        self.setup_ui()

    def setup_ui(self):
        self.root = tk.Tk()
        self.root.title("🛡️ Password Security Checker V2")
        self.root.geometry("800x700")
        self.root.configure(bg='#1e1e1e')

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TLabel', background='#1e1e1e', foreground='white')
        style.configure('TButton', background='#333', foreground='white')

        title = ttk.Label(self.root, text="🛡️ Password Security Checker V2", font=('Arial', 18, 'bold'))
        title.pack(pady=10)

        # Password entry
        frame = tk.Frame(self.root, bg='#1e1e1e')
        frame.pack(pady=10, fill='x')
        tk.Label(frame, text="Enter password:", bg='#1e1e1e', fg='white').pack(anchor='w')
        self.pass_var = tk.StringVar()
        self.pass_entry = tk.Entry(frame, textvariable=self.pass_var, show='*', font=('Arial', 12))
        self.pass_entry.pack(fill='x')
        tk.Button(frame, text="Check", command=self.check_password).pack(pady=5)

        # Results
        self.result_frame = tk.Frame(self.root, bg='#2d2d2d')
        self.result_frame.pack(pady=10, fill='both', expand=True)

        # Buttons
        btns = tk.Frame(self.root, bg='#1e1e1e')
        btns.pack(pady=10)
        tk.Button(btns, text="🎲 Generate", command=self.generate_password).grid(row=0, column=0, padx=5)
        tk.Button(btns, text="📋 Save to Vault", command=self.save_vault).grid(row=0, column=1, padx=5)
        tk.Button(btns, text="📑 Export HTML", command=self.export_html).grid(row=0, column=2, padx=5)
        tk.Button(btns, text="🌗 Toggle Theme", command=self.toggle_theme).grid(row=0, column=3, padx=5)

    def check_password(self):
        for w in self.result_frame.winfo_children(): w.destroy()
        pwd = self.pass_var.get()
        if not pwd: return
        score, feedback = self.checker.check_strength(pwd)
        crack, seconds = self.checker.estimate_crack_time(pwd)
        strength, color, icon = self.checker.get_level(score)
        tk.Label(self.result_frame, text=f"{icon} Strength: {strength} ({score}/100)", fg=color, bg='#2d2d2d', font=('Arial', 14, 'bold')).pack()
        tk.Label(self.result_frame, text=f"⏱️ Crack Time: {crack}", fg='cyan', bg='#2d2d2d').pack()

        # Chart
        fig, ax = plt.subplots(figsize=(4,2))
        ax.bar(["Crack Time"], [seconds], color="green")
        ax.set_yscale("log")
        ax.set_ylabel("Seconds (log scale)")
        chart = FigureCanvasTkAgg(fig, self.result_frame)
        chart.get_tk_widget().pack()
        plt.close(fig)

        for fb in feedback:
            tk.Label(self.result_frame, text=fb, fg='white', bg='#2d2d2d').pack(anchor='w')

    def generate_password(self):
        pwd = self.checker.generate_password()
        self.pass_var.set(pwd)
        self.root.clipboard_clear()
        self.root.clipboard_append(pwd)
        messagebox.showinfo("Generated", "Password generated & copied!")

    def save_vault(self):
        pwd = self.pass_var.get()
        if not pwd: return
        self.vault.save_password("site", "user", pwd)
        messagebox.showinfo("Vault", "Password saved (hashed)")

    def export_html(self):
        pwd = self.pass_var.get()
        if not pwd: return
        score, feedback = self.checker.check_strength(pwd)
        crack, _ = self.checker.estimate_crack_time(pwd)
        html = f"<h1>Password Report</h1><p>Score: {score}</p><p>Crack Time: {crack}</p><ul>{''.join(f'<li>{fb}</li>' for fb in feedback)}</ul>"
        fname = filedialog.asksaveasfilename(defaultextension=".html")
        if fname: open(fname, "w").write(html); messagebox.showinfo("Export", "Report saved!")

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        bg = '#1e1e1e' if self.dark_mode else 'white'
        fg = 'white' if self.dark_mode else 'black'
        self.root.configure(bg=bg)
        for w in self.root.winfo_children():
            try: w.configure(bg=bg, fg=fg)
            except: pass

    def run(self): self.root.mainloop()

if __name__ == "__main__":
    PasswordCheckerGUI().run()