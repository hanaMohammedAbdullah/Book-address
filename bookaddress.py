import csv
import os
import re
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
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
    user = db.login(username.get(), password.get())
    if user:
        Login_Frame.destroy()  # Hide the login frame

        if user[3]:  # Check if user is superuser
            superuser_dashboard()
        else:
            main_addressbook()

    else:
        messagebox.showerror("Error", "Invalid username or password")

def superuser_dashboard():
    def populate_user_list():
        user_trv.delete(*user_trv.get_children())
        for row in db.fetch_users():
            user_trv.insert('', 'end', values=row)

    def add_user():
        if user_username.get() == '' or user_password.get() == '':
            messagebox.showerror('Required Fields', 'Please include all fields (username, password)')
            return
        db.create_user(user_username.get(), user_password.get(), user_is_superuser.get())
        populate_user_list()
        clear_user_text()

    def select_user(event):
        try:
            global selected_user
            index = user_trv.identify_row(event.y)
            selected_user = user_trv.item(user_trv.focus())
            user_username.set(selected_user['values'][1])
            user_password.set(selected_user['values'][2])
            user_is_superuser.set(selected_user['values'][3])
        except IndexError:
            pass
    def select_user(event):
        try:
          global selected_user
          index = user_trv.identify_row(event.y)
          selected_user = user_trv.item(user_trv.focus())
          if selected_user:  # Check if selected_user is not None
              user_username.set(selected_user['values'][1])
              user_password.set(selected_user['values'][2])
              user_is_superuser.set(selected_user['values'][3])
        except IndexError:
            pass
    def remove_user():
        db.delete_user(selected_user['values'][0])
        populate_user_list()
        clear_user_text()

    def update_user():
        db.update_user(selected_user['values'][0], user_username.get(), user_password.get(), user_is_superuser.get())
        populate_user_list()

    def clear_user_text():
        UserUsername_entry.delete(0, tk.END)
        UserPassword_entry.delete(0, tk.END)
        UserIsSuperuser_entry.deselect()

    # Create superuser_window as Toplevel
    superuser_window = tk.Toplevel(window)
    superuser_window.title("Superuser Dashboard")
    superuser_window.geometry('800x600')

    # Frame initialization
    wrapperDataUser = tk.LabelFrame(superuser_window, text="User Data", bg="#333333", fg="white")
    wrapperActionUser = tk.LabelFrame(superuser_window, text="User Actions", bg="#333333", fg="white")
    wrapperDatatableUser = tk.LabelFrame(superuser_window, text="User List", bg="#333333", fg="white")

    wrapperDataUser.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
    wrapperActionUser.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')
    wrapperDatatableUser.grid(row=2, column=0, padx=10, pady=10, sticky='nsew')

    # Style for Treeview
    s = ttk.Style()
    s.configure('Treeview', rowheight=40, font=('Arial', 10), background='#333333', foreground='white')

    # Treeview widget for user list
    user_trv = ttk.Treeview(wrapperDatatableUser, columns=(1, 2, 3), show="headings")
    user_trv.pack(fill='both', expand=True)
    user_trv.column(1, stretch=tk.NO, width=50)
    user_trv.heading(1, text="ID")
    user_trv.column(2, stretch=tk.NO, width=150)
    user_trv.heading(2, text="Username")
    user_trv.column(3, stretch=tk.NO, width=150)
    user_trv.heading(3, text="Is Superuser")
    user_trv.bind('<<TreeviewSelect>>', select_user)

    populate_user_list()

    # User Username
    user_username = tk.StringVar()
    UserUsername_label = tk.Label(wrapperDataUser, text='Username:', font=('bold', 10), bg="#333333", fg="white")
    UserUsername_label.grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
    UserUsername_entry = tk.Entry(wrapperDataUser, textvariable=user_username)
    UserUsername_entry.grid(row=0, column=1, padx=10, pady=10)

    # User Password
    user_password = tk.StringVar()
    UserPassword_label = tk.Label(wrapperDataUser, text='Password:', font=('bold', 10), bg="#333333", fg="white")
    UserPassword_label.grid(row=1, column=0, sticky=tk.W, padx=10, pady=10)
    UserPassword_entry = tk.Entry(wrapperDataUser, textvariable=user_password, show="*")
    UserPassword_entry.grid(row=1, column=1, padx=10, pady=10)

    # User Is Superuser
    user_is_superuser = tk.IntVar()
    UserIsSuperuser_label = tk.Label(wrapperDataUser, text='Is Superuser:', font=('bold', 10), bg="#333333", fg="white")
    UserIsSuperuser_label.grid(row=2, column=0, sticky=tk.W, padx=10, pady=10)
    UserIsSuperuser_entry = tk.Checkbutton(wrapperDataUser, variable=user_is_superuser)
    UserIsSuperuser_entry.grid(row=2, column=1, padx=10, pady=10)

    # Buttons for user actions
    add_user_btn = tk.Button(wrapperActionUser, text='Add User', width=12, command=add_user)
    add_user_btn.grid(row=0, column=0, padx=10, pady=10)

    remove_user_btn = tk.Button(wrapperActionUser, text='Remove User', width=12, command=remove_user)
    remove_user_btn.grid(row=0, column=1, padx=10, pady=10)

    update_user_btn = tk.Button(wrapperActionUser, text='Update User', width=12, command=update_user)
    update_user_btn.grid(row=0, column=2, padx=10, pady=10)

    clear_user_btn = tk.Button(wrapperActionUser, text='Clear Input', width=12, command=clear_user_text)
    clear_user_btn.grid(row=0, column=3, padx=10, pady=10)

    # Function to clear user input fields
    def clear_user_text():
        UserUsername_entry.delete(0, tk.END)
        UserPassword_entry.delete(0, tk.END)
        UserIsSuperuser_entry.deselect()

    # Function to destroy the superuser window and return to main window
    def close_superuser_window():
        superuser_window.destroy()
        if Login_Frame:
            Login_Frame.pack(pady=20)


    # Button to close the superuser window
    close_btn = tk.Button(superuser_window, text='Close', width=12, command=close_superuser_window)
    close_btn.grid(row=3, column=0, padx=10, pady=10)
