# importing required modules
import tkinter as tk
import customtkinter
from tkinter import messagebox
from PIL import Image
import re

# login function ---------------------------------------------------------

def login():
    user_name = user_name_entry.get()
    password = password_entry.get()

    if not all([user_name, password]):
        messagebox.showerror("Error", "All fields are required!")
        return

    messagebox.showinfo("Success", "Successfully logged into your account!")

# ----------------------------------------------------------------------------

# Forgot password page --------------------------------------------------------------
def forgot_password():
    app.destroy()
    w2 = customtkinter.CTk()
    w2.geometry('1080x600')
    w2.resizable(False, False)
    w2.title('Reset password')

    w2.iconbitmap("naita_icon.ico")

    frame1 = customtkinter.CTkFrame(master=w2, width=300, height=400, fg_color='#ddd')
    frame1.place(relx=0, rely=0, relwidth=0.5, relheight=1)

    def is_valid_email(email):
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(pattern, email) is not None

    def reset_password():
        email = email_entry.get()
        new_password = new_password_entry.get()
        confirm_password = confirm_new_password_entry.get()

        if not all([email, new_password, confirm_password]):
            messagebox.showerror("Error", "All fields are required!")
            return

        if not is_valid_email(email):
            messagebox.showerror("Error", "Invalid e-mail address!")
            return

        if new_password != confirm_password:
            messagebox.showerror("Error", "Password doesn't match!")
            return

        messagebox.showinfo("Success!", "Password has been changed!")
        if all([email, new_password, confirm_password]):
            customtkinter.CTk.destroy(frame1)

    logo_image = Image.open("naita_icon2.jpg")
    logo_photo = customtkinter.CTkImage(light_image=logo_image, dark_image=logo_image, size=(100, 100))
    label_logo = customtkinter.CTkLabel(master=frame1, text="", image=logo_photo)
    label_logo.place(x=220, y=50)

    frame2 = customtkinter.CTkFrame(master=w2, width=300, height=400, corner_radius=10)
    frame2.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)

    image = Image.open("naita2.jpg")
    photo = customtkinter.CTkImage(light_image=image, dark_image=image, size=(600, 600))
    label_image = customtkinter.CTkLabel(master=frame2, text="", image=photo)
    label_image.place(relx=0, rely=0, relwidth=1, relheight=1)

    l2 = customtkinter.CTkLabel(master=frame1, text="Reset password", text_color="black", font=('Century Gothic', 25))
    l2.place(x=170, y=180)

    l3 = customtkinter.CTkLabel(master=frame1, text="E-mail:", text_color='black', font=('Century Gothic', 14))
    l3.place(x=20, y=250)

    email_entry = customtkinter.CTkEntry(master=frame1, width=220, placeholder_text="Enter your E-mail")
    email_entry.place(x=170, y=250)

    l4 = customtkinter.CTkLabel(master=frame1, text='New password:', text_color='black', font=('Century Gothic', 14))
    l4.place(x=20, y=310)

    new_password_entry = customtkinter.CTkEntry(master=frame1, width=220, placeholder_text="Enter new password")
    new_password_entry.place(x=170, y=310)

    l5 = customtkinter.CTkLabel(master=frame1, text='Confirm password:', text_color='black', font=('Century Gothic', 14))
    l5.place(x=20, y=370)

    confirm_new_password_entry = customtkinter.CTkEntry(master=frame1, width=220, placeholder_text="Confirm new password")
    confirm_new_password_entry.place(x=170, y=370)

    reset_btn = customtkinter.CTkButton(master=frame1, width=120, text="Reset password", corner_radius=6, fg_color="crimson", command=reset_password)
    reset_btn.place(x=170, y=430)

    w2.mainloop()

# -----------------------------------------------------------------------------------

# create new account page -----------------------------------------------------------

