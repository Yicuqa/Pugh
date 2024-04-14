import tkinter as tk
from tkinter import messagebox, ttk

# Custom checkbox-like class that cycles through "+", "-", and "S"
class CycleCheckbutton(tk.Label):
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.values = [" ", "+", "-", "S"]
        self.current_value = 0
        self.configure(text=self.values[self.current_value], borderwidth=1, relief="groove", width=2)
        self.bind("<Button-1>", self.cycle_value)

    def cycle_value(self, event=None):
        self.current_value = (self.current_value + 1) % len(self.values)
        self.configure(text=self.values[self.current_value])

class MyApp:
    def __init__(self, root):
        self.root = root
        root.title("Pugh")
        self.root.geometry("700x500")
        self.create_menu()
        self.create_content_frame()

        self.criteria_data = [
            {'name': 'Criteria 1', 'importance': 'Low'},
            {'name': 'Criteria 2', 'importance': 'Low'}
        ]

        self.solution_data = [
            {'name': 'Solution 1', 'details': ''},
            {'name': 'Solution 2', 'details': ''}
        ]

        self.criteria_entries = []  # Store criteria entries for access
        self.solution_entries = []  # Store solution entries for access

        # Open the application at the criteria view
        self.show_input_criteria_frame()

    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        fileMenu = tk.Menu(menubar, tearoff=0)
        fileMenu.add_command(label="Open New", command=lambda: messagebox.showinfo("Popup", "Not supported as of yet!"))
        fileMenu.add_separator()
        fileMenu.add_command(label="Help", command=lambda: messagebox.showinfo("Popup", "Not supported as of yet!"))
        fileMenu.add_separator()
        fileMenu.add_command(label="Close", command=self.root.quit)
        menubar.add_cascade(label="File", menu=fileMenu)

        viewMenu = tk.Menu(menubar, tearoff=0)
        viewMenu.add_command(label="Input Criteria", command=self.show_input_criteria_frame)
        viewMenu.add_command(label="Input Solution", command=self.show_input_solution_frame)
        viewMenu.add_command(label="View Calculation", command=self.show_input_calculation_frame)
        menubar.add_cascade(label="View", menu=viewMenu)

    def create_content_frame(self):
        self.content_frame = tk.Frame(self.root)
        self.content_frame.pack(fill='both', expand=True)

    def show_input_criteria_frame(self):
        self.clear_content_frame()
        self.criteria_entries.clear()  # Clear previous entries
        
        # Container for the criteria rows and headers
        criteria_container = tk.Frame(self.content_frame)
        criteria_container.pack(fill='x', side='top', expand=True, pady=(10, 0))
        
        # Creating header row
        header_frame = tk.Frame(criteria_container)
        header_frame.pack(fill='x', side='top')
        tk.Label(header_frame, text="Criteria", font=('Arial', 10), borderwidth=2, relief="groove").pack(side='left', fill='x', expand=True)
        tk.Label(header_frame, text="Importance", font=('Arial', 10), borderwidth=2, relief="groove").pack(side='left', fill='x', expand=True)

        for data in self.criteria_data:
            self.create_criteria_row(data, container=criteria_container)
        
        # Lower half for action buttons
        action_frame = tk.Frame(self.content_frame)
        action_frame.pack(fill='x', side='bottom', pady=10)
        ttk.Button(action_frame, text="Add Row", command=self.add_criteria_row).pack(side='left', padx=10)
        ttk.Button(action_frame, text="Delete Row", command=self.delete_criteria_row).pack(side='left')

    def create_criteria_row(self, data, container):
        row_frame = tk.Frame(container)
        row_frame.pack(fill='x', padx=5, pady=5)
        
        # Create the entry widget and store it in the list
        entry = tk.Entry(row_frame)
        self.criteria_entries.append(entry)  # Store the entry for later use
        entry.insert(0, data['name'])
        entry.pack(side='left', fill='x', expand=True)
        
        combobox = ttk.Combobox(row_frame, values=["Low", "Medium", "High"], state="readonly")
        combobox.set(data['importance'])
        combobox.pack(side='left', padx=5)

    def add_criteria_row(self):
        if len(self.criteria_data) > 12:
            messagebox.showinfo("Limit Reached", "A maximum of 13 criteria rows are allowed.")
            return
        self.criteria_data.append({'name': '', 'importance': 'Low'})
        self.show_input_criteria_frame()

    def delete_criteria_row(self):
        try:
            if len(self.criteria_data) > 1:
                self.criteria_data.pop()
                self.show_input_criteria_frame()
            else:
                messagebox.showinfo("Error", "At least one criteria must be present.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")


    def show_input_solution_frame(self):
        self.clear_content_frame()
        self.solution_entries.clear()  # Clear previous entries
        # Container for the solution rows
        solution_container = tk.Frame(self.content_frame)
        solution_container.pack(fill='x', side='top', expand=True)
        
        # Creating header row for solutions and details
        header_frame = tk.Frame(solution_container)
        header_frame.pack(fill='x', side='top')
        tk.Label(header_frame, text="Solutions", font=('Arial', 10), borderwidth=2, relief="groove").pack(side='left', fill='x', expand=True)
        tk.Label(header_frame, text="Details", font=('Arial', 10), borderwidth=2, relief="groove").pack(side='left', fill='x', expand=True)

        # Creating a row for each solution with a detail entry
        for data in self.solution_data:
            self.create_solution_row(data, container=solution_container)
        
        # Lower half for action buttons
        action_frame = tk.Frame(self.content_frame)
        action_frame.pack(fill='x', side='bottom', pady=10)
        ttk.Button(action_frame, text="Add Row", command=self.add_solution_row).pack(side='left', padx=10)
        ttk.Button(action_frame, text="Delete Row", command=self.delete_solution_row).pack(side='left')

    def create_solution_row(self, data, container):
        row_frame = tk.Frame(container)
        row_frame.pack(fill='x', padx=5, pady=5)
        
        # Solution Name Entry
        name_entry = tk.Entry(row_frame)
        self.solution_entries.append(name_entry)
        name_entry.insert(0, data['name'])
        name_entry.pack(side='left', fill='x', expand=True)

        # Details Entry
        details_entry = tk.Entry(row_frame)
        details_entry.insert(0, data.get('details', ''))
        details_entry.pack(side='left', fill='x', expand=True)

    def add_solution_row(self):
        if len(self.solution_data) > 14:
            messagebox.showinfo("Limit Reached", "A maximum of 15 solution rows are allowed.")
            return
        self.solution_data.append({'name': ''})
        self.show_input_solution_frame()

    def delete_solution_row(self):
        try:
            if len(self.solution_data) > 1:
                self.solution_data.pop()
                self.show_input_solution_frame()
            else:
                messagebox.showinfo("Error", "At least one solution must be present.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def show_input_calculation_frame(self):
        self.update_data_from_entries()
        self.clear_content_frame()
        
        # Ensure that there are criteria and solutions to display
        if not self.criteria_data or not self.solution_data:
            messagebox.showinfo("Info", "No data to display in calculation view.")
            return

        # Creating the solution headers and the criteria rows with checkbuttons
        for i, criterion in enumerate(self.criteria_data):
            tk.Label(self.content_frame, text=criterion['name'], borderwidth=1, relief="solid").grid(row=i+1, column=0, sticky="nsew")

        for j, solution in enumerate(self.solution_data):
            tk.Label(self.content_frame, text=solution['name'], borderwidth=1, relief="solid").grid(row=0, column=j+1, sticky="nsew")
            for i in range(len(self.criteria_data)):
                checkbutton = CycleCheckbutton(self.content_frame)
                checkbutton.grid(row=i+1, column=j+1, sticky="nsew")

        # Expand all cells equally
        for i in range(len(self.criteria_data) + 1):
            self.content_frame.grid_rowconfigure(i, weight=1)
        for j in range(len(self.solution_data) + 1):
            self.content_frame.grid_columnconfigure(j, weight=1)

    def update_data_from_entries(self):
        # Update criteria and solution lists based on entries content before clearing the content frame.
        updated_criteria_data = []
        updated_solution_data = []

        # Make sure entries are still there (not destroyed)
        for entry in self.criteria_entries:
            try:
                updated_criteria_data.append({'name': entry.get(), 'importance': 'Low'})
            except:
                pass  # Skip if entry has been destroyed

        for entry in self.solution_entries:
            try:
                updated_solution_data.append({'name': entry.get(), 'details': ''})
            except:
                pass  # Skip if entry has been destroyed

        # Only update the class attributes if we successfully got data
        if updated_criteria_data:
            self.criteria_data = updated_criteria_data
        if updated_solution_data:
            self.solution_data = updated_solution_data


if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()