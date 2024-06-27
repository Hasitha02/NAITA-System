def edit_CBT_function():
    import customtkinter as ctk
    import mysql.connector
    from tkinter import messagebox

    # Database connection configuration
    db_config = {
        'user': 'root',
        'password': '11156363312',
        'host': 'localhost',
        'database': 'NAITA'
    }

    updated_data = []
    headers = []

    # Headers mapping for labels
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
            query = "SELECT * FROM CBTSD WHERE fullName = %s AND NIC = %s"
            cursor.execute(query, (username, nic))
            result = cursor.fetchone()

            if result:
                global updated_data, headers
                updated_data = []
                headers = []

                result_text = ""
                for key, header in headers_mapping.items():
                    if key in result:
                        result_text += f"{header}: {result[key]}\n\n"
                        headers.append(header)
                        updated_data.append(result[key])

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
            query = """UPDATE CBTSD SET category=%s, district=%s, dateOfRegistration=%s, 
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


    # Set background color to white
    main_frame = ctk.CTkFrame(app, fg_color="white")
    main_frame.pack(fill="both", expand=True)

    # Header Frame in Main Frame
    header_frame_main = ctk.CTkFrame(main_frame, fg_color="white")
    header_frame_main.pack(pady=10, padx=20, fill="x", expand=False)

    header_label_main = ctk.CTkLabel(header_frame_main, text="Edit Student Details - CBT", font=("Arial", 24, "bold"),
                                     fg_color="white", text_color="black")
    header_label_main.pack(pady=10, padx=10, anchor="center")

    # Username and NIC entry
    ctk.CTkLabel(main_frame, text="Full Name:", text_color="black").pack(pady=(10, 5))
    entry_username = ctk.CTkEntry(main_frame, width=300, fg_color="#A1AEB1", text_color="black")
    entry_username.pack(pady=5)

    ctk.CTkLabel(main_frame, text="NIC:", text_color="black").pack(pady=(10, 5))
    entry_nic = ctk.CTkEntry(main_frame, width=300, fg_color="#A1AEB1", text_color="black")
    entry_nic.pack(pady=5)

    # Search Button
    btn_search = ctk.CTkButton(main_frame, text="Search", fg_color='crimson', command=search_data)
    btn_search.pack(pady=20)

    # Edit form
    edit_form = ctk.CTkToplevel(app)
    edit_form.title("Edit Data")
    edit_form.geometry("600x700")
    edit_form.withdraw()  # Hide the form initially

    # Set background color to white
    edit_frame = ctk.CTkFrame(edit_form, fg_color="white")
    edit_frame.pack(fill="both", expand=True)

    # Header Frame in Edit Form
    header_frame_edit = ctk.CTkFrame(edit_frame, fg_color="white")
    header_frame_edit.pack(pady=10, padx=20, fill="x", expand=False)

    header_label_edit = ctk.CTkLabel(header_frame_edit, text="Edit Student Details - CBT", font=("Arial", 24, "bold"),
                                     fg_color="white", text_color="black")
    header_label_edit.pack(pady=10, padx=10, anchor="center")

    # Create a scrollable frame for the fields
    scrollable_frame = ctk.CTkScrollableFrame(edit_frame, fg_color="white", width=450, height=600)
    scrollable_frame.pack(pady=10, padx=10, fill="both", expand=True)

    entry_fields = {}
    fields = ["category", "district", "dateOfRegistration", "indexNumber", "name", "fullName",
              "dateofBirth", "gender", "NIC", "telephoneNumber", "NAITAIDnumber", "dropOut",
              "dropOutDate", "addressNo", "addressFLine", "addressLLine", "nameofEstablishment",
              "establishmentType", "establishmentAddressDivision", "establishmentAddressDistrict",
              "establishmentTelephone", "DSDivision", "establishmentCode", "sectorName", "trade",
              "tradeCode", "mode", "NVQLevel", "inspectorName", "commencementDate",
              "scheduleDateCompletion", "signatureTM", "remark"]

    for idx, field in enumerate(fields):
        label_text = headers_mapping.get(field, field)
        ctk.CTkLabel(scrollable_frame, text=label_text + ":", text_color="black").grid(row=idx, column=0, padx=10,
                                                                                       pady=(5, 0), sticky='w')
        entry_fields[field] = ctk.CTkEntry(scrollable_frame, width=300, fg_color="#A1AEB1", text_color="black")
        entry_fields[field].grid(row=idx, column=1, padx=10, pady=5, sticky='w')

    # Update Button
    btn_update = ctk.CTkButton(scrollable_frame, fg_color='crimson', text="Update", command=update_data)
    btn_update.grid(row=len(fields), columnspan=2, pady=20)

    # Start the application
    app.mainloop()