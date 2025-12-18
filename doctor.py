from typing import List


class Doctor:
    """A class that deals with the Doctor operations"""

    def __init__(self, first_name: str, surname: str, speciality: str, experience: int = 5):
        """
        Args:
            first_name (string): First name
            surname (string): Surname
            speciality (string): Doctor`s speciality
            experience (int): Years of experience
        """
        self.__first_name = first_name
        self.__surname = surname
        self.__speciality = speciality
        self.__experience = experience
        self.__patients: List["Patient"] = []
        self.__appointments: List["Appointment"] = []

    def full_name(self) -> str:
        return f"{self.__first_name} {self.__surname}"

    def get_first_name(self) -> str:
        return self.__first_name

    def set_first_name(self, new_first_name: str) -> None:
        self.__first_name = new_first_first_name

    def get_surname(self) -> str:
        return self.__surname

    def set_surname(self, new_surname: str) -> None:
        self.__surname = new_surname

    def get_speciality(self) -> str:
        return self.__speciality

    def set_speciality(self, new_speciality: str) -> None:
        self.__speciality = new_speciality

    def get_experience(self) -> int:
        return self.__experience

    def add_patient(self, patient: "Patient") -> None:
        if patient not in self.__patients:
            self.__patients.append(patient)

    def remove_patient(self, patient: "Patient") -> None:
        if patient in self.__patients:
            self.__patients.remove(patient)

    def get_patients(self):
        return self.__patients

    def get_total_patients(self) -> int:
        return len(self.__patients)

    def add_appointment(self, appointment: "Appointment") -> None:
        self.__appointments.append(appointment)

    def get_appointments(self):
        return self.__appointments

    def __str__(self) -> str:
        return f'{self.full_name():^30}|{self.__speciality:^15}'

