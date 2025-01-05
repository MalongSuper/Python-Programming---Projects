# This program simulates Student Management System
import os.path
import platform
from tkinter import *
from tkinter import ttk, messagebox
import pickle
import pandas as ps
# Remember to download the module pandas if "No Module" error is received
root = Tk()

# Design the System
root.title("Student Management System")
root.geometry("2500x1500")
root['bg'] = 'light blue'


# Style the table
st = ttk.Style()
st.theme_use('clam')
# Design the Table
tv = ttk.Treeview(root)
tv['columns'] = ('SID', 'Last Name', 'First Name', 'Major', 'GPA', 'Status')
tv.grid(row=22, column=2, columnspan=8, padx=15, pady=15, sticky='nsew')
tv.column('#0', width=0, stretch=NO)  # Remove the index heading


sc = ttk.Scrollbar(root, orient="vertical", command=tv.yview)
tv.configure(yscrollcommand=sc.set)
tv.grid_columnconfigure(0, weight=1)
tv.grid_rowconfigure(0, weight=1)


sc.grid(row=22, column=9, padx=15, pady=15, sticky='ns')
root.grid_rowconfigure(6, weight=0)
root.grid_columnconfigure(6, weight=0)


for object_value in tv['columns']:
    tv.heading(object_value, text=object_value, anchor="center")  # Place the heading
    tv.column(object_value, anchor="center", width=100)  # Place the column
    if object_value == 'Last Name':
        tv.heading(object_value, text=object_value, anchor="center")  # Place the heading
        tv.column(object_value, anchor="center", width=200)  # Place the column
    if object_value == 'Status':
        tv.heading(object_value, text=object_value, anchor="center")  # Place the heading
        tv.column(object_value, anchor="center", width=120)


def is_valid():  # Define function for the valid input

    student_id = student_is.get()
    student_id_valid = student_id.isdigit() and (100000 <= int(student_id) <= 999999)  # Assume digits in Student ID

    last_name_id = last_name_is.get()
    last_name_id_valid = last_name_id.isdigit()  # Assume digits in Last Name

    first_name_id = first_name_is.get()  # Assume digits in First Name
    first_name_id_valid = first_name_id.isdigit()

    major_id = major_is.get()  # Assume digits in Major
    major_id_valid = major_id.isdigit()
    valid_major = ['IT', 'AI', 'CSC', 'RES', 'NID', 'KUN', 'TOR', 'DIG', 'IDS']

    gpa_id = gpa_is.get()  # Assume digits in GPA
    gpa_id_valid = gpa_id.replace(".", "").isdigit()

    if not student_id or not last_name_id or not first_name_id or not major_id or not gpa_id:
        result_label.config(text="Not Enough Value", fg='#f00', bg='light blue')
    else:
        if not student_id_valid:
            result_label.config(text="Student ID is Invalid", fg='#f00', bg='light blue')
            return False

        elif last_name_id_valid or first_name_id_valid:
            result_label.config(text="Last Name or First Name is Invalid", fg='#f00', bg='light blue')
            return False

        elif any(num.isnumeric() for num in last_name_is.get()) or any(num.isnumeric() for num in first_name_is.get()):
            result_label.config(text="Last Name or First Name is Invalid", fg='#f00', bg='light blue')
            return False

        elif major_id_valid:
            result_label.config(text="Major is Invalid", fg='#f00', bg='light blue')
            return False

        elif any(num.isnumeric() for num in major_is.get()):
            result_label.config(text="Major is Invalid", fg='#f00', bg='light blue')
            return False

        elif major_is.get() not in valid_major:
            result_label.config(text="Major Not Found (Major: 'IT', 'AI', "
                                     "'CSC', 'RES', 'NID', 'KUN', 'TOR', 'DIG', 'IDS')",
                                fg='#f00', bg='light blue')
            return False

        elif not gpa_id_valid or float(gpa_is.get()) > 10:
            result_label.config(text="GPA is Invalid", fg='#f00', bg='light blue')
            return False

        else:
            return True


