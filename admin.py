from datetime import datetime
from collections import defaultdict

from doctor import Doctor
from patient import Patient


class Appointment:
    """Simple Appointment structure used for reports and GUI"""

    def __init__(self, doctor: Doctor, patient: Patient, date):
        self.doctor = doctor
        self.patient = patient
        self.date = date

    def __str__(self):
        return f"{self.date} | {self.doctor.full_name()} | {self.patient.full_name()}"


class Admin:
    """A class that deals with the Admin operations"""

    def __init__(self, username, password, address=''):
        """
        Args:
            username (string): Username
            password (string): Password
            address (string, optional): Address Defaults to ''
        """
        self.__username = username
        self.__password = password
        self.__address = address

    # ---------- General / helper methods ----------

    def view(self, a_list):
        """Print a list of items with numeric IDs."""
        for index, item in enumerate(a_list):
            print(f'{index+1:3}|{item}')

    def login(self):
        """Console login used in main.py."""
        print("-----Login-----")
        username = input('Enter the username: ')
        password = input('Enter the password: ')
        return username == self.__username and password == self.__password

    def check_credentials(self, username, password):
        """Used by the GUI login screen."""
        return username == self.__username and password == self.__password

    def set_username(self, username):
        self.__username = username

    def set_password(self, password):
        self.__password = password

    def set_address(self, address):
        self.__address = address

    def find_index(self, index, collection):
        """Check if index is valid for a list/collection."""
        return index in range(0, len(collection))

    # ---------- Doctor management ----------

    def get_doctor_details(self):
        """Get the details needed to add a doctor (console)."""
        first_name = input("Enter First Name: ")
        surname = input("Enter Surname: ")
        speciality = input("Enter Speciality: ")
        return first_name, surname, speciality

    def doctor_management(self, doctors):
        """Registering, viewing, updating, deleting doctors (console menu)."""
        print("-----Doctor Management-----")
        print('Choose the operation:')
        print(' 1 - Register')
        print(' 2 - View')
        print(' 3 - Update')
        print(' 4 - Delete')

        op = input("Input: ")

        if op == '1':
            print("-----Register-----")
            first_name, surname, speciality = self.get_doctor_details()

            name_exists = False
            for doctor in doctors:
                if first_name == doctor.get_first_name() and surname == doctor.get_surname():
                    print('Name already exists.')
                    name_exists = True
                    break

            if not name_exists:
                doctors.append(Doctor(first_name, surname, speciality))
                print('Doctor registered.')

        elif op == '2':
            print("-----List of Doctors-----")
            print('ID |          Full name            |  Speciality')
            self.view(doctors)

        elif op == '3':
            while True:
                print("-----Update Doctor`s Details-----")
                print('ID |          Full name            |  Speciality')
                self.view(doctors)
                try:
                    index = int(input('Enter the ID of the doctor: ')) - 1
                    if self.find_index(index, doctors):
                        break
                    else:
                        print("Doctor not found")
                except ValueError:
                    print('The ID entered is incorrect')

            print('Choose the field to be updated:')
            print(' 1 First name')
            print(' 2 Surname')
            print(' 3 Speciality')
            try:
                op = int(input('Input: '))
                doctor = doctors[index]
                if op == 1:
                    new_first_name = input("Enter new first name: ")
                    doctor.set_first_name(new_first_name)
                elif op == 2:
                    new_surname = input("Enter new surname: ")
                    doctor.set_surname(new_surname)
                elif op == 3:
                    new_spec = input("Enter new speciality: ")
                    doctor.set_speciality(new_spec)
                else:
                    print("Invalid selection")
            except ValueError:
                print("Invalid input")

        elif op == '4':
            print("-----Delete Doctor-----")
            print('ID |          Full Name            |  Speciality')
            self.view(doctors)

            try:
                doctor_index = int(input('Enter the ID of the doctor to be deleted: ')) - 1
                if self.find_index(doctor_index, doctors):
                    doctors.pop(doctor_index)
                    print("Doctor deleted.")
                else:
                    print("Doctor not found.")
            except ValueError:
                print('The id entered is incorrect')

        else:
            print('Invalid operation chosen. Check your spelling!')

    # ---------- Patient viewing / assigning ----------

    def view_patient(self, patients):
        """Print a list of patients (console)."""
        print("-----View Patients-----")
        print('ID |          Full Name            |      Doctor`s Full Name       | Age |    Mobile     | Postcode ')
        self.view(patients)

    def assign_doctor_to_patient(self, patients, doctors):
        """Allow the admin to assign a doctor to a patient (console)."""
        print("-----Assign-----")
        print("-----Patients-----")
        print('ID |          Full Name            |      Doctor`s Full Name       | Age |    Mobile     | Postcode ')
        self.view(patients)

        try:
            patient_index = int(input('Please enter the patient ID: ')) - 1
            if patient_index not in range(len(patients)):
                print('The id entered was not found.')
                return
        except ValueError:
            print('The id entered is incorrect')
            return

        print("-----Doctors Select-----")
        print('Select the doctor that fits these symptoms:')
        patients[patient_index].print_symptoms()
        print('--------------------------------------------------')
        print('ID |          Full Name            |  Speciality   ')
        self.view(doctors)

        try:
            doctor_index = int(input('Please enter the doctor ID: ')) - 1
            if self.find_index(doctor_index, doctors):
                doctor = doctors[doctor_index]
                patient = patients[patient_index]
                doctor.add_patient(patient)
                patient.link(doctor.full_name())
                print('The patient is now assigned to the doctor.')
            else:
                print('The id entered was not found.')
        except ValueError:
            print('The id entered is incorrect')

    # ---------- Discharge & discharged list ----------

    def discharge(self, patients, discharge_patients):
        """Allow the admin to discharge a patient when treatment is done."""
        print("-----Discharge Patient-----")
        self.view_patient(patients)

        try:
            patient_index = int(input('Please enter the patient ID: ')) - 1
            if patient_index in range(len(patients)):
                p = patients.pop(patient_index)
                discharge_patients.append(p)
                print("Patient Discharged.")
            else:
                print("Patient not found.")
        except ValueError:
            print("Invalid ID")

    def view_discharge(self, discharged_patients):
        """Prints the list of all discharged patients."""
        print("-----Discharged Patients-----")
        print('ID |          Full Name            |      Doctor`s Full Name       | Age |    Mobile     | Postcode ')
        self.view(discharged_patients)

    # ---------- Admin details ----------

    def update_details(self):
        """Allows the user to update and change username, password and address (console)."""
        print('Choose the field to be updated:')
        print(' 1 Username')
        print(' 2 Password')
        print(' 3 Address')
        try:
            op = int(input('Input: '))

            if op == 1:
                new_username = input("Enter new username: ")
                self.__username = new_username

            elif op == 2:
                password = input('Enter the new password: ')
                if password == input('Enter the new password again: '):
                    self.__password = password
                else:
                    print('Passwords do not match.')

            elif op == 3:
                new_address = input("Enter new address: ")
                self.__address = new_address

            else:
                print("Invalid option")
        except ValueError:
            print("Invalid Input")

    # ---------- Relocate patient ----------

    def relocate_patient(self, patients, doctors):
        """Relocating patients from one doctor to another."""
        print("-----Relocate Patient-----")
        print("Select Patient to Relocate:")
        self.view_patient(patients)

        try:
            p_index = int(input("Enter Patient ID: ")) - 1
            if p_index not in range(len(patients)):
                print("Patient not found.")
                return
            patient = patients[p_index]

            print("Select New Doctor:")
            print('ID |          Full Name            |  Speciality   ')
            self.view(doctors)
            d_index = int(input("Enter New Doctor ID: ")) - 1

            if self.find_index(d_index, doctors):
                new_doctor = doctors[d_index]
                # remove patient from any current doctor
                for doc in doctors:
                    doc.remove_patient(patient)
                new_doctor.add_patient(patient)
                patient.link(new_doctor.full_name())
                print("Patient Relocated Successfully.")
            else:
                print("Doctor not found.")
        except ValueError:
            print("Invalid Input")

    # ---------- Management report ----------

    def management_report(self, doctors, patients, appointments):
        """
        Management Report (console):
        1) Total doctors
        2) Patients per doctor
        3) Appointments per month per doctor
        4) Patients by illness type
        """
        print("-----Management Report-----")

        # 1. Total number of doctors
        print(f"1. Total Doctors: {len(doctors)}")

        # 2. Total number of patients per doctor
        print("2. Patients per Doctor:")
        for doc in doctors:
            print(f"   - {doc.full_name()}: {doc.get_total_patients()}")
        print()

        # 3. Total number of appointments per month per doctor
        print("3. Appointments per Month per Doctor:")
        appts_per_month = defaultdict(lambda: defaultdict(int))
        for appt in appointments:
            doctor_name = appt.doctor.full_name()
            ym = appt.date.strftime("%Y-%m")
            appts_per_month[doctor_name][ym] += 1

        if not appointments:
            print("   No appointments have been scheduled yet.")
        else:
            for doctor_name, months in appts_per_month.items():
                print(f"   - {doctor_name}:")
                for ym, count in months.items():
                    print(f"       {ym}: {count} appointment(s)")
        print()

        # 4. Total number of patients based on illness type (symptoms)
        print("4. Patients by Illness Type:")
        illness_count = defaultdict(int)
        for p in patients:
            for s in p.get_symptoms():
                illness_count[s] += 1

        if not illness_count:
            print("   No symptoms/illness data recorded yet.")
        else:
            for illness, count in illness_count.items():
                print(f"   - {illness}: {count} patient(s)")
        print()

        return illness_count, appts_per_month

    # ---------- File save/load ----------

    def save_patients_to_file(self, patients, filename='patients.txt'):
        """Save all patient data to a file."""
        try:
            with open(filename, 'w') as f:
                for p in patients:
                    symptoms_str = ";".join(p.get_symptoms())
                    line = f"{p.get_first_name()},{p.get_surname()},{p.get_age()},{p.get_mobile()},{p.get_postcode()},{p.get_doctor()},{symptoms_str}\n"
                    f.write(line)
            print("Data Saved Successfully.")
        except Exception as e:
            print(f"Error saving file: {e}")

    def load_patients_from_file(self, filename='patients.txt'):
        """Load patient data from a file."""
        loaded_patients = []
        try:
            with open(filename, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    parts = line.split(',')
                    if len(parts) < 6:
                        continue
                    first_name, surname, age_str, mobile, postcode, doctor_name = parts[:6]
                    symptoms_str = ",".join(parts[6:])  # in case there are extra commas

                    try:
                        age = int(age_str)
                    except ValueError:
                        age = 0

                    patient = Patient(first_name, surname, age, mobile, postcode)

                    if doctor_name and doctor_name != 'None':
                        patient.link(doctor_name)

                    if symptoms_str:
                        for symptom in symptoms_str.split(';'):
                            symptom = symptom.strip()
                            if symptom:
                                patient.add_symptom(symptom)

                    loaded_patients.append(patient)
            print("Data Loaded.")
        except FileNotFoundError:
            print("No save file found.")
        except Exception as e:
            print(f"Error loading file: {e}")
        return loaded_patients

    # ---------- Grouping by surname ----------

    def view_patients_by_surname(self, patients):
        """View patients grouped by family (surname) in the console."""
        print("-----Patients Grouped by Surname (Family)-----")
        if not patients:
            print("No patients to display.")
            return

        families = defaultdict(list)
        for p in patients:
            families[p.get_surname()].append(p)

        for surname, members in families.items():
            print(f"\nFamily: {surname}")
            print('ID |          Full Name            |      Doctor`s Full Name       | Age |    Mobile     | Postcode ')
            for idx, patient in enumerate(members, start=1):
                print(f"{idx:3}|{patient}")
        print()

    # ---------- Schedule appointment (console) ----------

    def schedule_appointment(self, doctors, patients, appointments):
        """Create a new appointment between a doctor and a patient (console)."""
        print("-----Schedule Appointment-----")
        if not doctors:
            print("No doctors available.")
            return
        if not patients:
            print("No patients available.")
            return

        print("Select Patient:")
        self.view_patient(patients)
        try:
            p_index = int(input("Enter Patient ID: ")) - 1
            if p_index not in range(len(patients)):
                print("Patient not found.")
                return
        except ValueError:
            print("Invalid input.")
            return
        patient = patients[p_index]

        print("Select Doctor:")
        print('ID |          Full Name            |  Speciality   ')
        self.view(doctors)
        try:
            d_index = int(input("Enter Doctor ID: ")) - 1
            if d_index not in range(len(doctors)):
                print("Doctor not found.")
                return
        except ValueError:
            print("Invalid input.")
            return
        doctor = doctors[d_index]

        date_str = input("Enter appointment date (YYYY-MM-DD): ")
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.")
            return

        appointment = Appointment(doctor, patient, date_obj)
        appointments.append(appointment)
        doctor.add_appointment(appointment)
        print("Appointment scheduled:")
        print(appointment)

