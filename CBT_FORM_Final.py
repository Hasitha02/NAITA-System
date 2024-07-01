import re
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, LEFT
from reportlab.pdfgen import canvas as pdf_canvas
from openpyxl.workbook import Workbook
from reportlab.lib.pagesizes import letter
from tkcalendar import DateEntry
import mysql.connector
import customtkinter as ctk


# Custom class for CTkComboBox with suggestions
class SuggestionComboBox(ctk.CTkComboBox):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self._original_values = self._values  # Save original values
        self._entry_widget = self.children['!entry']  # Get the internal Entry widget
        self._entry_widget.bind('<KeyRelease>', self._on_key_release)

    def _on_key_release(self, event):
        value = self._entry_widget.get().lower()
        new_values = [item for item in self._original_values if value in item.lower()]
        self.configure(values=new_values)

# Initialize the customtkinter application
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Create the main window
app = ctk.CTk()
app.geometry("1020x700")
app.title("CBT Registration Form")

# Create a frame for the form inside a Canvas to allow scrolling
main_frame = ctk.CTkFrame(app)
main_frame.pack(fill=tk.BOTH, expand=0)

canvas = tk.Canvas(main_frame, width=1020, height=1000)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=0)

scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
canvas.configure(yscrollcommand=scrollbar.set)

scrollable_frame = ctk.CTkFrame(canvas)
scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

header1 = ctk.CTkLabel(scrollable_frame, text="Student Registration Form - CBT", font=("Arial", 35, "bold"), text_color="black")
header1.grid(row=0, column=0, columnspan=2, pady=10, padx=150, sticky="w")

header2 = ctk.CTkLabel(scrollable_frame, text="Apprentice Details", font=("Arial", 25, "bold"), text_color="black")
header2.grid(row=1, column=0, columnspan=2, pady=10, padx=100, sticky="w")

# Adding another header for Establishment Details
header3 = ctk.CTkLabel(scrollable_frame, text="Establishment Details", font=("Arial", 25, "bold"), text_color="black")

# Adding another header for Course Details
header4 = ctk.CTkLabel(scrollable_frame, text="Course Details", font=("Arial", 25, "bold"), text_color="black")

fields = {
    "category": "1. Category",
    "district": "2. District",
    "dateOfRegistration": "3. Date of Registration",
    "indexNumber": "4. Index Number",
    "name": "   a. Full Name",
    "fullName": "   b. Name with Initials",
    "addressNo": "  a. Address No",
    "addressFLine": "   b. Address First Line",
    "addressLLine": "   c. Address Last Line",
    "dateofBirth": "7. Date of Birth",
    "gender": "8. Gender",
    "NIC": "9. NIC",
    "telephoneNumber": "10. Telephone Number",
    "NAITAIDnumber": "11. NAITA ID Number",
    "dropOut": "12. Drop Out",
    "dropOutDate": "13. Drop Out Date",
    "nameofEstablishment": "14. Name of Establishment",
    "establishmentType": "15. Establishment Type",
    "establishmentAddressDivision": "16. Establishment Address Division",
    "establishmentAddressDistrict": "17. Establishment Address District",
    "establishmentTelephone": "18. Establishment Telephone",
    "DSDivision": "19. DS Division",
    "establishmentCode": "20. Establishment Code",
    "sectorName": "21. Sector Name",
    "trade": "22. Trade",
    "tradeCode": "23. Trade Code",
    "mode": "24. Mode",
    "NVQLevel": "25. NVQ Level",
    "inspectorName": "26. Inspector Name",
    "commencementDate": "27. Commencement Date",
    "scheduleDateCompletion": "28. Scheduled Date of Completion",
    "signatureTM": "29. Signature of TM",
    "remark": "30. Remark"
}

entries = {}
combo_fields = ["district", "nameofEstablishment", "sectorName", "trade", "mode", "NVQLevel", "inspectorName"]
date_fields = ["dateOfRegistration", "dateofBirth", "dropOutDate", "commencementDate", "scheduleDateCompletion"]

