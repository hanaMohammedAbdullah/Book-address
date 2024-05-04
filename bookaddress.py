from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from db import Database
# importing csv and os module
import csv
import os

db = Database('addressbook.db')


def populate_list():
    parts_list.delete(0, END)
    # parts_list.insert(END, ('ID', 'First_Name', 'Last_Name', 'State', 'City', 'Address', 'Email', 'Phone', 'Street' ))

    for row in db.fetch():
        parts_list.insert(END, row)


def add_item():
    if first_name.get() == '' or lastName_text.get() == '' or phone_text.get() == '' or email_text.get() == '':
        messagebox.showerror('Required Fields', 'Please include all fields (fist name, last name, phone number, email)')
        return
    db.insert(first_name.get(), lastName_text.get(),
              state_text.get(), city_text.get(), address_text.get(), email_text.get(), phone_text.get(), street_text.get())
    parts_list.delete(0, END)
    parts_list.insert(END, (first_name.get(), lastName_text.get(), state_text.get(),
                            city_text.get(), address_text.get(), email_text.get(), phone_text.get(), street_text.get()))
    clear_text()
    populate_list()


def select_item(event):
    try:
        global selected_item
        index = parts_list.curselection()[0]
        selected_item = parts_list.get(index)



        FirstName_entry.delete(0, END)
        FirstName_entry.insert(END, selected_item[1])
        LastName_entry.delete(0, END)
        LastName_entry.insert(END, selected_item[2])
        state_entry.delete(0, END)
        state_entry.insert(END, selected_item[3])
        city_entry.delete(0, END)
        city_entry.insert(END, selected_item[4])
        address_entry.delete(0, END)
        address_entry.insert(END, selected_item[5])
        email_entry.delete(0, END)
        email_entry.insert(END, selected_item[6])
        phone_entry.delete(0, END)
        phone_entry.insert(END, selected_item[7])
        street_entry.delete(0, END)
        street_entry.insert(END, selected_item[8])
        # Add text to entries
        
    except IndexError:
        pass


def remove_item():
    db.remove(selected_item[0])
    clear_text()
    populate_list()


def update_item():
    db.update(selected_item[0], first_name.get(), lastName_text.get(), state_text.get(), city_text.get(), address_text.get(), email_text.get(), phone_text.get(), street_text.get())
    populate_list()


def clear_text():
    FirstName_entry.delete(0, END)
    LastName_entry.delete(0, END)
    state_entry.delete(0, END)
    city_entry.delete(0, END)
    address_entry.delete(0, END)
    email_entry.delete(0, END)
    phone_entry.delete(0, END)
    street_entry.delete(0, END)

def export_data():
    if parts_list.size() == 0:
        messagebox.showerror('Export Data', 'there is no data to export')
        return
    fln = filedialog.asksaveasfilename(initialdir=os.getcwd(),initialfile='Address.csv', defaultextension=".csv", filetypes=[("CSV file", "*.csv")])
    with open(fln, mode='w') as f:
        writer = csv.writer(f ,delimiter=',')
        writer.writerow(['ID', 'First Name', 'Last Name', 'State', 'City', 'Address', 'Email', 'Phone', 'Street'])
        for i in range(parts_list.size()):
            writer.writerow(parts_list.get(i))
        messagebox.showinfo('Data Exported', 'Your data has been exported to ' + os.path.basename(fln) + ' successfully')
def search():
    parts_list.delete(0, END)
    for row in db.search(Search_text.get()):
        parts_list.insert(END, row)

