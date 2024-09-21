import tkinter as tk
from tkinter import messagebox
import sqlite3
import matplotlib.pyplot as plt
import datetime

# Initialize SQLite Database
def init_db():
    conn = sqlite3.connect('bmi_data.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS bmi_records
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                     user_name TEXT,
                     weight REAL, 
                     height REAL, 
                     bmi REAL, 
                     category TEXT, 
                     date TEXT)''')
    conn.commit()
    conn.close()

# Calculate BMI and store data
def calculate_bmi():
    try:
        weight = float(weight_entry.get())
        height = float(height_entry.get())
        name = name_entry.get()
        
        if not name:
            messagebox.showerror("Error", "Please enter a name")
            return
        
        if height <= 0 or weight <= 0:
            messagebox.showerror("Error", "Please enter valid height and weight")
            return
        
        bmi = weight / (height ** 2)
        category = classify_bmi(bmi)
        
        result_label.config(text=f"BMI: {bmi:.2f} - {category}")
        save_to_db(name, weight, height, bmi, category)
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers for weight and height")

# Classify BMI based on WHO categories
def classify_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obese"

# Save the BMI record to the database
def save_to_db(name, weight, height, bmi, category):
    conn = sqlite3.connect('bmi_data.db')
    cursor = conn.cursor()
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''INSERT INTO bmi_records (user_name, weight, height, bmi, category, date)
                      VALUES (?, ?, ?, ?, ?, ?)''', (name, weight, height, bmi, category, date))
    conn.commit()
    conn.close()

# View historical BMI data for a specific user
def view_history():
    name = name_entry.get()
    if not name:
        messagebox.showerror("Error", "Please enter a name")
        return
    
    conn = sqlite3.connect('bmi_data.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM bmi_records WHERE user_name = ? ORDER BY date DESC''', (name,))
    records = cursor.fetchall()
    conn.close()
    
    if records:
        history_window = tk.Toplevel(root)
        history_window.title("BMI History")
        
        for i, record in enumerate(records):
            record_text = f"{i+1}. Date: {record[6]}, Weight: {record[2]}kg, Height: {record[3]}m, BMI: {record[4]:.2f}, Category: {record[5]}"
            label = tk.Label(history_window, text=record_text)
            label.pack()
    else:
        messagebox.showinfo("No Records", "No BMI records found for this user")

# Visualize BMI trends
def view_trends():
    name = name_entry.get()
    if not name:
        messagebox.showerror("Error", "Please enter a name")
        return
    
    conn = sqlite3.connect('bmi_data.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT date, bmi FROM bmi_records WHERE user_name = ? ORDER BY date''', (name,))
    records = cursor.fetchall()
    conn.close()
    
    if records:
        dates = [record[0] for record in records]
        bmis = [record[1] for record in records]
        
        plt.plot(dates, bmis, marker='o', linestyle='-', color='b')
        plt.xlabel('Date')
        plt.ylabel('BMI')
        plt.title(f"BMI Trend for {name}")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()
    else:
        messagebox.showinfo("No Records", "No BMI records found for this user")

# Setup the GUI
root = tk.Tk()
root.title("Advanced BMI Calculator")

tk.Label(root, text="Name:").grid(row=0, column=0, padx=10, pady=10)
name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Weight (kg):").grid(row=1, column=0, padx=10, pady=10)
weight_entry = tk.Entry(root)
weight_entry.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="Height (m):").grid(row=2, column=0, padx=10, pady=10)
height_entry = tk.Entry(root)
height_entry.grid(row=2, column=1, padx=10, pady=10)

calculate_button = tk.Button(root, text="Calculate BMI", command=calculate_bmi)
calculate_button.grid(row=3, column=0, columnspan=2, pady=10)

result_label = tk.Label(root, text="BMI: -")
result_label.grid(row=4, column=0, columnspan=2, pady=10)

history_button = tk.Button(root, text="View History", command=view_history)
history_button.grid(row=5, column=0, pady=10)

trends_button = tk.Button(root, text="View Trends", command=view_trends)
trends_button.grid(row=5, column=1, pady=10)

init_db()  # Initialize database
root.mainloop()
