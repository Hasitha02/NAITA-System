import customtkinter as ctk
from PIL import Image
import pyodbc
from tkinter import messagebox

# Initialize the customtkinter library
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Login")
        self.geometry("1024x1280")

        # Set icon (make sure you have an icon file in the same directory)
        self.iconbitmap("naita_icon.ico")

        # Set background image
        self.bg_image = ctk.CTkImage(Image.open("naita.jpg"), size=(600, 400))
        self.bg_label = ctk.CTkLabel(self, image=self.bg_image)
        self.bg_label.place(relwidth=1, relheight=1)

        # Create a frame to hold the widgets
        self.frame = ctk.CTkFrame(self, width=700, height=350, corner_radius=15, bg_color="white")
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        # First Name Entry
        self.fname_entry = ctk.CTkEntry(self.frame, placeholder_text="First Name")
        self.fname_entry.pack(pady=5)

        # Last Name Entry
        self.lname_entry = ctk.CTkEntry(self.frame, placeholder_text="Last Name")
        self.lname_entry.pack(pady=5)

        # Username Entry
        self.username_entry = ctk.CTkEntry(self.frame, placeholder_text="Username")
        self.username_entry.pack(pady=5)

        # Email Entry
        self.email_entry = ctk.CTkEntry(self.frame, placeholder_text="Email")
        self.email_entry.pack(pady=5)

        # Password Entry
        self.password_entry = ctk.CTkEntry(self.frame, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=5)

        # Confirm Password Entry
        self.confirm_password_entry = ctk.CTkEntry(self.frame, placeholder_text="Confirm Password", show="*")
        self.confirm_password_entry.pack(pady=5)

        # Create a frame for the buttons
        self.button_frame = ctk.CTkFrame(self.frame)
        self.button_frame.pack(pady=20)

        # Create Account Button
        self.create_account_button = ctk.CTkButton(self.button_frame, text="Create Account", command=self.create_account)
        self.create_account_button.pack(side="left", padx=10)

        # Login Button
        self.login_button = ctk.CTkButton(self.button_frame, text="Login", command=self.login)
        self.login_button.pack(side="left", padx=10)

        # Forgot Password Button
        self.forgot_password_button = ctk.CTkButton(self.frame, text="Forgot Password", command=self.forgot_password)
        self.forgot_password_button.pack(pady=10)

    def create_account(self):
        # Get user input
        fname = self.fname_entry.get()
        lname = self.lname_entry.get()
        username = self.username_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        # Validate user input
        if not fname or not lname or not username or not email or not password or not confirm_password:
            messagebox.showerror("Error", "All fields are required")
            return
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return

        # Connect to the database
        try:
            connection = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};'
                'SERVER=MSSQL001;'
                'DATABASE=NAITA;'
                'UID=sa;'
                'PWD=123'
            )
            cursor = connection.cursor()

            # Create the table if it doesn't exist
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='CreateAccount' AND xtype='U')
                CREATE TABLE CreateAccount (
                    fname VARCHAR(255),
                    lname VARCHAR(255),
                    username VARCHAR(255),
                    email VARCHAR(255) PRIMARY KEY,
                    password CHAR(60)
                )
            """)

            # Insert the new user into the database
            cursor.execute("""
                INSERT INTO CreateAccount (fname, lname, username, email, password)
                VALUES (?, ?, ?, ?, ?)
            """, (fname, lname, username, email, password))

            # Commit the transaction
            connection.commit()

            messagebox.showinfo("Success", "Account created successfully")

        except pyodbc.Error as err:
            messagebox.showerror("Error", f"Database error: {err}")
        finally:
            if connection:
                cursor.close()
                connection.close()

    def login(self):
        # Placeholder for login functionality
        print("Login button clicked")

    def forgot_password(self):
        # Placeholder for forgot password functionality
        print("Forgot Password button clicked")

if __name__ == "__main__":
    app = App()
    app.mainloop()
