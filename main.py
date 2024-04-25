import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
from config import load_config

file_path = '' # Global variable to store the file path
age_groups = {'0-4 y. o.': {'min': 0, 'max': 4}} # Global variable to store age groups
config = load_config()

def select_file():
    global file_path
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    if file_path:
        selected_file_label.config(text=f"Selected File: {file_path}")
        disaggregate_button.config(state="normal")

def process_data(df, age_row, gender_row, dis_row, age_groups, male_data, female_data, disabilities_data):
    for index, row in df.iterrows():
        if row[age_row] == '---':
            continue
        age = int(row[age_row])
        gender = row[gender_row]
        dis = row[dis_row]

        for group, age_range in age_groups.items():
            if age_range['min'] <= age <= age_range['max']:
                if gender == 'male':
                    male_data[group] += 1
                elif gender == 'female':
                    female_data[group] += 1
                if dis == 'yes':
                    disabilities_data += 1        

def disaggregate_data():
    forms_df = pd.read_excel(file_path, sheet_name='Forms')
    adult_df = pd.read_excel(file_path, sheet_name='Repeat- hh_adult').dropna(subset=['number__0'])
    child_df = pd.read_excel(file_path, sheet_name='Repeat- hh_childs').dropna(subset=['number__0'])

    male_data = {group: 0 for group in age_groups}
    female_data = {group: 0 for group in age_groups}
    disabilities_data = 0
    low_income_data = 0
    idp_hh = 0
    idp_data = 0
    idp_count = 0
    hh_more_than_3_data = 0
    hh_children_under_5 = 0
    households_60_plus = 0

    process_data(adult_df, config['age_adult_row'], config['gender_adult_row'], config['dis_adult_row'],
                 age_groups, male_data, female_data, disabilities_data)
    process_data(child_df, config['age_child_row'], config['gender_child_row'], config['dis_child_row'],
                 age_groups, male_data, female_data, disabilities_data)

    for index, row in forms_df.iterrows():
        if row[config['age_app_row']] == '---':
            continue
        age = int(row[config['age_app_row']])
        gender = row[config['gender_app_row']]
        number = row[config['form_app_number']]
        hh_size = row[config['hh_size_app_row']]
        low_income = row[config['low_app_income']]
        hh_idp = row[config['hh_idp_app_row']]
        idp = row[config['idp_app_row']]
        child_count = row[config['child_count_app_row']]
        dis = row[config['dis_app_row']]

        for group, age_range in age_groups.items():
            if age_range['min'] <= age <= age_range['max']:
                if gender == 'male':
                    male_data[group] += 1
                elif gender == 'female':
                    female_data[group] += 1
                if low_income == 'yes':
                    low_income_data += 1
                if hh_idp == 'yes':
                    idp_data += 1
                if dis == 'yes':
                    disabilities_data += 1
                if child_count != '---':
                    if int(child_count) >= 3:
                        hh_more_than_3_data += 1
                if idp == "yes":
                    idp_hh += 1
                    idp_count += int(hh_size)

        if age >= 60 or any(row[config['age_adult_row']] != '---' and int(row[config['age_adult_row']]) >= 60
                            for index, row in adult_df[adult_df[config['form_app_number']] == number].iterrows()):
            households_60_plus += 1

        if age <= 5 or any(row[config['age_child_row']] != '---' and int(row[config['age_child_row']]) <= 5
                        for index, row in child_df[child_df[config['form_app_number']] == number].iterrows()):
            hh_children_under_5 += 1

    overall_data = {group: male_data[group] + female_data[group] for group in age_groups}

    results_text.delete('1.0', tk.END)
    results_text.insert(tk.END, "Male Data:\n")
    results_text.insert(tk.END, str(male_data) + "\n")
    results_text.insert(tk.END, "Female Data:\n")
    results_text.insert(tk.END, str(female_data) + "\n")
    results_text.insert(tk.END, "\nOverall number of people: " + str(sum(overall_data.values())) + "\n")
    results_text.insert(tk.END, "Disabilities Data: " + str(disabilities_data) + "\n")
    results_text.insert(tk.END, "Low Income: " + str(low_income_data) + "\n")
    results_text.insert(tk.END, "IDP HH: " + str(idp_hh) + "\n")
    results_text.insert(tk.END, "HH hosting IDP: " + str(idp_data) + "\n")
    results_text.insert(tk.END, "IDP's: " + str(idp_count) + "\n")
    results_text.insert(tk.END, "HH with more than 3 child: " + str(hh_more_than_3_data) + "\n")
    results_text.insert(tk.END, "HH with children under 5: " + str(hh_children_under_5) + "\n")
    results_text.insert(tk.END, "HH 60+: " + str(households_60_plus) + "\n")

def try_disaggregate_data():
    try:
        disaggregate_data()
    except KeyError as e:
        messagebox.showerror("Key Error", f"A key error occurred: {str(e)}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")  

