import customtkinter as ctk
from tkinter import StringVar, Frame, Scrollbar, Canvas, VERTICAL, RIGHT, LEFT, Y, BOTH, messagebox, filedialog
from tkcalendar import DateEntry
import mysql.connector
from mysql.connector import Error
import re
from openpyxl import Workbook
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas as pdf_canvas

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
def insert_into_db(*args):
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("USE NAITA;")
            query = """INSERT INTO EBTSD (category, district, dateOfRegistration, indexNumber, name, fullName, dateofBirth, gender, NIC,
                       telephoneNumber, NAITAIDnumber, dropOut, dropOutDate, addressNo, addressFLine, addressLLine, nameofEstablishment, establishmentType,
                       establishmentAddressDivision, establishmentAddressDistrict, establishmentTelephone, DSDivision, establishmentCode,
                       sectorName, trade, tradeCode, mode, NVQLevel, inspectorName, commencementDate, scheduleDateCompletion, signatureTM, remark)
                       VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(query, args)
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except Error:
            messagebox.showerror("Database Error", f"Error inserting data into the Database. Please check again.")
            return False


def form():
    # Create the main application window
    app = ctk.CTk()
    app.title("Form")
    app.geometry("1080x706")

    # Create a frame for the form
    form_frame = ctk.CTkFrame(app, fg_color="white")  # Whitish background
    form_frame.pack(padx=5, pady=5, fill="both", expand=True)

    # Create a canvas to hold the form and a scrollbar
    canvas = Canvas(form_frame, bg="#f0f0f0")  # Light background for canvas
    canvas.pack(side=LEFT, fill=BOTH, expand=True)

    scrollbar = Scrollbar(form_frame, orient=VERTICAL, command=canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    canvas.configure(yscrollcommand=scrollbar.set)

    scrollable_frame = Frame(canvas, bg="#f0f0f0")  # Light background for scrollable frame
    scrollable_frame_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def on_mouse_wheel(event):
        canvas.yview_scroll(-1 * int(event.delta / 120), "units")

    def submit():
        # Validate all fields before submission
        required_fields = [
            district_var.get(), date_of_registration.get(), index_number.get(), name.get(),
            full_name.get(), date_of_birth.get(), gender_var.get(), nic.get(), telephone_number.get(),
            naita_id_number.get(), address_no.get(), address_f_line.get(), address_l_line.get(),
            name_of_establishment_var.get(), establishment_type.get(), establishment_address_division.get(),
            establishment_address_district.get(), establishment_telephone.get(), ds_division.get(),
            establishment_code.get(), sector_var.get(), trade_var.get(), trade_code.get(), mode_var.get(),
            nvq_level_var.get(), inspector_var.get(), commencement_date.get(), schedule_date_completion.get(),
            signature_tm.get(), remark.get()
        ]

        # Add dropout date only if dropout is "Yes"
        if dropout_var.get() == "Yes":
            required_fields.append(dropout_date.get())

        nic_pattern_12_digits = re.compile(r'^\d{12}$')
        nic_pattern_9_digits_1_letter = re.compile(r'^\d{9}[A-Za-z]$')

        if not all(required_fields):
            messagebox.showerror("Error", "Please fill out all fields.")
        elif len(telephone_number.get()) != 10 or not telephone_number.get().isdigit():
            messagebox.showerror("Error", "Phone number should be exactly 10 digits and numeric only.")
        elif len(establishment_telephone.get()) != 10 or not establishment_telephone.get().isdigit():
            messagebox.showerror("Error", "Establishment phone number should be exactly 10 digits and numeric only.")
        elif not (nic_pattern_12_digits.match(nic.get()) or nic_pattern_9_digits_1_letter.match(nic.get())):
            messagebox.showerror("Error", "NIC should be exactly 12 digits or 9 digits followed by one letter.")
        else:
            # Confirmation dialog
            confirmed = messagebox.askyesno("Submit Form", "Are you sure you want to submit this form?")
            if confirmed:
                dropout_date_value = dropout_date.get() if dropout_var.get() == "Yes" else None

                if insert_into_db(
                        "EBT - Enterprise Based Training", district_var.get(), date_of_registration.get(),
                        index_number.get(),
                        name.get(), full_name.get(), date_of_birth.get(), gender_var.get(), nic.get(),
                        telephone_number.get(),
                        naita_id_number.get(), dropout_var.get(), dropout_date_value, address_no.get(),
                        address_f_line.get(),
                        address_l_line.get(), name_of_establishment_var.get(), establishment_type.get(),
                        establishment_address_division.get(), establishment_address_district.get(),
                        establishment_telephone.get(),
                        ds_division.get(), establishment_code.get(), sector_var.get(), trade_var.get(),
                        trade_code.get(),
                        mode_var.get(), nvq_level_var.get(), inspector_var.get(), commencement_date.get(),
                        schedule_date_completion.get(), signature_tm.get(), remark.get()
                ):
                    messagebox.showinfo("Success", "Form submitted successfully.")
            else:
                messagebox.showinfo("Submission Cancelled", "Form submission cancelled.")

    def back():
        print("a")
    def clear_form():
        # Ask for confirmation
        answer = messagebox.askyesno("Confirmation", "Are you sure you want to clear all fields?")

        if answer:
            # Function to clear all input fields
            for widget in scrollable_frame.winfo_children():
                if isinstance(widget, ctk.CTkEntry) or isinstance(widget, DateEntry):
                    widget.delete(0, 'end')
                elif isinstance(widget, ctk.CTkOptionMenu):
                    widget.set("")
                elif isinstance(widget, Frame):
                    for inner_widget in widget.winfo_children():
                        if isinstance(inner_widget, ctk.CTkEntry) or isinstance(inner_widget, DateEntry):
                            inner_widget.delete(0, 'end')
                        elif isinstance(inner_widget, ctk.CTkComboBox):
                            inner_widget.set("")
                        elif isinstance(inner_widget, Frame):
                            for radio in inner_widget.winfo_children():
                                if isinstance(radio, ctk.CTkRadioButton):
                                    radio.deselect()

    scrollable_frame.bind("<Configure>", on_frame_configure)
    canvas.bind_all("<MouseWheel>", on_mouse_wheel)

    def format_date(date_value):
        # Ensure date_value is a valid date
        if date_value:
            if isinstance(date_value, str):
                # If date_value is a string, try to convert it to datetime
                try:
                    date_value = datetime.datetime.strptime(date_value, '%Y-%m-%d').date()
                except ValueError:
                    return None
            return date_value.strftime('%Y-%m-%d')
        else:
            return None

    def save_to_pdf(file_path, headers, data):
        c = pdf_canvas.Canvas(file_path, pagesize=letter)
        width, height = letter

        x_offset = 40
        y_offset = height - 40
        line_height = 20

        # Write headers and data
        for header, datum in zip(headers, data[0]):
            c.drawString(x_offset, y_offset, f"{header}: {datum}")
            y_offset -= line_height

        c.save()

    def print_to_excel():
        # Ask for confirmation
        answer = messagebox.askyesno("Confirmation", "Are you sure you want to print the file?")

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

                # Collect form data and format dates
                data = [
                    [
                        "EBT - Enterprise Based Training", district_var.get(),
                        format_date(date_of_registration.get_date()),
                        index_number.get(), name.get(), full_name.get(), format_date(date_of_birth.get_date()),
                        gender_var.get(), nic.get(), telephone_number.get(), naita_id_number.get(), dropout_var.get(),
                        format_date(dropout_date.get_date()), address_no.get(), address_f_line.get(),
                        address_l_line.get(),
                        name_of_establishment_var.get(), establishment_type.get(), establishment_address_division.get(),
                        establishment_address_district.get(), establishment_telephone.get(), ds_division.get(),
                        establishment_code.get(), sector_var.get(), trade_var.get(), trade_code.get(), mode_var.get(),
                        nvq_level_var.get(), inspector_var.get(), format_date(commencement_date.get_date()),
                        format_date(schedule_date_completion.get_date()), signature_tm.get(), remark.get()
                    ]
                ]
                sheet.append(data[0])

                # Ask user for file name and directory to save
                file_path = filedialog.asksaveasfilename(
                    defaultextension=".xlsx",
                    filetypes=[("Excel files", "*.xlsx"), ("PDF files", "*.pdf"), ("All files", "*.*")],
                    title="Save file"
                )

                # Check if user canceled the dialog
                if file_path:
                    if file_path.endswith('.xlsx'):
                        # Save the workbook to the specified file
                        workbook.save(file_path)

                        # Show information box
                        messagebox.showinfo("Printed", f"Data has been printed to {file_path}")

                    elif file_path.endswith('.pdf'):
                        # Save the data to a PDF file
                        save_to_pdf(file_path, headers, data)

                        # Show information box
                        messagebox.showinfo("Printed", f"Data has been printed to {file_path}")

            except PermissionError:
                messagebox.showerror("Error", "Could not save data to file.\n"
                                              "Please close any open files and try again.")


    # Helper function to create labels and entries
    def create_label_entry(parent, row, label_text, col_offset=0, label_width=20, font_size=14):
        label = ctk.CTkLabel(parent, text=label_text, font=("Arial", font_size), fg_color="#f0f0f0", text_color="black",
                             anchor="w", width=label_width * 10)
        label.grid(row=row, column=col_offset, padx=5, pady=5, sticky="w")

        entry = ctk.CTkEntry(parent, width=300, font=("Arial", font_size), fg_color="#A1AEB1", text_color="black")
        entry.grid(row=row, column=col_offset + 1, padx=5, pady=5, sticky="w")

        return entry

    # Section 1: Category to Address of the Apprentice
    section1_frame = ctk.CTkFrame(scrollable_frame, fg_color="#f0f0f0")  # Whitish background for sections
    section1_frame.pack(pady=10, padx=20, fill="x", expand=True, anchor="center")

    header1 = ctk.CTkLabel(section1_frame, text="Student Registration Form - EBT    ", font=("Arial", 29, "bold"),
                           fg_color="#f0f0f0", text_color="black")
    header1.grid(row=0, column=0, columnspan=2, pady=10, padx=150, sticky="w")  # Center header

    header1 = ctk.CTkLabel(section1_frame, text="Apprentice Details", font=("Arial", 20, "bold"),
                           fg_color="#f0f0f0", text_color="black")
    header1.grid(row=1, column=0, columnspan=2, pady=10, padx=100, sticky="w")  # Center header

    # Categories (Fixed to "EBT")
    category_label = ctk.CTkLabel(section1_frame, text="01. Category", font=("Arial", 14), fg_color="#f0f0f0",
                                  text_color="black", anchor="w")
    category_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

    category_value = ctk.CTkLabel(section1_frame, text="EBT - Enterprise Based Training", font=("Arial", 14),
                                  text_color="black", anchor="w")
    category_value.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    # District Dropdown
    district_label = ctk.CTkLabel(section1_frame, text="02. District", font=("Arial", 14), fg_color="#f0f0f0",
                                  text_color="black", anchor="w")
    district_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")

    district_values =["Ampara", "Anuradhapura", "Badulla", "Batticaloa", "Colombo", "Gampaha", "Galle", "Hambantota",
        "Jaffna", "Kalutara", "Kandy", "Kegalle", "Kilinochchi", "Kurunegala", "Mannar", "Matale",
        "Matara", "Monaragala", "Mullaitivu", "Nuwara Eliya", "Polonnaruwa", "Puttalam", "Ratnapura",
        "Trincomalee", "Vavuniya"]
    district_var = StringVar()
    district_dropdown = ctk.CTkComboBox(section1_frame, variable=district_var, fg_color="#A1AEB1",
                                        values=district_values, width=300,
                                        font=("Arial", 14), button_color="gray", button_hover_color="#888",
                                        text_color="black")
    district_dropdown.grid(row=3, column=1, padx=5, pady=5, sticky="w")

    def update_district_combobox(event):
        value = event.widget.get()
        if value == '':
            filtered_values = district_values
        else:
            filtered_values = [item for item in district_values if value.lower() in item.lower()]

        district_dropdown.configure(values=filtered_values)
        district_dropdown.event_generate('<Down>')

    district_dropdown._entry.bind('<KeyRelease>', update_district_combobox)

    # Other fields
    date_of_registration_label = ctk.CTkLabel(section1_frame, text="03. Date of Registration", font=("Arial", 14), fg_color="#f0f0f0",
                                      text_color="black", anchor="w")
    date_of_registration_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")
    date_of_registration = DateEntry(section1_frame, width=31, background='gray', foreground='white', borderwidth=2,
                                     font=("Arial", 14))
    date_of_registration.grid(row=4, column=1, padx=5, pady=5, sticky="w")

    index_number = create_label_entry(section1_frame, 5, "04. Index Number", font_size=14)

    header_name = ctk.CTkLabel(section1_frame, text=" 05. Name of Apprentice", font=("Arial", 14),
                           fg_color="#f0f0f0", text_color="black")
    header_name.grid(row=7, column=0, columnspan=2, pady=10, sticky="w")

    name = create_label_entry(section1_frame, 8, "      a. Full Name", font_size=14)
    full_name = create_label_entry(section1_frame, 9, "      b. Name with Initials", font_size=14)

    date_of_birth_label = ctk.CTkLabel(section1_frame, text="06. Date of Birth", font=("Arial", 14),
                                              fg_color="#f0f0f0",
                                              text_color="black", anchor="w")
    date_of_birth_label.grid(row=10, column=0, padx=5, pady=5, sticky="w")
    date_of_birth = DateEntry(section1_frame, width=31, background='gray', foreground='white', borderwidth=2,
                              font=("Arial", 14))
    date_of_birth.grid(row=10, column=1, padx=5, pady=5, sticky="w")


    # Gender Radio Buttons
    gender_label = ctk.CTkLabel(section1_frame, text="07. Gender", font=("Arial", 14), fg_color="#f0f0f0",
                                text_color="black", anchor="w")
    gender_label.grid(row=11, column=0, padx=5, pady=5, sticky="w")

    gender_var = StringVar()
    gender_buttons_frame = Frame(section1_frame, bg="#f0f0f0")
    gender_buttons_frame.grid(row=11, column=1, padx=5, pady=5, sticky="w")

    male_radio = ctk.CTkRadioButton(gender_buttons_frame, text="Male", variable=gender_var, value="Male",
                                     font=("Arial", 14), fg_color="black", text_color="black")
    female_radio = ctk.CTkRadioButton(gender_buttons_frame, text="Female", variable=gender_var, value="Female",
                                      font=("Arial", 14), fg_color="black", text_color="black")
    male_radio.pack(side=LEFT, padx=5)
    female_radio.pack(side=LEFT, padx=5)

    # NIC Entry
    nic = create_label_entry(section1_frame, 12, "08. NIC", font_size=14)
    nic.grid(row=12, column=1, padx=5, pady=5, sticky="w")

    # Telephone Number Entry
    telephone_number = create_label_entry(section1_frame, 13, "09. Telephone Number", font_size=14)
    telephone_number.grid(row=13, column=1, padx=5, pady=5, sticky="w")

    # NAITA ID Number Entry
    naita_id_number = create_label_entry(section1_frame, 14, "10. NAITA ID Number", font_size=14)
    naita_id_number.grid(row=14, column=1, padx=5, pady=5, sticky="w")

    # Dropout Radio Buttons
    dropout_label = ctk.CTkLabel(section1_frame, text="11. Dropout", font=("Arial", 14), fg_color="#f0f0f0",
                                 text_color="black", anchor="w")
    dropout_label.grid(row=15, column=0, padx=5, pady=5, sticky="w")


    dropout_var = StringVar(value="No")

    def toggle_dropout_date(*args):
        if dropout_var.get() == "Yes":
            dropout_date.config(state="normal")
        else:
            dropout_date.config(state="disabled")

    # Set up the dropout buttons frame
    dropout_buttons_frame = Frame(section1_frame, bg="#f0f0f0")
    dropout_buttons_frame.grid(row=15, column=1, padx=5, pady=5, sticky="w")

    # Create dropout radio buttons
    dropout_yes_radio = ctk.CTkRadioButton(dropout_buttons_frame, text="Yes", variable=dropout_var, value="Yes",
                                           font=("Arial", 14), fg_color="black", text_color="black")
    dropout_no_radio = ctk.CTkRadioButton(dropout_buttons_frame, text="No", variable=dropout_var, value="No",
                                          font=("Arial", 14), fg_color="black", text_color="black")

    # Pack radio buttons
    dropout_yes_radio.pack(side=LEFT, padx=5)
    dropout_no_radio.pack(side=LEFT, padx=5)

    # Add trace to dropout_var to call toggle_dropout_date whenever the value changes
    dropout_var.trace_add("write", toggle_dropout_date)

    # Dropout date label
    dropout_date_label = ctk.CTkLabel(section1_frame, text="12. Drop Out Date", font=("Arial", 14), fg_color="#f0f0f0",
                                      text_color="black", anchor="w")
    dropout_date_label.grid(row=16, column=0, padx=5, pady=5, sticky="w")

    # Dropout date entry
    dropout_date = DateEntry(section1_frame, width=31, background='gray', foreground='white', borderwidth=2,
                             font=("Arial", 14))
    dropout_date.grid(row=16, column=1, padx=5, pady=5, sticky="w")

    # Initially disable the dropout date entry
    dropout_date.config(state="disabled")

    header_name1 = ctk.CTkLabel(section1_frame, text=" 13. Address of Apprentice", font=("Arial", 14),
                               fg_color="#f0f0f0", text_color="black")
    header_name1.grid(row=17, column=0, columnspan=2, pady=10, sticky="w")

    # Address Entries
    address_no = create_label_entry(section1_frame, 18,"       a. No.", font_size=14)
    address_no.grid(row=18, column=1, padx=5, pady=5, sticky="w")

    address_f_line = create_label_entry(section1_frame, 19, "       b. First Line", font_size=14)
    address_f_line.grid(row=19, column=1, padx=5, pady=5, sticky="w")

    address_l_line = create_label_entry(section1_frame, 20, "       c. Last Line", font_size=14)
    address_l_line.grid(row=20, column=1, padx=5, pady=5, sticky="w")


    # Section Header 2
    header2 = ctk.CTkLabel(section1_frame, text="Establishment Details", font=("Arial", 20, "bold"),
                           fg_color="#f0f0f0", text_color="black")
    header2.grid(row=22, column=0, columnspan=2, pady=10, padx=100, sticky="w")  # Center header

    # Name of Establishment Dropdown
    name_of_establishment_label = ctk.CTkLabel(section1_frame, text="14. Name of the Establishment", font=("Arial", 14),fg_color="#f0f0f0",text_color="black", anchor="w")
    name_of_establishment_label.grid(row=24, column=0, padx=5, pady=5, sticky="w")
    name_of_establishment_values = [
        "_Smallholder Agribusiness Partnerships Program","141 Motors","141, MOTORS PVT LTD","171 Bakers","1st Step Pre School - Matale",
        "1st Way Preschool","3 Arch Resort Lanka(PVT)LTD","3K - Focus Marketing & Engineering","3K- Modern Construction",
        "4*4 Automotive Holdings pvt Ltd","49 Hotel Rathnagiri Estate","4x4 Zone (PVT)LTD","7 to 11 Restaurant","98 Acres Resort & Spa",
        "99, Super Center","A & A Lathe Works","A & J Brand","A & J Moters","A & S Aquarium-Amb","A & S Tailors","A 3 , Carpentry Work Shop",
        "A A A Motors-Matara","A.B.C. Apparels","A.C. & Ref Engineering Service-Dondra","A.D Spey House-Athuraliya","A.J. Automobiles",
        "A.M.G Motors","A.M.K Electronics","A Max Mobile Center","A NEW LADY FASHION LADIES TAILORING SHOP","A One Mini Supermarket",
        "A One Tailors","A S Electrical.","A S J Tailors","A Sun Tailoring","A Tech Electrical & Plumbing Work","A&Z Fashion",
        "A. Viven Welding Workshop","A.A.Mechanical Engineering Field","A.Asam Mohammed Tailor","A.B.M.Consuiting Service",
        "A.C.M. Abaya Showroom","A.C.M.Cassim Workshop","A.C.M.Motors","A.C.S. Agro Centre","A.D.I.Electrical Works","A.F.M. MOTORS",
        "A.G.C. Electricals","A.G.P. Computers","A.H.A. Mobile & Computer System","A.H.Illyas Carepntry Work Shop","A.H.M.UWAIS Tailoring & Textile",
        "A.J. Fishing Industries (Pvt) Ltd","A.J.Electrical Work Shop","A.J.glass works","A.J.M.Ali Motors","A.J.Tailor","A.K Motors",
        "A.K. Refrigeration & Air Condition","A.L.Anver Tailor","A.L.M. Nizar Carpentry Work Shop and Sale Cen","A.L.M.Nisar Saw Mill Carpentry Work Shop & Sa",
        "A.M. Kanifu Electricals","A.M.S.Hardware","A.M.A. TAILORS","A.M.Aasik Electrician","A.M.Akmal Welding Shop","A.N.A Traders",
        "A.N.S Timber & Hardware","A.R.M.Tyre Shop","A.R.Motors","A.S.A. Motors","A.S.MOTORS","A.V.S.C.Electronic","A.Viven Welding shop",
        "A.W. Fashion","A4 Motor Garage","A4 Villa","A9 Mobile","A-9 Service Station",
        "AA Electronics", "AA Raheem Cushion Works", "AAA Ifthik Tailor", "AAA Welding workshop", "Aagarsh Enterprices",
        "Aakash Tailoring", "Aakif Equipment Industry", "Aaliya Tailor Shop", "Aariz Tailoring Center",
        "Aarogya Health Care", "Aasik Motor", "Aatham Bawa Tailor", "Aatheel Motors & Welding", "Aathil Cusson Work",
        "Aathiparasakthi Preschool", "Aathmi Beauticare", "Aaththy Aari Work", "Aayisha Tailor Shop",
        "Aaysha Pre School", "Aayush Medicals", "Ababil Pre School", "Abans Customer Service Centre",
        "Abans Electrical PLC", "Abans Engineering (Pvt) Ltd", "Abans Service Centre..", "Abans Show Room",
        "Abaya Center", "ABC Kids Pre School", "ABC Medical Clinic", "ABC Pre School", "ABD Engineering (Pvt) Ltd",
        "Abdullah Digital", "Abdullah Tex & Tailors", "Abee Handloom", "Abesekara Elder Home", "Abesingha Auto Care",
        "Abeysekara Beauty Salon", "ABEYSEKARA MOTOR ENGINEERS (PVT) LTD", "ABEYSINGHA MOTORS",
        "Abeysinghe Fleet Managment Service (PVT) Ltd", "Abeywickrama Motors", "Abhaya Pharmacy & Medical Center",
        "Abhimani Early Childhood Development Center", "Abi Alakakam", "Abi Construction", "Abi Electrical",
        "ABI Garments", "ABI Gold Workshop", "Abi Mobile Plaza", "ABI Tailor Shop",
        "ABI Tailoring Centre-Chavakachcheri", "ABI Tailoring-Nallur", "Abirami Sitbalayam", "Abisagini Tailor shop",
        "Abiththa Timber Deport", "ABMS Construction", "Absaras City Hotel", "Access Motors Body Shop",
        "Accis Cellular", "Accounts & Management Agencies", "Acha Service Center (NEW)", "Achila Motors",
        "ACHINI AUTO MOBILE ENGINEERING WORKS", "Achini Printers-Thihagoda", "ACME Automobile", "Acme Transit Hotel",
        "Active Lanka Apperals", "Adana Beach Resort - Mirissa - Weligama", "Adaptive Research Centre",
        "Adarsha Minimuthu Pre School & Daya Care Cent", "Adaviya Resort", "Adchaya Pathra (Pvt) Ltd", "Adham Tailor",
        "Adhari Tailors", "ADHIKARI ELECTRICALS", "ACME Automobile", "Adithya Ayurvedic (pvt)Ltd",
        "Adithya Cement Works", "Adon Tailors", "Adron Saloon", "Advance Auto", "ADVANCE TECHNOLOGICAL INSTITUTE",
        "Advance Training Institute (ATI)", "Advanced Auto care", "Advanced Micro Technology (pvt)Ltd",
        "AFI Carpentry Workshop & Furniture Sales Cent", "Aflal Tailoring Centre", "Afnan Tex & Tailor",
        "Afran Electricals", "Afsara Flower Garden", "Afshan Electricals", "Agalawatta Auto Engineers", "Agbo Hotel",
        "Agith Motors", "AGN Mobile Centre", "Agog Bees Pre School", "Agra Institute", "Agrarian Cervice Centre",
        "Agrarian Development Office", "Agrarian Extension center", "Agrarian Service Center",
        "Agrarian Services Center", "Agricultural & Agrarian Insurance Board", "Agricultural Department",
        "Agriculture and Agrarian Insurance Board", "Agriculture Extension Center",
        "Agriculture Faculty,Univercity of Ruhuna", "Agriculture Farm Theravil Puthukudiyirippu",
        "Agriculture Instructor Office", "Agriculture Instructor Office & Agriculture E",
        "Agriculture School - Angunukolapalassa", "Agriculture Training Farm", "Agriculture Training School",
        "Agro Technology & Rural Science Univercity of", "Agro Turf International (Pvt) Ltd.", "Agromet Asia (Pvt) Ltd",
        "Agros & Agros (Private) Limited", "AHAMED MOTORS", "Aheel Timber Depot", "Ahijan Welding Shop",
        "Ahinsa Pre School", "Ahla Tailoring", "Ahnab Motors", "Ahnaf Motors",
        "Ahrensburg Janavijaya Pre School-Matara", "Aikkiyam Pre School", "AIMAN HAFNI CARPENTER",
        "Aiman Juweller & workshop", "AINA Tailor", "Air Care Engineers", "Air Cold Engineers",
        "Air Condition Engineering Service", "Air Cool", "Air Cool Engineers LK (Pvt) Ltd",
        "Air Free Refrigeration & Air Conditioning Eng", "Air Frost (Pvt) Ltd", "Air Mech Air Conditioning Company",
        "Air Mech Air Conditioning Company 2022", "Air Technic", "Air Technics", "AIRCONCO ENGINEERING COMPANY",
        "Air-condition Trinco Best Service", "Aircool Engineers", "Airport & Aviation Services (Pvt) Ltd",
        "AIRTECH M&E TECHNOLOGE", "Aitken Spence Printing & Packaging (Pvt) Ltd", "AIWARIYA WELDING WORKS",
        "AJ ELECTRICALS", "Ajanth Motors", "Ajantha Early Childhood Development Center", "AJANTHA SALON",
        "Ajanthan Grinding Mill", "Ajanthan Studio", "Ajanthan tailoring Shop", "Ajeena Motors", "AJI Welding shop",
        "Ajinthan Motor Works", "Ajith Auto A/C", "Ajith Auto Engineering", "Ajith Car Audio", "Ajith cushion Work",
        "Ajith Electrical", "Ajith Electricals Daladagama", "AJITH ENGINERING WORK", "Ajith Iron Works-Matara",
        "Ajith Learth Work Shop", "Ajith Motor Engineers", "Ajith Motors", "Ajith Painting-Kirinda", "Ajith Pharmacy",
        "AJITH SALOON", "Ajith Service Centre", "Ajith Tailors", "Ajith Tyre Service", "Ajith Wheel Alignment Centre",
        "Ajudsan Bicycle Repairing Center", "Ajuman Tinker, Painting & Repair Work Shop", "AK Enterprise",
        "Ak Fitting & Glass Work", "Akalanka Motors", "Akalya Beauty Parlor", "Akalya Tailor Center",
        "Akaram Palmyrah Product and Tailor Centre", "Akarsha Beauty Salon - A", "Akarsha Min Farm", "Akarsha Saloon",
        "AKASH AUTO CLINIC", "Akathiyan Welding Shop", "Akbar Auto Service", "AKIF Fashion Tailors", "Akila Motors",
        "Akila Resort", "Akila Tailoring", "Akilan Cushion Works", "Akilan Tailor Centre", "Akram Carpentry Workshop",
        "Akram Work Shop", "Akshana Tailoring", "Akshaya Clinic", "Akshaya Tailor", "Akshika Beauty parlour",
        "Akura Pre School", "Akway Resort", "Al Akeel Pre School", "Al- Akram Pre School", "Al Ameen Techno Craft",
        "AL- Aqsha Pre School- Muttur", "Al Azhar Pre School", "Al Fath Production Center", "Al Hathi Tailor",
        "Al Hikma Pre School", "Al Hilal pre school-dikwella", "Al Hima Pre School",
        "AL HIRA PRE CHILD EDUCATION CENTER", "Al Hithaya Pre School", "AL IGRAH PRE SCHOOL", "AL IQRAH KIDS CAMPUS",
        "Al Kamar Pre School", "AL- Mathaniya Pre School", "Al Nisa Tailoring Center", "Al- Raiz Service Center",
        "Al Rasad Pre School", "AL Riyan Tinkering", "Al Saif Carpentry Workshop", "AL Salihath Pre School",
        "Al- Yoosuf Construction", "Al Zaif Carpentry Workshop & Furniture Sales",
        "Alakamanda Hotel Management (Pvt) Ltd", "Alakuthurai Tailor Centre", "A'Lanka Resort & Spa",
        "Alankulam Womens Development Center", "AL-ASBRAQ PRESCHOOL", "Aleesha Tailor Shop", "Alex Construction",
        "Alfa Auto A/C Engineering", "Alfa Auto Electricals", "Alfa Omega Engineers", "Alfa Phone shop",
        "Al-Faththah Group of Tailoring", "Alfiya Tailor", "ALHIRA MUSLIM MAHA VIDYALAYA",
        "Al-Hudha Islamic Pre School", "Alina Construction (Mobile Construction Workers)","B.A.Cellular",
        "B.A.S.Automobile Engineering","B.M.Engineering Work ","B.M.D.Engineering Works(PVT) Ltd",
        "B.M.S.Motor Garage ","B.S.Automobile Engineers","B.V.Pre School ","B2P Pre School ",
        "Babalanthaya Shop","BABIYOLA TAILOR ","Babu Electircal","Babu Photography Studio",
        "BABY BEES PRE SCHOOL ","Badulla-District Training Centre ","Badulla-Vocational Training Centre for Disable Persons",
        "Baduriya Pre School ","BAGYA IRON WORKS","Bahitha Tailor ","Bajaj Auto Care Centre - weligama",
        "Bajaj Auto Cycle ","Bajaj Motors ","BAJAJ TVS AUTO SERVICE ","Bala Electrical Work Shop","Balachandran Civil Work's",
        "Balachandre Auto Mobile ","Balagala Tea Factory -Akuressa","BALAKADUWA MOTORS ","Balasooriya Motors ",
        "Balcony Dealz -Matara - B","Bandara Auto Paint ","Bandara Hotel ","Bandara Iron Works","Bandara Motors",
        "Bandara Studio ","Bandara Tyre House ","Bandaranayaka Hospital (Pvt) Ltd","Bandarawela Hotel","Bandarawela Multi Purpose Co-operative Socity",
        "Bandaththara Garments -Thihagoda","Bandhu Motors ","Bandula Motors ","Baptist Wise Eanjal Pre School ","Barathi Palmyrah center",
        "Barathi Pre School ","Barathy Pre School ","Barberyn Ayurvedic Beach Resort -Weligama","Barberyn Reef Hotel Ltd",
        "Baroon Show Room & Mobile phone repairing ","Basanayake Tyre, Oil Battery Center","Base Ayurveda Hospital ,Minneriya",
        "Base Hospital ","Base Hospital - Dehiyathakandiya","Base Hospital - Eravur","Base Hospital - Kalmunai",
        "Base Hospital - KP","Base Hospital - Oddusuddan","Base Hospital Puthukudiyirippu","BASE HOSPITAL PUTTALAM",
        "Base Hospital , Kiribathgoda","Base Hospital , Mallavi","Base Hospital ,Minuwangoda","Base Hospital -Akkaraipattu",
        "Base Hospital - Ninthvur","Base Hospital - Sammanthurai","Base Hospital - Thirukkovil","Bashini Motors ",
        "Basilisk Pre School ","Basith Motors ","Baskaran Electrical","Basnayaka Chemicals ","Basoom Shop",
        "Basuru Pharmacy ","BATHIK SITHMA","Bathimina Sacrificial items - Kamburupitiya","BATHIYA MOTORS ",
        "Bavani Tailoring ","Bavany Tailors","Bavarian Automobile Engineering (Pvt ) Ltd","Bawa Tailor",
        "Bawani Studio ","BBLC PRE SCHOOL ","B - Cool Auto A/C","Beach Inns Holiday Resort ","Zaara Mobiles",
        "Zaath Electrical and Mechanical Works","Zahra Tailor","Zahthifa Tailor","Zainab Phone Repair Soluation"
        "Zainee Tailor","Zaki Engineering","Zam Zam Pharmacy","Zam Zam Tailors","Zamzam Mechanical Workshop",
        "Zarook Motors","ZED Works","Zeenath Blossom","Zeenath Tex","Zeenun Tailors","Zenith Plantationa Engineering PVT LTD",
        "Zexel Diesel Engineers","Zimtha Punchar Shop","Zodiac Lubrcating Service","Zodiac Men's Fashion Tailors","Zonal Education Office"
    ]

    name_of_establishment_var = StringVar()
    name_of_establishment_dropdown = ctk.CTkComboBox(section1_frame, variable=name_of_establishment_var,
                                                     fg_color="#A1AEB1", values=name_of_establishment_values, width=300,
                                                     font=("Arial", 14), button_color="gray", button_hover_color="#888",
                                                     text_color="black")
    name_of_establishment_dropdown.grid(row=24, column=1, padx=5, pady=5, sticky="w")

    def update_name_of_establishment_combobox(event):
        value = event.widget.get()
        if value == '':
            filtered_values = name_of_establishment_values
        else:
            filtered_values = [item for item in name_of_establishment_values if value.lower() in item.lower()]

        name_of_establishment_dropdown.configure(values=filtered_values)
        name_of_establishment_dropdown.event_generate('<Down>')

    name_of_establishment_dropdown._entry.bind('<KeyRelease>', update_name_of_establishment_combobox)

    establishment_type = create_label_entry(section1_frame, 25, "15. Type of the Establishment", font_size=14)
    establishment_type.grid(row=25, column=1, padx=5, pady=5, sticky="w")

    establishment_address_division = create_label_entry(section1_frame, 26, "16. Establishment Address Division",
                                                        font_size=14)

    establishment_address_division.grid(row=26, column=1, padx=5, pady=5, sticky="w")

    establishment_address_district = create_label_entry(section1_frame, 27, "17. Establishment Address District",
                                                        font_size=14)
    establishment_address_district.grid(row=27, column=1, padx=5, pady=5, sticky="w")

    establishment_telephone = create_label_entry(section1_frame, 28, "18. Establishment Telephone", font_size=14)
    establishment_telephone.grid(row=28, column=1, padx=5, pady=5, sticky="w")

    ds_division = create_label_entry(section1_frame, 29, "19. DS Division", font_size=14)
    ds_division.grid(row=29, column=1, padx=5, pady=5, sticky="w")

    establishment_code = create_label_entry(section1_frame, 30, "20. Establishment Code", font_size=14)
    establishment_code.grid(row=30, column=1, padx=5, pady=5, sticky="w")



    header3 = ctk.CTkLabel(section1_frame, text="Course Details", font=("Arial", 20, "bold"),
                           fg_color="#f0f0f0", text_color="black")
    header3.grid(row=32, column=0, columnspan=2, pady=10,padx=100, sticky="w")

    def update_combobox(event):
        value = event.widget.get()
        if value == '':
            filtered_values = sector_values
        else:
            filtered_values = [item for item in sector_values if value.lower() in item.lower()]

        # Update combobox values
        sector_dropdown.configure(values=filtered_values)

        # Open the dropdown to show filtered results
        sector_dropdown.event_generate('<Down>')

    sector_label = ctk.CTkLabel(section1_frame, text="21. Sector", font=("Arial", 14), fg_color="#f0f0f0",
                                text_color="black", anchor="w")
    sector_label.grid(row=34, column=0, padx=5, pady=5, sticky="w")

    sector_values = [
        "Agriculture plantation and live stock", "Art design and media (visual and performing",
        "Automobile repair and maintenance",
        "Building and construction", "Electrical, Electronics and telecommunications",
        "Finance banking and management",
        "Fisheries and Aquaculture", "Food technology", "Gem and juwellary", "Hotel and tourism",
        "Information communication and multimedia technology", "Languages", "Leather and footwear",
        "Marine and nautical science",
        "Medical and health science", "Metal and light engineering", "Office management", "Other",
        "Personal and community development",
        "Printing and packing", "Refrigeration and air conditioning", "Rubber and plastic",
        "Textile and garments", "Wood related"]

    sector_var = StringVar()
    sector_dropdown = ctk.CTkComboBox(section1_frame, variable=sector_var, fg_color="#A1AEB1", values=sector_values,
                                      width=300,
                                      font=("Arial", 14), button_color="gray", button_hover_color="#888",
                                      text_color="black")
    sector_dropdown.grid(row=34, column=1, padx=5, pady=5, sticky="w")

    sector_dropdown._entry.bind('<KeyRelease>', update_combobox)

    trade_var = StringVar()
    # Trade Dropdown
    trade_label = ctk.CTkLabel(section1_frame, text="22. Trade", font=("Arial", 14), fg_color="#f0f0f0",
                               text_color="black", anchor="w")
    trade_label.grid(row=35, column=0, padx=5, pady=5, sticky="w")

    trade_values = [
        "3K - Aluminium fabricator", "3K - Aquarium keeper", "3K - Bathik artist", "3K - Beautician",
        "3K - Care giver", "3K - Construction craftman(masonry)", "3K - Customer services and assistant",
        "3K - Diary farming assistant", "3K - Electrician(Domestic)", "3K - Field assistant(Agriculture)",
        "3K - Hair dresser",
        "3K - Industrial sewing machine operator(Team member â€' sewing)", "3K - Medical laboratory assistant",
        "3K - Mobile phone repair technician",
        "3K - Plant nursery development assistant", "3K - Plumber", "3K - Room attendant", "3K - Tailor",
        "3K - Vehicle lube serviceman",
        "3K - Waiter / Steward", "3K - Welder(manual metal Arc)", "Aari works", "Accounts clerk", "Aesthetic Artist",
        "Agricultural Equipment & Machinery Mechanic", "Agricultural Equipment & Mechanic",
        "Agrochemical Sales & Technical Assistant",
        "Air Conditioning Serviceman", "Air Conditioning Technician", "Air Conditioning Mechanic",
        "AL-Aluminium Fabricator",
        "AL-Automobile Air Conditioning Technician", "AL-Automobile Mechanic", "AL-Construction Site Supervisor",
        "AL-Electrician",
        "AL-Field Assistant (Agriculture)", "AL-Floriculture and Landscape Development Assistant",
        "AL-Livestock Technician",
        "AL-Mobile Phone Repairing Craftsman", "AL-Plant Nursery Development Assistant",
        "AL-Solar Photovoltaic System Installer/ Solar Photovoltaic System Technician",
        "Aluminum Fabricator", "AL- Welder", "Air Embroidery", "Armature Winder", "Assistant Factory Officer (Tea)",
        "Assistant Field Officer (Tea)", "Auto Tinker/Welder",
        "Automation Technician", "Automobile Air Conditioning Mechanic", "Automobile Electrician",
        "Automobile Mechanic", "Automobile Painter", "Automobile Tinker",
        "Baby Toys and Baby Items Producer", "Bag Maker", "Baker", "Baker and Pastry Cook", "Barman", "Bartender",
        "Basic Book Binder", "Batik Artist",
        "Beautician", "Bellman", "Bicycle Repairer", "Blacksmith", "Boiler Attendant", "Boiler Operator", "Book Binder",
        "BT-Automobile Electrician",
        "BT-Automobile Mechanic", "BT-Automobile Painter", "BT-Cook", "BT- Field Assistant (Agriculture)",
        "BT-Housekeeping Supervisor", "BT-Waiter / Steward",
        "BT-Welder", "Business Associate", "Cake Decorating", "Cake Decorator", "Camera Operator(Block Making)",
        "Cane Product Maker", "Care Giver", "Care Giver(Elder)",
        "Carpenter", "Carpenter(Furniture)", "Carpenter(Wood Furniture)", "Cashier", "CELV - 3M", "Cement Block Maker",
        "Channeling Assistant", "Child Car Center Assistant",
        "Child Care Giver", "Cinnamon Factory Officer", "Cinnamon Factory Operation", "Cinnamon Proccessor",
        "Clerk(General)", "Computer Application Assistant", "Computer Graphic Designer",
        "Computer Hardware Technician", "Computer Type Setting and Image Editor", "Construction Equipment Mechanic",
        "Construction Craftsman (Masonry)L3",
        "Construction Craftsman(Carpenter)", "Construction Craftsman(Masonry)", "Construction Equipment Mech",
        "Construction Equipment Mechanic",
        "Construction Machine Operator", "Construction Site Supervisor", "Cook", "Crane and Hoist Operator",
        "Crane Operator (Level Luffing Jib)", "Crane Operator(port)",
        "Customer Care Assistant", "Cutter(Tailoring)", "Dairy Farming Assistant", "Dental Nurse Assistant",
        "Dental surgery Nurse Assistant", "Desktop Publisher",
        "Diesel Engine Mechanic", "Diesel Injector Pump Repairer", "Diesel Pump Mechanic", "Diesel Pump Room Mechanic",
        "Electric Arc Welder / Fabricator", "Electric Motor Winder",
        "Electrical / Electronic Equipment Repairer", "Electrical Circuit Assembler", "Electrical Linesman",
        "Electrical Wireman", "Electrician",
        "Electrician (Industrial)", "Electronic Appliances Technician", "Electronic Equipment Mechanic",
        "Elevator Technician", "Embroider Machine Operator",
        "English(CELV)", "Factory Officer (Tea)", "Fiberglass Laminator", "Field Assistant (Agricultural)",
        "Field Officer (Rubber)", "Field Officer (Tea)",
        "Fireman", "Fish net Machine Operator", "Fitter (General)", "Fitter (Weaving)", "Food Maker",
        "Food Processor (Daily/Vegetables/Fruits)", "Footwear Components Cutter",
        "Footwear Craftman", "Footwear Finisher", "Footwear Sewer", "Fresh Water Orna. Fish Colle.",
        "Front Office Operation (Guest Relation Agent)",
        "Fuel Pump Operator", "Garment Cutter", "Gem Cutter", "Gem Cutter And Polisher", "General Child Care",
        "Glass & Reinforced plastic Moulder",
        "Grinding Machine Operator", "Hair Cutter/Dresser", "Hair Dresser", "Hair Dresser(Barber)",
        "Handcraft Maker (Sesath Maker)", "Handicraft Maker (Palmyra)", "Handicraft Maker(Coir/ Palmyra/Jute/Pulp)",
        "Handicraft Maker( Palmyra)", "Handicraft Maker(Coir/ Palmyra/ Jute/Pulp/Bamboo Sticks)", "Handloom Weaver",
        "Handloom Weaver (Artistic Design)",
        "Handloom Weaver (Artistic Fabric)", "Handy Craft Maker", "Handy Craft Maker(Palmyra)",
        "Heavy duty Machinery Mechanic", "Highspeed Sewing Machine Mechanic",
        "Household Electrical Appliance Repairer", "Housekeeping Supervisor", "Industrial Sawing Machine Operator",
        "Information And Communication Technology Technician", "Jewellery Maker",
        "Kitchen Steward", "Laboratory Assistant", "Laboratory Assistant (Rubber Research)", "Landscaping Technician",
        "Laster", "Laundryman", "Library Assistant",
        "Machinist", "Machinist (General)", "Management Assistant", "Manufacturing Assistant", "Marine Fitter", "Mason",
        "Medical Lab Assistant", "Medical Lab Technician", "Medical Laboratory Assistant",
        "Medical Receptionist", "Milk Collecting Centre Assistant", "Mining Craftman Assistant",
        "Mobile Phone Repair Technician", "Mobile Phone Repairer",
        "Motor Cycle Mechanic", "Motorcycle Mechanic", "Motorcycle Technician",
        "Moulder(Brass/Cast Iron/Aluminum/Fiberglass)", "Multi Skilled Construction Craftsman",
        "Multiskilled Craftsman", "Mushroom Cultivator", "Nurse", "Nurse Assistant", "Office Clerk",
        "Office Clerk(Accounts)", "Offset Litho Machine Operator",
        "Offset Machine Operator", "OJT-Automobile Mechanic/Automobile Technician",
        "Optical Instrument Maintanance Craftman", "Optician",
        "OR_Field Assistant (Agricultural)", "Ornamental Goods Maker(Ceramic/ Wooden/ Fabric)",
        "Ornamental Goods Maker (Ceramic/ Wooden/ Fabric /Banana Fibre)",
        "Outboard Motor Mechanic", "Painter(Building)", "Painter/Sign Writer", "Pastry And Baker", "Pattern Maker",
        "Pattern Maker (Bathick)",
        "Pattern Maker (Garment)", "Pattern Maker (Wood)", "Personal Secretary (English)", "Pharmacist Assistant",
        "Pharmacy Technician", "Phlebotomist", "Photographer",
        "Physical Fitness trainer", "Plant Nursery Development Assistant", "Plumber", "Power Tool Technician",
        "Pre-School Teacher", "Printing Machine Mechanic",
        "Production Assistant (Paper, Clove/Nutmeg)", "Production Assistant (Plastic/ Rubber/Tea/Ceramic)",
        "Production Assistant(Fabric)", "Production Assistant(Kitul)",
        "Production Machine Mechanic(Garment Industry)", "Production Machine Operator (Milk)",
        "Production of Rain Water Accessories", "Professional Cookery",
        "Quality Control Assistant (Metal Fabrication)", "Radio, TV and Allied Equipment Repairer", "Receptionist",
        "Ref And Air Con Mechanic",
        "Ref.&Air Cond.Serviceman", "Refrigeration And Air Conditioning Technician",
        "Refrigeration And Air Conditioning Serviceman", "Refrigeration Mechanic",
        "Refrigeration Serviceman", "Rigger", "Road Construction Site equipment Operator", "Room Attendant",
        "Room Boy/Room Maid", "Sales Assistant",
        "Sales Representative", "Sales Representative / Assistant", "SB-Construction Craftsman (Masonry)",
        "Secretary (Secretarial Practices)", "Security And Surveillance System Technician",
        "Sewing Machi. Mechanic", "Sewing Machine Mechanic", "Sewing Machine Operator", "Shoe Maker", "SLCCL",
        "Solar Photovoltaic System Technician", "Sole Fitter",
        "Spa & Leisure Tourism Operation Assistant", "Stenographer (Sinhala)", "Stiching Braids and crochet hat & bags",
        "Store Keeper", "Stores Clerk",
        "Supermarket Customer Service Assistant", "Swimming Pool Attendant", "Tailor", "Tailor (Gents)",
        "Tailor (Domestic)", "Tailor (Gents)",
        "Tailor (Ladies & Children)", "Tailor And Handicraft Maker", "Tailor(Gent)", "Tea Havester",
        "Telephone & Switchboard Mechanic", "Telephone Operator",
        "Television Mechanic", "Three Wheelar Mechanic", "Tinsmith", "Tool Issuer", "Traditional Art and Sculpture",
        "Turner", "TV & Electronic Equipment Repairer",
        "Tyre Fitter", "Upholsterer", "Vehicle Air Cond. Mechanic", "Vehicle Body Repairer and Painter",
        "Vehicle Serviceman", "Vehicle Serviceman and Interior Cleaner",
        "Waiter", "Waiter/Steward", "Weaver(P/ Driven Weaving Machine)", "Welder", "Wheel Alignment Technician",
        "Wood Carving Craftsman", "Wood Craftsman (Building)",
        "Wood Craftsman (Furniture)", "Wood Craftsman(Buildings)", "Wooden Craftman (Building)", "Wool Knitter"
    ]

    trade_var = StringVar()
    trade_dropdown = ctk.CTkComboBox(section1_frame, variable=trade_var, fg_color="#A1AEB1", values=trade_values,
                                     width=300,
                                     font=("Arial", 14), button_color="gray", button_hover_color="#888",
                                     text_color="black")
    trade_dropdown.grid(row=35, column=1, padx=5, pady=5, sticky="w")

    def update_trade_combobox(event):
        value = event.widget.get()
        if value == '':
            filtered_values = trade_values
        else:
            filtered_values = [item for item in trade_values if value.lower() in item.lower()]

        trade_dropdown.configure(values=filtered_values)
        trade_dropdown.event_generate('<Down>')

    trade_dropdown._entry.bind('<KeyRelease>', update_trade_combobox)

    trade_code = create_label_entry(section1_frame, 36, "23. Trade Code", font_size=14)
    trade_code.grid(row=36, column=1, padx=5, pady=5, sticky="w")

    # Mode Dropdown
    mode_label = ctk.CTkLabel(section1_frame, text="24. Mode", font=("Arial", 14), fg_color="#f0f0f0",
                              text_color="black", anchor="w")
    mode_label.grid(row=37, column=0, padx=5, pady=5, sticky="w")

    mode_values = ["ASS", "CRFT", "HVV", "NVQ", "PTC"]

    mode_var = StringVar()
    mode_dropdown = ctk.CTkComboBox(section1_frame, variable=mode_var, fg_color="#A1AEB1", values=mode_values,
                                    width=300,
                                    font=("Arial", 14), button_color="gray", button_hover_color="#888",
                                    text_color="black")
    mode_dropdown.grid(row=37, column=1, padx=5, pady=5, sticky="w")

    def update_mode_combobox(event):
        value = event.widget.get()
        if value == '':
            filtered_values = mode_values
        else:
            filtered_values = [item for item in mode_values if value.lower() in item.lower()]

        mode_dropdown.configure(values=filtered_values)
        mode_dropdown.event_generate('<Down>')

    mode_dropdown._entry.bind('<KeyRelease>', update_mode_combobox)

    # NVQ Level Dropdown
    nvq_level_label = ctk.CTkLabel(section1_frame, text="25. NVQ Level", font=("Arial", 14), fg_color="#f0f0f0",
                                   text_color="black", anchor="w")
    nvq_level_label.grid(row=38, column=0, padx=5, pady=5, sticky="w")

    nvq_level_values = ["3", "4", "6", "Certificate"]

    nvq_level_var = StringVar()
    nvq_level_dropdown = ctk.CTkComboBox(section1_frame, variable=nvq_level_var, fg_color="#A1AEB1",
                                         values=nvq_level_values, width=300,
                                         font=("Arial", 14), button_color="gray", button_hover_color="#888",
                                         text_color="black")
    nvq_level_dropdown.grid(row=38, column=1, padx=5, pady=5, sticky="w")

    def update_nvq_level_combobox(event):
        value = event.widget.get()
        if value == '':
            filtered_values = nvq_level_values
        else:
            filtered_values = [item for item in nvq_level_values if value.lower() in item.lower()]

        nvq_level_dropdown.configure(values=filtered_values)
        nvq_level_dropdown.event_generate('<Down>')

    nvq_level_dropdown._entry.bind('<KeyRelease>', update_nvq_level_combobox)

    # Inspector Dropdown
    inspector_label = ctk.CTkLabel(section1_frame, text="26. Name of the Inspector", font=("Arial", 14),
                                   fg_color="#f0f0f0",
                                   text_color="black", anchor="w")
    inspector_label.grid(row=39, column=0, padx=5, pady=5, sticky="w")

    inspector_values = [
        "A Sivanenthiran","A. Niyas","A.A. Nimali","A.A.I.P Wickramasinghe","A.A.M. Hemachandra","A.A.M. Sifnas",
        "A.G.D. Madusanka","A.I.K Abeysekara","A.K.M.R.B Maduwanthi","A.K.M.W.J.C Karunarathna","A.L Chathuranga",
        "A.L Rizvi","A.L. Sajuhan","A.L.M. Ashraff","A.L.M. Hafrath","A.L.M. Husnee","A.L.N.N. Pathirana","A.M.G. Kumara",
        "A.M.M. Niyas","A.M.M. Riyas","A.M.M.S. Hassan","A.M.S.A. Bandara","A.P.G.B. Chandrasekara","A.P.P.K Silva",
        "A.R. Fahim","A.R. Maroos","A.W. Raseen","B Regan","B Sriramanan","B.D.I.C Thilakarathna","B.G. Iroshan",
        "B.G.A.D.Weerakkodi. Weerakkodi","B.H.I.A. Jayathissa","B.K. Kumarasiri","B.K.G.P.N. Weerawardena","B.K.K. Samarasinghe",
        "B.M.G.M. Maluddeniya","B.P.K.Tharanga","C. Naotunna","C.B. Gamage","C.B.M.S.D. Abeysinghe","C.D.B. Weliwita",
        "C.D.P. Fonseka","C.S. Colambage","D.G. Mahinda","D.G.M. Chandrakumara","D.L.I.P Liyanage","D.M.G.T. Dissanayake","D.N.P.K. Kalapuge",
        "D.P. Rathnamalala","D.P.W. Ranathunga","D.S. Ratiyala","D.V.S. Sewwandi","E Naleem","E. Thirunavukkarasu","E.G.D.S. Karunarathna",
        "E.P.C.N. Edirisinghe","G.D.S. Mahanthamulla","G.G. Kumari","G.G. Pushpakumara","G.G.L.M.B. Karunathilaka","G.G.M. Dilhani","G.H. Nayanakanthi",
        "G.H.B.C. Gunawardhana","G.H.U. Wickramasinghe","G.K.A. Sampath","G.N. Pushpakumara","G.T. Kavirathna","G.W. Organdima","H.A.A.B. Jayathilaka",
        "H.A.A.C. Amaaweera","H.A.K.S. Mangalika","H.A.L.P. Gunasekara","H.A.T.S. Gunasena","H.G. Gunawardana","H.G. Kumara","H.G.A.U. Kumara",
        "H.J.M. Herath","H.L.A. Shalini","H.L.S. Hettiarachchi","H.M.E.K.G.N.T.K. Herath","H.M.N.S.R. Bandara","H.M.S.P. Herath","H.P.G.N.M. Gnanarathna",
        "H.R. Violet","H.Y.D. Silva","Hettipathira Kankanamalage Ishanka Uththara Premaw Premawansha","I.K. Sirimal","I.K.P. Kuruppu",
        "I.L. Weerasinghe","I.L.N. Jahan","J. Nirojan","J. Thushanthan","J.A. Sameera","J.H.S.S. Jayamaha","J.M. Sanas","J.M.C. Harischandra",
        "J.M.H. Jayaweera","J.M.P.S. Jayasinghe","J.W. Kumara", "K. Satheechandrakanthan","K. Kuhan","K. Nanthakumaran","K. Nithilan",
        "K. Selvaprakash","K. Seran","K. Subajini","K.A. Upamalika","K.A. Nishanthi","K.A. Premasinghe","K.A.H. Keenavinna","K.A.M.A. Gunathilaka","K.A.N.R. Kumarasinghe",
        "K.B. Sahabdeen","K.D.A. Samarweera","K.G. Priyadarshani","K.G. Nirosha","K.G. Priyankara","K.G.V.S. Gunarathna","K.H.K.M. Balasooriya",
        "K.I. Sandamali","K.M. Rila","K.M.N.M. Jayasena","K.M.T. Ruchira","K.P.K. Darshana","K.P.T.S. Sampath","K.T.M. Maduwanthi",
        "K.T.N. Pushpakumara","K.V.D.D. Ishanka","K.V.D.R. Rajitha","K.W.T. Mahendralal","K.Y.M.S. Ekanayake" , "L.B.A.P. Amararathna",
        "L.G.S.N. Fernando","L.N.K De Silver","L.P.N. Ranaweera","L.T.M. Raseem", "M. Gunatharan","M. Muraly","M. Sarankan","M. Sumanasena",
        "M. Thevarasa","M. Thusintha","M.A. De Silva","M.A. Rangana","M.A.C. Shamila","M.A.L. Hansika","M.C.M. Abeysundara","M.C.S. Jayawardena",
        "M.G. Chandrathlaka","M.G.J. Upeshika","M.G.N. Gunawardena","M.I.D. Salgadu","M.I.M. Ijlas","M.L. Chathurangani","M.M.M.Y. Athur Athur",
        "M.M. Wickramasooriya","M.N.F. Nazmira","M.P.D.R. Pathirana","M.R.S. Wickramasinghe","M.S. Safeek","M.T. Asker","M.W. Dilhan",
        "M.W.G. Peiris","M.W.M.P. Wijeshinghe","M.W.T.M. Dharmawardene", "N. Sothynathan","N. Abiman","N. Bayojan","N. Priyatharshani",
        "N.C. Arumapperuma","N.D.A. Nwanthika","N.D.K. Punchihewa","N.K.T.D. Kalathunga","N.L. Suwandaarachchi","N.M. Senewirathna",
        "N.M. Siyam","N.R. Ekanayaka","N.V. Bandara", "P. Kajanthan","P. Fajith","P. Premachandran","P.C. Kavinda","P.D.N.D. Ariyarathna",
        "P.G.A.P. Hewawissa","P.G.G. Pathberiya","P.K.N. Chamalki","P.L.P. Harshika","P.M. Pakkeer","P.M.M. Pushpanganai","P.R. Kumarasinghe",
        "P.S. Buddakorala","P.S.S. Perera","P.W.S.N. Madushani", "R. Thirumurukhan","R. Vinothini","R. Wickramarachchi","R.A.H.M. Ramanayaka",
        "R.D. Gunathilaka","R.D.P. Ranamuka","R.D.P. Prasanga","R.D.P.U. Rajapaksha","R.H.M. Wathsala","R.K.G. Rajakaruna","R.K.P.J. Bandara",
        "R.M. Hareef","R.M. Samarakoon","R.M.I.N. Dissanayake","R.M.R.S.B. Atugoda","R.M.U. Rathnayaka","R.P. Nishantha","R.P.S. Kumara",
        "R.P.T. Lakmal","R.U. Ariyasinghe", "S. Leefan","S. Varathaluxmy","S,M.T. Samaraweera","S. Animugam","S. Kirisanth","S. Nisthar",
        "S. Piratheeban","S. Prashanthan","S. Theepan","S.A. Meddevithana","S.A.D.S. Jayathilaka","S.A.I. Beshan","S.A.M. Ashraff",
        "S.A.M. Subasinghe","S.D. Samaradivakara","S.D. Silva","S.D.P.Alwis","S.G. Prasad","S.G.I. Liyanage","S.I. Athukorala","S.J.M.E.K.S. Bandara",
        "S.K.G.N.T. Kohilagoda","S.L.N.S.L. Madusanka","S.M. Najeem","S.M.A.U. Ahamed","S.M.L.M. Wijerathna","S.M.M. Risvan","S.S. Senavirathna",
        "S.S.S. Jumail","S.T. Abayasinghe","S.W. Wakishta" , "T. Krishnarajah","T. Uthyarasa","T.A. Wasana","T.A.R.W.M.M.T.N. Ubeyrathna",
        "T.A.T.D. Kulathunga","T.G. Mangalika","T.R.T.R. Galappaththi","T.R.C.E. Wijayarathna","T.T. Silva","T.V.K. Karunarathna" , "U.C. Dissanayake",
        "U.H.E.S. Rathnayake","U.P.S. Kumara","U.V.D.S. Kumari" ,"W. Nirojan","W.A.M.M.S. Jayawansa","W.B. Kumarasiri","W.D.P.M. Premarathna",
        "W.G.A. Bandara","W.G.U. Rajakaruna","W.H.N.P. Somasiri","W.K.N. Wakkumbura","W.K.S. Sankalpa","W.K.S. Sarojani","W.L.A. Amarasinghe",
        "W.M.A.K. Wijekoon","W.M.M. Weerarathna","W.M.M.D. Weerasinghe","W.M.N.T. Wanasundara","W.M.V.G. Geethani","W.R.A.S.C. Ranasinghe",
        "W.R.N. Weeragoda","W.T.M.L.I. Jayasinghe","W.W.A.S. Kumara","W.W.M.M.K.Gunasinghe", "Y. Sivasankar","Y.A.D.S Yahampath","Y.M. Jayathissa"
    ]

    inspector_var = StringVar()
    inspector_dropdown = ctk.CTkComboBox(section1_frame, variable=inspector_var, fg_color="#A1AEB1",
                                         values=inspector_values, width=300,
                                         font=("Arial", 14), button_color="gray", button_hover_color="#888",
                                         text_color="black")
    inspector_dropdown.grid(row=39, column=1, padx=5, pady=5, sticky="w")

    def update_inspector_combobox(event):
        value = event.widget.get()
        if value == '':
            filtered_values = inspector_values
        else:
            filtered_values = [item for item in inspector_values if value.lower() in item.lower()]

        inspector_dropdown.configure(values=filtered_values)
        inspector_dropdown.event_generate('<Down>')

    inspector_dropdown._entry.bind('<KeyRelease>', update_inspector_combobox)

    commencement_date_label = ctk.CTkLabel(section1_frame, text="27. Commencement Date", font=("Arial", 14),
                                       fg_color="#f0f0f0",
                                       text_color="black", anchor="w")
    commencement_date_label.grid(row=40, column=0, padx=5, pady=5, sticky="w")
    commencement_date = DateEntry(section1_frame, width=31, background='gray', foreground="white", borderwidth=2,
                                  font=("Arial", 14))
    commencement_date.grid(row=40, column=1, padx=5, pady=5, sticky="w")

    schedule_date_completion_label = ctk.CTkLabel(section1_frame, text="28. Schedule Date Completion", font=("Arial", 14),
                                           fg_color="#f0f0f0",
                                           text_color="black", anchor="w")
    schedule_date_completion_label.grid(row=41, column=0, padx=5, pady=5, sticky="w")
    schedule_date_completion = DateEntry(section1_frame, width=31, background='gray', foreground='white',
                                         borderwidth=2, font=("Arial", 14))
    schedule_date_completion.grid(row=41, column=1, padx=5, pady=5, sticky="w")

    signature_tm = create_label_entry(section1_frame, 42, "29. Signature of the Training Manager", font_size=14)
    signature_tm.grid(row=42, column=1, padx=5, pady=5, sticky="w")
    remark = create_label_entry(section1_frame, 43, "30. Remark", font_size=14)
    remark.grid(row=43, column=1, padx=5, pady=5, sticky="w")

    # Submit and Clear buttons
    button_frame = ctk.CTkFrame(scrollable_frame, fg_color="#f0f0f0")
    button_frame.pack(pady=10, padx=20, fill="x", expand=True, anchor="center")

    back_button = ctk.CTkButton(button_frame, text="Back", font=("Arial", 14, "bold"), command=back,
                                 fg_color="crimson", text_color="white")
    back_button.pack(side=LEFT, padx=20, pady=10)

    clear_button = ctk.CTkButton(button_frame, text="Clear", font=("Arial", 14, "bold"), command=clear_form,
                                  fg_color="crimson", text_color="white")
    clear_button.pack(side=LEFT, padx=20, pady=10)

    submit_button = ctk.CTkButton(button_frame, text="Submit", font=("Arial", 14, "bold"), command=submit,
                                 fg_color="crimson", text_color="white")
    submit_button.pack(side=LEFT, padx=20, pady=10)

    # Print Button
    print_button = ctk.CTkButton(button_frame, text="Print", font=("Arial", 14, "bold"), fg_color="crimson",
                                 text_color="white", command=print_to_excel)
    print_button.pack(pady=10, padx=20, side=LEFT)


    app.mainloop()

form()