custom_data = {
    "district": ["Ampara", "Anuradhapura", "Badulla", "Batticaloa", "Colombo", "Gampaha", "Galle", "Hambantota",
            "Jaffna", "Kalutara", "Kandy", "Kegalle", "Kilinochchi", "Kurunegala", "Mannar", "Matale",
            "Matara", "Monaragala", "Mullaitivu", "Nuwara Eliya", "Polonnaruwa", "Puttalam", "Ratnapura",
            "Trincomalee", "Vavuniya"],
    "nameofEstablishment": ["_Smallholder Agribusiness Partnerships Program","141 Motors","141, MOTORS PVT LTD","171 Bakers","1st Step Pre School - Matale",
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
            "Zexel Diesel Engineers","Zimtha Punchar Shop","Zodiac Lubrcating Service","Zodiac Men's Fashion Tailors","Zonal Education Office"],
    "sectorName": ["Agriculture plantation and live stock", "Art design and media (visual and performing",
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
    "trade": ["3K - Aluminium fabricator", "3K - Aquarium keeper", "3K - Bathik artist", "3K - Beautician",
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
            "Wood Craftsman (Furniture)", "Wood Craftsman(Buildings)", "Wooden Craftman (Building)", "Wool Knitter"],
    "mode": ["ASS", "CRFT", "HVV", "NVQ", "PTC"],
    "NVQLevel": ["NVQ 3", "NVQ 4", "NVQ 6", "Certificate"],
    "inspectorName": ["A Sivanenthiran","A. Niyas","A.A. Nimali","A.A.I.P Wickramasinghe","A.A.M. Hemachandra","A.A.M. Sifnas",
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
            "W.R.N. Weeragoda","W.T.M.L.I. Jayasinghe","W.W.A.S. Kumara","W.W.M.M.K.Gunasinghe", "Y. Sivasankar","Y.A.D.S Yahampath","Y.M. Jayathissa"]
}

drop_out_options = ["Yes", "No"]
gender_options = ["Male", "Female", "Other"]

def toggle_drop_out_date():
    if drop_out_var.get() == "Yes":
        entries["dropOutDate"].configure(state="normal")
    else:
        entries["dropOutDate"].configure(state="disabled")


row_index = 2

# Apprentice Details
for field_key in ["category", "district", "dateOfRegistration", "indexNumber"]:
    label = ctk.CTkLabel(scrollable_frame, text=fields[field_key], font=("Arial", 15))
    label.grid(row=row_index, column=0, padx=20, pady=10, sticky="w")

    if field_key == "category":
        entries[field_key] = ctk.CTkEntry(scrollable_frame, font=("Arial", 13), width=405)
        entries[field_key].insert(0, "CBT - Center Based Training")
        entries[field_key].configure(state="disabled")
        entries[field_key].grid(row=row_index, column=1, padx=20, pady=10, sticky="w")
    elif field_key in combo_fields:
        entries[field_key] = SuggestionComboBox(scrollable_frame, values=custom_data.get(field_key, []), width=405)
        entries[field_key].grid(row=row_index, column=1, padx=20, pady=10, sticky="w")
    elif field_key in date_fields:
        entries[field_key] = DateEntry(scrollable_frame, date_pattern="yyyy-mm-dd", background='gray', width=69)  # Adjust width as needed
        entries[field_key].grid(row=row_index, column=1, padx=20, pady=10, sticky="w")
    else:
        entries[field_key] = ctk.CTkEntry(scrollable_frame, font=("Arial", 13), width=405)  # Adjust width as needed
        entries[field_key].grid(row=row_index, column=1, padx=20, pady=10, sticky="w")

    row_index += 1

# Name Section
name_header = ctk.CTkLabel(scrollable_frame, text="5. Name of The Apprentice", font=("Arial", 15))
name_header.grid(row=row_index, column=0, columnspan=2, pady=10, padx=20, sticky="w")
row_index += 1

for field_key in ["name", "fullName"]:
    label = ctk.CTkLabel(scrollable_frame, text=fields[field_key], font=("Arial", 15))
    label.grid(row=row_index, column=0, padx=20, pady=10, sticky="w")

    entries[field_key] = ctk.CTkEntry(scrollable_frame, font=("Arial", 13), width=405)
    entries[field_key].grid(row=row_index, column=1, padx=20, pady=10, sticky="w")
    row_index += 1

# Address Section
address_header = ctk.CTkLabel(scrollable_frame, text="6. Address", font=("Arial", 15))
address_header.grid(row=row_index, column=0, columnspan=2, pady=10, padx=20, sticky="w")
row_index += 1

for field_key in ["addressNo", "addressFLine", "addressLLine"]:
    label = ctk.CTkLabel(scrollable_frame, text=fields[field_key], font=("Arial", 15))
    label.grid(row=row_index, column=0, padx=20, pady=10, sticky="w")

    entries[field_key] = ctk.CTkEntry(scrollable_frame, font=("Arial", 13), width=405)
    entries[field_key].grid(row=row_index, column=1, padx=20, pady=10, sticky="w")
    row_index += 1

# Gender, NIC, Telephone, NAITA ID Number, Drop Out
for field_key in ["dateofBirth", "gender", "NIC", "telephoneNumber", "NAITAIDnumber", "dropOut"]:
    label = ctk.CTkLabel(scrollable_frame, text=fields[field_key], font=("Arial", 15))
    label.grid(row=row_index, column=0, padx=20, pady=10, sticky="w")

    if field_key == "gender":
        gender_var = tk.StringVar(value="Male")
        gender_frame = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
        gender_frame.grid(row=row_index, column=1, padx=20, pady=10, sticky="w")
        for option in gender_options:
            rb = ctk.CTkRadioButton(gender_frame, text=option, variable=gender_var, value=option)
            rb.pack(side=tk.LEFT, padx=5)
        entries[field_key] = gender_var
    elif field_key == "dropOut":
        drop_out_var = tk.StringVar(value="No")
        drop_out_frame = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
        drop_out_frame.grid(row=row_index, column=1, padx=20, pady=10, sticky="w")
        for option in drop_out_options:
            rb = ctk.CTkRadioButton(drop_out_frame, text=option, variable=drop_out_var, value=option, command=toggle_drop_out_date)
            rb.pack(side=tk.LEFT, padx=5)
        entries[field_key] = drop_out_var
    elif field_key in date_fields:
        entries[field_key] = DateEntry(scrollable_frame, date_pattern="yyyy-mm-dd", background='gray', width=69)
        entries[field_key].grid(row=row_index, column=1, padx=20, pady=10, sticky="w")
    else:
        entries[field_key] = ctk.CTkEntry(scrollable_frame, font=("Arial", 13), width=405)
        entries[field_key].grid(row=row_index, column=1, padx=20, pady=10, sticky="w")

    row_index += 1

# Drop Out Date (initially disabled)
label = ctk.CTkLabel(scrollable_frame, text=fields["dropOutDate"], font=("Arial", 15))
label.grid(row=row_index, column=0, padx=20, pady=10, sticky="w")

entries["dropOutDate"] = DateEntry(scrollable_frame, date_pattern="yyyy-mm-dd", background='gray', width=69)
entries["dropOutDate"].grid(row=row_index, column=1, padx=20, pady=10, sticky="w")
entries["dropOutDate"].configure(state="disabled")
row_index += 1

# Establishment Details
header3.grid(row=row_index, column=0, columnspan=2, pady=10, padx=20, sticky="w")
row_index += 1

for field_key in ["nameofEstablishment", "establishmentType", "establishmentAddressDivision", "establishmentAddressDistrict", "establishmentTelephone", "DSDivision", "establishmentCode"]:
    label = ctk.CTkLabel(scrollable_frame, text=fields[field_key], font=("Arial", 15))
    label.grid(row=row_index, column=0, padx=20, pady=10, sticky="w")

    if field_key in combo_fields:
        entries[field_key] = SuggestionComboBox(scrollable_frame, values=custom_data.get(field_key, []), width=405)
        entries[field_key].grid(row=row_index, column=1, padx=20, pady=10, sticky="w")
    else:
        entries[field_key] = ctk.CTkEntry(scrollable_frame, font=("Arial", 13), width=405)
        entries[field_key].grid(row=row_index, column=1, padx=20, pady=10, sticky="w")

    row_index += 1

# Course Details
header4.grid(row=row_index, column=0, columnspan=2, pady=10, padx=20, sticky="w")
row_index += 1

for field_key in ["sectorName", "trade", "tradeCode", "mode", "NVQLevel", "inspectorName", "commencementDate", "scheduleDateCompletion", "signatureTM", "remark"]:
    label = ctk.CTkLabel(scrollable_frame, text=fields[field_key], font=("Arial", 15))
    label.grid(row=row_index, column=0, padx=20, pady=10, sticky="w")

    if field_key in combo_fields:
        entries[field_key] = SuggestionComboBox(scrollable_frame, values=custom_data.get(field_key, []), width=405)
        entries[field_key].grid(row=row_index, column=1, padx=20, pady=10, sticky="w")
    elif field_key in date_fields:
        entries[field_key] = DateEntry(scrollable_frame, date_pattern="yyyy-mm-dd", background='gray', width=69)
        entries[field_key].grid(row=row_index, column=1, padx=20, pady=10, sticky="w")
    else:
        entries[field_key] = ctk.CTkEntry(scrollable_frame, font=("Arial", 13), width=405)
        entries[field_key].grid(row=row_index, column=1, padx=20, pady=10, sticky="w")

    row_index += 1


# Assuming your existing clear_form function is defined as follows:
def clear_form(event=None):
    confirmed = True  # Default to true since we ask for confirmation
    if event:
        confirmed = messagebox.askyesno("Clear Form", "Are you sure you want to clear this form?")

    if confirmed:
        for field_key in entries:
            if isinstance(entries[field_key], tk.StringVar):
                entries[field_key].set("")
            elif isinstance(entries[field_key], SuggestionComboBox):
                entries[field_key].set("")
            elif isinstance(entries[field_key], DateEntry):
                entries[field_key].delete(0, tk.END)
            else:
                entries[field_key].delete(0, tk.END)

        entries["dropOutDate"].configure(state="disabled")


# Bind mouse wheel scrolling to the canvas
def on_mouse_wheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

canvas.bind_all("<MouseWheel>", on_mouse_wheel)

# Submit function
def insert_into_db(data):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="hasitha0214",
        database="NAITA"
    )
    cursor = conn.cursor()

    query = """
        INSERT INTO CBTSD (
            category, district, dateOfRegistration, indexNumber, name, fullName, addressNo, addressFLine,
            addressLLine, dateofBirth, gender, NIC, telephoneNumber, NAITAIDnumber, dropOut, dropOutDate,
            nameofEstablishment, establishmentType, establishmentAddressDivision, establishmentAddressDistrict,
            establishmentTelephone, DSDivision, establishmentCode, sectorName, trade, tradeCode, mode,
            NVQLevel, inspectorName, commencementDate, scheduleDateCompletion, signatureTM, remark
        ) VALUES (
            %(category)s, %(district)s, %(dateOfRegistration)s, %(indexNumber)s, %(name)s, %(fullName)s, %(addressNo)s,
            %(addressFLine)s, %(addressLLine)s, %(dateofBirth)s, %(gender)s, %(NIC)s, %(telephoneNumber)s,
            %(NAITAIDnumber)s, %(dropOut)s, %(dropOutDate)s, %(nameofEstablishment)s, %(establishmentType)s,
            %(establishmentAddressDivision)s, %(establishmentAddressDistrict)s, %(establishmentTelephone)s,
            %(DSDivision)s, %(establishmentCode)s, %(sectorName)s, %(trade)s, %(tradeCode)s, %(mode)s, %(NVQLevel)s,
            %(inspectorName)s, %(commencementDate)s, %(scheduleDateCompletion)s, %(signatureTM)s, %(remark)s
        )
    """
    # Adjust data to handle None for dropOutDate when dropOut is "No" or unspecified
    if data['dropOut'] != "Yes":
        data['dropOutDate'] = None

    cursor.execute(query, data)
    conn.commit()
    cursor.close()
    conn.close()

