import requests
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime

# Replace with your actual API key
API_KEY = '48793d9fd9e19f3bb29a29a59e7bce95'

# JotForm API base URL for EU accounts
BASE_URL = 'https://eu-api.jotform.com'

# Global variables to track sort state
current_sort_col = None
current_sort_reverse = False

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
            log_message(f"Unexpected response structure: {data}")
            return []
    
    except requests.exceptions.HTTPError as http_err:
        log_message(f"HTTP error occurred: {http_err}")
    except Exception as err:
        log_message(f"An error occurred: {err}")
    
    return []

# Function to retrieve the number of submissions for a form
def get_submission_count(form_id, api_key):
    url = f"{BASE_URL}/form/{form_id}/submissions"
    params = {
        'apiKey': api_key,
        'limit': 1  # Minimal data to reduce payload
    }
    response = requests.get(url, params=params)
    
    try:
        response.raise_for_status()
        
        # Attempt to retrieve the total count from headers
        total = response.headers.get('X-Total-Count')
        if total:
            return int(total)
        
        # If header not available, fetch all submissions and count
        params['limit'] = 1000  # Adjust as needed
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if 'content' in data:
            return len(data['content'])
        else:
            log_message(f"Unexpected response structure when fetching submissions: {data}")
            return 0
    except requests.exceptions.HTTPError as http_err:
        log_message(f"HTTP error occurred while fetching submissions for form {form_id}: {http_err}")
    except Exception as err:
        log_message(f"An error occurred while fetching submissions for form {form_id}: {err}")
    
    return 0

# Function to retrieve the date of the last submission for a form
def get_last_submission_date(form_id, api_key):
    url = f"{BASE_URL}/form/{form_id}/submissions"
    params = {
        'apiKey': api_key,
        'limit': 1,
        'orderby': 'created_at',  # Assuming the API supports ordering
        'sort': 'desc'            # Get the latest submission first
    }
    response = requests.get(url, params=params)
    
    try:
        response.raise_for_status()
        data = response.json()

        if 'content' in data and len(data['content']) > 0:
            last_submission = data['content'][0]
            created_at = last_submission.get('created_at')
            if created_at:
                # Try multiple date formats
                for fmt in ("%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%d %H:%M:%S"):
                    try:
                        dt = datetime.strptime(created_at, fmt)
                        return dt.strftime("%Y-%m-%d %H:%M:%S")
                    except ValueError:
                        continue
                # If none match, return the original string
                return created_at
            else:
                return "N/A"
        else:
            return "N/A"
    
    except requests.exceptions.HTTPError as http_err:
        log_message(f"HTTP error occurred while fetching last submission for form {form_id}: {http_err}")
    except Exception as err:
        log_message(f"An error occurred while fetching last submission for form {form_id}: {err}")
    
    return "N/A"

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
            log_message(f"Unexpected response structure: {data}")
            return []
    
    except requests.exceptions.HTTPError as http_err:
        log_message(f"HTTP error occurred: {http_err}")
    except Exception as err:
        log_message(f"An error occurred: {err}")
    
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

