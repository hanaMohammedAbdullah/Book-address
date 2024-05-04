from tkinter import *
from tkinter import messagebox
from db import Database

db = Database('store.db')


def populate_list():
    parts_list.delete(0, END)
    for row in db.fetch():
        parts_list.insert(END, row)


def add_item():
    if first_name.get() == '' or customer_text.get() == '' or retailer_text.get() == '' or price_text.get() == '':
        messagebox.showerror('Required Fields', 'Please include all fields')
        return
    db.insert(first_name.get(), customer_text.get(),
              retailer_text.get(), price_text.get())
    parts_list.delete(0, END)
    parts_list.insert(END, (first_name.get(), customer_text.get(),
                            retailer_text.get(), price_text.get()))
    clear_text()
    populate_list()


def select_item(event):
    try:
        global selected_item
        index = parts_list.curselection()[0]
        selected_item = parts_list.get(index)

        part_entry.delete(0, END)
        part_entry.insert(END, selected_item[1])
        customer_entry.delete(0, END)
        customer_entry.insert(END, selected_item[2])
        retailer_entry.delete(0, END)
        retailer_entry.insert(END, selected_item[3])
        price_entry.delete(0, END)
        price_entry.insert(END, selected_item[4])
    except IndexError:
        pass


def remove_item():
    db.remove(selected_item[0])
    clear_text()
    populate_list()


def update_item():
    db.update(selected_item[0], first_name.get(), customer_text.get(),
              retailer_text.get(), price_text.get())
    populate_list()


def clear_text():
    part_entry.delete(0, END)
    customer_entry.delete(0, END)
    retailer_entry.delete(0, END)
    price_entry.delete(0, END)


# Create window object
app = Tk()

# FirstName
first_name = StringVar()
FirstName_label = Label(app, text='First Name', font=('bold', 14), pady=20)
FirstName_label.grid(row=0, column=0, sticky=W)
FirstName_entry = Entry(app, textvariable=first_name)
FirstName_entry.grid(row=0, column=1)
# LastName
LastName_text = StringVar()
LastName_label = Label(app, text='Last name', font=('bold', 14))
LastName_label.grid(row=0, column=2, sticky=W)
LastName_entry = Entry(app, textvariable=LastName_text)
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
street_label.grid(row=3, column=0, sticky=W)
street_entry = Entry(app, textvariable=street_text)
street_entry.grid(row=3, column=1)
# Info List (Listbox)
parts_list = Listbox(app, height=8, width=50, border=0)
parts_list.grid(row=5, column=0, columnspan=3, rowspan=6, pady=20, padx=20)
# Create scrollbar
scrollbar = Scrollbar(app)
scrollbar.grid(row=5, column=3)
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
