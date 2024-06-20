import customtkinter as ctk
from tkinter import StringVar, Frame, Scrollbar, Canvas, VERTICAL, RIGHT, LEFT, Y, BOTH, messagebox
from tkcalendar import DateEntry

def form():
    # Create the main application window
    app = ctk.CTk()
    app.title("Form")
    app.geometry("1080x1200")

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
        if not all([district_var.get(), date_of_registration.get(), index_number.get(), name.get(),
                    full_name.get(), date_of_birth.get(), gender_var.get(), nic.get(), telephone_number.get(),
                    naita_id_number.get(), dropout_var.get(), dropout_date.get(), address_no.get(),
                    address_f_line.get(), address_l_line.get(), nameof_establishment.get(), establishment_type.get(),
                    establishment_address_division.get(), establishment_address_district.get(),
                    establishment_telephone.get(), ds_division.get(), establishment_code.get(), sector_var.get(),
                    trade.get(), trade_code.get(), mode.get(), nvq_level.get(), inspector_name.get(),
                    commencement_date.get(), schedule_date_completion.get(), signature_tm.get(), remark.get()]):
            messagebox.showerror("Error", "Please fill out all fields.")
        elif len(telephone_number.get()) > 10 or not telephone_number.get().isdigit():
            messagebox.showerror("Error", "Phone number should be 10 digits and numeric only.")
        elif len(nic.get()) != 10:
            messagebox.showerror("Error", "NIC should be exactly 10 characters.")
        elif len(naita_id_number.get()) >= 12:
            messagebox.showerror("Error", "NAITA ID Number should be less than 12 characters.")
        else:
            messagebox.showinfo("Submit", "Submitted successfully.")

    def clear_form():
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
                    elif isinstance(inner_widget, ctk.CTkOptionMenu):
                        inner_widget.set("")
                    elif isinstance(inner_widget, Frame):
                        for radio in inner_widget.winfo_children():
                            if isinstance(radio, ctk.CTkRadioButton):
                                radio.deselect()

    scrollable_frame.bind("<Configure>", on_frame_configure)
    canvas.bind_all("<MouseWheel>", on_mouse_wheel)

    # Helper function to create labels and entries
    def create_label_entry(parent, row, label_text, col_offset=0, label_width=20, font_size=14):
        label = ctk.CTkLabel(parent, text=label_text, font=("Arial", font_size), fg_color="#f0f0f0", text_color="black",
                             anchor="w", width=label_width * 10)
        label.grid(row=row, column=col_offset, padx=5, pady=5, sticky="w")

        entry = ctk.CTkEntry(parent, width=250, font=("Arial", font_size), fg_color="#A1AEB1", text_color="black")
        entry.grid(row=row, column=col_offset + 1, padx=5, pady=5, sticky="w")

        return entry

    # Section 1: Category to Address of the Apprentice
    section1_frame = ctk.CTkFrame(scrollable_frame, fg_color="#f0f0f0")  # Whitish background for sections
    section1_frame.pack(pady=10, padx=20, fill="x", expand=True, anchor="center")

    # Section Header 1
    header1 = ctk.CTkLabel(section1_frame, text="Apprentice Details", font=("Arial", 16, "bold"),
                           fg_color="#f0f0f0", text_color="black")
    header1.grid(row=0, column=0, columnspan=2, pady=10, sticky="w")  # Center header

    # Categories (Fixed to "CBT")
    category_label = ctk.CTkLabel(section1_frame, text="Category", font=("Arial", 14), fg_color="#f0f0f0",
                                  text_color="black", anchor="w")
    category_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

    category_value = ctk.CTkLabel(section1_frame, text="CBT - Center Based Training", font=("Arial", 14),
                                  text_color="black", anchor="w")
    category_value.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    # District Dropdown
    district_label = ctk.CTkLabel(section1_frame, text="District", font=("Arial", 14), fg_color="#f0f0f0",
                                   text_color="black", anchor="w")
    district_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

    district_var = StringVar()
    district_dropdown = ctk.CTkOptionMenu(section1_frame, variable=district_var, fg_color="#A1AEB1", values=[
        "Ampara", "Anuradhapura", "Badulla", "Batticaloa", "Colombo", "Gampaha", "Galle", "Hambantota",
        "Jaffna", "Kalutara", "Kandy", "Kegalle", "Kilinochchi", "Kurunegala", "Mannar", "Matale",
        "Matara", "Monaragala", "Mullaitivu", "Nuwara Eliya", "Polonnaruwa", "Puttalam", "Ratnapura",
        "Trincomalee", "Vavuniya"],
                                         font=("Arial", 14), button_color="gray", button_hover_color="#888",
                                         text_color="black")  # Gray background for dropdown arrow
    district_dropdown.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    # Other fields
    date_of_registration = DateEntry(section1_frame, width=12, background='darkblue', foreground='white', borderwidth=2,
                                     font=("Arial", 14))
    date_of_registration.grid(row=3, column=1, padx=5, pady=5, sticky="w")

    index_number = create_label_entry(section1_frame, 4, "Index Number", font_size=14)
    name = create_label_entry(section1_frame, 5, "Name", font_size=14)
    full_name = create_label_entry(section1_frame, 6, "Full Name", font_size=14)

    date_of_birth = DateEntry(section1_frame, width=12, background='darkblue', foreground='white', borderwidth=2,
                              font=("Arial", 14))
    date_of_birth.grid(row=7, column=1, padx=5, pady=5, sticky="w")

    # Gender Radio Buttons
    gender_label = ctk.CTkLabel(section1_frame, text="Gender", font=("Arial", 14), fg_color="#f0f0f0",
                                text_color="black", anchor="w")
    gender_label.grid(row=8, column=0, padx=5, pady=5, sticky="w")

    gender_var = StringVar()
    gender_buttons_frame = Frame(section1_frame, bg="#f0f0f0")
    gender_buttons_frame.grid(row=8, column=1, padx=5, pady=5, sticky="w")

    male_radio = ctk.CTkRadioButton(gender_buttons_frame, text="Male", variable=gender_var, value="Male",
                                     font=("Arial", 14), fg_color="black", text_color="black")
    female_radio = ctk.CTkRadioButton(gender_buttons_frame, text="Female", variable=gender_var, value="Female",
                                      font=("Arial", 14), fg_color="black", text_color="black")
    male_radio.pack(side=LEFT, padx=5)
    female_radio.pack(side=LEFT, padx=5)

    # NIC Entry
    nic = create_label_entry(section1_frame, 9, "NIC", font_size=14)

    # Telephone Number Entry
    telephone_number = create_label_entry(section1_frame, 10, "Telephone Number", font_size=14)

    # NAITA ID Number Entry
    naita_id_number = create_label_entry(section1_frame, 11, "NAITA ID Number", font_size=14)

    # Dropout Radio Buttons
    dropout_label = ctk.CTkLabel(section1_frame, text="Dropout", font=("Arial", 14), fg_color="#f0f0f0",
                                 text_color="black", anchor="w")
    dropout_label.grid(row=12, column=0, padx=5, pady=5, sticky="w")

    dropout_var = StringVar()
    dropout_buttons_frame = Frame(section1_frame, bg="#f0f0f0")
    dropout_buttons_frame.grid(row=12, column=1, padx=5, pady=5, sticky="w")

    dropout_yes_radio = ctk.CTkRadioButton(dropout_buttons_frame, text="Yes", variable=dropout_var, value="Yes",
                                           font=("Arial", 14), fg_color="black", text_color="black")
    dropout_no_radio = ctk.CTkRadioButton(dropout_buttons_frame, text="No", variable=dropout_var, value="No",
                                          font=("Arial", 14), fg_color="black", text_color="black")
    dropout_yes_radio.pack(side=LEFT, padx=5)
    dropout_no_radio.pack(side=LEFT, padx=5)

    # Dropout Date Entry
    dropout_date = DateEntry(section1_frame, width=12, background='darkblue', foreground='white', borderwidth=2,
                             font=("Arial", 14))
    dropout_date.grid(row=13, column=1, padx=5, pady=5, sticky="w")

    # Address Entries
    address_no = create_label_entry(section1_frame, 14, "Address No.", font_size=14)
    address_f_line = create_label_entry(section1_frame, 15, "Address First Line", font_size=14)
    address_l_line = create_label_entry(section1_frame, 16, "Address Last Line", font_size=14)

    # Section 2: Details of the Establishment to Signature of Training Manager
    section2_frame = ctk.CTkFrame(scrollable_frame, fg_color="#f0f0f0")  # Whitish background for sections
    section2_frame.pack(pady=10, padx=20, fill="x", expand=True, anchor="center")

    # Section Header 2
    header2 = ctk.CTkLabel(section2_frame, text="Establishment Details", font=("Arial", 16, "bold"),
                           fg_color="#f0f0f0", text_color="black")
    header2.grid(row=0, column=0, columnspan=2, pady=10, sticky="w")  # Center header

    nameof_establishment = create_label_entry(section2_frame, 1, "Name of the Establishment", font_size=14)
    establishment_type = create_label_entry(section2_frame, 2, "Type of the Establishment", font_size=14)
    establishment_address_division = create_label_entry(section2_frame, 3, "Establishment Address Division",
                                                        font_size=14)
    establishment_address_district = create_label_entry(section2_frame, 4, "Establishment Address District",
                                                        font_size=14)
    establishment_telephone = create_label_entry(section2_frame, 5, "Establishment Telephone", font_size=14)
    ds_division = create_label_entry(section2_frame, 6, "DS Division", font_size=14)
    establishment_code = create_label_entry(section2_frame, 7, "Establishment Code", font_size=14)

    # Sector Dropdown
    sector_label = ctk.CTkLabel(section2_frame, text="Sector", font=("Arial", 14), fg_color="#f0f0f0", text_color="black",
                                anchor="w")
    sector_label.grid(row=8, column=0, padx=5, pady=5, sticky="w")

    sector_var = StringVar()
    sector_dropdown = ctk.CTkOptionMenu(section2_frame, variable=sector_var, fg_color="#A1AEB1", values=[
        "Private", "Public"],
                                        font=("Arial", 14), button_color="gray", button_hover_color="#888",
                                        text_color="black")  # Gray background for dropdown arrow
    sector_dropdown.grid(row=8, column=1, padx=5, pady=5, sticky="w")

    trade = create_label_entry(section2_frame, 9, "Trade", font_size=14)
    trade_code = create_label_entry(section2_frame, 10, "Trade Code", font_size=14)
    mode = create_label_entry(section2_frame, 11, "Mode", font_size=14)
    nvq_level = create_label_entry(section2_frame, 12, "NVQ Level", font_size=14)
    inspector_name = create_label_entry(section2_frame, 13, "Name of the Inspector", font_size=14)

    commencement_date = DateEntry(section2_frame, width=12, background='darkblue', foreground='white', borderwidth=2,
                                  font=("Arial", 14))
    commencement_date.grid(row=14, column=1, padx=5, pady=5, sticky="w")

    schedule_date_completion = DateEntry(section2_frame, width=12, background='darkblue', foreground='white',
                                         borderwidth=2, font=("Arial", 14))
    schedule_date_completion.grid(row=15, column=1, padx=5, pady=5, sticky="w")

    signature_tm = create_label_entry(section2_frame, 16, "Signature of the Training Manager", font_size=14)
    remark = create_label_entry(section2_frame, 17, "Remark", font_size=14)

    # Submit and Clear buttons
    button_frame = ctk.CTkFrame(scrollable_frame, fg_color="#f0f0f0")  # Whitish background for buttons
    button_frame.pack(pady=10, padx=20, fill="x", expand=True, anchor="center")

    submit_button = ctk.CTkButton(button_frame, text="Submit", font=("Arial", 14, "bold"), command=submit,
                                  fg_color="#007BFF", text_color="white")  # Blue submit button
    submit_button.pack(side=LEFT, padx=20, pady=10)

    clear_button = ctk.CTkButton(button_frame, text="Clear", font=("Arial", 14, "bold"), command=clear_form,
                                 fg_color="#DC3545", text_color="white")  # Red clear button
    clear_button.pack(side=LEFT, padx=20, pady=10)

    app.mainloop()

form()