def add_clicked():  # Define function for add button
    if is_valid() is True:
        # Check for duplicate Student ID
        new_student_id = student_is.get()
        for item in tv.get_children():
            same_student_id = tv.item(item)['values'][0]  # Put the values in the list
            if str(same_student_id) == new_student_id:
                result_label.config(text="Student ID already exists", fg='#f00', bg='light blue')
                return
        # Display the new values
        tv.insert(parent="", index="end", text="",
                  values=(student_is.get(), last_name_is.get(), first_name_is.get(), major_is.get(), gpa_is.get(),
                          u"\u2022Active"))
        # Get the add item and make it visible
        last_item_id = tv.get_children()[-1]
        tv.see(last_item_id)
        tv.selection_set(last_item_id)

        result_label.config(text="Add Successful", fg='#008000', bg='light blue')
        restart_input()
        # Update Mean after adding a student
        update_gpa_mean()


def update_clicked():  # Define function for update button
    selected_item = tv.selection()
    if not selected_item:
        result_label.config(text="Please select a row of value to update", fg='#f00', bg='light blue')
    elif is_valid() is True:
        # Check for duplicate Student ID
        new_student_id = student_is.get()
        for item in tv.get_children():
            if item != selected_item[0]:  # Exclude the item being updated
                same_student_id = tv.item(item)['values'][0]  # Put the values in the list
                if str(same_student_id) == new_student_id:
                    result_label.config(text="Student ID already exists", fg='#f00', bg='light blue')
                    return

        selected_item = selected_item[0]
        tv.item(selected_item, text="",
                values=(student_is.get(), last_name_is.get(), first_name_is.get(), major_is.get(), gpa_is.get(),
                        u"\u2022Active"), tags='')
        result_label.config(text="Update Successful", fg='#008000', bg='light blue')
        # Clear the value in order to be updated again
        tv.selection_remove(selected_item)
        restart_input()
        # Update GPA mean after updating a student
        update_gpa_mean()


def find_clicked():  # Define function for find button
    find_value = student_is.get()  # Assume Student ID is the needed value
    if not find_value:
        result_label.config(text="Please enter a Student ID to find student", fg='#f00', bg='light blue')
    else:
        find_item = []
        for item in tv.get_children():
            student_id_find = tv.item(item)['values'][0]  # Put the values in the list
            if str(student_id_find) == find_value:
                find_item.append(item)  # Put the found item in the list

        if find_item:  # Select the item when it is in the list
            tv.selection_set(find_item)
            tv.focus(find_item[0])
            tv.see(find_item[0])  # Display the find item whether its column
            student_is.delete(0, END)
        elif not (student_is.get().isdigit() and (100000 <= int(student_is.get()) <= 999999)):
            result_label.config(text="Student ID is Invalid", fg='#f00', bg='light blue')
        else:
            result_label.config(text="Student Not Found", fg='#f00', bg='light blue')


def delete_clicked():  # Define function for delete button
    selected_item = tv.selection()
    if not selected_item:
        result_label.config(text="Please select a row of value to delete", fg='#f00', bg='light blue')
    else:
        selected_item = selected_item[0]
        tv.delete(selected_item)
        result_label.config(text="Delete Successful", fg='#008000', bg='light blue')
        # Update GPA mean after deleting a student
        update_gpa_mean()


def change_clicked():  # Define function for change button
    selected_item = tv.selection()
    if not selected_item:
        result_label.config(text="Please select a row of value to change", fg='#f00', bg='light blue')
    else:
        selected_item = selected_item[0]

        # Assume the current status
        current_status = tv.item(selected_item)['values'][5]
        # Change between Active and Inactive
        if current_status == u"\u2022Active":
            new_status = u"\u2022Inactive"
        else:
            new_status = u"\u2022Active"

        # Adjust the color of the row depending on the value
        if new_status == u"\u2022Inactive":
            tags = 'grey'
            tv.item(selected_item, text="",
                    values=(tv.item(selected_item)['values'][0],
                            tv.item(selected_item)['values'][1],
                            tv.item(selected_item)['values'][2],
                            tv.item(selected_item)['values'][3],
                            tv.item(selected_item)['values'][4], new_status), tags=tags)
            result_label.config(text="Student is Inactive", fg='#008000', bg='light blue')
            tv.tag_configure('grey', background='light grey', foreground='white')
        elif new_status == u"\u2022Active":
            tags = ''
            tv.item(selected_item, text="",
                    values=(tv.item(selected_item)['values'][0],
                            tv.item(selected_item)['values'][1],
                            tv.item(selected_item)['values'][2],
                            tv.item(selected_item)['values'][3],
                            tv.item(selected_item)['values'][4], new_status), tags=tags)
            result_label.config(text="Student is Active", fg='#008000', bg='light blue')
        # Update GPA mean after changing status
        update_gpa_mean()