def add_age_group():
    dialog = tk.Toplevel(root)
    dialog.title("Add Age Group")
    #dialog.geometry("300x200")
    window_width = 300
    window_height = 150
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    dialog.geometry(f"{window_width}x{window_height}+{x}+{y}")

    dialog.grab_set()

    min_age_label = ttk.Label(dialog, text="Minimum Age:")
    min_age_label.grid(row=0, column=0, padx=10, pady=5)
    min_age_var = tk.StringVar()
    min_age_dropdown = ttk.Combobox(dialog, textvariable=min_age_var, values=list(range(0, 61)), state="readonly")
    min_age_dropdown.grid(row=0, column=1, padx=10, pady=5)
    min_age_dropdown.current(0)

    max_age_label = ttk.Label(dialog, text="Maximum Age:")
    max_age_label.grid(row=1, column=0, padx=10, pady=5)
    max_age_var = tk.StringVar()
    max_age_options = [str(age) for age in range(0, 61)] + ["Inf"]
    max_age_var.set(max_age_options[0])  # Default value
    max_age_dropdown = ttk.Combobox(dialog, textvariable=max_age_var, values=max_age_options, state="readonly")
    max_age_dropdown.grid(row=1, column=1, padx=10, pady=5)
    max_age_dropdown.current(0)

    def save_age_group():
        try:
            min_age = int(min_age_var.get())
            max_age_option = max_age_var.get()
            if max_age_option == "Inf":
                max_age = float('inf')
            else:
                max_age = int(max_age_option)
            age_group_name = f"{min_age}-{max_age_option} y. o."
            age_groups[age_group_name] = {'min': min_age, 'max': max_age}
            #messagebox.showinfo("Success", f"Age group '{age_group_name}' added successfully!")
            refresh_age_groups()
            dialog.destroy()
        except ValueError:
            messagebox.showerror("Error", "Invalid input! Please enter valid age values.")

    save_button = ttk.Button(dialog, text="Save", command=save_age_group)
    save_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="we")

def modify_age_group(event):
    selected_index = age_group_listbox.curselection()
    if selected_index:
        selected_age_group = age_group_listbox.get(selected_index[0])
        min_age = age_groups[selected_age_group]['min']
        max_age = age_groups[selected_age_group]['max']

        dialog = tk.Toplevel(root)
        dialog.title("Modify Age Group")
        #dialog.geometry("300x200")
        window_width = 300
        window_height = 150
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        dialog.geometry(f"{window_width}x{window_height}+{x}+{y}")

        dialog.grab_set()

        min_age_label = ttk.Label(dialog, text="Minimum Age:")
        min_age_label.grid(row=0, column=0, padx=10, pady=5)
        min_age_var = tk.StringVar()
        min_age_dropdown = ttk.Combobox(dialog, textvariable=min_age_var, values=list(range(0, 61)), state="readonly")
        min_age_dropdown.grid(row=0, column=1, padx=10, pady=5)
        min_age_dropdown.current(0)

        max_age_label = ttk.Label(dialog, text="Maximum Age:")
        max_age_label.grid(row=1, column=0, padx=10, pady=5)
        max_age_var = tk.StringVar()
        max_age_options = [str(age) for age in range(0, 61)] + ["Inf"]
        max_age_var.set(max_age_options[0])  # Default value
        max_age_dropdown = ttk.Combobox(dialog, textvariable=max_age_var, values=max_age_options, state="readonly")
        max_age_dropdown.grid(row=1, column=1, padx=10, pady=5)
        max_age_dropdown.current(0)

        def save_modified_age_group():
            try:
                min_age = int(min_age_var.get())
                max_age_option = max_age_var.get()
                if max_age_option == "Inf":
                    max_age = float('inf')
                else:
                    max_age = int(max_age_option)
                age_group_name = f"{min_age}-{max_age_option} y. o."

                # Delete the old age group if it exists
                if selected_age_group in age_groups:
                    del age_groups[selected_age_group]

                age_groups[age_group_name] = {'min': min_age, 'max': max_age}
                #messagebox.showinfo("Success", f"Age group '{age_group_name}' added successfully!")
                refresh_age_groups()
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Error", "Invalid input! Please enter valid age values.")

        save_button = ttk.Button(dialog, text="Save", command=save_modified_age_group)
        save_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="we")

def refresh_age_groups():
    age_group_listbox.delete(0, tk.END)
    for age_group in age_groups:
        age_group_listbox.insert(tk.END, age_group)

root = tk.Tk()
root.title("Dis PY 0.1")

window_width = 800
window_height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

root.iconbitmap(default='')

script_dir = os.path.dirname(os.path.abspath(__file__))
azure_tcl_path = os.path.join(script_dir, "azure.tcl")

root.tk.call("source", azure_tcl_path)
root.tk.call("set_theme", "dark")

file_frame = ttk.Frame(root)
file_frame.pack(pady=20)
select_button = ttk.Button(file_frame, text="Select Excel File", command=select_file)
select_button.pack()
selected_file_label = ttk.Label(file_frame, text="Selected File: None")
selected_file_label.pack()

disaggregate_button = ttk.Button(root, text="Disaggregate", command=try_disaggregate_data, state="disabled")
disaggregate_button.pack(pady=10)

age_group_frame = ttk.Frame(root)
age_group_frame.pack(pady=20)
age_group_label = ttk.Label(age_group_frame, text="Age Groups:")
age_group_label.grid(row=0, column=0, padx=5)
add_age_group_button = ttk.Button(age_group_frame, text="Add Age Group", command=add_age_group)
add_age_group_button.grid(row=0, column=1, padx=5)
age_group_listbox = tk.Listbox(age_group_frame)
age_group_listbox.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
age_group_listbox.bind("<Double-Button-1>", modify_age_group)  # Bind double-click event
refresh_age_groups()

results_frame = ttk.Frame(root)
results_frame.pack(pady=20)
results_label = ttk.Label(results_frame, text="Disaggregated Results:")
results_label.pack()
results_text = tk.Text(results_frame, height=20, width=100)
results_text.pack()

root.mainloop()