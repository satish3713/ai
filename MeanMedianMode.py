import tkinter as tk
from tkinter import messagebox
from owlready2 import *
import statistics

# Load the ontology
onto = get_ontology(r"Desktop/Artifical/ITS_MeanMedianMode.owl").load()

# Function to calculate mean
def calculate_mean(data):
    return statistics.mean(data)

# Function to calculate median
def calculate_median(data):
    return statistics.median(data)

# Function to calculate mode
def calculate_mode(data):
    try:
        return statistics.mode(data)
    except statistics.StatisticsError:
        return "N/A"

# Function to add new individuals to the ontology dynamically
def add_to_ontology(dataset, mean=None, median=None, mode=None):
    data_ind = onto.DataSet("DynamicDataSet")
    calc_ind = onto.Calculation("DynamicCalculation")
    data_ind.hasCalculation = [calc_ind]
    if mean is not None:
        calc_ind.calculatesMean = [onto.Mean(f"Mean_{mean}")]
    if median is not None:
        calc_ind.calculatesMedian = [onto.Median(f"Median_{median}")]
    if mode is not None:
        calc_ind.calculatesMode = [onto.Mode(f"Mode_{mode}")]
    onto.save(file="Updated_ITS_MeanMedianMode.owl", format="rdfxml")

# Function to handle Mean calculation
def handle_mean():
    try:
        dataset = gather_dataset()
        mean = calculate_mean(dataset)
        add_to_ontology(dataset, mean=mean)
        result_label.config(text=f"The Mean value is: {mean:.2f}", fg="black")
        reset_entry_backgrounds()
    except ValueError as ve:
        handle_input_error(ve)

# Function to handle Median calculation
def handle_median():
    try:
        dataset = gather_dataset()
        median = calculate_median(dataset)
        add_to_ontology(dataset, median=median)
        result_label.config(text=f"The Median value is: {median:.2f}", fg="black")
        reset_entry_backgrounds()
    except ValueError as ve:
        handle_input_error(ve)

# Function to handle Mode calculation
def handle_mode():
    try:
        dataset = gather_dataset()
        mode = calculate_mode(dataset)
        add_to_ontology(dataset, mode=mode)
        result_label.config(text=f"The Mode value is: {mode}", fg="black")
        reset_entry_backgrounds()
    except ValueError as ve:
        handle_input_error(ve)

# Helper function to gather dataset from all text boxes
def gather_dataset():
    dataset = []
    for entry in entries:
        value = entry.get().strip()
        if not value:
            raise ValueError("All fields must have a value.")
        dataset.append(float(value))  # Convert to float
    return dataset

# Helper function to handle input errors
def handle_input_error(ve):
    messagebox.showerror("Input Error", str(ve))
    for entry in entries:
        entry.config(bg="#f8d7da")  # Highlight fields on error

# Helper function to reset entry backgrounds
def reset_entry_backgrounds():
    for entry in entries:
        entry.config(bg="#ffffff")  # Reset entry field background

# Function to clear the entry fields and result label
def handle_clear():
    for entry in entries:
        entry.delete(0, tk.END)
        entry.config(bg="#ffffff")  # Reset entry field background
    result_label.config(text="")

# Create the main window
root = tk.Tk()
root.title("Intelligent Tutoring System")
root.geometry("500x550")
root.configure(bg="#f0f8ff")  # Light blue background

# Create and place widgets
title_label = tk.Label(root, text="ITS System in Mean Median Mode", font=("Arial", 20, "bold"), bg="#f0f8ff", fg="#1e3d58")
title_label.pack(pady=20)

instruction_label = tk.Label(root, text="Enter your Values:", font=("Arial", 12), bg="#f0f8ff", fg="#1e3d58")
instruction_label.pack(pady=5)

entry_frame = tk.Frame(root, bg="#f0f8ff")
entry_frame.pack(pady=10)

# Create five entry boxes dynamically
entries = []
for i in range(5):  # Create 5 input text boxes
    entry = tk.Entry(entry_frame, width=20, font=("Arial", 12), justify="center", bd=2, relief="solid", fg="blue", bg="#ffffff")
    entry.pack(pady=5)
    entries.append(entry)

button_frame = tk.Frame(root, bg="#f0f8ff")
button_frame.pack(pady=20)

# Create buttons for Mean, Median, and Mode
mean_button = tk.Button(
    button_frame, 
    text="Calculate Mean", 
    command=handle_mean, 
    font=("Arial", 12, "bold"), 
    bg="#4CAF50",  # Green button
    fg="black", 
    relief="raised", 
    bd=3
)
mean_button.pack(side=tk.LEFT, padx=10)

median_button = tk.Button(
    button_frame, 
    text="Calculate Median", 
    command=handle_median, 
    font=("Arial", 12, "bold"), 
    bg="#2196F3",  # Blue button
    fg="black", 
    relief="raised", 
    bd=3
)
median_button.pack(side=tk.LEFT, padx=10)

mode_button = tk.Button(
    button_frame, 
    text="Calculate Mode", 
    command=handle_mode, 
    font=("Arial", 12, "bold"), 
    bg="#FF5722",  # Orange button
    fg="black", 
    relief="raised", 
    bd=3
)
mode_button.pack(side=tk.LEFT, padx=10)

# Create Clear Button
clear_button = tk.Button(
    root, 
    text="Clear All", 
    command=handle_clear, 
    font=("Arial", 14, "bold"), 
    bg="#f44336",  # Red button
    fg="black", 
    relief="raised", 
    bd=3
)
clear_button.pack(pady=10)

result_frame = tk.Frame(root, bg="#f0f8ff")
result_frame.pack(pady=10)
result_label = tk.Label(result_frame, text="", font=("Arial", 14), bg="#f0f8ff", fg="#1e3d58")
result_label.pack(padx=10, pady=5)

# Run the application
root.mainloop()