def create_new_account_page():
    app.destroy()
    creating_new_page = customtkinter.CTk()
    creating_new_page.geometry("1080x600")
    creating_new_page.resizable(False, False)
    creating_new_page.title("Create new account")

    creating_new_page.iconbitmap("naita_icon.ico")

    frame3 = customtkinter.CTkFrame(master=creating_new_page, width=300, height=400, fg_color='#ddd')
    frame3.place(relx=0, rely=0, relwidth=0.5, relheight=1)

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

    def is_valid_email(email):
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(pattern, email) is not None

    def create_account():
        first_name = entry_first_name.get()
        last_name = entry_last_name.get()
        email = entry_email.get()
        password = entry_password.get()
        confirm_password = entry_confirm_password.get()

        if not all([first_name, last_name, email, password, confirm_password]):
            messagebox.showerror("Error", "All fields are required.")
            return

        if not is_valid_email(email):
            messagebox.showerror("Error", "Invalid email address.")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        messagebox.showinfo("Success!", "Password has been changed!")
        if all([email, password, confirm_password]):
            customtkinter.CTk.destroy(frame3)

    frame4 = customtkinter.CTkFrame(master=creating_new_page, width=300, height=400, corner_radius=10)
    frame4.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)

    logo_image = Image.open("naita_icon2.jpg")
    logo_photo = customtkinter.CTkImage(light_image=logo_image, dark_image=logo_image, size=(100, 100))
    label_logo = customtkinter.CTkLabel(master=frame3, text="", image=logo_photo)
    label_logo.place(x=220, y=10)

    image = Image.open("naita2.jpg")
    photo = customtkinter.CTkImage(light_image=image, dark_image=image, size=(600, 600))
    label_image = customtkinter.CTkLabel(master=frame4, text="", image=photo)
    label_image.place(relx=0, rely=0, relwidth=1, relheight=1)

    label_new_account = customtkinter.CTkLabel(master=frame3, text="Create New account", text_color="black", font=('Century Gothic', 25))
    label_new_account.place(x=140, y=130)

    # Create and place the labels and entry fields
    label_first_name = customtkinter.CTkLabel(master=frame3, text="First Name:", text_color="black", font=("Arial", 14))
    label_first_name.place(x=20, y=170)
    entry_first_name = customtkinter.CTkEntry(master=frame3, placeholder_text="Enter your first name", width=220, height=30)
    entry_first_name.place(x=170, y=170)

    label_last_name = customtkinter.CTkLabel(master=frame3, text="Last Name:", text_color="black", font=("Arial", 14))
    label_last_name.place(x=20, y=230)
    entry_last_name = customtkinter.CTkEntry(master=frame3, placeholder_text="Enter your last name", width=220, height=30)
    entry_last_name.place(x=170, y=230)

    label_email = customtkinter.CTkLabel(master=frame3, text="Email:", text_color="black", font=("Arial", 14))
    label_email.place(x=20, y=290)
    entry_email = customtkinter.CTkEntry(master=frame3, placeholder_text="Enter your email", width=220, height=30)
    entry_email.place(x=170, y=290)

    label_password = customtkinter.CTkLabel(master=frame3, text="Password:", text_color="black", font=("Arial", 14))
    label_password.place(x=20, y=350)
    entry_password = customtkinter.CTkEntry(master=frame3, placeholder_text="Enter your password", show="*", width=220, height=30)
    entry_password.place(x=170, y=350)

    label_confirm_password = customtkinter.CTkLabel(master=frame3, text="Confirm Password:", text_color="black", font=("Arial", 14))
    label_confirm_password.place(x=20, y=410)
    entry_confirm_password = customtkinter.CTkEntry(master=frame3, placeholder_text="Confirm your password", show="*", width=220, height=30)
    entry_confirm_password.place(x=170, y=410)

    # Create and place the Show Password checkbox
    show_password_var = tk.BooleanVar()
    checkbox_show_password = customtkinter.CTkCheckBox(master=frame3, text="Show Password", text_color="black", variable=show_password_var, command=toggle_password)
    checkbox_show_password.place(x=170, y=460)

    # Create and place the Create Account button
    button_create_account = customtkinter.CTkButton(master=frame3, text="Create Account", width=120, height=30, fg_color="crimson", command=create_account)
    button_create_account.place(x=170, y=500)

    # Create and place the Help button
    button_help = customtkinter.CTkButton(master=frame3, text="Help", command=show_help, width=100, height=30, fg_color="crimson")
    button_help.place(x=420, y=540)

    creating_new_page.mainloop()

# -----------------------------------------------------------------------------------

# creating custom tkinter window ____________________________________________________

customtkinter.set_appearance_mode("dark")  # can set light or dark

app = customtkinter.CTk()
app.geometry("1080x600")
app.resizable(False, False)
app.title("Login")

app.iconbitmap("naita_icon.ico")

frame_left = customtkinter.CTkFrame(master=app, width=300, height=400, fg_color='#ddd')
frame_left.place(relx=0, rely=0, relwidth=0.5, relheight=1)

logo_image = Image.open("naita_icon2.jpg")
logo_photo = customtkinter.CTkImage(light_image=logo_image, dark_image=logo_image, size=(100, 100))
label_logo = customtkinter.CTkLabel(master=frame_left, text="", image=logo_photo)
label_logo.place(x=220, y=50)

frame_right = customtkinter.CTkFrame(master=app, width=300, height=400, corner_radius=10)
frame_right.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)

image = Image.open("naita2.jpg")
photo = customtkinter.CTkImage(light_image=image, dark_image=image, size=(600, 600))
label_image = customtkinter.CTkLabel(master=frame_right, text="", image=photo)
label_image.place(relx=0, rely=0, relwidth=1, relheight=1)

l2 = customtkinter.CTkLabel(master=frame_left, text="Log into your account",text_color="black", font=('Century Gothic', 25))
l2.place(x=140, y=190)

l3 = customtkinter.CTkLabel(master=frame_left, text="User name:", text_color='black', font=('Century Gothic', 14))
l3.place(x=20, y=280)

user_name_entry = customtkinter.CTkEntry(master=frame_left, width=220, placeholder_text="User name")
user_name_entry.place(x=170, y=280)

l4 = customtkinter.CTkLabel(master=frame_left, text='Password:', text_color='black', font=('Century Gothic', 14))
l4.place(x=20, y=340)

password_entry = customtkinter.CTkEntry(master=frame_left, width=220, placeholder_text="Password")
password_entry.place(x=170, y=340)

reset_password_btn = customtkinter.CTkButton(master=frame_left, text="Forgot password?", font=('Century Gothic', 12), fg_color='crimson', command=forgot_password)
reset_password_btn.place(x=170, y=390)

login_btn = customtkinter.CTkButton(master=frame_left, width=120, text="Login", corner_radius=6, fg_color="crimson", command=login)
login_btn.place(x=170, y=440)

create_account_btn = customtkinter.CTkButton(master=frame_left, text="Don't have an account?", corner_radius=6, fg_color='crimson', font=('Century Gothic', 12), command=create_new_account_page)
create_account_btn.place(x=350, y=440)

app.mainloop()

# -------------------------------------------------------------------------------