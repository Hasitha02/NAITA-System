import customtkinter as ctk
from tkinter import StringVar, Frame, Scrollbar, Canvas, VERTICAL, RIGHT, LEFT, Y, BOTH, messagebox
from tkcalendar import DateEntry

# Create the main application window
app = ctk.CTk()
app.title("Form")
app.geometry("800x1200")

# Create a frame for the form
form_frame = ctk.CTkFrame(app, fg_color="white")  # Whitish background
form_frame.pack(padx=30, pady=30, fill="both", expand=True)

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
    if not all([category.get(), district_var.get(), date_of_registration.get(), index_number.get(), name.get(),
                full_name.get(), date_of_birth.get(), gender_var.get(), nic.get(), telephone_number.get(),
                naita_id_number.get(), dropout_var.get(), address_no.get(), address_f_line.get(),
                address_l_line.get(), nameof_establishment.get(), establishment_type.get(),
                establishment_address_division.get(), establishment_address_district.get(),
                establishment_telephone.get(), ds_division.get(), establishment_code.get(), sector_var.get(),
                trade.get(), trade_code.get(), mode.get(), nvq_level.get(), inspector_name.get(),
                commencement_date.get(), schedule_date_completion.get(), signature_tm.get(), remark.get()]):
        messagebox.showerror("Error", "Please fill out all fields.")
    elif len(telephone_number.get()) != 10 or not telephone_number.get().isdigit():
        messagebox.showerror("Error", "Phone number should be 10 digits and numeric only.")
    elif len(nic.get()) != 12:
        messagebox.showerror("Error", "NIC should be exactly 12 characters.")
    elif len(naita_id_number.get()) >= 12:
        messagebox.showerror("Error", "NAITA ID Number should be less than 12 characters.")
    elif dropout_var.get() == "No" and dropout_date.get():
        messagebox.showerror("Error", "Dropout date should not be entered if the apprentice has not dropped out.")
    elif len(nic.get()) != 12:
        messagebox.showerror("Error", "NIC should be exactly 12 characters.")
    elif len(telephone_number.get()) != 10 or not telephone_number.get().isdigit():
        messagebox.showerror("Error", "Phone number should be 10 digits and numeric only.")
    elif dropout_var.get() == "No" and dropout_date.get():
        messagebox.showerror("Error", "Dropout date should not be entered if the apprentice has not dropped out.")


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
def create_label_entry(parent, row, label_text, col_offset=0, label_width=20):
    label = ctk.CTkLabel(parent, text=label_text, font=("Arial", 12), fg_color="#f0f0f0", text_color="black",
                         anchor="w", width=label_width * 10)
    label.grid(row=row, column=col_offset, padx=5, pady=5, sticky="w")

    entry = ctk.CTkEntry(parent, width=250, font=("Arial", 12), fg_color="#A1AEB1", text_color="black")
    entry.grid(row=row, column=col_offset + 1, padx=5, pady=5, sticky="w")

    return entry


# Section 1: Category to Address of the Apprentice
section1_frame = ctk.CTkFrame(scrollable_frame, fg_color="#f0f0f0")  # Whitish background for sections
section1_frame.pack(pady=10, padx=20, fill="x", expand=True, anchor="center")

# Section Header 1
header1 = ctk.CTkLabel(section1_frame, text="Apprentice Details", font=("Arial", 16, "bold"),
                       fg_color="#f0f0f0", text_color="black")
header1.grid(row=0, column=0, columnspan=2, pady=10, sticky="w")  # Center header

# Categories
category = create_label_entry(section1_frame, 1, "Category")

# District Dropdown
district_label = ctk.CTkLabel(section1_frame, text="District", font=("Arial", 12), fg_color="#f0f0f0",
                               text_color="black", anchor="w")
district_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

district_var = StringVar()
district_dropdown = ctk.CTkOptionMenu(section1_frame, variable=district_var, fg_color="#A1AEB1", values=[
    "Ampara", "Anuradhapura", "Badulla", "Batticaloa", "Colombo", "Gampaha", "Galle", "Hambantota",
    "Jaffna", "Kalutara", "Kandy", "Kegalle", "Kilinochchi", "Kurunegala", "Mannar", "Matale",
    "Matara", "Monaragala", "Mullaitivu", "Nuwara Eliya", "Polonnaruwa", "Puttalam", "Ratnapura",
    "Trincomalee", "Vavuniya"],
                                     font=("Arial", 12), button_color="gray", button_hover_color="#888",
                                     text_color="black")  # Gray background for dropdown arrow