def main_addressbook():
    def populate_list():
        trv.delete(*trv.get_children())
        for row in db.fetch_contacts():
            trv.insert('', 'end', values=row)

    def add_item():
        if first_name.get() == '' or lastName_text.get() == '' or phone_text.get() == '' or email_text.get() == '' or gender_var.get() == '' or city_text.get() == '' :
            messagebox.showerror('Required Fields', 'Please include all fields (first name, last name, phone number, email , gender , city)')
            return
        if not is_valid_email(email_text.get()):
         messagebox.showerror('Invalid Email', 'Please enter a valid email address')
         return
        if not is_valid_mobile(phone_text.get()):
         messagebox.showerror('Invalid Phone Number', 'Please enter a valid phone number')
         return
        db.insert_contact(first_name.get(), lastName_text.get(), gender_var.get(), city_text.get(), address_text.get(), email_text.get(), phone_text.get(), job.get())
        populate_list()
        clear_text()

    def is_valid_mobile(mobile):
     # Mobile number regex pattern
     pattern = r'^[0-9]\d{9}$'
     return re.match(pattern, mobile)   
    def is_valid_email(email):
    # Email regex pattern
        pattern = r'^[\w\-\.]+@[a-zA-Z0-9\-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email)

    def select_item(event):
        try:
            global selected_item
            index = trv.identify_row(event.y)
            selected_item = trv.item(trv.focus())
            first_name.set(selected_item['values'][2])
            lastName_text.set(selected_item['values'][3])
            email_text.set(selected_item['values'][7])
            phone_text.set(selected_item['values'][8])
        except IndexError:
            pass

    def remove_item():
        db.remove_contact(selected_item['values'][0])
        populate_list()
        clear_text()

    def update_item():
        db.update_contact(selected_item['values'][0], first_name.get(), lastName_text.get(), '', '', '', email_text.get(), phone_text.get(), '')
        populate_list()

    def clear_text():
        FirstName_entry.delete(0, tk.END)
        LastName_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
        phone_entry.delete(0, tk.END)
        gender_var.set('')
        city_entry.delete(0, tk.END)
        address_entry.delete(0, tk.END)
        job_entry.delete(0, tk.END)

    def search():
        trv.delete(*trv.get_children())
        for row in db.search_contacts(Search_text.get()):
            trv.insert('', 'end', values=row)

    def export_data():
        filename = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV Files', '*.csv')])
        if filename:
            with open(filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['ID', 'First Name', 'Last Name',"Gender","City" ,"Address",'Email', 'Phone' , "job" , "Job"])
                for row in db.fetch_contacts():
                    writer.writerow(row[0:2] + row[3:9])

    def import_data():
        fln = filedialog.askopenfilename(initialdir=os.getcwd(), title='Open CSV', filetypes=[("CSV file", "*.csv")])
        with open(fln) as f:
            reader = csv.reader(f)
            next(reader)  # skip the first row
            for row in reader:
                if len(row) >= 9:
                    db.insert_contact(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
                    trv.insert('', 'end', values=row[1:9])
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
    trv.heading(4, text="Gender")
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

    # gender
    gender_var = tk.StringVar(wrapperData , "Male")
    gender_label = tk.Label(wrapperData, text='Gender:', font=('bold', 10), bg="#333333", fg="white" )
    gender_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)

    # Options for gender selection
    gender_options = ["Male", "Female"]

    # OptionMenu for selecting gender
    gender_option = ttk.OptionMenu(wrapperData, gender_var, "", *gender_options )
    gender_option.grid(row=1, column=1, padx=10, pady=10)

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

    # job
    job = tk.StringVar()
    job_label = tk.Label(wrapperData, text='Job :', font=('bold', 10), bg="#333333", fg="white")
    job_label.grid(row=3, column=2, sticky=tk.W, padx=10, pady=10)
    job_entry = tk.Entry(wrapperData, textvariable=job)
    job_entry.grid(row=3, column=3)


try:
    window.mainloop()
except KeyboardInterrupt:
    # Handle the KeyboardInterrupt here, e.g., clean up resources, save data, or exit gracefully.
    print("Program interrupted. Exiting...")