import customtkinter as ctk
from tkinter import messagebox, ttk, filedialog, LEFT
import mysql.connector
from openpyxl import Workbook
import datetime
from PIL import Image

# Database connection configuration
db_config = {
    'user': 'root',
    'password': 'prabhashi915',
    'host': 'localhost',
    'database': 'NAITA'
}

# Function to retrieve and display all student data from the database
def retrieve_all_data():
    try:
        # Connect to the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # Query to retrieve all data
        query = "SELECT * FROM CBTSD"
        cursor.execute(query)
        results = cursor.fetchall()

        # Clear existing data in the treeview
        for item in tree.get_children():
            tree.delete(item)

        if results:
            for record in results:
                # Insert each record into the treeview
                values = [record.get(col, '') for col in columns]
                tree.insert("", "end", values=values)

        else:
            messagebox.showinfo("No Results", "No data found.")

        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

def format_date(date_value):
    try:
        # Try converting to datetime object and formatting
        if isinstance(date_value, datetime.date):
            return date_value.strftime('%Y-%m-%d')
        elif isinstance(date_value, str):
            return datetime.datetime.strptime(date_value, '%Y-%m-%d').strftime('%Y-%m-%d')
    except ValueError:
        return None

def print_to_excel():
    answer = messagebox.askyesno("Confirmation", "Are you sure you want to print data to Excel?")

    if answer:
        try:
            # Create a new workbook
            workbook = Workbook()
            sheet = workbook.active

            # Add headers to the worksheet
            headers = [
                "01. Category", "02. District", "03. Date of Registration", "04. Index Number",
                "05. Name with Initials", "06. Full Name", "07. Date of Birth", "08. Gender",
                "09. NIC", "10. Telephone Number", "11. NAITA ID Number", "12. Drop Out",
                "13. Drop Out Date", "14. Address - No.", "15. Address - First Line", "16. Address - Last Line",
                "17. Name of Establishment", "18. Type of Establishment", "19. Establishment Address Division",
                "20. Establishment Address District", "21. Establishment Telephone Number", "22. DS Division",
                "23. Establishment Code", "24. Sector Name", "25. Trade", "26. Trade Code", "27. Mode",
                "28. NVQ Level", "29. Name of Inspector", "30. Commencement Date",
                "31. Schedule Date of Completion",
                "32. Signature of T.M.", "33. Remark"
            ]
            sheet.append(headers)

            # Collect data from the treeview
            for item in tree.get_children():
                row_data = [tree.item(item, 'values')[i] for i in range(len(columns))]
                sheet.append(row_data)

            # Ask user for file name and directory to save
            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", ".xlsx"), ("All files", ".*")],
                title="Save Excel file"
            )

            if file_path:
                workbook.save(file_path)
                messagebox.showinfo("Printed", f"Data has been printed to {file_path}")

        except PermissionError:
            messagebox.showerror("Error", "Could not save data to Excel.\nPlease close any open Excel file and try again.")

# Create the main application window
app = ctk.CTk()
app.title("View Students")
app.geometry("1080x600")
app.configure(bg="white")

# Main Frame to hold other widgets
main_frame = ctk.CTkFrame(app, fg_color="white")
main_frame.pack(fill="both", expand=True, padx=10, pady=10)
image = Image.open("bg.png")
photo = ctk.CTkImage(light_image=image, dark_image=image, size=(1080, 600))
label_image = ctk.CTkLabel(master=main_frame, text='', image=photo)
label_image.place(relx=0, rely=0)

# Header Section
header_frame = ctk.CTkFrame(main_frame, fg_color="white")
header_frame.pack(pady=150, padx=40, fill="x", expand=False)  # Increase pady to lower the header

header_label = ctk.CTkLabel(header_frame, text="All Student Details - CBT", font=("Arial", 29, "bold"),
                            fg_color="white", text_color="black")
header_label.pack(pady=(30, 10), padx=150, anchor="center")  # Reduced the gap below the label

# Frame to hold buttons
button_frame = ctk.CTkFrame(header_frame, fg_color="white")
button_frame.pack(pady=(20, 0))  # Adjust padding as needed

# Retrieve Button
btn_retrieve = ctk.CTkButton(button_frame, text="Retrieve All Data", font=("Arial", 14, "bold"),
                             fg_color="crimson", text_color="white", command=retrieve_all_data)
btn_retrieve.pack(side=LEFT, padx=(20, 10), anchor='center')  # Pack to the left with center anchor

# Print Button
print_button = ctk.CTkButton(button_frame, text="Print", font=("Arial", 14, "bold"),
                             fg_color="crimson", text_color="white", command=print_to_excel)
print_button.pack(side=LEFT, padx=(10, 20), anchor='center')  # Pack to the left with center anchor

style = ttk.Style()
style.configure("Treeview", font=("Arial", 13))  # Increase the font size for rows
style.configure("Treeview.Heading", font=("Arial", 13, "bold"))  # Increase the font size for headers

# Frame for Treeview and scrollbars
tree_frame = ctk.CTkFrame(main_frame, fg_color="white")
tree_frame.pack(fill="both", expand=True, pady=(0, 0))  # Adjusted pady to move Treeview upwards

# Table to display results
columns = ['category', 'district', 'dateOfRegistration', 'indexNumber', 'name', 'fullName',
           'dateofBirth', 'gender', 'NIC', 'telephoneNumber', 'NAITAIDnumber', 'dropOut',
           'dropOutDate', 'addressNo', 'addressFLine', 'addressLLine', 'nameofEstablishment',
           'establishmentType', 'establishmentAddressDivision', 'establishmentAddressDistrict',
           'establishmentTelephone', 'DSDivision', 'establishmentCode', 'sectorName', 'trade',
           'tradeCode', 'mode', 'NVQLevel', 'inspectorName', 'commencementDate',
           'scheduleDateCompletion', 'signatureTM', 'remark']

column_names = ['Category', 'District', 'Date Of Registration', 'Index Number', 'Name', 'Full Name',
                'Date Of Birth', 'Gender', 'NIC', 'Telephone Number', 'NAITA ID Number', 'Dropout',
                'Dropout Date', 'Address No', 'Address First Line', 'Address Last Line',
                'Name Of Establishment', 'Establishment Type', 'Establishment Address Division',
                'Establishment Address District', 'Establishment Telephone', 'DS Division',
                'Establishment Code', 'Sector Name', 'Trade', 'Trade Code', 'Mode', 'NVQ Level',
                'Inspector Name', 'Commencement Date', 'Schedule Date Completion', 'Signature TM',
                'Remark']

# Create a Treeview widget
tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=20)

# Set up columns and column headings
for col, col_name in zip(columns, column_names):
    tree.heading(col, text=col_name)
    tree.column(col, width=350, anchor='center')

# Configure vertical scrollbar for the Treeview
v_scrollbar = ctk.CTkScrollbar(tree_frame, command=tree.yview)
tree.configure(yscrollcommand=v_scrollbar.set)
v_scrollbar.pack(side='right', fill='y')

# Configure horizontal scrollbar for the Treeview
h_scrollbar = ctk.CTkScrollbar(tree_frame, command=tree.xview, orientation='horizontal')
tree.configure(xscrollcommand=h_scrollbar.set)
h_scrollbar.pack(side='bottom', fill='x')

# Pack the Treeview widget
tree.pack(fill='both', expand=True)

# Start the application
app.mainloop()
