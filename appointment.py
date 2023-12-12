
# This is a program made for JOjo's SALON that works for different tasks for him
# like scheduling appointments, cancelling appointments, displaying the slots booked and available.
# and save the appointments booked in a file for keeping a directory for the SALON
 

# PROGRAM MADE BY: Nishchay Aggarwal
#                   AMANULLAH
#                   DEERGHA



import csv
import os

class Appointment:
    def __init__(self, day_of_week, start_time_hour):
        self.client_name = ""
        self.client_phone = ""
        self.appt_type = 0
        self.day_of_week = day_of_week
        self.start_time_hour = start_time_hour

    def get_client_name(self):
        return self.client_name

    def get_client_phone(self):
        return self.client_phone

    def get_appt_type(self):
        return self.appt_type

    def get_day_of_week(self):
        return self.day_of_week

    def get_start_time_hour(self):
        return self.start_time_hour

    def get_end_time_hour(self):
        return self.start_time_hour + 1

    def get_appt_type_desc(self):
        appt_type_dict = {
            0: "Available",
            1: "Mens Cut",
            2: "Ladies Cut",
            3: "Mens Colouring",
            4: "Ladies Colouring"
        }
        return appt_type_dict.get(self.appt_type, "Invalid")

    def set_client_name(self, name):
        self.client_name = name

    def set_client_phone(self, phone):
        self.client_phone = phone

    def set_appt_type(self, appt_type):
        self.appt_type = appt_type

    def schedule(self, name, phone, appt_type):
        self.set_client_name(name)
        self.set_client_phone(phone)
        self.set_appt_type(appt_type)

    def cancel(self):
        self.set_client_name("")
        self.set_client_phone("")
        self.set_appt_type(0)

    def format_record(self):
        return f"{self.client_name},{self.client_phone},{self.appt_type},{self.day_of_week},{self.start_time_hour:02d}"

    def __str__(self):
        return f"{self.client_name.ljust(20)} {self.client_phone.ljust(15)} {self.day_of_week.ljust(10)} " \
               f"{self.start_time_hour:02d}:00 - {self.get_end_time_hour():02d}:00 {self.get_appt_type_desc()}"
   

def create_weekly_calendar():    #Create a weekly calendar with available appointment slots.
#- calendar: List of Appointment objects representing the weekly calendar.
    calendar = []
    for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]:
        for hour in range(9, 17):
            appointment = Appointment(day, hour)
            calendar.append(appointment)
    return calendar

def load_scheduled_appointments(calendar, input_filename):#    Load previously scheduled appointments from a file and update the calendar.
    #                                                       - calendar: List of Appointment objects representing the weekly calendar.
    #- input_filename: The name of the file containing scheduled appointments.

    #Returns: None


    while True:   # Prompt the user to load previously scheduled appointments from a file
        load_previous = input("Would you like to load previously scheduled appointments from a file (Y/N)? ").lower()
        current_directory = os.path.dirname(__file__)
        if load_previous == 'y':
            filename = input("Enter appointment filename: ")
            user_filename = os.path.join(current_directory, filename)

            if os.path.isfile(user_filename):  # Load appointments from the specified file and update the calendar
                with open(user_filename, 'r') as file:
                    reader = csv.reader(file)
                    loaded_appointments = 0
                    for row in reader:
                        day_of_week, start_time_hour = row[3], int(row[4])
                        appointment = find_appointment_by_time(day_of_week, start_time_hour, calendar)
                        if appointment:
                            appointment.schedule(row[0], row[1], int(row[2]))
                            loaded_appointments += 1

                    if loaded_appointments > 0:
                        print(f"{loaded_appointments} previously scheduled appointments have been loaded")
                        break
                    else:
                        print("No appointments found in the file.")
            else:
                print(f"File {user_filename} not found. Re-enter the appointment filename.")
        else:
            break


def validate_day(day):
    valid_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    return day.capitalize() in valid_days

def validate_hour(hour):
    return 0 <= hour < 24

def find_appointment_by_time(day, start_hour, calendar):
    for appointment in calendar:
        if appointment.get_day_of_week().lower() == day.lower() and \
           appointment.get_start_time_hour() == start_hour:
            return appointment
    return None

def show_appointments_by_name(name, calendar):
    print(f"\nAppointments for {name}\n")
    print("{:20s}{:15s}{:10s}{:10s}{:10s}{:20s}".format("Client Name", "Phone", "Day", "Start", "End", "Type"))
    print("-" * 73)
    for appointment in calendar:
        if appointment.get_client_name().lower().find(name.lower()) != -1:
            print(appointment)

def show_appointments_by_day(day, calendar):
    print(f"\nAppointments for {day}\n")
    print("{:20s}{:15s}{:10s}{:10s}{:10s}{:20s}".format("Client Name", "Phone", "Day", "Start", "End", "Type"))
    print("-" * 73)
    for appointment in calendar:
        if appointment.get_day_of_week().lower() == day.lower():
            print(appointment)

