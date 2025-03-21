import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from PIL import Image
import re
import mysql.connector
from mysql.connector import Error

# Function to validate email
def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None

# Function to connect to the MySQL database
def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',  # Replace with your MySQL host
            database='NAITA',  # Replace with your MySQL database
            user='root',       # Replace with your MySQL username
            password='hasitha0214' # Replace with your MySQL password
        )
        if connection.is_connected():
            return connection
    except Error as e:
        messagebox.showerror("Database Error", f"Error connecting to MySQL: {e}")
        return None

# Function to insert data into the database
def insert_into_db(first_name, last_name, username, email, password):
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("USE NAITA;")
            query = """INSERT INTO CreateAccount (fname, lname, username, email, password)
                       VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(query, (first_name, last_name, username, email, password))
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except Error as e:
            messagebox.showerror("Database Error", f"Error inserting data into MySQL: {e}")
            return False

# Function to handle create account button click
def create_account():
    first_name = entry_first_name.get()
    last_name = entry_last_name.get()
    username = entry_username.get()
    email = entry_email.get()
    password = entry_password.get()
    confirm_password = entry_confirm_password.get()


    if not all([first_name, last_name, email, password, confirm_password, username]):
        messagebox.showerror("Error", "All fields are required.")
        return

    if not is_valid_email(email):
        messagebox.showerror("Error", "Invalid email address.")
        return

    if password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match.")
        return

    # Insert data into the database
    if insert_into_db(first_name, last_name, email, password):
        messagebox.showinfo("Success", "Account created successfully!")
        app.destroy()

# Function to handle help button click
def show_help():
    messagebox.showinfo("Help", "Please fill out all fields and make sure your email is valid.")

# Function to toggle password visibility
def toggle_password():
    if show_password_var.get():
        entry_password.configure(show="")
        entry_confirm_password.configure(show="")
    else:
        entry_password.configure(show="*")
        entry_confirm_password.configure(show="*")

# Initialize the main window
app = ctk.CTk()
app.geometry("1080x600")
app.title("Create New Account")

# Set window icon
app.iconbitmap("naita_icon.ico")

# Left Frame for the form
frame_left = ctk.CTkFrame(master=app, width=300, height=400, corner_radius=10, fg_color="#ddd")
frame_left.place(relx=0, rely=0, relwidth=0.5, relheight=1)

# Add logo to the left frame
logo_image = Image.open("naita_icon2.jpg")
logo_photo = ctk.CTkImage(light_image=logo_image, dark_image=logo_image, size=(100, 100))
label_logo = ctk.CTkLabel(master=frame_left, text="", image=logo_photo)
label_logo.place(x=220, y=10)

# Right Frame for the red background
frame_right = ctk.CTkFrame(master=app, width=300, height=400, corner_radius=10)
frame_right.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)

# Load and place the image in the right frame
image = Image.open("naita2.jpg")
photo = ctk.CTkImage(light_image=image, dark_image=image, size=(600, 600))
label_image = ctk.CTkLabel(master=frame_right, text="", image=photo)
label_image.place(relx=0, rely=0, relwidth=1, relheight=1)

# Create and place the labels and entry fields
label_first_name = ctk.CTkLabel(master=frame_left, text="First Name:", text_color="black", font=("Arial", 14))
label_first_name.place(x=20, y=130)
entry_first_name = ctk.CTkEntry(master=frame_left, placeholder_text="Enter your first name", width=220, height=30)
entry_first_name.place(x=170, y=130)

label_last_name = ctk.CTkLabel(master=frame_left, text="Last Name:", text_color="black", font=("Arial", 14))
label_last_name.place(x=20, y=190)
entry_last_name = ctk.CTkEntry(master=frame_left, placeholder_text="Enter your last name", width=220, height=30)
entry_last_name.place(x=170, y=190)

label_username = ctk.CTkLabel(master=frame_left, text="Username:", text_color="black", font=("Arial", 14))
label_username.place(x=20, y=250)
entry_username = ctk.CTkEntry(master=frame_left, placeholder_text="Enter your username", width=220, height=30)
entry_username.place(x=170, y=250)

label_email = ctk.CTkLabel(master=frame_left, text="Email:", text_color="black", font=("Arial", 14))
label_email.place(x=20, y=310)
entry_email = ctk.CTkEntry(master=frame_left, placeholder_text="Enter your email", width=220, height=30)
entry_email.place(x=170, y=310)

label_password = ctk.CTkLabel(master=frame_left, text="Password:", text_color="black", font=("Arial", 14))
label_password.place(x=20, y=370)
entry_password = ctk.CTkEntry(master=frame_left, placeholder_text="Enter your password", show="*", width=220, height=30)
entry_password.place(x=170, y=370)

label_confirm_password = ctk.CTkLabel(master=frame_left, text="Confirm Password:", text_color="black", font=("Arial", 14))
label_confirm_password.place(x=20, y=420)
entry_confirm_password = ctk.CTkEntry(master=frame_left, placeholder_text="Confirm your password", show="*", width=220, height=30)
entry_confirm_password.place(x=170, y=420)

# Create and place the Show Password checkbox
show_password_var = tk.BooleanVar()
checkbox_show_password = ctk.CTkCheckBox(master=frame_left, text="Show Password", text_color="black", variable=show_password_var, command=toggle_password)
checkbox_show_password.place(x=170, y=470)

# Create and place the Create Account button
button_create_account = ctk.CTkButton(master=frame_left, text="Create Account", command=create_account, width=120, height=30, fg_color="crimson")
button_create_account.place(x=170, y=520)

# Create and place the Help button
button_help = ctk.CTkButton(master=frame_left, text="Help", command=show_help, width=100, height=30, fg_color="crimson")
button_help.place(x=420, y=540)

# Prevent maximize
app.resizable(False, False)

# Run the application
app.mainloop()