def import_data():
    fln = filedialog.askopenfilename(initialdir=os.getcwd(), title='Open CSV', filetypes=[("CSV file", "*.csv")])
    with open(fln) as f:
        reader = csv.reader(f)
        # skip the first row
        next(reader)
        for row in reader:
            db.insert(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
            parts_list.insert(END, row)
        messagebox.showinfo('Data Imported', 'Your data has been imported successfully')       
# Create window object
app = Tk()

# FirstName
first_name = StringVar()
FirstName_label = Label(app, text='First Name', font=('bold', 14), pady=20)
FirstName_label.grid(row=0, column=0, sticky=W)
FirstName_entry = Entry(app, textvariable=first_name)
FirstName_entry.grid(row=0, column=1)
# LastName
lastName_text = StringVar()
LastName_label = Label(app, text='Last name', font=('bold', 14))
LastName_label.grid(row=0, column=2, sticky=W)
LastName_entry = Entry(app, textvariable=lastName_text)
LastName_entry.grid(row=0, column=3)
# state
state_text = StringVar()
state_label = Label(app, text='State', font=('bold', 14))
state_label.grid(row=1, column=0, sticky=W)
state_entry = Entry(app, textvariable=state_text)
state_entry.grid(row=1, column=1)
# city
city_text = StringVar()
city_label = Label(app, text='City', font=('bold', 14))
city_label.grid(row=1, column=2, sticky=W)
city_entry = Entry(app, textvariable=city_text)
city_entry.grid(row=1, column=3)

# address
address_text = StringVar()
address_label = Label(app, text='Address', font=('bold', 14))
address_label.grid(row=2, column=0, sticky=W)
address_entry = Entry(app, textvariable=address_text)
address_entry.grid(row=2, column=1)
# email
email_text = StringVar()
email_label = Label(app, text='Email', font=('bold', 14))
email_label.grid(row=2, column=2, sticky=W)
email_entry = Entry(app, textvariable=email_text)
email_entry.grid(row=2, column=3)
# phone
phone_text = StringVar()
phone_label = Label(app, text='Phone Number', font=('bold', 14))
phone_label.grid(row=3, column=0, sticky=W)
phone_entry = Entry(app, textvariable=phone_text)
phone_entry.grid(row=3, column=1)
# street
street_text = StringVar()
street_label = Label(app, text='Street', font=('bold', 14))
street_label.grid(row=3, column=2, sticky=W)
street_entry = Entry(app, textvariable=street_text)
street_entry.grid(row=3, column=3)

# # Search
Search_text = StringVar()
Search_Label = Button(app, text='Search', font=('bold', 14 ), command=search)
Search_Label.grid(row=5, column=1, sticky=W)
Search_entry = Entry(app, textvariable=Search_text  )
Search_entry.grid(row=5, column=0)
# Id
Id_text = StringVar()
Id_label = Label(app, text='Id', font=('bold', 12))
Id_label.grid(row=6, column=0, sticky=W , padx=20)
# First_name
First_name_text = StringVar()
First_name_label = Label(app, text='First Name', font=('bold', 12))
First_name_label.grid(row=6, column=1, sticky=W )
# Info List (Listbox)
parts_list = Listbox(app, height=8, width=80, border=0)
parts_list.grid(row=7, column=0, columnspan=3, rowspan=6, pady=20, padx=20)
# Create scrollbar
scrollbar = Scrollbar(app)
scrollbar.grid(row=7, column=3)
# Set scroll to listbox
parts_list.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=parts_list.yview)
# Bind select
parts_list.bind('<<ListboxSelect>>', select_item)

# Buttons
add_btn = Button(app, text='Add Part', width=12, command=add_item)
add_btn.grid(row=4, column=0, pady=20)

remove_btn = Button(app, text='Remove Part', width=12, command=remove_item)
remove_btn.grid(row=4, column=1)

update_btn = Button(app, text='Update Part', width=12, command=update_item)
update_btn.grid(row=4, column=2)

clear_btn = Button(app, text='Clear Input', width=12, command=clear_text)
clear_btn.grid(row=4, column=3)

export_btn = Button(app, text='Export', width=12, command=export_data)
export_btn.grid(row=4, column=4)

inport_btn = Button(app, text='Import', width=12, command=import_data)
inport_btn.grid(row=4, column=5)

app.title('Address Book')
app.geometry('1400x750')

# Populate data
populate_list()

# Start program
app.mainloop()


# To create an executable, install pyinstaller and run
# '''
# pyinstaller --onefile --add-binary='/System/Library/Frameworks/Tk.framework/Tk':'tk' --add-binary='/System/Library/Frameworks/Tcl.framework/Tcl':'tcl' part_manager.py
# '''
