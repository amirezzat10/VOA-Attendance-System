# tab1.py
import pandas as pd
import json
from PyQt5.QtWidgets import QWidget, QDateEdit, QLabel, QPushButton, QTableView, QVBoxLayout, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QStandardItemModel, QStandardItem


class Attendance(QWidget):
    def __init__(self):
        super(Attendance, self).__init__()

        self.attendanceDate = QDateEdit(self)
        self.attendance_date_lbl = QLabel(self)
        self.attendance_text_lbl = QLabel(self)
        self.attendance_text_edit = QLineEdit(self)
        self.attendance_date_btn = QPushButton(self)
        self.attendance_text_btn = QPushButton(self)
        self.attendance_excuse_btn = QPushButton(self)
        self.attendanceTable = QTableView(self)

        self.setup_ui()

        # Create the model once during initialization
        self.model = QStandardItemModel(self)
        self.model.setHorizontalHeaderLabels(["Name", "Serial Number"])
        self.attendanceTable.setModel(self.model)

        # Make the table view read-only
        self.attendanceTable.setEditTriggers(QTableView.NoEditTriggers)

        # Set the initial date to today's date
        self.attendanceDate.setDate(QDate.currentDate())

        # Connect the signal to the function
        self.attendance_date_btn.clicked.connect(self.handle_print_date)

        self.attendance_text_btn.clicked.connect(self.add_person)

        try:
            # Read Excel file
            print("Reading Excel file from:", "Data/attendance.xlsx")
            self.df = pd.read_excel("Data/attendance.xlsx")
        except Exception as e:
            print("Error reading Excel file:", e)


    def setup_ui(self):
        self.attendance_date_lbl.setText("Enter Date:")
        self.attendance_date_lbl.setGeometry(0, 10, 65, 13)

        self.attendanceDate.setGeometry(75, 10, 110, 22)

        self.attendance_date_btn.setText("Add Date")
        self.attendance_date_btn.setGeometry(190, 10, 100, 23)

        self.attendance_text_lbl.setText("Serial Number: ")
        self.attendance_text_lbl.setGeometry(0, 50, 100, 21)

        self.attendance_text_edit.setGeometry(85, 50, 113, 20)

        self.attendance_text_btn.setText("Add")
        self.attendance_text_btn.setGeometry(205, 50, 75, 23)

        self.attendance_excuse_btn.setText("Add Excuse")
        self.attendance_excuse_btn.setGeometry(285, 50, 110, 23)

        self.remove_row_btn = QPushButton(self)
        self.remove_row_btn.setText("Remove Selected Row")
        self.remove_row_btn.setGeometry(400, 50, 180, 23)
        self.remove_row_btn.clicked.connect(self.remove_selected_row)

        self.attendance_text_edit.returnPressed.connect(self.add_person)

        self.attendance_excuse_btn.clicked.connect(self.attendance_excuse_btn_clicked)



        # Create an invisible QLabel for displaying the entered date
        self.date_display_label = QLabel(self)
        self.date_display_label.setGeometry(310, 10, 150, 22)
        self.date_display_label.setVisible(False)  # Initially invisible

        # Set up the table model with two columns
        model = QStandardItemModel(self)
        model.setHorizontalHeaderLabels(["Name", "Serial Number"])

        # Set up the table view with the model
        self.attendanceTable.setModel(model)
        self.attendanceTable.setGeometry(0, 80, 671, 221)

        # Set equal stretch factors for both columns
        header = self.attendanceTable.horizontalHeader()
        header.setSectionResizeMode(0, header.Stretch)
        header.setSectionResizeMode(1, header.Stretch)

    def handle_print_date(self):
        # Retrieve the date from the QDateEdit
        selected_date = self.attendanceDate.date()

        # Check if the date is valid
        if not selected_date.isValid():
            # Invalid date, hide the label
            self.date_display_label.clear()
            self.date_display_label.setVisible(False)
            return

        # Show the date in the QLabel
        self.date_display_label.setText(selected_date.toString(Qt.ISODate))
        self.date_display_label.setVisible(True)  # Make the label visible

        # Check if the selected date column already exists in the DataFrame
        selected_date_str = selected_date.toString(Qt.ISODate)
        if selected_date_str in self.df.columns:
            print(f"Column '{selected_date_str}' already exists in the Excel sheet.")

        else:
            # Clear the model of the attendanceTable
            self.model.clear()

            # Set up the table view with a new model
            self.model = QStandardItemModel(self)
            self.model.setHorizontalHeaderLabels(["Name", "Serial Number"])


            self.attendanceTable.setModel(self.model)
            self.attendanceTable.setGeometry(0, 80, 671, 221)

            # Set equal stretch factors for both columns
            header = self.attendanceTable.horizontalHeader()
            header.setSectionResizeMode(0, header.Stretch)
            header.setSectionResizeMode(1, header.Stretch)

            # Make the table view read-only
            self.attendanceTable.setEditTriggers(QTableView.NoEditTriggers)

            # Add a new column with the selected date to the DataFrame
            self.df[selected_date_str] = ""

            try:
                # Save Excel file
                print("Saving Excel file to:", "Data/attendance.xlsx")
                self.df.to_excel("Data/attendance.xlsx", index=False)
            except Exception as e:
                print("Error saving Excel file:", e)

    def add_person(self):
        try:
            # Check if a valid date is selected
            if not self.date_display_label.isVisible():
                # No date entered, show a message box
                msg_box = QMessageBox(self)
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setWindowTitle("Enter Date First")
                msg_box.setText("Please enter a date first.")
                msg_box.exec_()
                return

            # Retrieve the entered value
            input_value = self.attendance_text_edit.text()

            # Check if the person is already in the table view
            if self.is_person_already_entered(input_value):
                # Person is already entered, show a message box
                msg_box = QMessageBox(self)
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setWindowTitle("Duplicate Entry")
                msg_box.setText(f"The person with name or serial number '{input_value}' is already entered.")
                msg_box.exec_()
                self.attendance_text_edit.clear()
                return

            # Load the JSON data from the file
            with open("Data/data.json", "r", encoding="utf-8") as file:
                json_data = json.load(file)

            if self.is_serial_number_in_json(input_value):
                self.add_person_by_serial_number(input_value)
            else:
                self.add_person_by_name(input_value)

            # Scroll down to the last entered person
            last_row_index = self.model.rowCount() - 1
            self.attendanceTable.scrollToBottom()

            # Clear the text in the QLineEdit after adding the person
            self.attendance_text_edit.clear()
        except Exception as e:
            print(f"An error occurred in handle_absences_more_than_3: {str(e)}")
            # Print the traceback for more details
            import traceback
            traceback.print_exc()

    def is_person_already_entered(self, value):
        # Check if the person is already in the table view
        for row in range(self.model.rowCount()):
            if self.model.item(row, 0) and self.model.item(row, 0).text() == value:
                return True
            if self.model.item(row, 1) and self.model.item(row, 1).text() == value:
                return True
        return False

    def add_person_by_serial_number(self, serial_number):
        # Check if the serial number exists in the table view
        if self.is_person_already_entered(serial_number):
            # Person is already entered, show a message box
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("Duplicate Entry")
            msg_box.setText(f"The person with serial number '{serial_number}' is already entered.")
            msg_box.exec_()
            self.attendance_text_edit.clear()

            return

        # Load the JSON data from the file
        with open("Data/data.json", "r", encoding="utf-8") as file:
            json_data = json.load(file)

        # Check if the serial number exists in the JSON file
        if serial_number in json_data:
            # Serial number exists, get name from the value
            name = json_data[serial_number]["اسم المخدوم رباعى"]
            print(f"Data for serial number {serial_number}:", name.encode('utf-8'))

            # Append the new entry to the model without deleting previous ones
            self.model.appendRow([QStandardItem(name), QStandardItem(serial_number)])

            # Find the column index corresponding to the displayed date
            date_column_index = self.df.columns.get_loc(self.date_display_label.text())

            # Find the row index corresponding to the serial number
            row_index = self.df[self.df['Serial Number'] == int(serial_number)].index[0]

            # Mark '*' in the Excel sheet at the intersection of the row and column
            self.df.iat[row_index, date_column_index] = "*"

            # Save the updated DataFrame back to the Excel file
            self.df.to_excel("Data/attendance.xlsx", index=False)

        else:
            # Serial number doesn't exist, show a message box
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("Serial Number Not Found")
            msg_box.setText(f"The serial number {serial_number} doesn't exist.")
            self.attendance_text_edit.clear()
            msg_box.exec_()

    def add_person_by_name(self, name):
        # Check if the name exists in the table view
        if self.is_person_already_entered(name):
            # Person is already entered, show a message box
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("Duplicate Entry")
            msg_box.setText(f"The person with name '{name}' is already entered.")
            msg_box.exec_()
            self.attendance_text_edit.clear()
            return

        # Load the JSON data from the file
        with open("Data/data.json", "r", encoding="utf-8") as file:
            json_data = json.load(file)

        # Check if the name exists in the values of the JSON file
        for serial_number, person_data in json_data.items():
            # Perform a case-insensitive and whitespace-insensitive comparison
            if person_data["اسم المخدوم رباعى"].strip().lower() == name.strip().lower():
                print(f"Data for name {name.encode('utf-8')}:", person_data)

                # Append the new entry to the model without deleting previous ones
                self.model.appendRow([QStandardItem(name), QStandardItem(serial_number)])

                # Find the column index corresponding to the displayed date
                date_column_index = self.df.columns.get_loc(self.date_display_label.text())

                # Find the row index corresponding to the serial number
                row_index = self.df[self.df['Serial Number'] == int(serial_number)].index[0]

                # Mark '*' in the Excel sheet at the intersection of the row and column
                self.df.iat[row_index, date_column_index] = "*"

                # Save the updated DataFrame back to the Excel file
                self.df.to_excel("Data/attendance.xlsx", index=False)

                return

        # Name doesn't exist, show a message box
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("Name Not Found")
        msg_box.setText(f"The person with the name {name} doesn't exist.")
        self.attendance_text_edit.clear()
        msg_box.exec_()

    def remove_selected_row(self):
        # Get the selected indexes
        selected_indexes = self.attendanceTable.selectionModel().selectedIndexes()

        if not selected_indexes:
            # No row selected, show a message box
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("No Row Selected")
            msg_box.setText("Please select a row to delete.")
            msg_box.exec_()
            return

        # Get the row numbers of the selected indexes
        rows_to_remove = set(index.row() for index in selected_indexes)

        # Iterate over the selected rows
        for row in sorted(rows_to_remove, reverse=True):
            # Get the data from the removed row
            name_item = self.model.item(row, 0)
            serial_number_item = self.model.item(row, 1)

            if name_item and serial_number_item:
                name = name_item.text()
                serial_number = serial_number_item.text()

                # Find the column index corresponding to the displayed date
                date_column_index = self.df.columns.get_loc(self.date_display_label.text())

                # Find the row index corresponding to the serial number
                row_index = self.df[self.df['Serial Number'] == int(serial_number)].index[0]

                # Remove '*' from the Excel sheet at the intersection of the row and column
                self.df.iat[row_index, date_column_index] = ""

            # Remove rows from the model
            self.model.removeRow(row)

        # Clear the selection after removing rows
        self.attendanceTable.clearSelection()

        # Save the updated DataFrame back to the Excel file
        self.df.to_excel("Data/attendance.xlsx", index=False)

    def attendance_excuse_btn_clicked(self):
        # Check if a valid date is selected
        if not self.date_display_label.isVisible():
            # No date entered, show a message box
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("Enter Date First")
            msg_box.setText("Please enter a date first.")
            msg_box.exec_()
        # Retrieve the entered value
        input_value = self.attendance_text_edit.text()

        # Check if the person is already in the table view
        if self.is_person_already_entered(input_value):
            # Person is already entered, show a message box
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("Duplicate Entry")
            msg_box.setText(f"The person with name or serial number '{input_value}' is already entered.")
            msg_box.exec_()
            self.attendance_text_edit.clear()
            return

        # Load the JSON data from the file
        with open("Data/data.json", "r", encoding="utf-8") as file:
            json_data = json.load(file)

        # Check if the input value is a serial number
        if input_value in json_data:
            self.add_excuse_by_serial_number(input_value)
        else:
            self.add_excuse_by_name(input_value)

        # Clear the text in the QLineEdit after adding the excuse
        self.attendance_text_edit.clear()

    def add_excuse_by_serial_number(self, serial_number):
        # Check if the serial number exists in the table view
        if self.is_person_already_entered(serial_number):
            # Person is already entered, show a message box
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("Duplicate Entry")
            msg_box.setText(f"The person with serial number '{serial_number}' is already entered.")
            msg_box.exec_()
            self.attendance_text_edit.clear()
            return

        # Load the JSON data from the file
        with open("Data/data.json", "r", encoding="utf-8") as file:
            json_data = json.load(file)

        # Check if the serial number exists in the JSON file
        if serial_number in json_data:
            # Serial number exists, get name from the value
            name = json_data[serial_number]["اسم المخدوم رباعى"]
            print(f"Data for serial number {serial_number}:", name.encode('utf-8'))

            # Append the new entry with "Excuse" to the model without deleting previous ones
            self.model.appendRow([QStandardItem(name), QStandardItem(serial_number), QStandardItem("Excuse")])
            self.model.setHorizontalHeaderItem(2, QStandardItem("Excuses"))

            # Find the column index corresponding to the displayed date
            date_column_index = self.df.columns.get_loc(self.date_display_label.text())

            # Find the row index corresponding to the serial number
            row_index = self.df[self.df['Serial Number'] == int(serial_number)].index[0]

            # Mark 'Excuse' in the Excel sheet at the intersection of the row and column
            self.df.iat[row_index, date_column_index] = "Excuse"

            # Save the updated DataFrame back to the Excel file
            self.df.to_excel("Data/attendance.xlsx", index=False)

        else:
            # Serial number doesn't exist, show a message box
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("Serial Number Not Found")
            msg_box.setText(f"The serial number {serial_number} doesn't exist.")
            self.attendance_text_edit.clear()
            msg_box.exec_()

    def add_excuse_by_name(self, name):
        # Check if the name exists in the table view
        if self.is_person_already_entered(name):
            # Person is already entered, show a message box
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("Duplicate Entry")
            msg_box.setText(f"The person with name '{name}' is already entered.")
            msg_box.exec_()
            self.attendance_text_edit.clear()
            return

        # Load the JSON data from the file
        with open("Data/data.json", "r", encoding="utf-8") as file:
            json_data = json.load(file)

        # Check if the name exists in the values of the JSON file
        for serial_number, person_data in json_data.items():
            # Perform a case-insensitive and whitespace-insensitive comparison
            if person_data["اسم المخدوم رباعى"].strip().lower() == name.strip().lower():
                print(f"Data for name {name.encode('utf-8')}:", person_data)

                # Append the new entry with "Excuse" to the model without deleting previous ones
                self.model.appendRow([QStandardItem(name), QStandardItem(serial_number), QStandardItem("Excuse")])
                self.model.setHorizontalHeaderItem(2, QStandardItem("Excuses"))

                # Find the column index corresponding to the displayed date
                date_column_index = self.df.columns.get_loc(self.date_display_label.text())

                # Find the row index corresponding to the serial number
                row_index = self.df[self.df['Serial Number'] == int(serial_number)].index[0]

                # Mark 'Excuse' in the Excel sheet at the intersection of the row and column
                self.df.iat[row_index, date_column_index] = "Excuse"

                # Save the updated DataFrame back to the Excel file
                self.df.to_excel("Data/attendance.xlsx", index=False)

                return

        # Name doesn't exist, show a message box
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("Name Not Found")
        msg_box.setText(f"The person with the name {name} doesn't exist.")
        self.attendance_text_edit.clear()
        msg_box.exec_()

    def handle_scanned_input(self, scanned_data):
        """
        Handle the input received from the scanner.
        This method assumes that the scanned data includes the serial number.
        You may need to adjust it based on the actual output from your scanner.
        """
        # Check if a valid date is selected
        if not self.date_display_label.isVisible():
            # No date entered, show a message box
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("Enter Date First")
            msg_box.setText("Please enter a date first.")
            msg_box.exec_()
            return

        # Assuming scanned data contains the serial number
        serial_number = scanned_data.strip()

        # Perform the same actions as if entered manually
        if not self.is_serial_number_in_json(serial_number):
            # Serial number doesn't exist, show a message box
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("Serial Number Not Found")
            msg_box.setText(f"The serial number {serial_number} doesn't exist.")
            msg_box.exec_()
            self.attendance_text_edit.clear()
            return

        self.add_person_by_serial_number(serial_number)

    def is_serial_number_in_json(self, serial_number):
        # Load the JSON data from the file
        with open("Data/data.json", "r", encoding="utf-8") as file:
            json_data = json.load(file)

        return serial_number in json_data


