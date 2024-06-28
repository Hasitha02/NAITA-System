def ee():
    import customtkinter as ctk
    import tkinter as tk
    from tkinter import ttk
    from tkcalendar import DateEntry
    import mysql.connector

    # Initialize the customtkinter application
    ctk.set_appearance_mode("light")  # Modes: "System", "Dark", "Light"
    ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"

    # Create the main window
    app = ctk.CTk()
    app.geometry("850x600")
    app.title("EBTSD Registration Form")

    # Create a frame for the form inside a Canvas to allow scrolling
    main_frame = ctk.CTkFrame(app)
    main_frame.pack(fill=tk.BOTH, expand=1)

    canvas = tk.Canvas(main_frame)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    # Create a scrollbar and bind it to the canvas
    scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create a frame inside the canvas
    scrollable_frame = ctk.CTkFrame(canvas)
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    # Define all column labels and entry widgets
    fields = {
        "category": "Category",
        "district": "District",
        "dateOfRegistration": "Date of Registration",
        "indexNumber": "Index Number",
        "name": "Name",
        "fullName": "Full Name",
        "dateofBirth": "Date of Birth",
        "gender": "Gender",
        "NIC": "NIC",
        "telephoneNumber": "Telephone Number",
        "NAITAIDnumber": "NAITA ID Number",
        "dropOut": "Drop Out",
        "dropOutDate": "Drop Out Date",
        "addressNo": "Address No",
        "addressFLine": "Address First Line",
        "addressLLine": "Address Last Line",
        "nameofEstablishment": "Name of Establishment",
        "establishmentType": "Establishment Type",
        "establishmentAddressDivision": "Establishment Address Division",
        "establishmentAddressDistrict": "Establishment Address District",
        "establishmentTelephone": "Establishment Telephone",
        "DSDivision": "DS Division",
        "establishmentCode": "Establishment Code",
        "sectorName": "Sector Name",
        "trade": "Trade",
        "tradeCode": "Trade Code",
        "mode": "Mode",
        "NVQLevel": "NVQ Level",
        "inspectorName": "Inspector Name",
        "commencementDate": "Commencement Date",
        "scheduleDateCompletion": "Scheduled Date of Completion",
        "signatureTM": "Signature of TM",
        "remark": "Remark"
    }

    # Initialize dictionary for entries and combo boxes
    entries = {}
    combo_fields = ["district", "nameofEstablishment", "sectorName", "trade", "mode", "NVQLevel"]
    date_fields = ["dateOfRegistration", "dateofBirth", "dropOutDate", "commencementDate", "scheduleDateCompletion"]

    # Fetch data from the MySQL database for dropdowns
    def fetch_data():
        try:
            # Connect to MySQL
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="prabhashi915",  # Replace with your MySQL password
                database="NAITA"  # Replace with your MySQL database name
            )
            cursor = connection.cursor()

            # Fetch distinct values for combo box fields
            data = {}
            for field in combo_fields:
                cursor.execute(f"SELECT DISTINCT {field} FROM EBTSD")
                data[field] = [item[0] for item in cursor.fetchall()]

            cursor.close()
            connection.close()
            return data
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return {}

    # Populate the fetched data
    data = fetch_data()

    # Layout the form
    row_index = 0
    for field_key, field_label in fields.items():
        label = ctk.CTkLabel(scrollable_frame, text=field_label)
        label.grid(row=row_index, column=0, padx=20, pady=10, sticky="w")

        if field_key in combo_fields:
            entries[field_key] = ctk.CTkComboBox(scrollable_frame, values=data.get(field_key, []))
        elif field_key in date_fields:
            entries[field_key] = DateEntry(scrollable_frame, date_pattern="yyyy-mm-dd", background='darkblue',
                                           borderwidth=2)
        else:
            entries[field_key] = ctk.CTkEntry(scrollable_frame)

        entries[field_key].grid(row=row_index, column=1, padx=20, pady=10, sticky="w")
        row_index += 1

    def on_mouse_wheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # Enable scrolling with mouse wheel on Windows and Linux
    app.bind_all("<MouseWheel>", on_mouse_wheel)

    # Add a submit button
    def submit_form():
        # Collect form data
        form_data = {field_key: entries[field_key].get() for field_key in fields}
        print("Form Data:", form_data)

        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="prabhashi915",
                database="NAITA"
            )
            cursor = connection.cursor()

            # Prepare the insert query
            placeholders = ', '.join(['%s'] * len(fields))
            columns = ', '.join(fields.keys())
            sql = f"INSERT INTO EBTSD ({columns}) VALUES ({placeholders})"
            cursor.execute(sql, tuple(form_data.values()))

            connection.commit()
            cursor.close()
            connection.close()
            print("Data inserted successfully.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    submit_button = ctk.CTkButton(scrollable_frame, text="Submit", command=submit_form)
    submit_button.grid(row=row_index, columnspan=2, padx=20, pady=20)

    # Bind mouse wheel scrolling
    app.bind_all("<MouseWheel>", on_mouse_wheel)

    # Start the application
    app.mainloop()
