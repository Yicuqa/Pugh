import csv
import tkinter as tk
from tkinter import messagebox, ttk
from openpyxl import Workbook
from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Solution Results', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

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
            {'name': 'Criteria 1', 'details': '', 'importance': 'Low'},
            {'name': 'Criteria 2', 'details': '', 'importance': 'Low'}
        ]
        self.solution_data = [
            {'name': 'Solution 1', 'details': ''},
            {'name': 'Solution 2', 'details': ''}
        ]

        self.criteria_entries = []  # Entries for criteria names
        self.importance_comboboxes = []  # Comboboxes for criteria importance
        self.solution_entries = []  # Entries for solution names

        self.show_input_criteria_frame()

    def export_to_csv(self, data, filename="Results.csv"):
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            # Assuming data is a list of tuples (name, score)
            writer.writerow(['Solution', 'Score'])
            for name, score in data:
                writer.writerow([name, score])
        messagebox.showinfo("Export Success", "Results exported successfully to CSV.")

    def export_to_xlsx(self, scores, filename="Results.xlsx"):
        print("Exporting to XLSX", scores)  # Debug print
        wb = Workbook()
        ws = wb.active
        ws.append(["Solution", "Score"])
        sorted_scores = sorted(scores.items(), key=lambda item: (-item[1], item[0]))
        for solution_name, score in sorted_scores:
            ws.append([solution_name, score])
        wb.save(filename)
        print(f"Exported results to {filename}")  # Confirm file save
        messagebox.showinfo("Export Success", f"Results exported successfully to {filename}.")

    def prepare_data_for_export(self):
        # Calculate scores
        scores = self.calculate_scores()
        # Convert all scores to integers if they aren't already
        prepared_data = [(name, int(score)) for name, score in scores.items()]
        return prepared_data

    def export_to_pdf(self, data, filename="Results.pdf"):
        pdf = PDF()
        pdf.add_page()
        pdf.set_font('Arial', '', 12)
        pdf.cell(40, 10, 'Solution', 0, 0)  # Adjusted cell width
        pdf.cell(0, 10, 'Score', 0, 1, 'R')  # 'R' aligns right

        # Ensure data is in the correct format and sort it
        sorted_data = sorted(data, key=lambda x: (-x[1], x[0]))

        # Adding sorted data to the PDF
        for name, score in sorted_data:
            pdf.cell(40, 10, name, 0, 0)  # Adjusted cell width for name
            pdf.cell(0, 10, str(score), 0, 1, 'R')

        pdf.output(filename)
        messagebox.showinfo("Export Success", f"Results exported successfully to PDF as {filename}")

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
        
        exportMenu = tk.Menu(menubar, tearoff=0)
        exportMenu.add_command(label="Export to CSV", command=self.perform_csv_export)
        exportMenu.add_command(label="Export to XLSX", command=self.perform_xlsx_export)
        exportMenu.add_command(label="Export to PDF", command=self.perform_pdf_export)
        menubar.add_cascade(label="Export", menu=exportMenu)

        viewMenu = tk.Menu(menubar, tearoff=0)
        viewMenu.add_command(label="Input Criteria", command=self.show_input_criteria_frame)
        viewMenu.add_command(label="Input Solution", command=self.show_input_solution_frame)
        viewMenu.add_command(label="View Calculation", command=self.show_input_calculation_frame)
        menubar.add_cascade(label="View", menu=viewMenu)

    def perform_csv_export(self):
        scores = self.get_scores()
        self.export_to_csv(scores)

    def perform_xlsx_export(self):
        scores = self.calculate_scores()
        self.export_to_xlsx(scores)

    def perform_pdf_export(self):
        data = self.prepare_data_for_export()
        self.export_to_pdf(data, filename="Results.pdf")

    def get_scores(self):
        # Logic to collect scores from your application's data
        return [(solution['name'], score) for solution, score in zip(self.solution_data, self.calculate_scores())]

    def calculate_scores(self):
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
        
        return scores


    def display_results(self, scores):
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

    def calculate_and_display(self):
        scores = self.calculate_scores()
        self.display_results(scores)


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

    def update_data_from_entries(self):
        for i, entry in enumerate(self.criteria_entries):
            if i < len(self.criteria_data):
                self.criteria_data[i]['name'] = entry.get()
                self.criteria_data[i]['importance'] = self.importance_comboboxes[i].get()
                details_entry = entry.master.children['details_entry']
                self.criteria_data[i]['details'] = details_entry.get()

        for i, entry in enumerate(self.solution_entries):
            if i < len(self.solution_data):
                self.solution_data[i]['name'] = entry.get()
                # Capture details from the adjacent details entry widget
                details_entry = entry.master.children['details_entry']
                self.solution_data[i]['details'] = details_entry.get()

    def show_input_criteria_frame(self):
        self.clear_content_frame()
        criteria_container = tk.Frame(self.content_frame)
        criteria_container.pack(fill='x', expand=True, pady=10)
        header_frame = tk.Frame(criteria_container)
        header_frame.pack(fill='x', expand=True)
        tk.Label(header_frame, text="Criteria", font=('Arial', 12), borderwidth=1, relief="groove").pack(side='left', expand=True)
        tk.Label(header_frame, text="Details", font=('Arial', 12), borderwidth=1, relief="groove").pack(side='left', expand=True)
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

        # Add detail entry
        details_entry = tk.Entry(row_frame, name='details_entry')
        details_entry.insert(0, criterion.get('details', ''))
        details_entry.pack(side='left', fill='x', expand=True)
        
        # Add importance rank
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
        
        details_entry = tk.Entry(row_frame, name='details_entry')
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
                    added_score = int(checkbox.get_score()) if isinstance(checkbox.get_score(), str) else checkbox.get_score()
                    scores[solution['name']] += added_score * importance_score

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