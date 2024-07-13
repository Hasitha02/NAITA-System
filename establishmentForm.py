import customtkinter as ctk
import mysql.connector
from tkinter import messagebox

def insert_into_db():
    if not messagebox.askyesno("Confirmation", "Do you want to submit the form?"):
        return

    est_name = est_name_entry.get()
    est_code = est_code_entry.get()
    est_type = est_type_entry.get()
    est_addr_div = est_addr_div_entry.get()
    est_addr_dist = est_addr_dist_entry.get()
    est_tel = est_tel_entry.get()
    ds_div = ds_div_entry.get()

    if not est_code:
        messagebox.showerror("Input Error", "Establishment Code is required")
        return

    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='hasitha0214',
            database='NAITA'
        )
        cursor = conn.cursor()
        insert_query = """
        INSERT INTO establishments 
        (establishment_code, establishment_name, establishment_type, address_division, address_district, telephone, ds_division)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (est_code, est_name, est_type, est_addr_div, est_addr_dist, est_tel, ds_div))
        conn.commit()
        messagebox.showinfo("Success", "Data inserted successfully")
        cursor.close()
        conn.close()
        clear_form()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

def clear_form():
    if not messagebox.askyesno("Confirmation", "Do you want to clear the form?"):
        return

    est_name_entry.delete(0, ctk.END)
    est_code_entry.delete(0, ctk.END)
    est_type_entry.delete(0, ctk.END)
    est_addr_div_entry.delete(0, ctk.END)
    est_addr_dist_entry.delete(0, ctk.END)
    est_tel_entry.delete(0, ctk.END)
    ds_div_entry.delete(0, ctk.END)

# Set appearance mode
ctk.set_appearance_mode("light")

# Create the main window
esta_form = ctk.CTk()
esta_form.geometry("620x400")
esta_form.title("New Establishment Form")

# Add a label and entry for "Name of Establishment"
est_name_label = ctk.CTkLabel(esta_form, text="01. Name of Establishment:")
est_name_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
est_name_entry = ctk.CTkEntry(esta_form)
est_name_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

# Add a label and entry for "Establishment Code"
est_code_label = ctk.CTkLabel(esta_form, text="02. Establishment Code:")
est_code_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
est_code_entry = ctk.CTkEntry(esta_form)
est_code_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

# Add a label and entry for "Establishment Type"
est_type_label = ctk.CTkLabel(esta_form, text="03. Establishment Type:")
est_type_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
est_type_entry = ctk.CTkEntry(esta_form)
est_type_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

# Add a label and entry for "Establishment Address Division"
est_addr_div_label = ctk.CTkLabel(esta_form, text="04. Establishment Address Division:")
est_addr_div_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
est_addr_div_entry = ctk.CTkEntry(esta_form)
est_addr_div_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")

# Add a label and entry for "Establishment Address District"
est_addr_dist_label = ctk.CTkLabel(esta_form, text="05. Establishment Address District:")
est_addr_dist_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")
est_addr_dist_entry = ctk.CTkEntry(esta_form)
est_addr_dist_entry.grid(row=4, column=1, padx=10, pady=10, sticky="w")

# Add a label and entry for "Establishment Telephone"
est_tel_label = ctk.CTkLabel(esta_form, text="06. Establishment Telephone:")
est_tel_label.grid(row=5, column=0, padx=10, pady=10, sticky="w")
est_tel_entry = ctk.CTkEntry(esta_form)
est_tel_entry.grid(row=5, column=1, padx=10, pady=10, sticky="w")

# Add a label and entry for "DS Division"
ds_div_label = ctk.CTkLabel(esta_form, text="07. DS Division:")
ds_div_label.grid(row=6, column=0, padx=10, pady=10, sticky="w")
ds_div_entry = ctk.CTkEntry(esta_form)
ds_div_entry.grid(row=6, column=1, padx=10, pady=10, sticky="w")

# Add submit and clear buttons
submit_button = ctk.CTkButton(esta_form, text="Submit", command=insert_into_db)
submit_button.grid(row=7, column=0, padx=10, pady=20, sticky="e")

clear_button = ctk.CTkButton(esta_form, text="Clear", command=clear_form)
clear_button.grid(row=7, column=1, padx=10, pady=20, sticky="w")

# Run the main loop
esta_form.mainloop()
