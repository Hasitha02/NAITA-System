def search_EBT():
    import customtkinter as ctk
    from tkinter import messagebox, filedialog
    import mysql.connector
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas as pdf_canvas
    from openpyxl import Workbook

    # Database connection configuration
    db_config = {
        'user': 'root',
        'password': '11156363312',
        'host': 'localhost',
        'database': 'NAITA'
    }

    # Global variables to hold retrieved data and headers
    retrieved_data = []
    headers = []

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
                'category': 'Category',
                'district': 'District',
                'dateOfRegistration': 'Date Of Registration',
                'indexNumber': 'Index Number',
                'name': 'Name',
                'fullName': 'Full Name',
                'dateofBirth': 'Date Of Birth',
                'gender': 'Gender',
                'NIC': 'NIC',
                'telephoneNumber': 'Telephone Number',
                'NAITAIDnumber': 'NAITA ID Number',
                'dropOut': 'Dropout',
                'dropOutDate': 'Dropout Date',
                'addressNo': 'Address No',
                'addressFLine': 'Address First Line',
                'addressLLine': 'Address Last Line',
                'nameofEstablishment': 'Name Of Establishment',
                'establishmentType': 'Establishment Type',
                'establishmentAddressDivision': 'Establishment Address Division',
                'establishmentAddressDistrict': 'Establishment Address District',
                'establishmentTelephone': 'Establishment Telephone',
                'DSDivision': 'DS Division',
                'establishmentCode': 'Establishment Code',
                'sectorName': 'Sector Name',
                'trade': 'Trade',
                'tradeCode': 'Trade Code',
                'mode': 'Mode',
                'NVQLevel': 'NVQ Level',
                'inspectorName': 'Inspector Name',
                'commencementDate': 'Commencement Date',
                'scheduleDateCompletion': 'Schedule Date Completion',
                'signatureTM': 'Signature TM',
                'remark': 'Remark'
            }

            # Query to retrieve data
            query = """
                WITH StudentData AS (
                    SELECT * FROM EBTSD WHERE fullName = %s AND NIC = %s
                )
                SELECT * FROM StudentData;
            """
            cursor.execute(query, (full_name, nic))
            result = cursor.fetchone()

            if result:
                global retrieved_data, headers
                retrieved_data = []
                headers = []

                result_text = ""
                for key, header in headers_mapping.items():
                    if key in result:
                        result_text += f"{header}: {result[key]}\n\n"
                        headers.append(header)
                        retrieved_data.append(result[key])

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

    # Function to save data to a PDF
    def save_to_pdf(file_path):
        c = pdf_canvas.Canvas(file_path, pagesize=letter)
        width, height = letter

        x_offset = 40
        y_offset = height - 40
        line_height = 20

        for header, datum in zip(headers, retrieved_data):
            c.drawString(x_offset, y_offset, f"{header}: {datum}")
            y_offset -= line_height

        c.save()

    # Function to save data to an Excel file
    def save_to_excel(file_path):
        workbook = Workbook()
        sheet = workbook.active

        sheet.append(headers)
        sheet.append(retrieved_data)

        workbook.save(file_path)

    # Function to handle the print button click
    def handle_save_to_pdf():
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("PDF files", "*.pdf"), ("All files", "*.*")],
            title="Save file"
        )

        if file_path:
            try:
                if file_path.endswith('.xlsx'):
                    save_to_excel(file_path)
                    messagebox.showinfo("Printed", f"Data has been printed to {file_path}")
                elif file_path.endswith('.pdf'):
                    save_to_pdf(file_path)
                    messagebox.showinfo("Printed", f"Data has been printed to {file_path}")
            except PermissionError:
                messagebox.showerror("Error", "Could not save data to file.\n"
                                              "Please close any open files and try again.")

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
    full_name_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")

    entry_full_name = ctk.CTkEntry(form_frame, width=300, fg_color="white", text_color="black", font=("Arial", 14))
    entry_full_name.grid(row=0, column=2, padx=10, pady=5, sticky="w")

    # NIC entry
    nic_label = ctk.CTkLabel(form_frame, text="NIC:", text_color="black", font=("Arial", 14, "bold"), fg_color="white")
    nic_label.grid(row=0, column=3, padx=10, pady=5, sticky="w")

    entry_nic = ctk.CTkEntry(form_frame, width=300, fg_color="white", text_color="black", font=("Arial", 14))
    entry_nic.grid(row=0, column=4, padx=10, pady=5, sticky="w")

    # Retrieve Button
    btn_retrieve = ctk.CTkButton(main_frame, text="Retrieve Data", font=("Arial", 14), fg_color="crimson", text_color="white", command=retrieve_data)
    btn_retrieve.pack(pady=20)

    # Print Button
    btn_print = ctk.CTkButton(main_frame, text="Print", font=("Arial", 14), fg_color="crimson", text_color="white", command=handle_save_to_pdf)
    btn_print.pack(pady=20)

    # Textbox to display results
    text_result = ctk.CTkTextbox(main_frame, width=800, height=600, fg_color="gray", text_color="black", font=("Arial", 14))
    text_result.pack(pady=(0, 20))
    text_result.configure(state='disabled')

    # Start the application
    app.mainloop()