district_dropdown.grid(row=2, column=1, padx=5, pady=5, sticky="w")

# Other fields
date_of_registration = DateEntry(section1_frame,text="Date of Registration", width=12, background='darkblue', foreground='white', borderwidth=2,
                                 font=("Arial", 12))
date_of_registration.grid(row=3, column=1, padx=5, pady=5, sticky="w")

index_number = create_label_entry(section1_frame, 4, "Index Number")
name = create_label_entry(section1_frame, 5, "Name")
full_name = create_label_entry(section1_frame, 6, "Full Name")

date_of_birth = DateEntry(section1_frame,text="Date of Birth", width=12, background='darkblue', foreground='white', borderwidth=2,
                          font=("Arial", 12))
date_of_birth.grid(row=7, column=1, padx=5, pady=5, sticky="w")

# Gender Radio Buttons
gender_label = ctk.CTkLabel(section1_frame, text="Gender", font=("Arial", 12), fg_color="#f0f0f0",
                            text_color="black", anchor="w")
gender_label.grid(row=8, column=0, padx=5, pady=5, sticky="w")

gender_var = StringVar()
gender_buttons_frame = Frame(section1_frame, bg="#f0f0f0")
gender_buttons_frame.grid(row=8, column=1, padx=5, pady=5, sticky="w")

male_radio = ctk.CTkRadioButton(gender_buttons_frame, text="Male", variable=gender_var, value="Male",
                                 font=("Arial", 12), fg_color="black", text_color="black")
female_radio = ctk.CTkRadioButton(gender_buttons_frame, text="Female", variable=gender_var, value="Female",
                                   font=("Arial", 12), fg_color="black", text_color="black")
other_radio = ctk.CTkRadioButton(gender_buttons_frame, text="Other", variable=gender_var, value="Other",
                                  font=("Arial", 12), fg_color="black", text_color="black")
male_radio.pack(side=LEFT, padx=5)
female_radio.pack(side=LEFT, padx=5)
other_radio.pack(side=LEFT, padx=5)

nic = create_label_entry(section1_frame, 9, "NIC")

telephone_number = create_label_entry(section1_frame, 10, "Telephone Number")
naita_id_number = create_label_entry(section1_frame, 11, "NAITA ID Number")

# Dropout Radio Buttons
dropout_label = ctk.CTkLabel(section1_frame, text="Drop Out", font=("Arial", 12), fg_color="#f0f0f0",
                             text_color="black", anchor="w")
dropout_label.grid(row=12, column=0, padx=5, pady=5, sticky="w")

dropout_var = StringVar()
dropout_buttons_frame = Frame(section1_frame, bg="#f0f0f0")
dropout_buttons_frame.grid(row=12, column=1, padx=5, pady=5, sticky="w")

dropout_yes = ctk.CTkRadioButton(dropout_buttons_frame, text="Yes", variable=dropout_var, value="Yes",
                                 font=("Arial", 12), fg_color="black", text_color="black")
dropout_no = ctk.CTkRadioButton(dropout_buttons_frame, text="No", variable=dropout_var, value="No",
                                font=("Arial", 12), fg_color="black", text_color="black")
dropout_yes.pack(side=LEFT, padx=5)
dropout_no.pack(side=LEFT, padx=5)

# Dropout Date
dropout_date_label = ctk.CTkLabel(section1_frame, text="Drop Out Date", font=("Arial", 12), fg_color="#f0f0f0",
                                  text_color="black", anchor="w")
dropout_date_label.grid(row=13, column=0, padx=5, pady=5, sticky="w")

dropout_date = DateEntry(section1_frame, width=12, background='darkblue', foreground='white', borderwidth=2,
                         font=("Arial", 12))
dropout_date.grid(row=13, column=1, padx=5, pady=5, sticky="w")

# Address fields
address_no = create_label_entry(section1_frame, 14, "Address No")
address_f_line = create_label_entry(section1_frame, 15, "Address First Line")
address_l_line = create_label_entry(section1_frame, 16, "Address Last Line")

# Section 2: Establishment Details
section2_frame = ctk.CTkFrame(scrollable_frame, fg_color="#f0f0f0")
section2_frame.pack(pady=10, padx=20, fill="x", expand=True, anchor="center")

