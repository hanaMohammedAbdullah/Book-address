from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
from db import Database
# importing csv and os module
import csv
import os

db = Database('addressbook.db')


def populate_list():
    trv.delete(*trv.get_children())
    for row in db.fetch():
        trv.insert('' , 'end', values=row )


def add_item():
    if first_name.get() == '' or lastName_text.get() == '' or phone_text.get() == '' or email_text.get() == '':
        messagebox.showerror('Required Fields', 'Please include all fields (fist name, last name, phone number, email)')
        return
    db.insert(first_name.get(), lastName_text.get(),
              state_text.get(), city_text.get(), address_text.get(), email_text.get(), phone_text.get(), street_text.get())
    trv.delete(*trv.get_children())
    trv.insert('', 'end', values=(first_name.get(), lastName_text.get(), state_text.get(), city_text.get(), address_text.get(), email_text.get(), phone_text.get(), street_text.get()))
    clear_text()
    populate_list()


def select_item(event):
    try:
        global selected_item
        index = trv.identify_row(event.y)
        selected_item = trv.item(trv.focus())



        first_name.set(selected_item['values'][1])
        LastName_entry.set(END, selected_item['values'][2])
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
    if trv.size() == 0:
        messagebox.showerror('Export Data', 'there is no data to export')
        return
    fln = filedialog.asksaveasfilename(initialdir=os.getcwd(),initialfile='Address.csv', defaultextension=".csv", filetypes=[("CSV file", "*.csv")])
    with open(fln, mode='w') as f:
        writer = csv.writer(f ,delimiter=',')
        writer.writerow(['ID', 'First Name', 'Last Name', 'State', 'City', 'Address', 'Email', 'Phone', 'Street'])
        for i in range(trv.size()):
            writer.writerow(trv.get(i))
        messagebox.showinfo('Data Exported', 'Your data has been exported to ' + os.path.basename(fln) + ' successfully')
def search():
    trv.delete(*trv.get_children())
    for row in db.search(Search_text.get()):
        trv.insert('' , 'end', values=row )

