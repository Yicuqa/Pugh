import tkinter as tk
from tkinter import ttk

class PughMatrixApp:
    def __init__(self, master):
        self.master = master
        master.title("Pugh Matrix")
        
        self.setup_menu()

        # Initial data setup for dynamic row content
        self.criteria_data = [{'name': '', 'importance': 'Medium'} for _ in range(3)]
        self.solution_data = [{'solution': '', 'info': ''} for _ in range(3)]

        # Setup initial view
        self.current_view = None
        self.show_criteria_view()

    def setup_menu(self):
        menu_bar = tk.Menu(self.master)
        self.master.config(menu=menu_bar)

        views_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Views", menu=views_menu)
        views_menu.add_command(label="Criteria View", command=self.show_criteria_view)
        views_menu.add_command(label="Solution View", command=self.show_solution_view)
        views_menu.add_command(label="Calculation View", command=self.show_calculation_view)

    def clear_content_frame(self):
        # Ensure the content frame is cleared or initialized
        if hasattr(self, 'content_frame'):
            self.content_frame.destroy()
        self.content_frame = ttk.Frame(self.master)
        self.content_frame.pack(fill="both", expand=True)

    def show_criteria_view(self):
        if self.current_view != "criteria":
            self.save_data()
        self.clear_content_frame()
        self.current_view = "criteria"
        
        # Container for the criteria rows
        self.criteria_container = ttk.Frame(self.content_frame)
        self.criteria_container.pack(fill='x', side='top')
        
        for data in self.criteria_data:
            self.create_criteria_row(data)
            
        # Action buttons stay at the bottom
        self.add_action_buttons(self.create_criteria_row, self.remove_criteria_row, self.criteria_data)

        # Dynamic row creation
        for criteria in self.criteria_data:
            self.create_criteria_row(criteria)

    def create_criteria_row(self, data=None):
        row_frame = ttk.Frame(self.criteria_container)
        row_frame.pack(fill='x', padx=5, pady=5)
        entry = ttk.Entry(row_frame)
        entry.insert(0, data['name'])
        entry.pack(side='left', fill='x', expand=True)
        combobox = ttk.Combobox(row_frame, values=["Low", "Medium", "High"], state="readonly")
        combobox.set(data['importance'])
        combobox.pack(side='left', padx=5)
        
        # Save reference to the frame and widgets
        data['entry'] = entry
        data['combobox'] = combobox
        data['frame'] = row_frame
        
        # Update the data structure to reference the created widgets
        data.update({'entry': entry, 'combobox': combobox, 'frame': row_frame})

    def remove_criteria_row(self, data_list):
        if data_list:
            data_to_remove = data_list[-1]  # Get the last item
            data_to_remove['frame'].destroy()
            data_list.remove(data_to_remove)

    def remove_solution_row(self):
        if self.solution_data:
            self.solution_data.pop()  # Remove the last entry from the solution data list
            self.show_solution_view()  # Refresh the view to reflect the changes

    def show_solution_view(self):
        if self.current_view != "solution":
            self.save_data()
        self.clear_content_frame()
        self.current_view = "solution"
        
        # Container for the solution rows
        self.solution_container = ttk.Frame(self.content_frame)
        self.solution_container.pack(fill='x', side='top')

        for data in self.solution_data:
            self.create_solution_row(data)
            
        # Action buttons stay at the bottom
        self.add_action_buttons(self.create_solution_row, self.remove_solution_row, self.solution_data)
        
        # Dynamic row creation
        for solution in self.solution_data:
            self.create_solution_row(solution)

    def create_solution_row(self, data=None):
        row_frame = ttk.Frame(self.solution_container)
        row_frame.pack(fill='x', padx=5, pady=5)
        entry = ttk.Entry(row_frame)
        entry.insert(0, data['solution'])
        entry.pack(side='left', fill='x', expand=True)
        info_entry = ttk.Entry(row_frame)
        info_entry.insert(0, data['info'])
        info_entry.pack(side='left', fill='x', expand=True, padx=5)
        
        # Save reference to the frame and widgets
        data['entry'] = entry
        data['info_entry'] = info_entry
        data['frame'] = row_frame
        
        # Update the data structure to reference the created widgets
        data.update({'entry': entry, 'info_entry': info_entry, 'frame': row_frame})

        def remove_solution_row(self, data_list):
            if data_list:
                data_to_remove = data_list[-1]  # Get the last item
                data_to_remove['frame'].destroy()
                data_list.remove(data_to_remove)

    def add_action_buttons(self, add_func, remove_func, data_list):
        action_frame = ttk.Frame(self.content_frame)
        action_frame.pack(fill='x', side='bottom', pady=10)
        ttk.Button(action_frame, text="Add", command=lambda: add_func({'solution': '', 'info': ''} if data_list is self.solution_data else {'name': '', 'importance': 'Medium'})).pack(side='left', padx=10)
        ttk.Button(action_frame, text="Remove", command=lambda: remove_func(data_list)).pack(side='left')

    def save_data(self):
        # Save data from the fields into the data structures before switching views
        if self.current_view == "criteria":
            for data in self.criteria_data:
                data['name'] = data['entry'].get()
                data['importance'] = data['combobox'].get()
        elif self.current_view == "solution":
            for data in self.solution_data:
                data['solution'] = data['entry'].get()
                data['info'] = data['info_entry'].get()

    def show_calculation_view(self):
        self.save_data()
        self.clear_content_frame()
        self.current_view = "calculation"
        # Calculation view logic here

def main():
    root = tk.Tk()
    app = PughMatrixApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