def submit_form():
    form_data = {}
    for key, entry in entries.items():
        if isinstance(entry, DateEntry):
            form_data[key] = entry.get_date().strftime("%Y-%m-%d")
        elif isinstance(entry, ctk.CTkOptionMenu):
            form_data[key] = entry.get()
        else:
            form_data[key] = entry.get()

        # Add dropout date only if dropout is "Yes"
        if entries['dropOut'].get() == "Yes":
            form_data['dropOutDate'] = entries['dropOutDate'].get_date().strftime("%Y-%m-%d")
        else:
            form_data['dropOutDate'] = None  # Set dropOutDate to None if dropout is "No" or unspecified

    # Define NIC patterns
    nic_pattern_12_digits = re.compile(r'^\d{12}$')
    nic_pattern_9_digits_1_letter = re.compile(r'^\d{9}[A-Za-z]$')

    # Retrieve necessary fields
    telephone_number = form_data.get('telephoneNumber', '')
    establishment_telephone = form_data.get('establishmentTelephone', '')
    nic = form_data.get('NIC', '')

    # Perform validations
    if telephone_number and (len(telephone_number) != 10 or not telephone_number.isdigit()):
        messagebox.showerror("Error", "Phone number should be exactly 10 digits and numeric only.")
    elif establishment_telephone and (len(establishment_telephone) != 10 or not establishment_telephone.isdigit()):
        messagebox.showerror("Error", "Establishment phone number should be exactly 10 digits and numeric only.")
    elif nic and not (nic_pattern_12_digits.match(nic) or nic_pattern_9_digits_1_letter.match(nic)):
        messagebox.showerror("Error", "NIC should be exactly 12 digits or 9 digits followed by one letter if entered.")
    else:
        # Confirmation dialog
        confirmed = messagebox.askyesno("Submit Form", "Are you sure you want to submit this form?")
        if confirmed:
            try:
                insert_into_db(form_data)
                messagebox.showinfo("Success", "Data inserted successfully!")
                clear_form()
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error inserting data: {err}")
                clear_form()
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
                clear_form()


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
                "05. Full Name", "06. Name with Initials", "07. Date of Birth", "08. Gender",
                "09. NIC", "10. Telephone Number", "11. NAITA ID Number", "12. Drop Out",
                "13. Drop Out Date", "14. Address - No.", "15. Address - First Line", "16. Address - Last Line",
                "17. Name of Establishment", "18. Type of Establishment", "19. Establishment Address Division",
                "20. Establishment Address District", "21. Establishment Telephone Number", "22. DS Division",
                "23. Establishment Code", "24. Sector Name", "25. Trade", "26. Trade Code", "27. Mode",
                "28. NVQ Level", "29. Name of Inspector", "30. Commencement Date",
                "31. Schedule Date of Completion", "32. Signature of T.M.", "33. Remark"
            ]
            sheet.append(headers)

            # Collect form data and format dates
            data = [
                [
                    entries["category"].get(), entries["district"].get(),
                    entries["dateOfRegistration"].get_date().strftime("%Y-%m-%d"),
                    entries["indexNumber"].get(), entries["name"].get(), entries["fullName"].get(),
                    entries["dateofBirth"].get_date().strftime("%Y-%m-%d"),
                    entries["gender"].get(), entries["NIC"].get(), entries["telephoneNumber"].get(),
                    entries["NAITAIDnumber"].get(), entries["dropOut"].get(),
                    entries["dropOutDate"].get_date().strftime("%Y-%m-%d") if entries["dropOutDate"].get() else "",
                    entries["addressNo"].get(), entries["addressFLine"].get(), entries["addressLLine"].get(),
                    entries["nameofEstablishment"].get(), entries["establishmentType"].get(),
                    entries["establishmentAddressDivision"].get(), entries["establishmentAddressDistrict"].get(),
                    entries["establishmentTelephone"].get(), entries["DSDivision"].get(),
                    entries["establishmentCode"].get(), entries["sectorName"].get(), entries["trade"].get(),
                    entries["tradeCode"].get(), entries["mode"].get(), entries["NVQLevel"].get(),
                    entries["inspectorName"].get(),
                    entries["commencementDate"].get_date().strftime("%Y-%m-%d"),
                    entries["scheduleDateCompletion"].get_date().strftime("%Y-%m-%d"),
                    entries["signatureTM"].get(), entries["remark"].get()
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


# Create a frame for the buttons
button_frame = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
button_frame.grid(row=62, column=0, columnspan=3, padx=20, pady=20, sticky="w")

# Back button
Back_button = ctk.CTkButton(button_frame, text="Back", fg_color='crimson', font=("Arial", 14, "bold"), hover_color='#46070F')
Back_button.pack(side=tk.LEFT, padx=20)

# Clear button
clear_button = ctk.CTkButton(button_frame, text="Clear", command=lambda: clear_form(event=True), fg_color='crimson', font=("Arial", 14, "bold"), hover_color='#46070F')
clear_button.pack(side=tk.LEFT, padx=20)

# Submit button
submit_button = ctk.CTkButton(button_frame, text="Submit", command=submit_form, fg_color='crimson', font=("Arial", 14, "bold"), hover_color='#46070F')
submit_button.pack(side=tk.LEFT, padx=30)

# Print button
print_button = ctk.CTkButton(button_frame, text="Print File", command=print_to_excel, fg_color='crimson', font=("Arial", 14, "bold"), hover_color='#46070F')
print_button.pack(side=tk.LEFT, padx=20)


clear_form()


app.mainloop()
