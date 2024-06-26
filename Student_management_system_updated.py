# importing required modules
import customtkinter
import tkinter as tk
from tkinter import messagebox
from PIL import Image
import re
import mysql.connector
from mysql.connector import Error
from cbtForm import cbt_form_function
from ebtForm import ebt_form_function
from edit_CBT import edit_CBT_function
from edit_EBT import edit_EBT_function
from View_All_Student_Deatails_EBT import view_all_EBT
from View_All_Student_Details_CBT import view_all_CBT
from View_All_Student_Details import view_all_details
from Search_Student_Deatails_CBT import search_CBT
from Search_Student_Details_EBT import search_EBT

# Function to connect to the MySQL database
def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',  # Replace with your MySQL host
            database='NAITA',  # Replace with your MySQL database
            user='root',       # Replace with your MySQL username
            password='11156363312' # Replace with your MySQL password
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

# export data for login
def select_from_db(username, password):
    # Replace with your MySQL database connection details
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='11156363312',
        database='NAITA'
    )
    cursor = connection.cursor()

    query = "SELECT username, password FROM CreateAccount WHERE username=%s AND password=%s"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()

    connection.close()
    return result is not None

def login_window_function():

    def create_new_account_page():
        login_window.destroy()
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
            username = entry_username.get()
            email = entry_email.get()
            password = entry_password.get()
            confirm_password = entry_confirm_password.get()

            if not all([first_name, last_name,username, email, password, confirm_password]):
                messagebox.showerror("Error", "All fields are required.")
                return

            if not is_valid_email(email):
                messagebox.showerror("Error", "Invalid email address.")
                return

            if password != confirm_password:
                messagebox.showerror("Error", "Passwords do not match.")
                return

            # Insert data into the database
            if insert_into_db(first_name, last_name, username, email, password):
                messagebox.showinfo("Success", "Account created successfully!")

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
        label_first_name.place(x=20, y=180)
        entry_first_name = customtkinter.CTkEntry(master=frame3, placeholder_text="Enter your first name", width=220, height=30)
        entry_first_name.place(x=170, y=180)

        label_last_name = customtkinter.CTkLabel(master=frame3, text="Last Name:", text_color="black", font=("Arial", 14))
        label_last_name.place(x=20, y=230)
        entry_last_name = customtkinter.CTkEntry(master=frame3, placeholder_text="Enter your last name", width=220, height=30)
        entry_last_name.place(x=170, y=230)

        label_username = customtkinter.CTkLabel(master=frame3, text="Username:", text_color="black", font=("Arial", 14))
        label_username.place(x=20, y=280)
        entry_username = customtkinter.CTkEntry(master=frame3, placeholder_text="Enter your Username", width=220, height=30)
        entry_username.place(x=170, y=280)

        label_email = customtkinter.CTkLabel(master=frame3, text="Email:", text_color="black", font=("Arial", 14))
        label_email.place(x=20, y=330)
        entry_email = customtkinter.CTkEntry(master=frame3, placeholder_text="Enter your email", width=220, height=30)
        entry_email.place(x=170, y=330)

        label_password = customtkinter.CTkLabel(master=frame3, text="Password:", text_color="black", font=("Arial", 14))
        label_password.place(x=20, y=380)
        entry_password = customtkinter.CTkEntry(master=frame3, placeholder_text="Enter your password", show="*", width=220, height=30)
        entry_password.place(x=170, y=380)

        label_confirm_password = customtkinter.CTkLabel(master=frame3, text="Confirm Password:", text_color="black", font=("Arial", 14))
        label_confirm_password.place(x=20, y=430)
        entry_confirm_password = customtkinter.CTkEntry(master=frame3, placeholder_text="Confirm your password", show="*", width=220, height=30)
        entry_confirm_password.place(x=170, y=430)

        # Create and place the Show Password checkbox
        show_password_var = tk.BooleanVar()
        checkbox_show_password = customtkinter.CTkCheckBox(master=frame3, text="Show Password", text_color="black", variable=show_password_var, command=toggle_password, hover_color='#46070F')
        checkbox_show_password.place(x=170, y=480)

        # Create and place the Create Account button
        button_create_account = customtkinter.CTkButton(master=frame3, text="Create Account", width=120, height=30, fg_color="#87212E", command=create_account, hover_color='#46070F')
        button_create_account.place(x=270, y=530)

        # Create and place the Help button
        button_help = customtkinter.CTkButton(master=frame3, text="Help", command=show_help, width=100, height=30, fg_color="#87212E", hover_color='#46070F')
        button_help.place(x=420, y=530)

        creating_new_page.mainloop()

    # -----------------------------------------------------------------------------------

    # Forgot password page --------------------------------------------------------------

    def forgot_password():
        login_window.destroy()
        forgot_password_window = customtkinter.CTk()
        forgot_password_window.geometry('1080x600')
        forgot_password_window.resizable(False, False)
        forgot_password_window.title('Reset password')
        forgot_password_window.iconbitmap("naita_icon.ico")

        frame1 = customtkinter.CTkFrame(master=forgot_password_window, width=300, height=400, fg_color='#ddd')
        frame1.place(relx=0, rely=0, relwidth=0.5, relheight=1)

        def toggle_password():
            if show_password_var.get():
                new_password_entry.configure(show="")
                confirm_new_password_entry.configure(show="")
            else:
                new_password_entry.configure(show="*")
                confirm_new_password_entry.configure(show="*")

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

            try:
                connection = mysql.connector.connect(
                    host='localhost',  # Update with your host
                    database='NAITA',  # Update with your database name
                    user='root',  # Update with your MySQL username
                    password='11156363312'  # Update with your MySQL password
                )

                if connection.is_connected():
                    cursor = connection.cursor()
                    sql_update_query = """UPDATE CreateAccount SET password = %s WHERE email = %s"""
                    cursor.execute(sql_update_query, (new_password, email))
                    connection.commit()

                    if cursor.rowcount == 0:
                        messagebox.showerror("Error", "No account found with the provided email!")
                    else:
                        messagebox.showinfo("Success!", "Password has been changed!")

                    cursor.close()
                    connection.close()

            except Error as e:
                messagebox.showerror("Error", f"Error while connecting to MySQL: {e}")

        logo_image = Image.open("naita_icon2.jpg")
        logo_photo = customtkinter.CTkImage(light_image=logo_image, dark_image=logo_image, size=(100, 100))
        label_logo = customtkinter.CTkLabel(master=frame1, text="", image=logo_photo)
        label_logo.place(x=220, y=50)

        frame2 = customtkinter.CTkFrame(master=forgot_password_window, width=300, height=400, corner_radius=10)
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

        new_password_entry = customtkinter.CTkEntry(master=frame1, width=220, placeholder_text="Enter new password", show="*")
        new_password_entry.place(x=170, y=310)

        l5 = customtkinter.CTkLabel(master=frame1, text='Confirm password:', text_color='black', font=('Century Gothic', 14))
        l5.place(x=20, y=370)

        confirm_new_password_entry = customtkinter.CTkEntry(master=frame1, width=220, placeholder_text="Confirm new password", show="*")
        confirm_new_password_entry.place(x=170, y=370)

        # Create and place the Show Password checkbox
        show_password_var = tk.BooleanVar()
        checkbox_show_password = customtkinter.CTkCheckBox(master=frame1, text="Show Password", text_color="black", variable=show_password_var, command=toggle_password, hover_color='#46070F')
        checkbox_show_password.place(x=170, y=420)

        reset_btn = customtkinter.CTkButton(master=frame1, width=120, text="Reset password", corner_radius=6,fg_color="#87212E", command=reset_password, hover_color='#46070F')
        reset_btn.place(x=170, y=480)

        forgot_password_window.mainloop()
    # -----------------------------------------------------------------------------------

    # creating login window ____________________________________________________
    app.destroy()
    login_window = customtkinter.CTk()
    login_window.geometry("1080x600")
    login_window.resizable(False, False)
    login_window.title("Login")

    login_window.iconbitmap("naita_icon.ico")

    frame_left_lg = customtkinter.CTkFrame(master=login_window, width=300, height=400, fg_color='#ddd')
    frame_left_lg.place(relx=0, rely=0, relwidth=0.5, relheight=1)

    # login function ---------------------------------------------------------

    def login():
        username = user_name_entry.get()
        password = password_entry.get()

        if not all([username, password]):
            messagebox.showerror("Error", "All fields are required!")
            return

        if select_from_db(username, password):
            messagebox.showinfo("Success!", "Successfully logged into your account " + username)

            # creating categories window--------------------------------------------------------------------------------
            def categories_window():
                login_window.destroy()
                customtkinter.set_appearance_mode("dark")  # can set light or dark
                categories = customtkinter.CTk()
                categories.title("Categories")
                categories.geometry('1080x600')
                categories.resizable(False, False)
                categories.iconbitmap('naita_icon.ico')

                frame_4 = customtkinter.CTkFrame(master=categories, height=600, width=1080, fg_color="#ddd")
                frame_4.place(relx=0, rely=0)

                image = Image.open("NAITA Student Management System.png")
                photo = customtkinter.CTkImage(light_image=image, dark_image=image, size=(1080, 600))
                label_image = customtkinter.CTkLabel(master=frame_4, text="", image=photo)
                label_image.place(relx=0, rely=0)

                # Function for CBT selection window
                def selection_cbt_window():
                    categories.destroy()
                    customtkinter.set_appearance_mode("dark")
                    selection = customtkinter.CTk()
                    selection.geometry("1080x600")
                    selection.resizable(False, False)
                    selection.iconbitmap("naita_icon.ico")

                    frame_5 = customtkinter.CTkFrame(master=selection, height=600, width=1080, fg_color='#ddd')
                    frame_5.place(relx=0, rely=0)

                    image1 = Image.open("Selection page.png")
                    photo1 = customtkinter.CTkImage(light_image=image1, dark_image=image1, size=(1080, 600))
                    label_image = customtkinter.CTkLabel(master=frame_5, text="", image=photo1)
                    label_image.place(relx=0, rely=0)

                    add_btn = customtkinter.CTkButton(master=frame_5, text='Add', height=40, text_color='white',
                                                      fg_color='#87212E', font=('Century Gothic', 20), corner_radius=0,
                                                      command=cbt_form_function, hover_color='#46070F')
                    add_btn.place(x=150, y=400)

                    view_btn = customtkinter.CTkButton(master=frame_5, text='View', height=40, text_color='#87212E',
                                                       fg_color='white', font=('Century Gothic', 20), corner_radius=0,
                                                       hover_color='#46070F', command=view_all_CBT)
                    view_btn.place(x=350, y=400)

                    edit_btn = customtkinter.CTkButton(master=frame_5, text='Edit', height=40, text_color='#87212E',
                                                       fg_color='white', font=('Century Gothic', 20), corner_radius=0,
                                                       hover_color='#46070F', command=edit_CBT_function)
                    edit_btn.place(x=550, y=400)

                    search_btn = customtkinter.CTkButton(master=frame_5, text='Search', height=40, text_color='#87212E',
                                                       fg_color='white', font=('Century Gothic', 20), corner_radius=0,
                                                       hover_color='#46070F', command=search_CBT)
                    search_btn.place(x=310, y=480)

                    selection.mainloop()

                # Function for EBT selection window
                def selection_ebt_window():
                    categories.destroy()
                    customtkinter.set_appearance_mode("dark")
                    selection = customtkinter.CTk()
                    selection.geometry("1080x600")
                    selection.resizable(False, False)
                    selection.iconbitmap("naita_icon.ico")

                    frame_5 = customtkinter.CTkFrame(master=selection, height=600, width=1080, fg_color='#ddd')
                    frame_5.place(relx=0, rely=0)

                    image1 = Image.open("Selection page.png")
                    photo1 = customtkinter.CTkImage(light_image=image1, dark_image=image1, size=(1080, 600))
                    label_image = customtkinter.CTkLabel(master=frame_5, text="", image=photo1)
                    label_image.place(relx=0, rely=0)

                    add_btn = customtkinter.CTkButton(master=frame_5, text='Add', height=40, text_color='white',
                                                      fg_color='#87212E', font=('Century Gothic', 20), corner_radius=0,
                                                      command=ebt_form_function, hover_color='#46070F')
                    add_btn.place(x=150, y=400)

                    view_btn = customtkinter.CTkButton(master=frame_5, text='View', height=40, text_color='#87212E',
                                                       fg_color='white', font=('Century Gothic', 20), corner_radius=0,
                                                       hover_color='#46070F', command=view_all_EBT)
                    view_btn.place(x=350, y=400)

                    edit_btn = customtkinter.CTkButton(master=frame_5, text='Edit', height=40, text_color='#87212E',
                                                       fg_color='white', font=('Century Gothic', 20), corner_radius=0,
                                                       hover_color='#46070F', command=edit_EBT_function)
                    edit_btn.place(x=550, y=400)

                    search_btn = customtkinter.CTkButton(master=frame_5, text='Search', height=40, text_color='#87212E',
                                                         fg_color='white', font=('Century Gothic', 20), corner_radius=0,
                                                         hover_color='#46070F', command=search_EBT)
                    search_btn.place(x=310, y=480)

                    selection.mainloop()

                btn_cbt = customtkinter.CTkButton(master=frame_4, text='CBT', height=40, text_color='white',
                                                  fg_color='#87212E', font=('Century Gothic', 20), corner_radius=0,
                                                  hover_color='#46070F', command=selection_cbt_window)
                btn_cbt.place(x=100, y=400)

                btn_ebt = customtkinter.CTkButton(master=frame_4, text='EBT', font=('Century Gothic', 20), height=40,
                                                  text_color='#87212E', fg_color='white', hover_color='#46070F',
                                                  corner_radius=0, command=selection_ebt_window)
                btn_ebt.place(x=380, y=400)

                btn_view_all = customtkinter.CTkButton(master=frame_4, text='View all details', height=40,
                                                       text_color='#87212E', fg_color='white', hover_color='#46070F',
                                                       font=('Century Gothic', 20), corner_radius=0,
                                                       command=view_all_details, width=200)
                btn_view_all.place(x=320, y=500)

                categories.mainloop()

            categories_window()
        else:
            messagebox.showerror("Error!", "Invalid user name or password.")

    # ----------------------------------------------------------------------------

    logo_image = Image.open("naita_icon2.jpg")
    logo_photo = customtkinter.CTkImage(light_image=logo_image, dark_image=logo_image, size=(100, 100))
    label_logo = customtkinter.CTkLabel(master=frame_left_lg, text="", image=logo_photo)
    label_logo.place(x=220, y=50)

    frame_right_lg = customtkinter.CTkFrame(master=login_window, width=300, height=400, corner_radius=10)
    frame_right_lg.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)

    image = Image.open("naita2.jpg")
    photo = customtkinter.CTkImage(light_image=image, dark_image=image, size=(600, 600))
    label_image = customtkinter.CTkLabel(master=frame_right_lg, text="", image=photo)
    label_image.place(relx=0, rely=0, relwidth=1, relheight=1)

    l2 = customtkinter.CTkLabel(master=frame_left_lg, text="Log into your account", text_color="black", font=('Century Gothic', 25))
    l2.place(x=140, y=190)

    l3 = customtkinter.CTkLabel(master=frame_left_lg, text="User name:", text_color='black', font=('Century Gothic', 14))
    l3.place(x=20, y=280)

    user_name_entry = customtkinter.CTkEntry(master=frame_left_lg, width=220, placeholder_text="User name")
    user_name_entry.place(x=170, y=280)

    l4 = customtkinter.CTkLabel(master=frame_left_lg, text='Password:', text_color='black', font=('Century Gothic', 14))
    l4.place(x=20, y=340)

    password_entry = customtkinter.CTkEntry(master=frame_left_lg, width=220, placeholder_text="Password", show="*")
    password_entry.place(x=170, y=340)

    # Function to toggle password visibility
    def toggle_password():
        if show_password_var.get():
            password_entry.configure(show="")
        else:
            password_entry.configure(show="*")

    # Create and place the Show Password checkbox
    show_password_var = tk.BooleanVar()
    checkbox_show_password = customtkinter.CTkCheckBox(master=frame_left_lg, text="Show Password", text_color="black", variable=show_password_var, command=toggle_password, hover_color='#46070F')
    checkbox_show_password.place(x=170, y=380)

    reset_password_btn = customtkinter.CTkButton(master=frame_left_lg, text="Forgot password?", font=('Century Gothic', 12), fg_color='#87212E', command=forgot_password, hover_color='#46070F')
    reset_password_btn.place(x=250, y=420)

    login_btn = customtkinter.CTkButton(master=frame_left_lg, width=120, text="Login", corner_radius=6, fg_color="#87212E", command=login, hover_color='#46070F')
    login_btn.place(x=270, y=470)

    create_account_btn = customtkinter.CTkButton(master=frame_left_lg, text="Don't have an account?", corner_radius=6,fg_color='#87212E', font=('Century Gothic', 12), command=create_new_account_page, hover_color='#46070F')
    create_account_btn.place(x=230, y=520)

    login_window.mainloop()

    # -------------------------------------------------------------------------------

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
        username = entry_username.get()
        email = entry_email.get()
        password = entry_password.get()
        confirm_password = entry_confirm_password.get()

        if not all([first_name, last_name, username, email, password, confirm_password]):
            messagebox.showerror("Error", "All fields are required.")
            return

        if not is_valid_email(email):
            messagebox.showerror("Error", "Invalid email address.")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        # Insert data into the database
        if insert_into_db(first_name, last_name, username, email, password):
            messagebox.showinfo("Success", "Account created successfully!")

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
    label_first_name.place(x=20, y=180)
    entry_first_name = customtkinter.CTkEntry(master=frame3, placeholder_text="Enter your first name", width=220, height=30)
    entry_first_name.place(x=170, y=180)

    label_last_name = customtkinter.CTkLabel(master=frame3, text="Last Name:", text_color="black", font=("Arial", 14))
    label_last_name.place(x=20, y=230)
    entry_last_name = customtkinter.CTkEntry(master=frame3, placeholder_text="Enter your last name", width=220, height=30)
    entry_last_name.place(x=170, y=230)

    label_username = customtkinter.CTkLabel(master=frame3, text="Username:", text_color="black", font=("Arial", 14))
    label_username.place(x=20, y=280)
    entry_username = customtkinter.CTkEntry(master=frame3, placeholder_text="Enter your Username", width=220, height=30)
    entry_username.place(x=170, y=280)

    label_email = customtkinter.CTkLabel(master=frame3, text="Email:", text_color="black", font=("Arial", 14))
    label_email.place(x=20, y=330)
    entry_email = customtkinter.CTkEntry(master=frame3, placeholder_text="Enter your email", width=220, height=30)
    entry_email.place(x=170, y=330)

    label_password = customtkinter.CTkLabel(master=frame3, text="Password:", text_color="black", font=("Arial", 14))
    label_password.place(x=20, y=380)
    entry_password = customtkinter.CTkEntry(master=frame3, placeholder_text="Enter your password", show="*", width=220, height=30)
    entry_password.place(x=170, y=380)

    label_confirm_password = customtkinter.CTkLabel(master=frame3, text="Confirm Password:", text_color="black", font=("Arial", 14))
    label_confirm_password.place(x=20, y=430)
    entry_confirm_password = customtkinter.CTkEntry(master=frame3, placeholder_text="Confirm your password", show="*", width=220, height=30)
    entry_confirm_password.place(x=170, y=430)

    # Create and place the Show Password checkbox
    show_password_var = tk.BooleanVar()
    checkbox_show_password = customtkinter.CTkCheckBox(master=frame3, text="Show Password", text_color="black", variable=show_password_var, command=toggle_password, hover_color='#46070F')
    checkbox_show_password.place(x=170, y=480)

    # Create and place the Create Account button
    button_create_account = customtkinter.CTkButton(master=frame3, text="Create Account", width=120, height=30, fg_color="#87212E", command=create_account, hover_color='#46070F')
    button_create_account.place(x=270, y=530)

    # Create and place the Help button
    button_help = customtkinter.CTkButton(master=frame3, text="Help", command=show_help, width=100, height=30, fg_color="#87212E", hover_color='#46070F')
    button_help.place(x=420, y=530)

    creating_new_page.mainloop()

