import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
import csv
import os
from db import Database

db = Database('addressbook.db')

# Create window object
window = tk.Tk()
window.title('Address Book')
window.geometry('1400x750')
window.configure(bg="#333333")

# Create a Frame for login
Login_Frame = tk.Frame(window, bg="#333333")
Login_Frame.pack(pady=20)

username = tk.StringVar()
password = tk.StringVar()

tk.Label(Login_Frame, text="Username", font=('bold', 14), bg="#333333", fg="white").pack()
tk.Entry(Login_Frame, textvariable=username).pack()
tk.Label(Login_Frame, text="Password", font=('bold', 14), bg="#333333", fg="white").pack()
tk.Entry(Login_Frame, textvariable=password, show="*").pack()
tk.Button(Login_Frame, text="Login", command=lambda: login()).pack()

def login():
    if username.get() == "admin" and password.get() == "admin":
        Login_Frame.destroy()
        main_addressbook()
    else:
        messagebox.showerror("Error", "Invalid username or password")

def main_addressbook():
    def populate_list():
        trv.delete(*trv.get_children())
        for row in db.fetch():
            trv.insert('', 'end', values=row)

    def add_item():
        if first_name.get() == '' or lastName_text.get() == '' or phone_text.get() == '' or email_text.get() == '':
            messagebox.showerror('Required Fields', 'Please include all fields (first name, last name, phone number, email)')
            return
        db.insert(first_name.get(), lastName_text.get(), state_text.get(), city_text.get(), address_text.get(), email_text.get(), phone_text.get(), street_text.get())
        populate_list()
        clear_text()

    def select_item(event):
        try:
            global selected_item
            index = trv.identify_row(event.y)
            selected_item = trv.item(trv.focus())
            first_name.set(selected_item['values'][1])
            lastName_text.set(selected_item['values'][2])
            state_text.set(selected_item['values'][3])
            city_text.set(selected_item['values'][4])
            address_text.set(selected_item['values'][5])
            email_text.set(selected_item['values'][6])
            phone_text.set(selected_item['values'][7])
            street_text.set(selected_item['values'][8])
        except IndexError:
            pass

    def remove_item():
        db.remove(selected_item['values'][0])
        populate_list()
        clear_text()

    def update_item():
        db.update(selected_item['values'][0], first_name.get(), lastName_text.get(), state_text.get(), city_text.get(), address_text.get(), email_text.get(), phone_text.get(), street_text.get())
        populate_list()

    def clear_text():
        FirstName_entry.delete(0, tk.END)
        LastName_entry.delete(0, tk.END)
        state_entry.delete(0, tk.END)
        city_entry.delete(0, tk.END)
        address_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
        phone_entry.delete(0, tk.END)
        street_entry.delete(0, tk.END)

    def export_data():
        if trv.size() == 0:
            messagebox.showerror('Export Data', 'There is no data to export')
            return
        fln = filedialog.asksaveasfilename(initialdir=os.getcwd(), initialfile='Address.csv', defaultextension=".csv", filetypes=[("CSV file", "*.csv")])
        with open(fln, mode='w') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(['ID', 'First Name', 'Last Name', 'State', 'City', 'Address', 'Email', 'Phone', 'Job'])
            for i in trv.get_children():
                value = trv.item(i)['values']
                writer.writerow(value)
            messagebox.showinfo('Data Exported', f'Your data has been exported to {os.path.basename(fln)} successfully')

    def search():
        trv.delete(*trv.get_children())
        for row in db.search(Search_text.get()):
            trv.insert('', 'end', values=row)

    def import_data():
        fln = filedialog.askopenfilename(initialdir=os.getcwd(), title='Open CSV', filetypes=[("CSV file", "*.csv")])
        with open(fln) as f:
            reader = csv.reader(f)
            next(reader)  # skip the first row
            for row in reader:
                if len(row) >= 9:
                    db.insert(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
                    trv.insert('', 'end', values=row)
            messagebox.showinfo('Data Imported', 'Your data has been imported successfully')

    app = tk.Frame(window, bg="#333333")
    app.pack(fill="both", expand=True)

    wrapperData = tk.LabelFrame(app, text="Address Book data", bg="#333333", fg="white")
    wrapperAction = tk.LabelFrame(app, text="Address Book Action", bg="#333333", fg="white")
    wrapperDatatable = tk.LabelFrame(app, text="Address Book List", bg="#333333", fg="white")

    wrapperData.pack(fill="both", expand="yes", padx=20, pady=10)
    wrapperAction.pack(fill="both", expand="yes", padx=20, pady=10)
    wrapperDatatable.pack(fill="both", expand="yes", padx=20, pady=10)

    s = ttk.Style()
    s.configure('Treeview', rowheight=40, font=('Arial', 10), background='#333333', foreground='white')

    trv = ttk.Treeview(wrapperDatatable, columns=(1, 2, 3, 4, 5, 6, 7, 8, 9), show="headings")
    trv.pack()
    trv.column(1, stretch=tk.NO, width=50)
    trv.heading(1, text="ID")
    trv.column(2, stretch=tk.NO, width=150)
    trv.heading(2, text="First Name")
    trv.column(3, stretch=tk.NO, width=150)
    trv.heading(3, text="Last Name")
    trv.column(4, stretch=tk.NO, width=150)
    trv.heading(4, text="State")
    trv.column(5, stretch=tk.NO, width=150)
    trv.heading(5, text="City")
    trv.column(6, stretch=tk.NO, width=120)
    trv.heading(6, text="Address")
    trv.column(7, stretch=tk.NO, width=150)
    trv.heading(7, text="Email")
    trv.column(8, stretch=tk.NO, width=150)
    trv.heading(8, text="Phone")
    trv.column(9, stretch=tk.NO, width=150)
    trv.heading(9, text="Job")
    trv.bind('<<TreeviewSelect>>', select_item)

    populate_list()

    add_btn = tk.Button(wrapperAction, text='Add New', width=12, command=add_item)
    add_btn.grid(row=4, column=0, padx=10)

    remove_btn = tk.Button(wrapperAction, text='Remove', width=12, command=remove_item)
    remove_btn.grid(row=4, column=1, padx=10)

    update_btn = tk.Button(wrapperAction, text='Update', width=12, command=update_item)
    update_btn.grid(row=4, column=2, padx=10)

    clear_btn = tk.Button(wrapperAction, text='Clear Input', width=12, command=clear_text)
    clear_btn.grid(row=4, column=3, padx=10)

    export_btn = tk.Button(wrapperAction, text='Export', width=12, command=export_data)
    export_btn.grid(row=4, column=4, padx=10)

    import_btn = tk.Button(wrapperAction, text='Import', width=12, command=import_data)
    import_btn.grid(row=4, column=5, padx=10)

    Search_text = tk.StringVar()
    Search_Label = tk.Button(wrapperAction, text='Search', font=('bold', 10), command=search)
    Search_Label.grid(row=5, column=1, sticky=tk.W, padx=10, pady=10)
    Search_entry = tk.Entry(wrapperAction, textvariable=Search_text)
    Search_entry.grid(row=5, column=0, padx=10, pady=10)

    # FirstName
    first_name = tk.StringVar()
    FirstName_label = tk.Label(wrapperData, text='First Name :', font=('bold', 10), bg="#333333", fg="white")
    FirstName_label.grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
    FirstName_entry = tk.Entry(wrapperData, textvariable=first_name)
    FirstName_entry.grid(row=0, column=1)

    # LastName
    lastName_text = tk.StringVar()
    LastName_label = tk.Label(wrapperData, text='Last Name :', font=('bold', 10), bg="#333333", fg="white")
    LastName_label.grid(row=0, column=2, sticky=tk.W, padx=10, pady=10)
    LastName_entry = tk.Entry(wrapperData, textvariable=lastName_text)
    LastName_entry.grid(row=0, column=3)

    # State
    state_text = tk.StringVar()
    state_label = tk.Label(wrapperData, text='State :', font=('bold', 10), bg="#333333", fg="white")
    state_label.grid(row=1, column=0, sticky=tk.W, padx=10, pady=10)
    state_entry = tk.Entry(wrapperData, textvariable=state_text)
    state_entry.grid(row=1, column=1)

    # City
    city_text = tk.StringVar()
    city_label = tk.Label(wrapperData, text='City :', font=('bold', 10), bg="#333333", fg="white")
    city_label.grid(row=1, column=2, sticky=tk.W, padx=10, pady=10)
    city_entry = tk.Entry(wrapperData, textvariable=city_text)
    city_entry.grid(row=1, column=3)

    # Address
    address_text = tk.StringVar()
    address_label = tk.Label(wrapperData, text='Address :', font=('bold', 10), bg="#333333", fg="white")
    address_label.grid(row=2, column=0, sticky=tk.W, padx=10, pady=10)
    address_entry = tk.Entry(wrapperData, textvariable=address_text)
    address_entry.grid(row=2, column=1)

    # Email
    email_text = tk.StringVar()
    email_label = tk.Label(wrapperData, text='Email :', font=('bold', 10), bg="#333333", fg="white")
    email_label.grid(row=2, column=2, sticky=tk.W, padx=10, pady=10)
    email_entry = tk.Entry(wrapperData, textvariable=email_text)
    email_entry.grid(row=2, column=3)

    # Phone
    phone_text = tk.StringVar()
    phone_label = tk.Label(wrapperData, text='Phone Number :', font=('bold', 10), bg="#333333", fg="white")
    phone_label.grid(row=3, column=0, sticky=tk.W, padx=10, pady=10)
    phone_entry = tk.Entry(wrapperData, textvariable=phone_text)
    phone_entry.grid(row=3, column=1)

    # Street
    street_text = tk.StringVar()
    street_label = tk.Label(wrapperData, text='Job :', font=('bold', 10), bg="#333333", fg="white")
    street_label.grid(row=3, column=2, sticky=tk.W, padx=10, pady=10)
    street_entry = tk.Entry(wrapperData, textvariable=street_text)
    street_entry.grid(row=3, column=3)

window.mainloop()
