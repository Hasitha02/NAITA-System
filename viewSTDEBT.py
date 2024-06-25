import customtkinter as ctk
from tkinter import messagebox
import mysql.connector

# Database connection configuration
db_config = {
    'user': 'root',
    'password': 'prabhashi915',
    'host': 'localhost',
    'database': 'NAITA'
}


# Function to retrieve data from the database
def retrieve_data():
    full_name = entry_full_name.get()
    nic = entry_nic.get()

    if not full_name or not nic:
        messagebox.showwarning("Input Error", "Please enter both Full Name and NIC.")
        return

    try:
        # Connect to the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        headers_mapping = {
             'category' : 'Category',
             'district' : 'District',
             'dateOfRegistration' : 'Date Of Registration',
             'indexNumber' : 'Index Number',
             'name' : 'Name',
             'fullName' : 'Full Name',
             'dateofBirth' : 'Date Of Birth',
             'gender' : 'Gender',
             'NIC' : 'NIC',
             'telephoneNumber' : 'Telephone Number',
             'NAITAIDnumber' : 'NAITA ID Number',
             'dropOut' : 'Dropout',
             'dropOutDate' : 'Dropout Date',
             'addressNo' : 'Address No',
             'addressFLine' : 'Address First Line',
             'addressLLine' : 'Address Last Line',
             'nameofEstablishment' : 'Name Of Establishment',
             'establishmentType' : 'Establishment Type',
             'establishmentAddressDivision' : 'Establishment Address Division',
             'establishmentAddressDistrict' : 'Establishment Address District',
             'establishmentTelephone' : 'Establishment Telephone',
             'DSDivision' : 'DS Division',
             'establishmentCode' : 'Establishment Code',
             'sectorName' : 'Sector Name',
             'trade' : 'Trade',
             'tradeCode' : 'Trade Code',
             'mode' : 'Mode',
             'NVQLevel' : 'NVQ Level',
             'inspectorName' : 'Inspector Name',
             'commencementDate' : 'Commencement Date',
             'scheduleDateCompletion' : 'Schedule Date Completion',
             'signatureTM' : 'Signature TM',
             'remark' : 'Remark'
        }

        # Query to retrieve data using a CTE
        query = """
            WITH StudentData AS (
                SELECT * FROM EBTSD WHERE fullName = %s AND NIC = %s
            )
            SELECT * FROM StudentData;
        """
        cursor.execute(query, (full_name, nic))
        result = cursor.fetchone()

        if result:
            result_text = ""
            for key, header in headers_mapping.items():
                if key in result:
                    result_text += f"{header}: {result[key]}\n\n"

            # Adding extra newlines for spacing
            text_result.configure(state='normal')
            text_result.delete("1.0", ctk.END)
            text_result.insert(ctk.END, result_text)
            text_result.configure(state='disabled')
        else:
            messagebox.showinfo("No Results", "No data found for the given Full Name and NIC.")

        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")


# Create the main application window
app = ctk.CTk()
app.title("View Students")
app.geometry("1080x600")

# Set background color to white for the app
app.configure(bg="white")

# Main Frame to hold other widgets
main_frame = ctk.CTkFrame(app, fg_color="white")
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

# Header Section
header_frame = ctk.CTkFrame(main_frame, fg_color="white")
header_frame.pack(pady=10, padx=20, fill="x", expand=False)

header_label = ctk.CTkLabel(header_frame, text="Search Student Details - EBT", font=("Arial", 29, "bold"),
                            fg_color="white", text_color="black")
header_label.pack(pady=10, padx=150, anchor="center")

# Form Section
form_frame = ctk.CTkFrame(main_frame, fg_color="white")
form_frame.pack(pady=10, padx=20, fill="x", expand=False)

# Full Name entry
full_name_label = ctk.CTkLabel(form_frame, text="Full Name:", text_color="black", font=("Arial", 14, "bold"), fg_color="white")
full_name_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

entry_full_name = ctk.CTkEntry(form_frame, width=300, fg_color="white", text_color="black", font=("Arial", 14))
entry_full_name.grid(row=0, column=1, padx=10, pady=5, sticky="w")

# NIC entry
nic_label = ctk.CTkLabel(form_frame, text="NIC:", text_color="black", font=("Arial", 14, "bold"), fg_color="white")
nic_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

entry_nic = ctk.CTkEntry(form_frame, width=300, fg_color="white", text_color="black", font=("Arial", 14))
entry_nic.grid(row=1, column=1, padx=10, pady=5, sticky="w")

# Retrieve Button
btn_retrieve = ctk.CTkButton(main_frame, text="Retrieve Data", font=("Arial", 14), fg_color="crimson", text_color="white", command=retrieve_data)
btn_retrieve.pack(pady=20)

# Textbox to display results
text_result = ctk.CTkTextbox(main_frame, width=800, height=600, fg_color="gray", text_color="black", font=("Arial", 14))
text_result.pack(pady=(0, 20))
text_result.configure(state='disabled')

# Start the application
app.mainloop()