def update_gpa_mean():  # Calculate the mean GPA
    total_gpa = 0
    count = 0
    max_gpa = -float('inf')  # Initialize to negative infinity to ensure any GPA is greater
    min_gpa = float('inf')  # Initialize to positive infinity to ensure any GPA is smaller
    # Loop through all the rows in the Treeview and calculate the GPA mean
    for item in tv.get_children():
        gpa_value = tv.item(item)['values'][4]  # GPA is the 5th column (index 4)
        try:
            gpa_value = float(gpa_value)  # Convert GPA to float
            total_gpa += gpa_value
            count += 1
            # Update max and min GPA
            max_gpa = max(max_gpa, gpa_value)
            min_gpa = min(min_gpa, gpa_value)
        except ValueError:
            continue  # Skip invalid GPA values (if any)
    if count > 0:
        mean_gpa = total_gpa / count
        gpa_mean_label.config(text=f"Average GPA: {mean_gpa: .2f}")
        max_gpa_label.config(text=f"Max GPA: {max_gpa:.2f}")
        min_gpa_label.config(text=f"Min GPA: {min_gpa:.2f}")
    else:
        gpa_mean_label.config(text="Average GPA: N/A")
        max_gpa_label.config(text="Max GPA: N/A")
        min_gpa_label.config(text="Min GPA: N/A")
    # After updating, save the current GPA mean
    save_data()


# Add GPA Mean Label
gpa_mean_label = Label(root, text="Average GPA: N/A", bg='light blue', fg='black')
gpa_mean_label.grid(row=3, column=8, columnspan=4, padx=15, pady=15)
# Add Max GPA and Min GPA Labels
max_gpa_label = Label(root, text="Max GPA: N/A", bg='light blue', fg='black')
max_gpa_label.grid(row=3, column=6, columnspan=3, padx=15, pady=15)
min_gpa_label = Label(root, text="Min GPA: N/A", bg='light blue', fg='black')
min_gpa_label.grid(row=3, column=4, columnspan=6, padx=15, pady=15)


def restart_input():  # Define function for restarting the input
    # Restart the input after update
    student_is.delete(0, END)
    last_name_is.delete(0, END)
    first_name_is.delete(0, END)
    major_is.delete(0, END)
    gpa_is.delete(0, END)


def sort_value():  # Define function for sorting the value
    sorted_value = value_inside.get()
    if sorted_value == 'Select an option':
        return None
    else:
        # Make a list of column based on heading
        column = {'Student ID': '#1', 'Last Name': '#2',
                  'First Name': '#3', 'Major': '#4', 'GPA': '#5'}[sorted_value]
        # Use function to sort treeview by column
        if sorted_value == 'GPA':  # GPA should be sorted in ascended order
            items = [(tv.set(item, column), item) for item in tv.get_children('')]
            items.sort(reverse=True)
            for index, (value, item) in enumerate(items):
                tv.move(item, '', index)
        else:
            items = [(tv.set(item, column), item) for item in tv.get_children('')]
            items.sort(reverse=False)
            for index, (value, item) in enumerate(items):
                tv.move(item, '', index)