def print_menu():
    print("\nJojo's Hair Salon Appointment Manager")
    print("=" * 37)
    print(" 1) Schedule an appointment\n 2) Find appointment by name\n 3) Print calendar for a specific day\n 4) Cancel an appointment\n 9) Exit the system")

def save_scheduled_appointments(filename, calendar):
    try:
        current_directory = os.path.dirname(__file__)
        abs_path = os.path.join(current_directory, filename)

        if os.path.isfile(abs_path):
            overwrite = input("The file already exists. Do you want to overwrite it? (Y/N): ").lower()
            if overwrite == 'n':
                filename = input("Enter Appointment Filename: ")
                abs_path = os.path.join(current_directory, filename)
                with open(abs_path, 'w', newline='') as file:
                    writer = csv.writer(file)
                    for appointment in calendar:
                        if appointment.get_appt_type() != 0:
                            writer.writerow(appointment.format_record().split(','))
                print(f"Appointments successfully saved to file: {abs_path}")
                return
        with open(abs_path, 'w', newline='') as file:
            writer = csv.writer(file)  # Save appointments to the specified file
            for appointment in calendar:
                if appointment.get_appt_type() != 0:
                    writer.writerow(appointment.format_record().split(','))
        print(f"Appointments successfully saved to file: {abs_path}")
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    print("Starting the Appointment Manager System")
    print("Weekly calendar created")

    calendar = create_weekly_calendar()
    load_scheduled_appointments(calendar, "appointments.csv")

    while True:
        print_menu()
        choice = input("Enter your selection: ")

        if choice == '1':
            print("\n** Schedule an appointment **")
            day = input("What day: ")
            if day.lower() == 'sunday':
                print("Sorry, Sunday is not available for appointments.")
                continue

            start_hour = int(input("Enter start hour (24-hour clock): "))
            if not validate_day(day) or not validate_hour(start_hour):
                print("Invalid day or hour. Please enter valid values.")
                continue

            appointment = find_appointment_by_time(day, start_hour, calendar)

            if appointment and appointment.get_appt_type() == 0:
                client_name = input("Client Name: ")
                client_phone = input("Client Phone: ")
                print("Appointment types\n1: Mens Cut $50, 2: Ladies Cut $80, 3: Mens Colouring $50, 4: Ladies Colouring $120")
                appt_type = int(input("Type 1 of Appointment: "))
                if appt_type not in [1, 2, 3, 4]:
                    while appt_type not in [1, 2, 3, 4]:
                        print("Invalid Entry")
                        print("Appointment  types\n1: Mens Cut $50, 2: Ladies Cut $80, 3: Mens Colouring $50, 4: Ladies Colouring $120")
                        appt_type = int(input("Type 1 of Appointment: "))

                
                appointment.schedule(client_name, client_phone, appt_type)
                print(f"OK, {client_name}'s appointment is scheduled!")
            elif appointment:
                print("Sorry, that time slot is already booked.")
            else:
                print("Sorry, that time slot is not in the weekly calendar!")

        elif choice == '2':
            print("\n** Find appointment by name **") # Find appointment by name
            name = input("Enter Client Name: ")
            show_appointments_by_name(name, calendar)

        elif choice == '3': # Print calendar for a specific day
            print("\n** Print calendar for a specific day **")
            while True:
                day = input("Enter day of week: ")
                if validate_day(day):
                    show_appointments_by_day(day, calendar)
                    break
                else:
                    print("Invalid day. Please enter a valid day.")

        elif choice == '4': # Cancel an appointment
            print("\n** Cancel an appointment **")
            while True:
                day = input("What day: ")
                if day.lower() == 'sunday':
                    print("Sorry, Sunday is not available for appointments.")
                    continue

                start_hour = int(input("Enter start hour (24-hour clock): "))
                if validate_day(day) and validate_hour(start_hour):
                    appointment = find_appointment_by_time(day, start_hour, calendar)
                    if appointment:
                        if appointment.get_appt_type() != 0:
                            print(f"Appointment: {day} {start_hour:02d}:00 - {appointment.get_end_time_hour():02d}:00 for {appointment.get_client_name()} has been cancelled!")
                            appointment.cancel()
                        else:
                            print("That time slot isn't booked and doesn't need to be cancelled")
                        break
                    else:
                        print("Sorry, that time slot is not in the weekly calendar!")
                else:
                    print("Invalid day or hour. Please enter valid values.")

        elif choice == '9':
            print("\n** Exit the system **")  # Exit the system
            save = input("Would you like to save all scheduled appointments to a file (Y/N)? ").lower()
            if save == 'y':
                filename = input("Enter appointment filename: ")
                save_scheduled_appointments(filename, calendar)
                print(f"{len([a for a in calendar if a.get_appt_type() != 0])} scheduled appointments have been successfully saved")
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()



