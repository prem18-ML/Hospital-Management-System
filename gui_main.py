import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from admin import Admin, Appointment
from doctor import Doctor
from patient import Patient


class HospitalGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Management System")
        self.root.geometry("1000x600")

        # --- data setup (same as console main) ---
        self.admin = Admin('admin', '123', 'B1 1AB')

        self.doctors = [
            Doctor('John', 'Smith', 'Internal Med.'),
            Doctor('Jone', 'Smith', 'Pediatrics'),
            Doctor('Jone', 'Carlos', 'Cardiology')
        ]

        try:
            self.patients = self.admin.load_patients_from_file('patients.txt')
            if not self.patients:
                raise FileNotFoundError
        except (FileNotFoundError, Exception):
            self.patients = [
                Patient('Sara', 'Smith', 20, '07012345678', 'B1 234'),
                Patient('Mike', 'Jones', 37, '07555551234', 'L2 2AB'),
                Patient('Daivd', 'Smith', 15, '07123456789', 'C1 ABC')
            ]

        # link any loaded patients to doctors based on stored doctor name
        doctor_lookup = {d.full_name(): d for d in self.doctors}
        for p in self.patients:
            doc_name = p.get_doctor()
            if doc_name in doctor_lookup:
                doctor_lookup[doc_name].add_patient(p)

        self.discharged_patients = []
        self.appointments = []

        # frames
        self.login_frame = None
        self.main_frame = None
        self.nav_frame = None
        self.content_frame = None

        self.build_login_screen()

    # ==================== LOGIN ====================

    def build_login_screen(self):
        self.login_frame = ttk.Frame(self.root, padding=20)
        self.login_frame.pack(expand=True)

        ttk.Label(self.login_frame, text="Admin Login", font=("Arial", 18)).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(self.login_frame, text="Username:").grid(row=1, column=0, sticky="e", pady=5)
        ttk.Label(self.login_frame, text="Password:").grid(row=2, column=0, sticky="e", pady=5)

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        ttk.Entry(self.login_frame, textvariable=self.username_var).grid(row=1, column=1, pady=5)
        ttk.Entry(self.login_frame, textvariable=self.password_var, show="*").grid(row=2, column=1, pady=5)

        ttk.Button(self.login_frame, text="Login", command=self.handle_login).grid(row=3, column=0, columnspan=2, pady=10)

    def handle_login(self):
        username = self.username_var.get()
        password = self.password_var.get()

        if self.admin.check_credentials(username, password):
            self.login_frame.destroy()
            self.build_main_ui()
        else:
            messagebox.showerror("Login failed", "Incorrect username or password")

    # ==================== MAIN LAYOUT ====================

    def build_main_ui(self):
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(expand=True, fill="both")

        self.nav_frame = ttk.Frame(self.main_frame, width=200)
        self.nav_frame.pack(side="left", fill="y", padx=5, pady=5)

        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(side="right", expand=True, fill="both", padx=5, pady=5)

        ttk.Label(self.nav_frame, text="Menu", font=("Arial", 14)).pack(pady=10)

        buttons = [
            ("Doctors", self.show_doctors),
            ("Patients", self.show_patients),
            ("Discharged", self.show_discharged),
            ("Assign Doctor", self.show_assign),
            ("Relocate Patient", self.show_relocate),
            ("Appointments", self.show_appointments),
            ("Families (Surname)", self.show_families),
            ("Reports", self.show_reports),
            ("Admin Details", self.show_admin_details),
            ("Save & Quit", self.save_and_quit)
        ]

        for text, cmd in buttons:
            ttk.Button(self.nav_frame, text=text, command=cmd).pack(fill="x", pady=3)

        self.show_doctors()

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    # ==================== DOCTORS ====================

    def show_doctors(self):
        self.clear_content()
        ttk.Label(self.content_frame, text="Doctors", font=("Arial", 16)).pack(pady=10)

        cols = ("name", "speciality", "experience")
        self.doctor_tree = ttk.Treeview(self.content_frame, columns=cols, show="headings")
        self.doctor_tree.heading("name", text="Full Name")
        self.doctor_tree.heading("speciality", text="Speciality")
        self.doctor_tree.heading("experience", text="Experience (yrs)")
        self.doctor_tree.pack(expand=True, fill="both", pady=5)

        self.refresh_doctor_tree()

        btn_frame = ttk.Frame(self.content_frame)
        btn_frame.pack(pady=5)

        ttk.Button(btn_frame, text="Add Doctor", command=self.add_doctor_window).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Edit Selected", command=self.edit_doctor_window).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Delete Selected", command=self.delete_doctor).grid(row=0, column=2, padx=5)

    def refresh_doctor_tree(self):
        for item in self.doctor_tree.get_children():
            self.doctor_tree.delete(item)
        for idx, d in enumerate(self.doctors):
            self.doctor_tree.insert("", "end", iid=str(idx),
                                    values=(d.full_name(), d.get_speciality(), d.get_experience()))

    def add_doctor_window(self):
        win = tk.Toplevel(self.root)
        win.title("Add Doctor")

        ttk.Label(win, text="First Name:").grid(row=0, column=0, sticky="e", pady=5, padx=5)
        ttk.Label(win, text="Surname:").grid(row=1, column=0, sticky="e", pady=5, padx=5)
        ttk.Label(win, text="Speciality:").grid(row=2, column=0, sticky="e", pady=5, padx=5)
        ttk.Label(win, text="Experience (years):").grid(row=3, column=0, sticky="e", pady=5, padx=5)

        fn_var = tk.StringVar()
        sn_var = tk.StringVar()
        spec_var = tk.StringVar()
        exp_var = tk.StringVar(value="5")

        ttk.Entry(win, textvariable=fn_var).grid(row=0, column=1, pady=5, padx=5)
        ttk.Entry(win, textvariable=sn_var).grid(row=1, column=1, pady=5, padx=5)
        ttk.Entry(win, textvariable=spec_var).grid(row=2, column=1, pady=5, padx=5)
        ttk.Entry(win, textvariable=exp_var).grid(row=3, column=1, pady=5, padx=5)

        def save():
            try:
                exp = int(exp_var.get())
            except ValueError:
                messagebox.showerror("Error", "Experience must be a number")
                return
            d = Doctor(fn_var.get(), sn_var.get(), spec_var.get(), exp)
            self.doctors.append(d)
            self.refresh_doctor_tree()
            win.destroy()

        ttk.Button(win, text="Save", command=save).grid(row=4, column=0, columnspan=2, pady=10)

    def edit_doctor_window(self):
        sel = self.doctor_tree.focus()
        if not sel:
            messagebox.showwarning("Select", "Please select a doctor to edit.")
            return
        idx = int(sel)
        doctor = self.doctors[idx]

        win = tk.Toplevel(self.root)
        win.title("Edit Doctor")

        ttk.Label(win, text="First Name:").grid(row=0, column=0, sticky="e", pady=5, padx=5)
        ttk.Label(win, text="Surname:").grid(row=1, column=0, sticky="e", pady=5, padx=5)
        ttk.Label(win, text="Speciality:").grid(row=2, column=0, sticky="e", pady=5, padx=5)
        ttk.Label(win, text="Experience (years):").grid(row=3, column=0, sticky="e", pady=5, padx=5)

        fn_var = tk.StringVar(value=doctor.get_first_name())
        sn_var = tk.StringVar(value=doctor.get_surname())
        spec_var = tk.StringVar(value=doctor.get_speciality())
        exp_var = tk.StringVar(value=str(doctor.get_experience()))

        ttk.Entry(win, textvariable=fn_var).grid(row=0, column=1, pady=5, padx=5)
        ttk.Entry(win, textvariable=sn_var).grid(row=1, column=1, pady=5, padx=5)
        ttk.Entry(win, textvariable=spec_var).grid(row=2, column=1, pady=5, padx=5)
        ttk.Entry(win, textvariable=exp_var).grid(row=3, column=1, pady=5, padx=5)

        def save():
            try:
                exp = int(exp_var.get())
            except ValueError:
                messagebox.showerror("Error", "Experience must be a number")
                return
            doctor.set_first_name(fn_var.get())
            doctor.set_surname(sn_var.get())
            doctor.set_speciality(spec_var.get())
            doctor._Doctor__experience = exp  # quick update
            self.refresh_doctor_tree()
            win.destroy()

        ttk.Button(win, text="Save", command=save).grid(row=4, column=0, columnspan=2, pady=10)

    def delete_doctor(self):
        sel = self.doctor_tree.focus()
        if not sel:
            messagebox.showwarning("Select", "Please select a doctor to delete.")
            return
        idx = int(sel)
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this doctor?"):
            self.doctors.pop(idx)
            self.refresh_doctor_tree()

    # ==================== PATIENTS ====================

    def show_patients(self):
        self.clear_content()
        ttk.Label(self.content_frame, text="Patients", font=("Arial", 16)).pack(pady=10)

        cols = ("name", "doctor", "age", "mobile", "postcode", "symptoms")
        self.patient_tree = ttk.Treeview(self.content_frame, columns=cols, show="headings")
        for c in cols:
            self.patient_tree.heading(c, text=c.capitalize())
        self.patient_tree.pack(expand=True, fill="both", pady=5)

        self.refresh_patient_tree()

        btn_frame = ttk.Frame(self.content_frame)
        btn_frame.pack(pady=5)

        ttk.Button(btn_frame, text="Add Patient", command=self.add_patient_window).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Discharge Selected", command=self.discharge_patient).grid(row=0, column=1, padx=5)

    def refresh_patient_tree(self):
        """Refresh the patient table (Patients tab)."""
        if not hasattr(self, "patient_tree"):
            return

        for item in self.patient_tree.get_children():
            self.patient_tree.delete(item)

        for idx, p in enumerate(self.patients):
            symptoms_str = "; ".join(p.get_symptoms())
            self.patient_tree.insert(
                "", "end", iid=str(idx),
                values=(p.full_name(), p.get_doctor(), p.get_age(),
                        p.get_mobile(), p.get_postcode(), symptoms_str)
            )

    def add_patient_window(self):
        win = tk.Toplevel(self.root)
        win.title("Add Patient")

        labels = ["First Name", "Surname", "Age", "Mobile", "Postcode", "Symptoms (separate with ';')"]
        vars_ = [tk.StringVar() for _ in labels]

        for i, label in enumerate(labels):
            ttk.Label(win, text=label + ":").grid(row=i, column=0, sticky="e", pady=5, padx=5)
            ttk.Entry(win, textvariable=vars_[i]).grid(row=i, column=1, pady=5, padx=5)

        def save():
            try:
                age = int(vars_[2].get())
            except ValueError:
                messagebox.showerror("Error", "Age must be a number")
                return

            p = Patient(vars_[0].get(), vars_[1].get(), age, vars_[3].get(), vars_[4].get())
            symptoms_text = vars_[5].get().strip()
            if symptoms_text:
                for s in symptoms_text.split(";"):
                    s = s.strip()
                    if s:
                        p.add_symptom(s)
            self.patients.append(p)
            self.refresh_patient_tree()
            win.destroy()

        ttk.Button(win, text="Save", command=save).grid(row=len(labels), column=0, columnspan=2, pady=10)

    def discharge_patient(self):
        sel = self.patient_tree.focus()
        if not sel:
            messagebox.showwarning("Select", "Please select a patient to discharge.")
            return
        idx = int(sel)
        patient = self.patients.pop(idx)
        self.discharged_patients.append(patient)
        for d in self.doctors:
            d.remove_patient(patient)
        self.refresh_patient_tree()
        messagebox.showinfo("Discharged", "Patient discharged.")

    # ==================== DISCHARGED ====================

    def show_discharged(self):
        self.clear_content()
        ttk.Label(self.content_frame, text="Discharged Patients", font=("Arial", 16)).pack(pady=10)

        cols = ("name", "doctor", "age", "mobile", "postcode")
        tree = ttk.Treeview(self.content_frame, columns=cols, show="headings")
        for c in cols:
            tree.heading(c, text=c.capitalize())
        tree.pack(expand=True, fill="both", pady=5)

        for p in self.discharged_patients:
            tree.insert("", "end",
                        values=(p.full_name(), p.get_doctor(), p.get_age(), p.get_mobile(), p.get_postcode()))

    # ==================== ASSIGN / RELOCATE ====================

    def show_assign(self):
        """Screen to assign a doctor to a patient."""
        self.clear_content()
        ttk.Label(self.content_frame, text="Assign Doctor to Patient", font=("Arial", 16)).pack(pady=10)

        frame = ttk.Frame(self.content_frame)
        frame.pack(expand=True, fill="both")

        ttk.Label(frame, text="Patients").grid(row=0, column=0, pady=5)
        p_cols = ("name", "doctor")
        self.assign_patient_tree = ttk.Treeview(frame, columns=p_cols, show="headings", height=10)
        for c in p_cols:
            self.assign_patient_tree.heading(c, text=c.capitalize())
        self.assign_patient_tree.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        ttk.Label(frame, text="Doctors").grid(row=0, column=1, pady=5)
        d_cols = ("name", "speciality")
        self.assign_doctor_tree = ttk.Treeview(frame, columns=d_cols, show="headings", height=10)
        for c in d_cols:
            self.assign_doctor_tree.heading(c, text=c.capitalize())
        self.assign_doctor_tree.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        self.refresh_assign_lists()

        ttk.Button(
            self.content_frame,
            text="Assign Selected Doctor to Selected Patient",
            command=self.assign_selected
        ).pack(pady=10)

    def refresh_assign_lists(self):
        for item in self.assign_patient_tree.get_children():
            self.assign_patient_tree.delete(item)
        for idx, p in enumerate(self.patients):
            self.assign_patient_tree.insert(
                "", "end", iid=str(idx),
                values=(p.full_name(), p.get_doctor())
            )

        for item in self.assign_doctor_tree.get_children():
            self.assign_doctor_tree.delete(item)
        for idx, d in enumerate(self.doctors):
            self.assign_doctor_tree.insert(
                "", "end", iid=str(idx),
                values=(d.full_name(), d.get_speciality())
            )

    def assign_selected(self):
        """Assign selected doctor to selected patient (and update all data)."""
        p_sel = self.assign_patient_tree.focus()
        d_sel = self.assign_doctor_tree.focus()

        if not p_sel or not d_sel:
            messagebox.showwarning("Select", "Select both a patient and a doctor.")
            return

        p_idx = int(p_sel)
        d_idx = int(d_sel)

        patient = self.patients[p_idx]
        doctor = self.doctors[d_idx]

        for d in self.doctors:
            d.remove_patient(patient)

        doctor.add_patient(patient)
        patient.link(doctor.full_name())

        self.refresh_assign_lists()
        self.refresh_patient_tree()

        messagebox.showinfo("Assigned", f"{patient.full_name()} assigned to {doctor.full_name()}.")

    def show_relocate(self):
        """Screen for relocating a patient (same logic as assign)."""
        self.show_assign()
        for child in self.content_frame.winfo_children():
            if isinstance(child, ttk.Button) and "Assign Selected Doctor" in child.cget("text"):
                child.config(text="Relocate Selected Patient")

    # ==================== APPOINTMENTS ====================

    def show_appointments(self):
        self.clear_content()
        ttk.Label(self.content_frame, text="Appointments", font=("Arial", 16)).pack(pady=10)

        top = ttk.Frame(self.content_frame)
        top.pack(pady=5)

        ttk.Label(top, text="Doctor:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(top, text="Patient:").grid(row=0, column=2, padx=5, pady=5)
        ttk.Label(top, text="Date (YYYY-MM-DD):").grid(row=0, column=4, padx=5, pady=5)

        self.appt_doc_var = tk.StringVar()
        self.appt_pat_var = tk.StringVar()
        self.appt_date_var = tk.StringVar()

        doc_names = [d.full_name() for d in self.doctors]
        pat_names = [p.full_name() for p in self.patients]

        self.doc_combo = ttk.Combobox(top, textvariable=self.appt_doc_var, values=doc_names, state="readonly")
        self.doc_combo.grid(row=0, column=1, padx=5, pady=5)

        self.pat_combo = ttk.Combobox(top, textvariable=self.appt_pat_var, values=pat_names, state="readonly")
        self.pat_combo.grid(row=0, column=3, padx=5, pady=5)

        ttk.Entry(top, textvariable=self.appt_date_var).grid(row=0, column=5, padx=5, pady=5)

        ttk.Button(top, text="Schedule", command=self.schedule_appointment_gui).grid(row=0, column=6, padx=5, pady=5)

        cols = ("date", "doctor", "patient")
        self.appt_tree = ttk.Treeview(self.content_frame, columns=cols, show="headings")
        for c in cols:
            self.appt_tree.heading(c, text=c.capitalize())
        self.appt_tree.pack(expand=True, fill="both", pady=5)

        self.refresh_appt_tree()

    def schedule_appointment_gui(self):
        """Create an Appointment object from GUI selections."""
        doc_name = self.appt_doc_var.get()
        pat_name = self.appt_pat_var.get()
        date_str = self.appt_date_var.get()

        if not doc_name or not pat_name or not date_str:
            messagebox.showwarning("Missing", "Please select doctor, patient and date.")
            return

        doctor = next((d for d in self.doctors if d.full_name() == doc_name), None)
        patient = next((p for p in self.patients if p.full_name() == pat_name), None)

        if not doctor or not patient:
            messagebox.showerror("Error", "Doctor or patient not found.")
            return

        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            messagebox.showerror("Error", "Date format must be YYYY-MM-DD.")
            return

        appt = Appointment(doctor, patient, date_obj)
        self.appointments.append(appt)
        doctor.add_appointment(appt)

        self.refresh_appt_tree()
        messagebox.showinfo("Scheduled", "Appointment scheduled.")

    def refresh_appt_tree(self):
        if not hasattr(self, "appt_tree"):
            return
        for item in self.appt_tree.get_children():
            self.appt_tree.delete(item)
        for a in self.appointments:
            self.appt_tree.insert(
                "", "end",
                values=(a.date.strftime("%Y-%m-%d"), a.doctor.full_name(), a.patient.full_name())
            )

    # ==================== FAMILIES (SURNAME GROUPING) ====================

    def show_families(self):
        from collections import defaultdict

        self.clear_content()
        ttk.Label(self.content_frame, text="Families (Grouped by Surname)", font=("Arial", 16)).pack(pady=10)

        text = tk.Text(self.content_frame, wrap="word")
        text.pack(expand=True, fill="both", pady=5)

        families = defaultdict(list)
        for p in self.patients:
            families[p.get_surname()].append(p)

        if not families:
            text.insert("end", "No patients available.\n")
        else:
            for surname, members in families.items():
                text.insert("end", f"Family: {surname}\n")
                for p in members:
                    line = f"  - {p.full_name()} | Doctor: {p.get_doctor()} | Age: {p.get_age()} | Mobile: {p.get_mobile()} | Postcode: {p.get_postcode()}\n"
                    text.insert("end", line)
                text.insert("end", "\n")

        text.config(state="disabled")

    # ==================== REPORTS ====================

    def show_reports(self):
        from collections import defaultdict

        self.clear_content()
        ttk.Label(self.content_frame, text="Management Report", font=("Arial", 16)).pack(pady=10)

        report_box = tk.Text(self.content_frame, wrap="word")
        report_box.pack(expand=True, fill="both", pady=5)

        report_box.insert("end", f"1. Total Doctors: {len(self.doctors)}\n\n")

        report_box.insert("end", "2. Patients per Doctor:\n")
        patients_per_doc = {}
        for d in self.doctors:
            count = d.get_total_patients()
            patients_per_doc[d.full_name()] = count
            report_box.insert("end", f"   - {d.full_name()}: {count}\n")
        report_box.insert("end", "\n")

        report_box.insert("end", "3. Appointments per Month per Doctor:\n")
        appts_per_month = defaultdict(lambda: defaultdict(int))
        for a in self.appointments:
            doctor_name = a.doctor.full_name()
            ym = a.date.strftime("%Y-%m")
            appts_per_month[doctor_name][ym] += 1

        if not self.appointments:
            report_box.insert("end", "   No appointments have been scheduled yet.\n\n")
        else:
            for doctor_name, months in appts_per_month.items():
                report_box.insert("end", f"   - {doctor_name}:\n")
                for ym, count in months.items():
                    report_box.insert("end", f"       {ym}: {count} appointment(s)\n")
            report_box.insert("end", "\n")

        report_box.insert("end", "4. Patients by Illness Type:\n")
        illness_count = defaultdict(int)
        for p in self.patients:
            for s in p.get_symptoms():
                illness_count[s] += 1

        if not illness_count:
            report_box.insert("end", "   No symptoms/illness data recorded yet.\n")
        else:
            for illness, count in illness_count.items():
                report_box.insert("end", f"   - {illness}: {count} patient(s)\n")

        report_box.config(state="disabled")

        ttk.Button(
            self.content_frame,
            text="Show Charts (for reports)",
            command=lambda: self.show_charts(patients_per_doc, illness_count, appts_per_month)
        ).pack(pady=10)

    def show_charts(self, patients_per_doc, illness_count, appts_per_month):
        """Draw simple bar charts in a new Tkinter window."""
        win = tk.Toplevel(self.root)
        win.title("Management Report Charts")

        canvas = tk.Canvas(win, width=900, height=600, bg="white")
        canvas.pack()

        def draw_bar_chart(x, y, width, height, data_dict, title):
            if not data_dict:
                canvas.create_text(x + width / 2, y + height / 2, text=f"No data for {title}", font=("Arial", 12))
                return

            max_value = max(data_dict.values())
            if max_value == 0:
                max_value = 1

            keys = list(data_dict.keys())
            values = list(data_dict.values())

            bar_width = max(20, width / max(len(keys) * 1.5, 1))

            canvas.create_text(x + width / 2, y + 15, text=title, font=("Arial", 12, "bold"))

            chart_bottom = y + height - 40
            chart_top = y + 40

            for i, (label, value) in enumerate(zip(keys, values)):
                bar_height = (value / max_value) * (chart_bottom - chart_top)
                bx1 = x + 20 + i * bar_width
                bx2 = bx1 + bar_width * 0.8
                by1 = chart_bottom - bar_height
                by2 = chart_bottom

                canvas.create_rectangle(bx1, by1, bx2, by2, outline="black")
                canvas.create_text((bx1 + bx2) / 2, by1 - 10, text=str(value), font=("Arial", 8))

                short_label = label
                if len(short_label) > 10:
                    short_label = short_label[:10] + "..."
                canvas.create_text((bx1 + bx2) / 2, chart_bottom + 15, text=short_label, font=("Arial", 7), angle=45)

        # Chart 1: Patients per doctor
        pd_clean = {k if k else "No doctor": v for k, v in patients_per_doc.items()}
        draw_bar_chart(20, 20, 260, 180, pd_clean, "Patients per Doctor")

        # Chart 2: Patients by illness
        draw_bar_chart(320, 20, 260, 180, illness_count, "Patients by Illness")

        # Chart 3: Appointments per month per doctor (flattened)
        flat_labels = []
        flat_counts = []
        for doctor, months in appts_per_month.items():
            for ym, count in months.items():
                flat_labels.append(f"{doctor} {ym}")
                flat_counts.append(count)
        appt_dict = dict(zip(flat_labels, flat_counts))
        draw_bar_chart(620, 20, 260, 180, appt_dict, "Appointments per Month/Doctor")

    # ==================== ADMIN DETAILS ====================

    def show_admin_details(self):
        self.clear_content()
        ttk.Label(self.content_frame, text="Admin Details", font=("Arial", 16)).pack(pady=10)

        frame = ttk.Frame(self.content_frame)
        frame.pack(pady=10)

        ttk.Label(frame, text="Username:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        ttk.Label(frame, text="Password:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        ttk.Label(frame, text="Address:").grid(row=2, column=0, sticky="e", padx=5, pady=5)

        username_var = tk.StringVar()
        password_var = tk.StringVar()
        address_var = tk.StringVar()

        ttk.Entry(frame, textvariable=username_var).grid(row=0, column=1, padx=5, pady=5)
        ttk.Entry(frame, textvariable=password_var, show="*").grid(row=1, column=1, padx=5, pady=5)
        ttk.Entry(frame, textvariable=address_var).grid(row=2, column=1, padx=5, pady=5)

        def save():
            if username_var.get():
                self.admin.set_username(username_var.get())
            if password_var.get():
                self.admin.set_password(password_var.get())
            if address_var.get():
                self.admin.set_address(address_var.get())
            messagebox.showinfo("Saved", "Admin details updated for this session.")

        ttk.Button(frame, text="Save Changes", command=save).grid(row=3, column=0, columnspan=2, pady=10)

    # ==================== SAVE & QUIT ====================

    def save_and_quit(self):
        self.admin.save_patients_to_file(self.patients, 'patients.txt')
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = HospitalGUI(root)
    root.mainloop()