# Save the data in order to stay displayed after exit
def save_data():
    data = []
    for item in tv.get_children():
        values = tv.item(item)['values']
        data.append(values)  # Add the student data to the list

    # Calculate GPA mean
    total_gpa = 0
    count = 0
    max_gpa = -float('inf')  # Initialize to negative infinity to ensure any GPA is greater
    min_gpa = float('inf')
    for values in data:
        try:
            gpa_value = float(values[4])  # GPA is the 5th column (index 4)
            total_gpa += gpa_value
            count += 1
            # Update max and min GPA
            max_gpa = max(max_gpa, gpa_value)
            min_gpa = min(min_gpa, gpa_value)
        except ValueError:
            continue  # Skip invalid GPA values
    if count > 0:
        mean_gpa = total_gpa / count
    else:
        mean_gpa = None  # If no GPA values, set it as None

    # Save the data and GPA mean together in a tuple
    with open('Images/student_data.pkl', 'wb') as file:
        # Save both data and GPA stats when existing the program
        pickle.dump((data, mean_gpa, min_gpa, max_gpa), file)


def load_data():
    if os.path.exists('Images/student_data.pkl'):  # Check if the file exists
        with open('Images/student_data.pkl', 'rb') as file:  # Open the file
            try:
                # Load the data and GPA mean from the pickle file
                saved_data = pickle.load(file)

                # Check if the data is in the expected format (a tuple with two elements)
                if isinstance(saved_data, tuple) and len(saved_data) == 4:
                    data, mean_gpa, min_gpa, max_gpa = saved_data
                else:
                    # If the format is unexpected, set data to an empty list and GPA mean to None
                    data, mean_gpa, min_gpa, max_gpa = [], None, None, None
            except EOFError:
                # If file is empty, initialize empty data and None for GPA mean
                data, mean_gpa, min_gpa, max_gpa = [], None, None, None

        # Load the student data into the Treeview
        for values in data:
            tags = ''
            if u"\u2022Inactive" in values:
                tags = 'grey'  # Retain the grey color for inactive students
            tv.insert(parent="", index="end", text="", values=values, tags=tags)

        tv.tag_configure('grey', background='light grey', foreground='white')

        # Update the GPA mean label
        if mean_gpa is not None:
            gpa_mean_label.config(text=f"Average GPA: {mean_gpa: .2f}")
        else:
            gpa_mean_label.config(text="Average GPA: N/A")
        # Update the GPA Max label
        if max_gpa is not None:
            max_gpa_label.config(text=f"Max GPA: {max_gpa:.2f}")
        else:
            max_gpa_label.config(text="Max GPA: N/A")
        # Update the GPA Min label
        if min_gpa is not None:
            min_gpa_label.config(text=f"Min GPA: {min_gpa:.2f}")
        else:
            min_gpa_label.config(text="Min GPA: N/A")


# Call the function when the program starts
load_data()


def save_to_excel():  # Function to save the data to an Excel file
    # Remember to download openpyxl before importing to Excel
    result = (tv.item(item)['values'] for item in tv.get_children())
    columns = ['SID', 'Last Name', 'First Name', 'Major', 'GPA', 'Status']
    data = ps.DataFrame(result, columns=columns)
    # Convert GPA column to numeric to preserve the number format in Excel
    data['GPA'] = ps.to_numeric(data['GPA'], errors='coerce')  # This will convert valid GPA values to numbers
    data.to_excel("Images/student_management_system.xlsx", index=False)
    messagebox.showinfo("Notification", message="Successfully Imported data to Excel")


# Display the system for input
student = (Label(root, text="Student ID:", bg='light blue', fg='black'))
student.grid(row=1, column=1, columnspan=1, padx=10, pady=10)
student_is = (Entry(root, bg='white', fg='black', highlightbackground='light blue'))
student_is.grid(row=1, column=2, columnspan=1, padx=10, pady=10)


last_name = (Label(text="Last Name:", bg='light blue', fg='black'))
last_name.grid(row=2, column=1, columnspan=1, padx=10, pady=10)
last_name_is = (Entry(root, bg='white', fg='black', highlightbackground='light blue'))
last_name_is.grid(row=2, column=2, columnspan=1, padx=10, pady=10)


