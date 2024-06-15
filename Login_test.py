import customtkinter as ctk
from PIL import Image

# Initialize the customtkinter library
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Login")
        self.geometry("600x400")

        # Set icon (make sure you have an icon file in the same directory)
        self.iconbitmap("naita_icon.ico")

        # Set background image
        self.bg_image = ctk.CTkImage(Image.open("naita.jpg"), size=(600, 400))
        self.bg_label = ctk.CTkLabel(self, image=self.bg_image)
        self.bg_label.place(relwidth=1, relheight=1)

        # Create a frame to hold the widgets
        self.frame = ctk.CTkFrame(self, width=300, height=250, corner_radius=15)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        # Username Entry
        self.username_entry = ctk.CTkEntry(self.frame, placeholder_text="Username")
        self.username_entry.pack(pady=10)

        # Password Entry
        self.password_entry = ctk.CTkEntry(self.frame, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=10)

        # Create a frame for the buttons
        self.button_frame = ctk.CTkFrame(self.frame)
        self.button_frame.pack(pady=10)

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
        # Placeholder for create account functionality
        print("Create Account button clicked")

    def login(self):
        # Placeholder for login functionality
        print("Login button clicked")

    def forgot_password(self):
        # Placeholder for forgot password functionality
        print("Forgot Password button clicked")

if __name__ == "__main__":
    app = App()
    app.mainloop()
