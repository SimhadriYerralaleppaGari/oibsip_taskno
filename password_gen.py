import tkinter as tk
from tkinter import messagebox, ttk
import random
import string
import pyperclip

# Function to generate password
def generate_password():
    try:
        length = int(length_entry.get())
        if length < 8:
            messagebox.showwarning("Warning", "Password length should be at least 8 characters")
            return
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number for password length")
        return

    # Check which character types are selected
    selected_chars = ""
    if lowercase_var.get():
        selected_chars += string.ascii_lowercase
    if uppercase_var.get():
        selected_chars += string.ascii_uppercase
    if digits_var.get():
        selected_chars += string.digits
    if symbols_var.get():
        selected_chars += string.punctuation
    
    if not selected_chars:
        messagebox.showwarning("Warning", "Please select at least one character type")
        return

    # Generate password
    password = ''.join(random.choice(selected_chars) for _ in range(length))
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)

# Function to copy password to clipboard
def copy_to_clipboard():
    password = password_entry.get()
    if password:
        pyperclip.copy(password)
        messagebox.showinfo("Copied", "Password copied to clipboard")
    else:
        messagebox.showerror("Error", "No password to copy")

# Modernize the GUI appearance
def create_ui(root):
    root.title("Advanced Password Generator")
    root.geometry("400x450")
    root.configure(bg="#f0f0f0")
    root.resizable(False, False)

    # Title label
    title_label = tk.Label(root, text="Password Generator", font=("Arial", 20, "bold"), bg="#f0f0f0", fg="#333")
    title_label.pack(pady=(10, 20))

    # Create a frame to hold the form elements
    frame = tk.Frame(root, bg="white", padx=20, pady=20, relief=tk.RAISED, bd=2)
    frame.pack(padx=20, pady=(0, 20))

    # Password length
    length_label = tk.Label(frame, text="Length:", font=("Arial", 12), bg="white")
    length_label.grid(row=0, column=0, pady=10, sticky="w")

    length_entry = tk.Entry(frame, font=("Arial", 12), width=8)
    length_entry.grid(row=0, column=1, pady=10, padx=10)
    length_entry.insert(0, "12")  # Default length

    # Checkboxes for character types
    global lowercase_var, uppercase_var, digits_var, symbols_var
    lowercase_var = tk.IntVar(value=1)
    uppercase_var = tk.IntVar(value=1)
    digits_var = tk.IntVar(value=1)
    symbols_var = tk.IntVar(value=1)

    lowercase_check = tk.Checkbutton(frame, text="Include Lowercase", variable=lowercase_var, font=("Arial", 12), bg="white")
    lowercase_check.grid(row=1, column=0, columnspan=2, sticky="w")
    uppercase_check = tk.Checkbutton(frame, text="Include Uppercase", variable=uppercase_var, font=("Arial", 12), bg="white")
    uppercase_check.grid(row=2, column=0, columnspan=2, sticky="w")
    digits_check = tk.Checkbutton(frame, text="Include Digits", variable=digits_var, font=("Arial", 12), bg="white")
    digits_check.grid(row=3, column=0, columnspan=2, sticky="w")
    symbols_check = tk.Checkbutton(frame, text="Include Symbols", variable=symbols_var, font=("Arial", 12), bg="white")
    symbols_check.grid(row=4, column=0, columnspan=2, sticky="w")

    # Generate password button
    generate_button = tk.Button(frame, text="Generate Password", font=("Arial", 12), bg="#4caf50", fg="white", width=20, height=1, command=generate_password)
    generate_button.grid(row=5, column=0, columnspan=2, pady=20)

    # Password display
    password_label = tk.Label(frame, text="Generated Password:", font=("Arial", 12), bg="white")
    password_label.grid(row=6, column=0, pady=10, sticky="w")

    global password_entry
    password_entry = tk.Entry(frame, font=("Arial", 12), width=30)
    password_entry.grid(row=6, column=1, pady=10, padx=10)

    # Copy to clipboard button
    copy_button = tk.Button(frame, text="Copy to Clipboard", font=("Arial", 12), bg="#2196f3", fg="white", width=20, height=1, command=copy_to_clipboard)
    copy_button.grid(row=7, column=0, columnspan=2, pady=10)

    return length_entry, password_entry

# Main code
root = tk.Tk()
length_entry, password_entry = create_ui(root)

root.mainloop()
