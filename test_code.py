import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import hashlib
import random
import string

# Database setup
conn = sqlite3.connect('naita.db')
c = conn.cursor()

  njklk


# Create tables
c.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fname VARCHAR(255),
    lname VARCHAR(255),
    username VARCHAR(255) UNIQUE,
    email VARCHAR(255),
    password CHAR(60)
)''')

conn.commit()

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to create a new account
def create_account():
    fname = fname_entry.get()
    lname = lname_entry.get()
    username = username_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    re_password = re_password_entry.get()

    if fname and lname and username and email and password and re_password:
        if password == re_password:
            hashed_password = hash_password(password)
            try:
                c.execute('INSERT INTO users (fname, lname, username, email, password) VALUES (?, ?, ?, ?, ?)',
                          (fname, lname, username, email, hashed_password))
                conn.commit()
                messagebox.showinfo("Success", "Account created successfully")
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Username already exists")
        else:
            messagebox.showerror("Error", "Passwords do not match")
    else:
        messagebox.showerror("Error", "All fields are required")

# Function to login
def login():
    username = login_username_entry.get()
    password = login_password_entry.get()
    hashed_password = hash_password(password)

    c.execute('SELECT * FROM users WHERE username=? AND password=?', (username, hashed_password))
    user = c.fetchone()

    if user:
        messagebox.showinfo("Success", "Login successful")
        show_home_page()
    else:
        messagebox.showerror("Error", "Invalid username or password")

# Function to show the home page
def show_home_page():
    for widget in root.winfo_children():
        widget.destroy()
    home_label = tk.Label(root, text="Welcome to NAITA", font=("Helvetica", 16), bg="beige")
    home_label.pack(pady=20)
    logout_button = tk.Button(root, text="Logout", command=logout)
    logout_button.pack(pady=10)

# Function to logout
def logout():
    answer = messagebox.askyesno("Logout", "Are you sure you want to logout?")
    if answer:
        show_login_page()

# Function to show the login page
def show_login_page():
    for widget in root.winfo_children():
        widget.destroy()
    login_label = tk.Label(root, text="Login", font=("Helvetica", 16), bg="beige")
    login_label.pack(pady=20)
    global login_username_entry, login_password_entry
    login_username_entry = tk.Entry(root, bg="white")
    login_username_entry.pack(pady=5)
    login_password_entry = tk.Entry(root, show='*', bg="white")
    login_password_entry.pack(pady=5)
    login_button = tk.Button(root, text="Login", command=login, bg="lightgrey")
    login_button.pack(pady=10)
    forgot_password_button = tk.Button(root, text="Forgot Password?", command=show_forgot_password_page, bg="lightgrey")
    forgot_password_button.pack(pady=10)
    create_account_button = tk.Button(root, text="Create Account", command=show_create_account_page, bg="lightgrey")
    create_account_button.pack(pady=10)

# Function to show the create account page
def show_create_account_page():
    for widget in root.winfo_children():
        widget.destroy()
    create_label = tk.Label(root, text="Create Account", font=("Helvetica", 16), bg="beige")
    create_label.pack(pady=20)
    global fname_entry, lname_entry, username_entry, email_entry, password_entry, re_password_entry
    fname_entry = tk.Entry(root, bg="white")
    fname_entry.pack(pady=5)
    lname_entry = tk.Entry(root, bg="white")
    lname_entry.pack(pady=5)
    username_entry = tk.Entry(root, bg="white")
    username_entry.pack(pady=5)
    email_entry = tk.Entry(root, bg="white")
    email_entry.pack(pady=5)
    password_entry = tk.Entry(root, show='*', bg="white")
    password_entry.pack(pady=5)
    re_password_entry = tk.Entry(root, show='*', bg="white")
    re_password_entry.pack(pady=5)
    create_button = tk.Button(root, text="Create Account", command=create_account, bg="lightgrey")
    create_button.pack(pady=10)
    back_button = tk.Button(root, text="Back", command=show_login_page, bg="lightgrey")
    back_button.pack(pady=10)

# Function to show forgot password page
def show_forgot_password_page():
    for widget in root.winfo_children():
        widget.destroy()
    forgot_label = tk.Label(root, text="Reset Password", font=("Helvetica", 16), bg="beige")
    forgot_label.pack(pady=20)
    global email_reset_entry
    email_reset_entry = tk.Entry(root, bg="white")
    email_reset_entry.pack(pady=5)
    reset_button = tk.Button(root, text="Reset", command=reset_password, bg="lightgrey")
    reset_button.pack(pady=10)
    back_button = tk.Button(root, text="Back", command=show_login_page, bg="lightgrey")
    back_button.pack(pady=10)

# Function to reset password
def reset_password():
    email = email_reset_entry.get()
    c.execute('SELECT username FROM users WHERE email=?', (email,))
    user = c.fetchone()
    if user:
        new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        hashed_password = hash_password(new_password)
        c.execute('UPDATE users SET password=? WHERE email=?', (hashed_password, email))
        conn.commit()
        messagebox.showinfo("Success", f"Your new password is: {new_password}")
    else:
        messagebox.showerror("Error", "Email not found")

# Initialize the main window
root = tk.Tk()
root.title("NAITA System")
root.geometry("400x400")
root.configure(bg="beige")

show_login_page()

root.mainloop()

# Close the database connection
conn.close()