# Section Header 2
header2 = ctk.CTkLabel(section2_frame, text="Establishment Details", font=("Arial", 16, "bold"),
                       fg_color="#f0f0f0", text_color="black")
header2.grid(row=0, column=0, columnspan=2, pady=10, sticky="w")

nameof_establishment = create_label_entry(section2_frame, 1, "Name of Establishment")
establishment_type = create_label_entry(section2_frame, 2, "Establishment Type")
establishment_address_division = create_label_entry(section2_frame, 3, "Establishment Address Division")
establishment_address_district = create_label_entry(section2_frame, 4, "Establishment Address District")
establishment_telephone = create_label_entry(section2_frame, 5, "Establishment Telephone")
ds_division = create_label_entry(section2_frame, 6, "DS Division")
establishment_code = create_label_entry(section2_frame, 7, "Establishment Code")

# Section 3: Sector Name to the End
section3_frame = ctk.CTkFrame(scrollable_frame, fg_color="#f0f0f0")
section3_frame.pack(pady=10, padx=20, fill="x", expand=True, anchor="center")

# Section Header 3
header3 = ctk.CTkLabel(section3_frame, text="Additional Details", font=("Arial", 16, "bold"),
                       fg_color="#f0f0f0", text_color="black")
header3.grid(row=0, column=0, columnspan=2, pady=10, sticky="w")

sector_label = ctk.CTkLabel(section3_frame, text="Sector Name", font=("Arial", 12), fg_color="#f0f0f0",
                            text_color="black", anchor="w")
sector_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

sector_var = StringVar()
sector_dropdown = ctk.CTkOptionMenu(section3_frame, variable=sector_var, fg_color="#A1AEB1", values=[
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
    "Textile and garments", "Wood related"],
                                 font=("Arial", 12), button_color="gray", button_hover_color="#888",
                                 text_color="black")  # Gray background for dropdown arrow
sector_dropdown.grid(row=1, column=1, padx=5, pady=5, sticky="w")

trade = create_label_entry(section3_frame, 2, "Trade")
trade_code = create_label_entry(section3_frame, 3, "Trade Code")
mode = create_label_entry(section3_frame, 4, "Mode")
nvq_level = create_label_entry(section3_frame, 5, "NVQ Level")
inspector_name = create_label_entry(section3_frame, 6, "Inspector Name")

# Commencement Date
commencement_date_label = ctk.CTkLabel(section3_frame, text="Commencement Date", font=("Arial", 12), fg_color="#f0f0f0",
                                       text_color="black", anchor="w")
commencement_date_label.grid(row=9, column=0, padx=5, pady=5, sticky="w")

commencement_date = DateEntry(section3_frame, width=12, background='darkblue', foreground='white', borderwidth=2,
                              font=("Arial", 12))
commencement_date.grid(row=9, column=1, padx=5, pady=5, sticky="w")

# Schedule Date Completion
schedule_date_completion_label = ctk.CTkLabel(section3_frame, text="Schedule Date Completion", font=("Arial", 12),
                                              fg_color="#f0f0f0", text_color="black", anchor="w")
schedule_date_completion_label.grid(row=10, column=0, padx=5, pady=5, sticky="w")

schedule_date_completion = DateEntry(section3_frame, width=12, background='darkblue', foreground='white',
                                     borderwidth=2, font=("Arial", 12))
schedule_date_completion.grid(row=10, column=1, padx=5, pady=5, sticky="w")

signature_tm = create_label_entry(section3_frame, 11, "Signature TM")

# Remark
remark_label = ctk.CTkLabel(section3_frame, text="Remark", font=("Arial", 12), fg_color="#f0f0f0",
                            text_color="black", anchor="w")
remark_label.grid(row=12, column=0, padx=5, pady=5, sticky="w")

remark = ctk.CTkEntry(section3_frame, width=250, font=("Arial", 12), text_color="black", fg_color="#A1AEB1")
remark.grid(row=12, column=1, padx=5, pady=5, sticky="w")

# Submit and Clear Form Buttons
button_submit = ctk.CTkButton(master=form_frame, text="Submit", command=submit, width=100, height=30, fg_color="crimson")
button_submit.pack(side="bottom", padx=10, pady=10)

button_clear = ctk.CTkButton(master=form_frame, text="Clear Form", command=clear_form, width=100, height=30,
                             fg_color="crimson")
button_clear.pack(side="bottom", padx=10, pady=10)
# Run the application
app.mainloop()
