import requests
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Replace with your actual API key
API_KEY = '48793d9fd9e19f3bb29a29a59e7bce95'

# JotForm API base URL for EU accounts
BASE_URL = 'https://eu-api.jotform.com'

# Function to retrieve all available forms
def get_forms(api_key):
    url = f"{BASE_URL}/user/forms"
    params = {
        'apiKey': api_key
    }
    response = requests.get(url, params=params)
    
    try:
        response.raise_for_status()
        data = response.json()

        if 'content' in data:
            forms = data['content']
            return forms
        else:
            print(f"Unexpected response structure: {data}")
            return []
    
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")
    
    return []

# Function to retrieve the number of submissions for a form
def get_submission_count(form_id, api_key):
    url = f"{BASE_URL}/form/{form_id}/submissions"
    params = {
        'apiKey': api_key,
        'limit': 0  # Assuming the API returns the total count without fetching submissions
    }
    response = requests.get(url, params=params)
    
    try:
        response.raise_for_status()
        data = response.json()

        if 'total' in data:
            return data['total']
        elif 'content' in data:
            return len(data['content'])
        else:
            print(f"Unexpected response structure when fetching submissions: {data}")
            return 0
    
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred while fetching submissions for form {form_id}: {http_err}")
    except Exception as err:
        print(f"An error occurred while fetching submissions for form {form_id}: {err}")
    
    return 0

# Function to retrieve all submissions for the form
def get_submissions(form_id, api_key):
    url = f"{BASE_URL}/form/{form_id}/submissions"
    params = {
        'apiKey': api_key
    }
    response = requests.get(url, params=params)
    
    try:
        response.raise_for_status()
        data = response.json()

        if 'content' in data:
            submissions = data['content']
            return submissions
        else:
            print(f"Unexpected response structure: {data}")
            return []
    
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")
    
    return []

# Function to delete a submission
def delete_submission(submission_id, api_key):
    url = f"{BASE_URL}/submission/{submission_id}"
    params = {
        'apiKey': api_key
    }
    response = requests.delete(url, params=params)
    if response.status_code == 200:
        log_message(f"Submission {submission_id} deleted successfully.")
    else:
        log_message(f"Failed to delete submission {submission_id}. Error: {response.status_code}")

# Main function to delete all submissions for the form
def delete_all_submissions(form_id, api_key):
    submissions = get_submissions(form_id, api_key)
    if not submissions:
        log_message(f"No submissions found for form {form_id} or error fetching submissions.")
        return
    
    for submission in submissions:
        submission_id = submission['id']
        delete_submission(submission_id, api_key)

# Function to log messages to the log box
def log_message(message):
    log_box.insert(tk.END, message + '\n')
    log_box.see(tk.END)

# GUI Functions
def retrieve_forms():
    log_message("Retrieving forms...")
    forms = get_forms(API_KEY)
    for item in form_tree.get_children():
        form_tree.delete(item)  # Clear existing tree items
    if forms:
        for index, form in enumerate(forms, start=1):
            form_title = form.get('title', 'No Title')
            form_id = form.get('id', 'N/A')
            log_message(f"Fetching submission count for form {index}/{len(forms)}: {form_title} (ID: {form_id})")
            submission_count = get_submission_count(form_id, API_KEY)
            form_tree.insert("", "end", iid=form_id, values=(form_title, form_id, submission_count))
        log_message(f"Retrieved {len(forms)} forms with their submission counts.")
    else:
        messagebox.showerror("Error", "Could not retrieve forms. Please check your API key or connection.")
        log_message("Failed to retrieve forms.")

def delete_selected_forms():
    selected_items = form_tree.selection()  # Get selected form IDs
    if not selected_items:
        messagebox.showwarning("No Selection", "Please select at least one form.")
        return
    
    for form_id in selected_items:
        form_values = form_tree.item(form_id, 'values')
        form_title = form_values[0]
        log_message(f"Deleting submissions for form: {form_title} (ID: {form_id})")
        delete_all_submissions(form_id, API_KEY)
        # Optionally, update the submission count to 0 after deletion
        form_tree.set(form_id, column="Submissions", value=0)
    
    messagebox.showinfo("Complete", "Submission deletion process completed.")
    log_message("Deletion process completed.")

# Main GUI Application
root = tk.Tk()
root.title("JotForm Submission Deleter")
root.geometry("700x500")

# Create a style object to use a modern look if possible
style = ttk.Style()
style.theme_use("clam")  # You can try other themes such as 'default', 'classic'

# Instruction Frame
instruction_frame = ttk.Frame(root, padding="10")
instruction_frame.pack(fill=tk.X)
instruction_label = ttk.Label(instruction_frame, text="Select JotForm forms to delete submissions:")
instruction_label.pack(side=tk.LEFT)

# Form Treeview with scrollbar
form_frame = ttk.Frame(root, padding="10")
form_frame.pack(fill=tk.BOTH, expand=True)

columns = ("Title", "ID", "Submissions")
form_tree = ttk.Treeview(form_frame, columns=columns, show="headings", selectmode="extended")
for col in columns:
    form_tree.heading(col, text=col)
    form_tree.column(col, anchor="w", width=200 if col == "Title" else 150)

form_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(form_frame, orient="vertical", command=form_tree.yview)
scrollbar.pack(side=tk.RIGHT, fill="y")
form_tree.config(yscrollcommand=scrollbar.set)

# Button Frame for actions
button_frame = ttk.Frame(root, padding="10")
button_frame.pack(fill=tk.X)

retrieve_button = ttk.Button(button_frame, text="Retrieve Forms", command=retrieve_forms)
retrieve_button.pack(side=tk.LEFT, padx=5, pady=5)

delete_button = ttk.Button(button_frame, text="Delete Selected Forms' Submissions", command=delete_selected_forms)
delete_button.pack(side=tk.LEFT, padx=5, pady=5)

# Log box to display actions
log_frame = ttk.Frame(root, padding="10")
log_frame.pack(fill=tk.BOTH, expand=True)

log_label = ttk.Label(log_frame, text="Log:")
log_label.pack(anchor="w")

log_box = tk.Text(log_frame, height=10, state=tk.NORMAL, wrap="word")
log_box.pack(fill=tk.BOTH, expand=True)

# Start the GUI application
root.mainloop()