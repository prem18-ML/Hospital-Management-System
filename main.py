from admin import Admin
from doctor import Doctor
from patient import Patient


def main():
    """the main function to be ran when the program runs"""

    admin = Admin('admin', '123', 'B1 1AB')  # username is 'admin', password is '123'

    doctors = [
        Doctor('John', 'Smith', 'Internal Med.'),
        Doctor('Jone', 'Smith', 'Pediatrics'),
        Doctor('Jone', 'Carlos', 'Cardiology')
    ]

    try:
        patients = admin.load_patients_from_file('patients.txt')
        if not patients:
            raise FileNotFoundError
    except (FileNotFoundError, Exception):
        patients = [
            Patient('Sara', 'Smith', 20, '07012345678', 'B1 234'),
            Patient('Mike', 'Jones', 37, '07555551234', 'L2 2AB'),
            Patient('Daivd', 'Smith', 15, '07123456789', 'C1 ABC')
        ]

    appointments = []

    doctor_lookup = {d.full_name(): d for d in doctors}
    for p in patients:
        doc_name = p.get_doctor()
        if doc_name in doctor_lookup:
            doctor_lookup[doc_name].add_patient(p)

    discharged_patients = []

    while True:
        if admin.login():
            running = True
            break
        else:
            print('Incorrect username or password.')

    while running:
        print('\nChoose the operation:')
        print(' 1- Register/view/update/delete doctor')
        print(' 2- Discharge patients')
        print(' 3- View discharged patient')
        print(' 4- Assign doctor to a patient')
        print(' 5- Update admin details')
        print(' 6- Relocate Patient')
        print(' 7- Management Report')
        print(' 8- Schedule Appointment')
        print(' 9- View patients grouped by surname (family)')
        print('10- Quit')

        op = input('Option: ')

        if op == '1':
            admin.doctor_management(doctors)

        elif op == '2':
            admin.view_patient(patients)
            while True:
                op2 = input('Do you want to discharge a patient(Y/N):').lower()
                if op2 in ('yes', 'y'):
                    admin.discharge(patients, discharged_patients)
                elif op2 in ('no', 'n'):
                    break
                else:
                    print('Please answer by yes or no.')

        elif op == '3':
            admin.view_discharge(discharged_patients)

        elif op == '4':
            admin.assign_doctor_to_patient(patients, doctors)

        elif op == '5':
            admin.update_details()

        elif op == '6':
            admin.relocate_patient(patients, doctors)

        elif op == '7':
            admin.management_report(doctors, patients, appointments)
            input("Press Enter to return to the menu...")

        elif op == '8':
            admin.schedule_appointment(doctors, patients, appointments)

        elif op == '9':
            admin.view_patients_by_surname(patients)

        elif op == '10':
            print("Saving data...")
            admin.save_patients_to_file(patients, 'patients.txt')
            running = False
            print("Goodbye!")

        else:
            print('Invalid option. Try again')


if __name__ == '__main__':
    main()
