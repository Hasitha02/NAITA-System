from customtkinter import *

app = CTk()
app.geometry("500x400")

frame = CTkFrame(master=app, fg_color="#8d6f3a", border_color="#ffcc70", border_width=2)
frame.pack(expand=True)

label = CTkLabel(master=frame, text="Frame")
entry = CTkEntry(master=frame, placeholder_text="type...", placeholder_text_color="gray")
btn = CTkButton(master=frame, text="submit")

label.pack(anchor="s", expand=True, pady=10, padx=30)
label.pack(anchor="s", expand=True, pady=10, padx=30)
label.pack(anchor="n", expand=True, pady=30, padx=20)
CTkButton(master=frame, text="another widget").pack(expand=True, pady=30, padx=20)
CTkButton(master=frame, text="another widget").pack(expand=True, pady=30, padx=20)
CTkButton(master=frame, text="another widget").pack(expand=True, pady=30, padx=20)

app.mainloop()