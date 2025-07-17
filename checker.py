import tkinter as tk
import math
import re

def calculate_entropy(password):
    charset_size = 0
    if re.search(r'[a-z]', password): charset_size += 26
    if re.search(r'[A-Z]', password): charset_size += 26
    if re.search(r'[0-9]', password): charset_size += 10
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password): charset_size += 32
    return len(password) * math.log2(charset_size) if charset_size else 0

def get_strength(entropy, password):
    if len(password) < 8:
        return "Too Short", "#e57373"
    elif entropy < 28:
        return "Very Weak", "#f44336"
    elif entropy < 36:
        return "Weak", "#ff9800"
    elif entropy < 60:
        return "Moderate", "#ffeb3b"
    else:
        return "Strong", "#4caf50"

def check_password():
    password = entry.get()
    if not password:
        strength_label.config(text="Enter a password to check", fg="#666666")
        entropy_label.config(text="")
        update_requirements("")
        return

    entropy = calculate_entropy(password)
    strength, color = get_strength(entropy, password)

    strength_label.config(text=f"Strength: {strength}", fg=color)
    entropy_label.config(text=f"Entropy: {entropy:.1f} bits")
    update_requirements(password)

def update_requirements(password):
    requirements = [
        ("✓ Lowercase letters" if re.search(r'[a-z]', password) else "✗ Lowercase letters", 
         "#4caf50" if re.search(r'[a-z]', password) else "#e57373"),
        ("✓ Uppercase letters" if re.search(r'[A-Z]', password) else "✗ Uppercase letters",
         "#4caf50" if re.search(r'[A-Z]', password) else "#e57373"),
        ("✓ Numbers" if re.search(r'[0-9]', password) else "✗ Numbers",
         "#4caf50" if re.search(r'[0-9]', password) else "#e57373"),
        ("✓ Special characters" if re.search(r'[!@#$%^&*(),.?\":{}|<>]', password) else "✗ Special characters",
         "#4caf50" if re.search(r'[!@#$%^&*(),.?\":{}|<>]', password) else "#e57373"),
        ("✓ At least 8 characters" if len(password) >= 8 else "✗ At least 8 characters",
         "#4caf50" if len(password) >= 8 else "#e57373")
    ]
    
    result_text = ""
    for req, color in requirements:
        result_text += f"{req}\n"
    detail_label.config(text=result_text)

# GUI Setup
app = tk.Tk()
app.title("🔐 Password Strength Checker")
app.configure(bg="#eceff1")
app.geometry("500x520")
app.minsize(500, 520)

# Center the window
app.update_idletasks()
x = (app.winfo_screenwidth() // 2) - (500 // 2)
y = (app.winfo_screenheight() // 2) - (520 // 2)
app.geometry(f"500x520+{x}+{y}")

# Title
tk.Label(app, text="🔒 Password Strength Checker",
         font=("Segoe UI", 18, "bold"),
         bg="#eceff1",
         fg="#263238").pack(pady=20)

# Input Frame
input_frame = tk.Frame(app, bg="#ffffff", relief="groove", bd=1)
input_frame.pack(fill="x", padx=20, pady=10)

tk.Label(input_frame, text="Enter your password:",
         font=("Segoe UI", 12),
         bg="#ffffff").pack(anchor="w", padx=15, pady=(15, 5))

entry = tk.Entry(input_frame, font=("Segoe UI", 12), show="*", width=30, relief="flat")
entry.pack(padx=15, pady=(0, 15))

# Check Button
tk.Button(app, text="Check Password Strength",
          font=("Segoe UI", 12, "bold"),
          bg="#007acc",
          fg="white",
          relief="flat",
          padx=20,
          pady=10,
          command=check_password).pack(pady=10)

# Results Frame
results_frame = tk.Frame(app, bg="#ffffff", relief="groove", bd=1)
results_frame.pack(fill="both", expand=True, padx=20, pady=10)

strength_label = tk.Label(results_frame,
                          text="Enter a password to check",
                          font=("Segoe UI", 14, "bold"),
                          bg="#ffffff",
                          fg="#666666")
strength_label.pack(pady=(20, 5))

entropy_label = tk.Label(results_frame,
                         text="",
                         font=("Segoe UI", 10),
                         bg="#ffffff",
                         fg="#666666")
entropy_label.pack(pady=(0, 10))

tk.Label(results_frame, text="Requirements:",
         font=("Segoe UI", 11, "bold"),
         bg="#ffffff",
         fg="#333333").pack(anchor="w", padx=15, pady=(10, 5))

detail_label = tk.Label(results_frame,
                        text="",
                        font=("Segoe UI", 10),
                        bg="#ffffff",
                        fg="#666666",
                        justify="left")
detail_label.pack(anchor="w", padx=15, pady=(0, 10))

# Bind Enter key
app.bind('<Return>', lambda event: check_password())

app.mainloop()