first_name = (Label(text="First Name:", bg='light blue', fg='black'))
first_name.grid(row=2, column=3, padx=10, pady=10)
first_name_is = (Entry(root, bg='white', fg='black', highlightbackground='light blue'))
first_name_is.grid(row=2, column=4, padx=10, pady=10)


major = (Label(text="Major:", bg='light blue', fg='black'))
major.grid(row=2, column=5, columnspan=1, padx=10, pady=10)
major_is = (Entry(root, bg='white', fg='black', highlightbackground='light blue'))
major_is.grid(row=2, column=6, columnspan=1, padx=10, pady=10)


gpa = (Label(text="GPA:", bg='light blue', fg='black'))
gpa.grid(row=2, column=7, columnspan=1, padx=10, pady=10)
gpa_is = Entry(root, bg='white', fg='black', highlightbackground='light blue')
gpa_is.grid(row=2, column=8, columnspan=1, padx=10, pady=10)


sort_by = (Label(text="Sort By:", bg='light blue', fg='black'))
sort_by.grid(row=1, column=4, columnspan=1, padx=10, pady=10)

# Make value for sort_by
option_list = ["Student ID", "Last Name", "First Name", "Major", "GPA"]
value_inside = StringVar(root)
value_inside.set("Select an option")  # Initial value
option_is = (OptionMenu(root, value_inside, *option_list, command=lambda _: sort_value()))
option_is.grid(row=1, column=5, columnspan=1, padx=10, pady=10)
option_is.config(background='light blue', foreground='black')

# Display buttons
find = (Button(root, text="Find", width=4, highlightbackground='light blue', command=find_clicked))
find.grid(row=1, column=3, columnspan=1, padx=10, pady=10)

add = (Button(root, text="Add", width=4, command=add_clicked, highlightbackground='light blue'))
add.grid(row=3, column=2, columnspan=1, padx=10, pady=10)

update = (Button(root, text="Update", width=4, command=update_clicked, highlightbackground='light blue'))
update.grid(row=3, column=3, columnspan=1, padx=10, pady=10)

delete = (Button(root, text="Delete", width=4, command=delete_clicked, highlightbackground='light blue'))
delete.grid(row=3, column=4, columnspan=1, padx=10, pady=10)

hide = (Button(root, text="Change", width=4, command=change_clicked, highlightbackground='light blue'))
hide.grid(row=3, column=5, columnspan=1, padx=10, pady=10)


import_file = (Button(root, text="Import Data to Excel", command=save_to_excel, width=30,
                      highlightbackground='light blue'))
import_file.grid(row=23, column=3, columnspan=5, padx=10, pady=10)


# For each platform supports different types of Open File
if platform.system() == "Darwin":  # MacOS users
    open_file = Button(root, text="Open Excel File",
                       command=lambda: os.system(f"open {"Images/student_management_system.xlsx"}"),
                       highlightbackground='light blue')
    open_file.grid(row=24, column=3, columnspan=5, padx=15, pady=15)
elif platform.system() == "Windows":  # Windows users
    open_file = Button(root, text="Open Excel File",
                       command=lambda: os.system(f"start excel {"Images/student_management_system.xlsx"}"),
                       highlightbackground='light blue')
    open_file.grid(row=24, column=4, columnspan=2, padx=15, pady=15)
elif platform.system() == "Linux":  # Linux users
    open_file = Button(root, text="Open Excel File",
                       command=lambda: os.system(f"xdg-open {"Images/student_management_system.xlsx"}"),
                       highlightbackground='light blue')
    open_file.grid(row=24, column=4, columnspan=2, padx=15, pady=15)


notice_line = (Label(root, text='\tNotes: Student ID (SID) is distinct for all students '
                                'and cannot be duplicated\t',
                     bg='yellow', fg='red'))
notice_line.grid(row=30, column=3, columnspan=5, padx=15, pady=15)

# Make a result label for invalid input
result_label = Label(root, text="")
result_label['bg'] = 'light blue'
result_label.grid(row=7, column=2, columnspan=3)


def on_exit():  # Function to handle exit the system
    save_data()
    root.destroy()


# Exit event
root.protocol("WM_DELETE_WINDOW", on_exit)

root.mainloop()