def import_data():
    fln = filedialog.askopenfilename(initialdir=os.getcwd(), title='Open CSV', filetypes=[("CSV file", "*.csv")])
    with open(fln) as f:
        reader = csv.reader(f)
        # skip the first row
        next(reader)
        for row in reader:
            db.insert(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
            trv.insert(END, row)
        messagebox.showinfo('Data Imported', 'Your data has been imported successfully')       
# Create window object
app = Tk()






# # Info List (Listbox)
# parts_list = Listbox(app, height=8, width=80, border=0)
# parts_list.grid(row=7, column=0, columnspan=3, rowspan=6, pady=20, padx=20)
# # Create scrollbar
# scrollbar = Scrollbar(app)
# scrollbar.grid(row=7, column=3)
# # Set scroll to listbox
# parts_list.configure(yscrollcommand=scrollbar.set)
# scrollbar.configure(command=parts_list.yview)
# 



#

# # Start program
# app.mainloop()


# # To create an executable, install pyinstaller and run
# # '''
# # pyinstaller --onefile --add-binary='/System/Library/Frameworks/Tk.framework/Tk':'tk' --add-binary='/System/Library/Frameworks/Tcl.framework/Tcl':'tcl' part_manager.py
# # '''
#  another way of displaying   2222222222

# adding frame 

app.title('Address Book')
app.geometry('1400x750')


wrapperData = LabelFrame(app, text="Address Book data" ,bg="white")
wrapperAction = LabelFrame(app, text="Address Book Action" , bg="white")
wrapperDatatable = LabelFrame(app, text="Address Book List", bg="white")



wrapperData.pack(fill="both", expand="yes", padx=20, pady=10 )
wrapperAction.pack(fill="both", expand="yes", padx=20, pady=10)
wrapperDatatable.pack(fill="both", expand="yes", padx=20, pady=10)


s=ttk.Style()
s.theme_use('clam')

# Add the rowheight
s.configure('Treeview', rowheight=40 , font=('Arial', 10) , rowWeight=1)


trv = ttk.Treeview(wrapperDatatable, columns=(1, 2, 3, 4, 5, 6, 7, 8, 9), show="headings" )    
trv.pack()
trv.column(1, stretch=NO, width=250)
trv.heading(1, text="ID")
trv.column(2, stretch=NO, width=250)
trv.heading(2, text="First Name")
trv.column(3, stretch=NO, width=250)
trv.heading(3, text="Last Name")
trv.column(4, stretch=NO, width=250)
trv.heading(4, text="State")
trv.column(5, stretch=NO, width=250)
trv.heading(5, text="City")
trv.column(6, stretch=NO, width=250)
trv.heading(6, text="Address" )
trv.column(7, stretch=NO, width=250)
trv.heading(7, text="Email")
trv.column(8, stretch=NO, width=250)
trv.heading(8, text="Phone")
trv.column(9, stretch=NO, width=250)
trv.heading(9, text="Job ")
 # Populate data
populate_list()

# # Buttons
add_btn = Button(wrapperAction, text='Add New', width=12, command=add_item)
add_btn.grid(row=4, column=0, padx=10 )

remove_btn = Button(wrapperAction, text='Remove ', width=12, command=remove_item)
remove_btn.grid(row=4, column=1 , padx=10)

update_btn = Button(wrapperAction, text='Update ', width=12, command=update_item)
update_btn.grid(row=4, column=2 , padx=10)

clear_btn = Button(wrapperAction, text='Clear Input', width=12, command=clear_text)
clear_btn.grid(row=4, column=3 , padx=10)

export_btn = Button(wrapperAction, text='Export', width=12, command=export_data)
export_btn.grid(row=4, column=4 , padx=10)

inport_btn = Button(wrapperAction, text='Import', width=12, command=import_data)
inport_btn.grid(row=4, column=5 , padx=10)

# app.title('Address Book')
# app.geometry('1400x750')

# # # Search
Search_text = StringVar()
Search_Label = Button(wrapperAction, text='Search', font=('bold', 10), command=search)
Search_Label.grid(row=5, column=1, sticky=W , padx=10 , pady=10)
Search_entry = Entry(wrapperAction, textvariable=Search_text  )
Search_entry.grid(row=5, column=0 , padx=10 , pady=10)




# # FirstName
first_name = StringVar()
FirstName_label = Label(wrapperData, text='First Name :', font=('bold', 10),  bg="white")
FirstName_label.grid(row=0, column=0 , sticky=W , padx=10 , pady=10)
FirstName_entry = Entry(wrapperData, textvariable=first_name)
FirstName_entry.grid(row=0, column=1)
# LastName
lastName_text = StringVar()
LastName_label = Label(wrapperData, text='Last Name :', font=('bold', 10) , bg="white")
LastName_label.grid(row=0, column=2, sticky=W , padx=10 , pady=10)
LastName_entry = Entry(wrapperData, textvariable=lastName_text)
LastName_entry.grid(row=0, column=3)
# state
state_text = StringVar()
state_label = Label(wrapperData, text='State :', font=('bold', 10) , bg="white")
state_label.grid(row=1, column=0, sticky=W , padx=10 , pady=10)
state_entry = Entry(wrapperData, textvariable=state_text)
state_entry.grid(row=1, column=1)
# city
city_text = StringVar()
city_label = Label(wrapperData, text='City :', font=('bold', 10) , bg="white")
city_label.grid(row=1, column=2, sticky=W , padx=10 , pady=10)
city_entry = Entry(wrapperData, textvariable=city_text)
city_entry.grid(row=1, column=3)

# address
address_text = StringVar()
address_label = Label(wrapperData, text='Address :', font=('bold', 10) , bg="white")
address_label.grid(row=2, column=0, sticky=W , padx=10 , pady=10)
address_entry = Entry(wrapperData, textvariable=address_text)
address_entry.grid(row=2, column=1)
# email
email_text = StringVar()
email_label = Label(wrapperData, text='Email :', font=('bold', 10) , bg="white")
email_label.grid(row=2, column=2, sticky=W , padx=10 , pady=10)
email_entry = Entry(wrapperData, textvariable=email_text)
email_entry.grid(row=2, column=3)
# phone
phone_text = StringVar()
phone_label = Label(wrapperData, text='Phone Number :', font=('bold', 10) , bg="white")
phone_label.grid(row=3, column=0, sticky=W , padx=10 , pady=10)
phone_entry = Entry(wrapperData, textvariable=phone_text)
phone_entry.grid(row=3, column=1)
# street
street_text = StringVar()
street_label = Label(wrapperData, text='Job :', font=('bold', 10) , bg="white")
street_label.grid(row=3, column=2, sticky=W , padx=10 , pady=10)
street_entry = Entry(wrapperData, textvariable=street_text)
street_entry.grid(row=3, column=3)


# Bind select
trv.bind('<<ListboxSelect>>', select_item)

app.mainloop()



# # tree view

