# importing required modules
import tkinter
import customtkinter
from tkinter import messagebox
from PIL import Image
import re

customtkinter.set_appearance_mode("dark")  # can set light or dark
# customtkinter.set_default_color_theme("blue")  # themes: blue, dark-blue or green

app = customtkinter.CTk()  # creating custom tkinter window
app.geometry("1080x600")
app.resizable(False, False)
app.title("Login")

app.iconbitmap("naita_icon.ico")

def login():
    user_name = entry1.get()
    password = entry2.get()

    if not all([user_name, password]):
        messagebox.showerror("Error", "All fields are required!")
        return

    messagebox.showinfo("Success", "Successfully logged into your account!")

def forgot_password():
    app.destroy()
    w2 = customtkinter.CTk()
    w2.geometry('1080x600')
    w2.resizable(False, False)
    w2.title('Reset password')

    frame1 = customtkinter.CTkFrame(master=w2, width=300, height=400, fg_color='#ddd')
    frame1.place(relx=0, rely=0, relwidth=0.5, relheight=1)

    def is_valid_email(email):
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(pattern, email) is not None

    def reset_password():
        email = entry1.get()
        new_password = entry2.get()
        confirm_password = entry3.get()

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

    l2 = customtkinter.CTkLabel(master=frame1, text="Reset password", text_color="black", font=('Century Gothic', 20))
    l2.place(x=190, y=180)

    l3 = customtkinter.CTkLabel(master=frame1, text="E-mail:", text_color='black', font=('Century Gothic', 14))
    l3.place(x=20, y=250)

    entry1 = customtkinter.CTkEntry(master=frame1, width=220, placeholder_text="Enter your E-mail")
    entry1.place(x=170, y=250)

    l4 = customtkinter.CTkLabel(master=frame1, text='New password:', text_color='black', font=('Century Gothic', 14))
    l4.place(x=20, y=310)

    entry2 = customtkinter.CTkEntry(master=frame1, width=220, placeholder_text="Enter new password")
    entry2.place(x=170, y=310)

    l5 = customtkinter.CTkLabel(master=frame1, text='Confirm password:', text_color='black', font=('Century Gothic', 14))
    l5.place(x=20, y=370)

    entry3 = customtkinter.CTkEntry(master=frame1, width=220, placeholder_text="Confirm new password")
    entry3.place(x=170, y=370)

    button1 = customtkinter.CTkButton(master=frame1, width=120, text="Reset password", corner_radius=6, fg_color="crimson", command=reset_password)
    button1.place(x=170, y=430)

    w2.mainloop()

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

l2 = customtkinter.CTkLabel(master=frame_left, text="Log into your account",text_color="black", font=('Century Gothic', 20))
l2.place(x=160, y=180)

l3 = customtkinter.CTkLabel(master=frame_left, text="User name:", text_color='black', font=('Century Gothic', 14))
l3.place(x=20, y=280)

entry1 = customtkinter.CTkEntry(master=frame_left, width=220, placeholder_text="User name")
entry1.place(x=170, y=280)

l4 = customtkinter.CTkLabel(master=frame_left, text='Password:', text_color='black', font=('Century Gothic', 14))
l4.place(x=20, y=340)

entry2 = customtkinter.CTkEntry(master=frame_left, width=220, placeholder_text="Password")
entry2.place(x=170, y=340)

button2 = customtkinter.CTkButton(master=frame_left, text="Forget password?", font=('Century Gothic', 12), fg_color='crimson', hover_color='red', command=forgot_password)
button2.place(x=170, y=380)

button1 = customtkinter.CTkButton(master=frame_left, width=120, text="Login", corner_radius=6, fg_color="crimson", command=login)
button1.place(x=170, y=430)

app.mainloop()