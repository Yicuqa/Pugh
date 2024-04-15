import tkinter as tk
from tkinter import messagebox, ttk

class CycleCheckbutton(tk.Label):
    def __init__(self, master=None, state_change_callback=None, **kw):
        super().__init__(master, **kw)
        self.configure(wraplength=100)  # Wrap text if longer than 100 pixels
        self.values = [" ", "+", "-", "S"]
        self.current_value = 0
        self.configure(text=self.values[self.current_value], borderwidth=1, relief="groove", width=2)
        self.bind("<Button-1>", self.cycle_value)
        self.state_change_callback = state_change_callback  # Store the callback

    def cycle_value(self, event=None):
        self.current_value = (self.current_value + 1) % len(self.values)
        self.configure(text=self.values[self.current_value])
        # Invoke the callback if it's set
        if self.state_change_callback:
            self.state_change_callback(self.get_state())

    def get_state(self):
        return self.values[self.current_value]

    def set_state(self, state):
        if state in self.values:
            self.current_value = self.values.index(state)
            self.configure(text=state)

    def get_score(self):
        value_scores = {"+": 1, "-": -1, "S": 0, " ": 0}
        return value_scores[self.values[self.current_value]]


class MyApp:
    def __init__(self, root):
        self.root = root
        root.title("Pugh Matrix")
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

        self.criteria_entries = []  # Entries for criteria names
        self.importance_comboboxes = []  # Comboboxes for criteria importance
        self.solution_entries = []  # Entries for solution names

        self.show_input_criteria_frame()

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        fileMenu = tk.Menu(menubar, tearoff=0)
        fileMenu.add_command(label="Open New", command=lambda: messagebox.showinfo("Popup", "Not supported yet!"))
        fileMenu.add_separator()
        fileMenu.add_command(label="Help", command=lambda: messagebox.showinfo("Popup", "Not supported yet!"))
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

    def clear_content_frame(self):
        self.update_data_from_entries()  # Update data model before clearing frame
        self.criteria_entries.clear()
        self.importance_comboboxes.clear()
        self.solution_entries.clear()
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_input_criteria_frame(self):
        self.clear_content_frame()
        criteria_container = tk.Frame(self.content_frame)
        criteria_container.pack(fill='x', expand=True, pady=10)
        header_frame = tk.Frame(criteria_container)
        header_frame.pack(fill='x', expand=True)
        tk.Label(header_frame, text="Criteria", font=('Arial', 12), borderwidth=1, relief="groove").pack(side='left', expand=True)
        tk.Label(header_frame, text="Importance", font=('Arial', 12), borderwidth=1, relief="groove").pack(side='left', expand=True)

        for index, criterion in enumerate(self.criteria_data):
            self.add_criteria_row(criteria_container, criterion, index)

        action_frame = tk.Frame(self.content_frame)
        action_frame.pack(fill='x', pady=10)
        ttk.Button(action_frame, text="Add Criteria", command=self.add_criteria).pack(side='left', padx=10)
        ttk.Button(action_frame, text="Delete Last Criteria", command=self.delete_criteria).pack(side='left')

    def add_criteria_row(self, container, criterion, index):
        row_frame = tk.Frame(container)
        row_frame.pack(fill='x', expand=True, padx=5, pady=5)
        entry = tk.Entry(row_frame)
        entry.insert(0, criterion['name'])
        entry.pack(side='left', fill='x', expand=True)
        self.criteria_entries.append(entry)

        importance_combobox = ttk.Combobox(row_frame, values=["Low", "Medium", "High"], state="readonly")
        importance_combobox.set(criterion['importance'])
        importance_combobox.pack(side='left', expand=True)
        self.importance_comboboxes.append(importance_combobox)

    def add_criteria(self):
        if len(self.criteria_data) < 13:
            self.criteria_data.append({'name': '', 'importance': 'Low'})
            self.show_input_criteria_frame()
        else:
            messagebox.showinfo("Limit Reached", "A maximum of 13 criteria rows are allowed.")

    def delete_criteria(self):
        if len(self.criteria_data) > 1:
            self.criteria_data.pop()
            self.show_input_criteria_frame()
        else:
            messagebox.showinfo("Minimum Requirement", "At least one criteria must be present.")

    def update_data_from_entries(self):
        for i, entry in enumerate(self.criteria_entries):
            if i < len(self.criteria_data):
                self.criteria_data[i]['name'] = entry.get()
                self.criteria_data[i]['importance'] = self.importance_comboboxes[i].get()

        for i, entry in enumerate(self.solution_entries):
            if i < len(self.solution_data):
                self.solution_data[i]['name'] = entry.get()

    def show_input_solution_frame(self):
        self.clear_content_frame()
        solution_container = tk.Frame(self.content_frame)
        solution_container.pack(fill='x', expand=True, pady=10)
        header_frame = tk.Frame(solution_container)
        header_frame.pack(fill='x', expand=True)
        tk.Label(header_frame, text="Solutions", font=('Arial', 12), borderwidth=1, relief="groove").pack(side='left', expand=True)
        tk.Label(header_frame, text="Details", font=('Arial', 12), borderwidth=1, relief="groove").pack(side='left', expand=True)

        for index, solution in enumerate(self.solution_data):
            self.add_solution_row(solution_container, solution, index)

        action_frame = tk.Frame(self.content_frame)
        action_frame.pack(fill='x', pady=10)
        ttk.Button(action_frame, text="Add Solution", command=self.add_solution).pack(side='left', padx=10)
        ttk.Button(action_frame, text="Delete Last Solution", command=self.delete_solution).pack(side='left')

    def add_solution_row(self, container, solution, index):
        row_frame = tk.Frame(container)
        row_frame.pack(fill='x', expand=True, padx=5, pady=5)
        entry = tk.Entry(row_frame)
        entry.insert(0, solution['name'])
        entry.pack(side='left', fill='x', expand=True)
        self.solution_entries.append(entry)

        details_entry = tk.Entry(row_frame)
        details_entry.insert(0, solution.get('details', ''))
        details_entry.pack(side='left', fill='x', expand=True)

    def add_solution(self):
        if len(self.solution_data) < 14:
            self.solution_data.append({'name': '', 'details': ''})
            self.show_input_solution_frame()
        else:
            messagebox.showinfo("Limit Reached", "A maximum of 14 solution rows are allowed.")

    def delete_solution(self):
        if len(self.solution_data) > 1:
            self.solution_data.pop()
            self.show_input_solution_frame()
        else:
            messagebox.showinfo("Minimum Requirement", "At least one solution must be present.")

    def show_input_calculation_frame(self):
        self.clear_content_frame()
        if not self.criteria_data or not self.solution_data:
            messagebox.showinfo("Info", "No data to display in calculation view.")
            return

        # Create labels for criteria and solutions
        for i, criterion in enumerate(self.criteria_data):
            tk.Label(self.content_frame, text=criterion['name'], borderwidth=1, relief="solid", wraplength=100).grid(row=i+1, column=0, sticky="nsew")

        for j, solution in enumerate(self.solution_data):
            tk.Label(self.content_frame, text=solution['name'], borderwidth=1, relief="solid", wraplength=100).grid(row=0, column=j+1, sticky="nsew")
            for i, criterion in enumerate(self.criteria_data):
                # Retrieve the saved state or default to " "
                state = criterion.get('states', {}).get(solution['name'], " ")
                checkbutton = CycleCheckbutton(
                    self.content_frame,
                    state_change_callback=lambda state, c=criterion, s=solution['name']: self.update_checkbox_state(c, s, state)
                )
                checkbutton.set_state(state)
                checkbutton.grid(row=i+1, column=j+1, sticky="nsew")

        # Grid configuration for equal distribution
        for i in range(len(self.criteria_data) + 1):
            self.content_frame.grid_rowconfigure(i, weight=1)
        for j in range(len(self.solution_data) + 1):
            self.content_frame.grid_columnconfigure(j, weight=1)

        # Button for calculating the scores
        calculate_button = ttk.Button(self.content_frame, text="Calculate", command=self.calculate)
        calculate_button.grid(row=len(self.criteria_data) + 1, columnspan=len(self.solution_data) + 1, sticky="ew")

    def update_checkbox_state(self, criterion, solution_name, state):
        # This method updates the state in the model
        criterion.setdefault('states', {})[solution_name] = state


    def calculate(self):
        scores = {}
        importance_scores = {"Low": 1, "Medium": 2, "High": 3}
        
        # Initialize scores dictionary with solution names
        for solution in self.solution_data:
            scores[solution['name']] = 0
        
        for i, criterion in enumerate(self.criteria_data):
            importance = criterion['importance']
            importance_score = importance_scores[importance]
            
            for j, solution in enumerate(self.solution_data):
                checkbox = self.content_frame.grid_slaves(row=i + 1, column=j + 1)[0]
                if isinstance(checkbox, CycleCheckbutton):
                    # Multiply the checkbox score by the importance score and add to the solution's total
                    scores[solution['name']] += checkbox.get_score() * importance_score

        # Create a new Toplevel window to display results
        result_window = tk.Toplevel(self.root)
        result_window.title("Results")
        result_window.geometry("400x400")
        
        # Sort solutions by score descending, and by name alphabetically if scores are the same
        sorted_solutions = sorted(scores.items(), key=lambda item: (-item[1], item[0]))
        
        # Display each solution and its score
        for i, (solution_name, score) in enumerate(sorted_solutions):
            result_label = tk.Label(result_window, text=f"{solution_name}: {score}", font=("Arial", 14))
            result_label.pack(pady=(20, 0) if i == 0 else (10, 0))

        # Add a close button to the window
        close_button = tk.Button(result_window, text="Close", command=result_window.destroy)
        close_button.pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()