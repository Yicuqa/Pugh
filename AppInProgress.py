import tkinter as tk
from tkinter import messagebox

class Root(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.grid(sticky="nsew")  # Make the frame expand to the full space of the grid cell
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)
        self.create_widgets()

    def create_widgets(self):
        """This method will be overridden in subclasses to create frame-specific widgets."""
        pass

class InputCriteriaFrame(Root):
    def __init__(self, master, controller):
        super().__init__(master, controller)
        self.rows = []

    def create_widgets(self):
        super().create_widgets()
        self.entries_frame = tk.Frame(self)
        self.entries_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.buttons_frame = tk.Frame(self)
        self.buttons_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.add_row_button = tk.Button(self.buttons_frame, text="Add Row", command=self.add_row)
        self.add_row_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.delete_row_button = tk.Button(self.buttons_frame, text="Delete Row", command=self.delete_row)
        self.delete_row_button.pack(side=tk.RIGHT, padx=5, pady=5)

        self.add_row()  # Initialize with one row

    def add_row(self):
        entry = tk.Entry(self.entries_frame)
        entry.pack(fill=tk.X, pady=5)
        self.rows.append(entry)

    def delete_row(self):
        if self.rows:
            entry_to_remove = self.rows.pop()
            entry_to_remove.pack_forget()
            entry_to_remove.destroy()

class InputSolutionFrame(Root):
    def __init__(self, master, controller):
        super().__init__(master, controller)
        self.rows = []

    def create_widgets(self):
        super().create_widgets()
        self.entries_frame = tk.Frame(self)
        self.entries_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.buttons_frame = tk.Frame(self)
        self.buttons_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.add_row_button = tk.Button(self.buttons_frame, text="Add Row", command=self.add_row)
        self.add_row_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.delete_row_button = tk.Button(self.buttons_frame, text="Delete Row", command=self.delete_row)
        self.delete_row_button.pack(side=tk.RIGHT, padx=5, pady=5)

        self.add_row()  # Initialize with one row

    def add_row(self):
        entry = tk.Entry(self.entries_frame)
        entry.pack(fill=tk.X, pady=5)
        self.rows.append(entry)

    def delete_row(self):
        if self.rows:
            entry_to_remove = self.rows.pop()
            entry_to_remove.pack_forget()
            entry_to_remove.destroy()

class ViewCalculationFrame(Root):
    def __init__(self, master, controller):
        super().__init__(master, controller)
        self.rows = []

    def create_widgets(self):
        super().create_widgets()
        self.entries_frame = tk.Frame(self)
        self.entries_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.buttons_frame = tk.Frame(self)
        self.buttons_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.add_row_button = tk.Button(self.buttons_frame, text="Add Row", command=self.add_row)
        self.add_row_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.delete_row_button = tk.Button(self.buttons_frame, text="Delete Row", command=self.delete_row)
        self.delete_row_button.pack(side=tk.RIGHT, padx=5, pady=5)

        self.add_row()  # Initialize with one row

    def add_row(self):
        entry = tk.Entry(self.entries_frame)
        entry.pack(fill=tk.X, pady=5)
        self.rows.append(entry)

    def delete_row(self):
        if self.rows:
            entry_to_remove = self.rows.pop()
            entry_to_remove.pack_forget()
            entry_to_remove.destroy()

class PythonGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pugh Matrix")
        self.geometry("500x500")

        self.create_menus()
        self.frames = {}
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        for F in (InputCriteriaFrame, InputSolutionFrame, ViewCalculationFrame):
            frame = F(master=self.container, controller=self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(InputCriteriaFrame)

    def create_menus(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # File Menu
        fileMenu = tk.Menu(menubar, tearoff=0)
        fileMenu.add_command(label="Open New", command=lambda: popupmsg("Not supported as of yet!"))
        fileMenu.add_separator()
        fileMenu.add_command(label="Something new", command=lambda: popupmsg("Not supported as of yet!"))
        fileMenu.add_command(label="Close", command=self.quit)
        menubar.add_cascade(label="File", menu=fileMenu)

        # View Menu
        viewMenu = tk.Menu(menubar, tearoff=0)
        viewMenu.add_command(label="Input Criteria", command=lambda: self.show_frame(InputCriteriaFrame))
        viewMenu.add_command(label="Input Solution", command=lambda: self.show_frame(InputSolutionFrame))
        viewMenu.add_command(label="View Calculation", command=lambda: self.show_frame(ViewCalculationFrame))
        menubar.add_cascade(label="View", menu=viewMenu)

    def show_frame(self, cls):
        """Show a frame for the given class"""
        for frame in self.frames.values():
            frame.grid_remove()
        frame = self.frames[cls]
        frame.grid(row=0, column=0, sticky="nsew")

def popupmsg(msg):
    messagebox.showinfo("Popup", msg)

if __name__ == "__main__":
    app = PythonGUI()
    app.mainloop()