customtkinter.set_appearance_mode("dark")  # can set light or dark
app = customtkinter.CTk()
app.geometry('1080x600')
app.title('Home page')
app.resizable(False, False)
app.iconbitmap('naita_icon.ico')

frame_main = customtkinter.CTkFrame(master=app, height=600, width=1080)
frame_main.place(relx=0, rely=0)

image = Image.open('Home background.png')
photo = customtkinter.CTkImage(light_image=image, dark_image=image, size=(1080, 600))
label_image = customtkinter.CTkLabel(master=frame_main, image=photo, text='')
label_image.place(relx=0, rely=0)

login_btn = customtkinter.CTkButton(master=frame_main, width=200, height=50, font=('Century Gothic', 20), text='Login', text_color='white', fg_color='#87212E', corner_radius=0, command=login_window_function, hover_color='#46070F')
login_btn.place(x=350, y=370)

sign_up_btn = customtkinter.CTkButton(master=frame_main, width=200, height=50, font=('Century Gothic', 20), text='Sign up', text_color='white', fg_color='#87212E', corner_radius=0, command=create_new_account_page, hover_color='#46070F')
sign_up_btn.place(x=300, y=470)

def exit():
    app.destroy()

exit_btn = customtkinter.CTkButton(master=frame_main, width=130, height=40, font=('Century Gothic', 20), text="EXIT", text_color='#87212E', fg_color='white', hover_color='#46070F', corner_radius=0, command=exit)
exit_btn.place(x=20, y=540)

app.mainloop()

