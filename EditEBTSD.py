import customtkinter as ctk
import mysql.connector
from tkinter import messagebox

# Database connection configuration
db_config = {
    'user': 'root',
    'password': 'hasitha0214',
    'host': 'localhost',
    'database': 'NAITA'
}

# Function to search data in the database
def search_data():
    username = entry_username.get()
    nic = entry_nic.get()

    if not username or not nic:
        messagebox.showwarning("Input Error", "Please enter both Username and NIC.")
        return

    try:
        # Connect to the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # Query to search for data
        query = "SELECT * FROM EBTSD WHERE fullName = %s AND NIC = %s"
        cursor.execute(query, (username, nic))
        result = cursor.fetchone()

        if result:
            # Populate fields in the edit form
            for key, value in result.items():
                if key in entry_fields:
                    entry_fields[key].delete(0, ctk.END)
                    entry_fields[key].insert(0, str(value))  # Ensure the value is a string
            app.withdraw()  # Hide the main application window
            edit_form.deiconify()  # Show the edit form
        else:
            messagebox.showinfo("No Results", "No data found for the given Username and NIC.")

        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    except Exception as e:
        messagebox.showerror("Error", f"Unexpected error: {e}")

# Function to update data in the database
def update_data():
    if not messagebox.askyesno("Confirm Update", "Are you sure you want to update the data?"):
        return

    data = {key: entry.get() for key, entry in entry_fields.items()}

    try:
        # Connect to the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Query to update data
        query = """UPDATE EBTSD SET category=%s, district=%s, dateOfRegistration=%s, 
                   name=%s, fullName=%s, dateofBirth=%s, gender=%s, telephoneNumber=%s,
                   NAITAIDnumber=%s, dropOut=%s, dropOutDate=%s, addressNo=%s, 
                   addressFLine=%s, addressLLine=%s, nameofEstablishment=%s, 
                   establishmentType=%s, establishmentAddressDivision=%s, 
                   establishmentAddressDistrict=%s, establishmentTelephone=%s, 
                   DSDivision=%s, establishmentCode=%s, sectorName=%s, trade=%s, 
                   tradeCode=%s, mode=%s, NVQLevel=%s, inspectorName=%s, 
                   commencementDate=%s, scheduleDateCompletion=%s, signatureTM=%s, 
                   remark=%s WHERE indexNumber=%s"""
        cursor.execute(query, (
            data['category'], data['district'], data['dateOfRegistration'],
            data['name'], data['fullName'], data['dateofBirth'], data['gender'],
            data['telephoneNumber'], data['NAITAIDnumber'], data['dropOut'],
            data['dropOutDate'], data['addressNo'], data['addressFLine'],
            data['addressLLine'], data['nameofEstablishment'],
            data['establishmentType'], data['establishmentAddressDivision'],
            data['establishmentAddressDistrict'], data['establishmentTelephone'],
            data['DSDivision'], data['establishmentCode'], data['sectorName'],
            data['trade'], data['tradeCode'], data['mode'], data['NVQLevel'],
            data['inspectorName'], data['commencementDate'],
            data['scheduleDateCompletion'], data['signatureTM'],
            data['remark'], data['indexNumber']
        ))

        conn.commit()
        cursor.close()
        conn.close()

        messagebox.showinfo("Success", "Data updated successfully.")
        edit_form.destroy()  # Destroy the edit form
        app.quit()  # Terminate the main loop
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    except Exception as e:
        messagebox.showerror("Error", f"Unexpected error: {e}")

# Function to terminate the application
def on_closing():
    app.quit()

# Create the main application window
app = ctk.CTk()
app.title("Data Retrieval")
app.geometry("400x300")
app.protocol("WM_DELETE_WINDOW", on_closing)

# Set background color to white
main_frame = ctk.CTkFrame(app, fg_color="white")
main_frame.pack(fill="both", expand=True)

# Username and NIC entry
ctk.CTkLabel(main_frame, text="Full Name:", text_color="black").pack(pady=(20, 5))
entry_username = ctk.CTkEntry(main_frame, width=300, fg_color="#A1AEB1", text_color="black")
entry_username.pack(pady=5)

ctk.CTkLabel(main_frame, text="NIC:", text_color="black").pack(pady=(20, 5))
entry_nic = ctk.CTkEntry(main_frame, width=300, fg_color="#A1AEB1", text_color="black")
entry_nic.pack(pady=5)

# Search Button
btn_search = ctk.CTkButton(main_frame, text="Search", fg_color='crimson', command=search_data)
btn_search.pack(pady=20)

# Edit form
edit_form = ctk.CTkToplevel(app)
edit_form.title("Edit Data")
edit_form.geometry("500x700")
edit_form.protocol("WM_DELETE_WINDOW", on_closing)
edit_form.withdraw()  # Hide the form initially

# Set background color to white
edit_frame = ctk.CTkFrame(edit_form, fg_color="white")
edit_frame.pack(fill="both", expand=True)

# Create a scrollable frame for the fields
scrollable_frame = ctk.CTkScrollableFrame(edit_frame, fg_color="white", width=450, height=600)
scrollable_frame.pack(pady=10, padx=10, fill="both", expand=True)

# Create fields for each column in the EBTSD table
entry_fields = {}
fields = ["category", "district", "dateOfRegistration", "indexNumber", "name", "fullName",
          "dateofBirth", "gender", "NIC", "telephoneNumber", "NAITAIDnumber", "dropOut",
          "dropOutDate", "addressNo", "addressFLine", "addressLLine", "nameofEstablishment",
          "establishmentType", "establishmentAddressDivision", "establishmentAddressDistrict",
          "establishmentTelephone", "DSDivision", "establishmentCode", "sectorName", "trade",
          "tradeCode", "mode", "NVQLevel", "inspectorName", "commencementDate",
          "scheduleDateCompletion", "signatureTM", "remark"]

for field in fields:
    ctk.CTkLabel(scrollable_frame, text=field + ":", text_color="black").pack(pady=(5, 0))
    entry_fields[field] = ctk.CTkEntry(scrollable_frame, width=300, fg_color="#A1AEB1", text_color="black")
    entry_fields[field].pack(pady=5)

# Update Button
btn_update = ctk.CTkButton(scrollable_frame, fg_color='crimson', text="Update", command=update_data)
btn_update.pack(pady=20)

# Start the application
app.mainloop()