# Function to log messages to the log box with timestamps
def log_message(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_box.insert(tk.END, f"{timestamp} - {message}\n")
    log_box.see(tk.END)

# GUI Functions
def retrieve_forms():
    global current_sort_col, current_sort_reverse

    # Save current selections
    selected_form_ids = set()
    for item in form_tree.get_children():
        if form_tree.set(item, "Select") == "✔":
            selected_form_ids.add(item)
    
    # Save current sort state
    sort_col = current_sort_col
    sort_reverse = current_sort_reverse

    log_message("Retrieving forms...")
    forms = get_forms(API_KEY)
    for item in form_tree.get_children():
        form_tree.delete(item)  # Clear existing tree items
    if forms:
        for index, form in enumerate(forms, start=1):
            form_title = form.get('title', 'No Title')
            form_id = form.get('id', 'N/A')
            form_status = form.get('status', 'ENABLED')  # Assuming 'status' field exists
            is_active = form_status.upper() == 'ENABLED'  # Determine if form is active

            # Log the status for debugging
            log_message(f"Form {index}/{len(forms)}: '{form_title}' (ID: {form_id}) - Status: {form_status}")

            log_message(f"Fetching submission count for form {index}/{len(forms)}: {form_title} (ID: {form_id})")
            submission_count = get_submission_count(form_id, API_KEY)
            last_submission_date = get_last_submission_date(form_id, API_KEY)

            # Insert form into Treeview with appropriate tag
            form_tree.insert(
                "",
                "end",
                iid=form_id,
                values=("", form_title, form_id, form_status, submission_count, last_submission_date),  # Added checkbox column
                tags=('active',) if is_active else ('disabled',)
            )
        log_message(f"Retrieved {len(forms)} forms with their submission counts and last submission dates.")
    else:
        messagebox.showerror("Error", "Could not retrieve forms. Please check your API key or connection.")
        log_message("Failed to retrieve forms.")

    # Restore selections
    for form_id in selected_form_ids:
        if form_id in form_tree.get_children():
            form_tree.set(form_id, "Select", "✔")
    
    # Restore sort
    if sort_col:
        sort_treeview(sort_col, sort_reverse)

def toggle_checkbox(event):
    region = form_tree.identify("region", event.x, event.y)
    if region != "cell":
        return
    column = form_tree.identify_column(event.x)
    if column != "#1":  # Assuming "Select" is the first column
        return
    item = form_tree.identify_row(event.y)
    if not item:
        return
    # Get current state
    current = form_tree.set(item, "Select")
    new_state = "✔" if current == "" else ""
    form_tree.set(item, "Select", new_state)

def delete_selected_forms():
    selected_forms = []
    for item in form_tree.get_children():
        if form_tree.set(item, "Select") == "✔":
            tags = form_tree.item(item, 'tags')
            if 'disabled' in tags:
                form_title = form_tree.set(item, "Title")
                form_id = form_tree.set(item, "ID")
                log_message(f"Skipping disabled form: {form_title} (ID: {form_id})")
                continue  # Skip disabled forms
            selected_forms.append(item)
    
    if not selected_forms:
        messagebox.showwarning("No Selection", "Please select at least one active form using the checkboxes.")
        return
    
    for form_id in selected_forms:
        form_values = form_tree.item(form_id, 'values')
        form_title = form_values[1]  # Title is the second column
        log_message(f"Deleting submissions for form: {form_title} (ID: {form_id})")
        delete_all_submissions(form_id, API_KEY)
        # Optionally, update the submission count and last submission date after deletion
        form_tree.set(form_id, column="Submissions", value=0)
        form_tree.set(form_id, column="Last Submission", value="N/A")
        form_tree.set(form_id, column="Select", value="" )  # Uncheck the checkbox after deletion
    
    messagebox.showinfo("Complete", "Submission deletion process completed.")
    log_message("Deletion process completed.")

# Function to automatically retrieve forms every 60 seconds
def auto_retrieve_forms():
    retrieve_forms()
    # Schedule the next retrieval after 60000 milliseconds (60 seconds)
    root.after(60000, auto_retrieve_forms)

# Function to handle Treeview selection to prevent selecting disabled forms
def on_treeview_select(event):
    pass  # No longer needed since we use checkboxes

# Main GUI Application
root = tk.Tk()
root.title("JotForm Submission Deleter")
root.geometry("1000x600")  # Increased width to accommodate the new column

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

# Added "Select" column for checkboxes and "Status" column for form status
columns = ("Select", "Title", "ID", "Status", "Submissions", "Last Submission")
form_tree = ttk.Treeview(form_frame, columns=columns, show="headings", selectmode="none")

# Define the headings
form_tree.heading("Select", text="Select")
form_tree.heading("Title", text="Title")
form_tree.heading("ID", text="ID")
form_tree.heading("Status", text="Status")
form_tree.heading("Submissions", text="Submissions")
form_tree.heading("Last Submission", text="Last Submission")

# Define the column properties
form_tree.column("Select", width=60, anchor="center")
form_tree.column("Title", anchor="w", width=300)
form_tree.column("ID", anchor="w", width=150)
form_tree.column("Status", anchor="center", width=100)
form_tree.column("Submissions", anchor="center", width=100)
form_tree.column("Last Submission", anchor="center", width=200)

# Define tags for active and disabled forms
form_tree.tag_configure('disabled', foreground='gray')  # Grayed out for disabled forms
form_tree.tag_configure('active', foreground='black')   # Normal text for active forms

# Add checkboxes by using a simple text "✔" to represent checked state
# Bind a click event on the "Select" column to toggle the checkbox
form_tree.bind("<Button-1>", toggle_checkbox)

form_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Add a vertical scrollbar to the Treeview
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

# Enable sorting by clicking on column headers
def sort_treeview(col, reverse):
    global current_sort_col, current_sort_reverse

    # Update current sort state
    current_sort_col = col
    current_sort_reverse = reverse

    # Get all items and sort them based on the given column
    data = []
    for k in form_tree.get_children(''):
        value = form_tree.set(k, col)
        if col == "Submissions":
            try:
                value = int(value)
            except ValueError:
                value = 0
        elif col == "Last Submission":
            try:
                value = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                value = datetime.min
        data.append((value, k))
    
    # Sort data
    data.sort(reverse=reverse)
    
    # Rearrange items in sorted positions
    for index, (val, k) in enumerate(data):
        form_tree.move(k, '', index)
    
    # Reverse sort next time
    form_tree.heading(col, command=lambda: sort_treeview(col, not reverse))

# Attach the sort function to each column header
for col in columns:
    form_tree.heading(col, text=col, command=lambda _col=col: sort_treeview(_col, False))

# Start the auto retrieval process
auto_retrieve_forms()

# Start the GUI application
root.mainloop()
