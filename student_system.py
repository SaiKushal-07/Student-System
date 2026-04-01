import customtkinter as ctk
from tkinter import messagebox, ttk
import json
import os

# Theme Settings
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

DB_FILE = "students.json"

class ModernStudentSystem(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Setup
        self.title("Student Record System Pro")
        self.geometry("1000x600")
        self.students = self.load_data()

        # Layout Configuration
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- SIDEBAR ---
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar, text="GRADES PORTAL", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.btn_add = ctk.CTkButton(self.sidebar, text="Save Record", command=self.add_student)
        self.btn_add.grid(row=1, column=0, padx=20, pady=10)

        self.btn_delete = ctk.CTkButton(self.sidebar, text="Delete Student", fg_color="#912a2a", hover_color="#6b1f1f", command=self.delete_student)
        self.btn_delete.grid(row=2, column=0, padx=20, pady=10)

        # --- MAIN CONTENT ---
        self.main_frame = ctk.CTkFrame(self, corner_radius=15)
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        # 1. SEARCH BAR (Top)
        search_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        search_frame.grid(row=0, column=0, columnspan=3, padx=20, pady=(20, 10))

        # Adding the "Search" text label
        self.lbl_search = ctk.CTkLabel(search_frame, text="Search:", font=ctk.CTkFont(size=14, weight="bold"))
        self.lbl_search.pack(side="left", padx=10)

        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", self.filter_records) 
        
        # The search entry itself
        self.entry_search = ctk.CTkEntry(search_frame, placeholder_text="Enter Name or ID...", 
                                        width=350, textvariable=self.search_var)
        self.entry_search.pack(side="left")

        # 2. INPUT FIELDS (Middle)
        self.entry_id = ctk.CTkEntry(self.main_frame, placeholder_text="Student ID", width=180)
        self.entry_id.grid(row=1, column=0, padx=10, pady=10)

        self.entry_name = ctk.CTkEntry(self.main_frame, placeholder_text="Full Name", width=180)
        self.entry_name.grid(row=1, column=1, padx=10, pady=10)

        self.entry_cgpa = ctk.CTkEntry(self.main_frame, placeholder_text="CGPA (0.0 - 10.0)", width=180)
        self.entry_cgpa.grid(row=1, column=2, padx=10, pady=10)

        # 3. TABLE (Bottom)
        # Applying styling to the standard Treeview to match Dark Mode
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#2a2d2e", foreground="white", rowheight=30, fieldbackground="#2a2d2e", borderwidth=0)
        style.configure("Treeview.Heading", background="#1f538d", foreground="white", relief="flat")
        style.map("Treeview", background=[('selected', '#1f538d')])

        self.tree = ttk.Treeview(self.main_frame, columns=("ID", "Name", "CGPA"), show='headings')
        self.tree.heading("ID", text="STUDENT ID")
        self.tree.heading("Name", text="FULL NAME")
        self.tree.heading("CGPA", text="CGPA")
        
        # Column Formatting (The specific alignment you asked for)
        self.tree.column("ID", width=100, anchor="center")
        self.tree.column("Name", width=250, anchor="w")
        self.tree.column("CGPA", width=100, anchor="center")

        self.tree.grid(row=2, column=0, columnspan=3, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_rowconfigure(2, weight=1)
        
        self.refresh_table()

    # --- LOGIC METHODS ---
    def load_data(self):
        if os.path.exists(DB_FILE):
            try:
                with open(DB_FILE, 'r') as f: return json.load(f)
            except: return {}
        return {}

    def save_data(self):
        with open(DB_FILE, 'w') as f: json.dump(self.students, f, indent=4)

    def refresh_table(self):
        """Reloads all data into the table."""
        for item in self.tree.get_children(): self.tree.delete(item)
        for s_id, info in self.students.items():
            # Formatting CGPA to one decimal point
            val = info.get('cgpa', 0.0)
            display_cgpa = f"{float(val):.1f}"
            self.tree.insert("", "end", values=(s_id, info['name'], display_cgpa))

    def filter_records(self, *args):
        """Filters table based on search bar input."""
        search_term = self.search_var.get().lower()
        for item in self.tree.get_children(): self.tree.delete(item)
        
        for s_id, info in self.students.items():
            if search_term in s_id.lower() or search_term in info['name'].lower():
                val = info.get('cgpa', 0.0)
                display_cgpa = f"{float(val):.1f}"
                self.tree.insert("", "end", values=(s_id, info['name'], display_cgpa))

    def add_student(self):
        s_id = self.entry_id.get().strip()
        name = self.entry_name.get().strip()
        cgpa_val = self.entry_cgpa.get().strip()

        if not s_id or not name or not cgpa_val:
            messagebox.showwarning("Input Error", "All fields are required!")
            return

        try:
            cgpa = float(cgpa_val)
            if 0 <= cgpa <= 10:
                self.students[s_id] = {"name": name, "cgpa": round(cgpa, 1)}
                self.save_data()
                self.refresh_table()
                # Clear fields after saving
                self.entry_id.delete(0, 'end'); self.entry_name.delete(0, 'end'); self.entry_cgpa.delete(0, 'end')
                messagebox.showinfo("Success", f"Record for {name} saved!")
            else:
                messagebox.showerror("Error", "CGPA must be between 0 and 10")
        except ValueError:
            messagebox.showerror("Error", "Enter a numeric value for CGPA")

    def delete_student(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection", "Select a student to delete")
            return
        
        s_id = str(self.tree.item(selected[0])['values'][0])
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this record?"):
            if s_id in self.students:
                del self.students[s_id]
                self.save_data()
                self.refresh_table()

if __name__ == "__main__":
    app = ModernStudentSystem()
    app.mainloop()