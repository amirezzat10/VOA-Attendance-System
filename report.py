import pandas as pd
import json

from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIntValidator
from PyQt5.QtWidgets import QWidget, QLabel, QComboBox, QPushButton, QTableView, QMessageBox, QFileDialog, QLineEdit
import csv


# Define a custom class that inherits from QComboBox
class CheckableComboBox(QComboBox):
    # Define the __init__ method, which is called when a new object is created
    def __init__(self, parent=None):
        # Call the __init__ method of the parent class (QComboBox)
        super(CheckableComboBox, self).__init__(parent)
        # Connect the pressed signal of the combo box's view to the handle_item_pressed method
        self.view().pressed.connect(self.handle_item_pressed)
        # Set a flag to keep track of whether the checked state has changed
        self._changed = False
        # Create an empty list to store the checked items
        self._items = []

    # Define a method to handle when an item is pressed (i.e. clicked)
    def handle_item_pressed(self, index):
        # Get the item that was clicked
        item = self.model().itemFromIndex(index)

        # If "Select All" is clicked
        if item.text() == "Select All":
            # If "Select All" is unchecked, check all items and add them to the list
            if item.checkState() == 0:
                for i in range(self.count()):
                    combo_item = self.model().item(i)
                    combo_item.setCheckState(2)  # Check the item
                    if combo_item.text() not in self._items:
                        self._items.append(combo_item.text())  # Add the item to the list of checked items

            # If "Select All" is checked, uncheck all items and clear the list
            else:
                for i in range(self.count()):
                    combo_item = self.model().item(i)
                    combo_item.setCheckState(0)  # Uncheck the item
                self._items.clear()

            # Set the flag to indicate that the checked state has changed
            self._changed = True
        else:
            # Handle other items as before
            if item.checkState() == 2:
                item.setCheckState(0)
                self._items.remove(item.text())
                # If any individual item is unchecked, uncheck "Select All"
                self.model().item(0).setCheckState(0)
            else:
                item.setCheckState(2)
                self._items.append(item.text())
                self._changed = True
                # If all individual items are checked, check "Select All"
                if all(self.model().item(i).checkState() == 2 for i in range(1, self.count())):
                    self.model().item(0).setCheckState(2)

    # Override the hidePopup method to only hide the popup if the checked state has not changed
    def hidePopup(self):
        # If the checked state has not changed
        if not self._changed:
            # Call the hidePopup method of the parent class (QComboBox)
            super().hidePopup()
        # Reset the flag to indicate that the checked state has not changed
        self._changed = False

    # Define a method to return the list of checked items
    def items(self):
        return self._items

    # Define a method to return the indices of the checked items in a given DataFrame
    def selected_indices(self, df):
        selected_cols = []
        for item in self._items:
            if item in df.columns:
                selected_cols.append(df.columns.get_loc(item))
        return selected_cols


class Report(QWidget):
    def __init__(self):
        super(Report, self).__init__()

        self.report_date_lbl = QLabel(self)
        self.report_date_cb = CheckableComboBox()
        # self.report_date_cb.setStyleSheet(StyleClass.get_combo_box_style())
        self.report_condition_lbl = QLabel(self)
        self.report_condition_cb = QComboBox(self)
        # self.report_condition_cb.setStyleSheet(StyleClass.get_combo_box_style())
        self.report_show_btn = QPushButton(self)
        self.tableView_2 = QTableView(self)
        self.report_save_btn = QPushButton(self)
        self.search_lbl = QLabel(self)
        self.search_edit = QLineEdit(self)
        self.search_btn = QPushButton(self)


        self.setup_ui()

        # Connect the signal to the function
        self.report_show_btn.clicked.connect(self.handle_tab2_action)

    def setup_ui(self):
        self.report_date_lbl.setGeometry(300, 18, 100, 13)
        self.report_date_lbl.setText("Select Date: ")

        # Call a function to populate report_date_cb
        self.populate_column_names()

        # Call condition_type to populate report_condition_cb
        self.condition_type()


        self.report_date_cb.setGeometry(405, 10, 200, 22)
        self.report_date_cb.setParent(self)  # Add this line to set the parent

        self.report_condition_lbl.setText("Select Condition: ")
        self.report_condition_lbl.setGeometry(300, 48, 100, 13)

        self.report_condition_cb.setGeometry(405, 40, 200, 22)

        self.report_show_btn.setGeometry(525, 69, 75, 23)
        self.report_show_btn.setText("Show")

        self.tableView_2.setGeometry(0, 100, 671, 171)

        self.report_save_btn.setText("Save")
        self.report_save_btn.setGeometry(580, 275, 75, 23)

        self.search_lbl.setText("Search by Serial Number: ")
        self.search_lbl.setGeometry(QRect(10, 70, 150, 16))
        self.search_edit.setGeometry(QRect(155, 70, 91, 20))
        self.search_btn.setText("Search")
        self.search_btn.setGeometry(QRect(255, 70, 75, 23))

        # Connect the signal for the search button
        self.search_btn.clicked.connect(self.handle_search_button)

        # Connect the signal for the save button
        self.report_save_btn.clicked.connect(self.handle_save_button)

        # Initialize the QIntValidator for SN_add_lineedit
        self.int_val_only = QIntValidator(self)

        self.search_edit.setValidator(self.int_val_only)

        self.search_edit.returnPressed.connect(self.handle_search_button)


        # Create the model once during initialization
        self.model = QStandardItemModel(self)
        self.model.setHorizontalHeaderLabels(['Name', 'Serial Number'])
        self.tableView_2.setModel(self.model)

        # Make the table view read-only
        self.tableView_2.setEditTriggers(QTableView.NoEditTriggers)

        # Set equal stretch factors for both columns
        header = self.tableView_2.horizontalHeader()
        header.setSectionResizeMode(0, header.Stretch)
        header.setSectionResizeMode(1, header.Stretch)

        # Adjust column widths to fit the content
        for column in range(self.model.columnCount()):
            self.tableView_2.resizeColumnToContents(column)

    def selectionchange(self):
        """
        This function is a callback function that is triggered when the selection in a combo box is changed.
        If the selection has changed, it prints the items in the combo box.
        """
        if self.report_date_cb._changed:
            print(self.report_date_cb.items())
            self.report_date_cb._changed = False

    def get_combobox_changed_text(self):
        """
        This method is part of a class and is used to get the text of the currently selected item in a combo box.
        @return The text of the currently selected item in the combo box.
        """
        selected = self.report_date_cb.currentText()
        return selected

    def know_the_change(self, index):
        """
        Given an index, check if the current item in the combo box is different from the previous item.
        @param index - the index of the current item in the combo box
        @return True if the current item is different from the previous item, False otherwise.
        """
        old_item = self.report_date_cb.itemText(index - 1) if index > 0 else self.report_date_cb.itemText(0)
        new_item = self.report_date_cb.currentText()

        if old_item == new_item:
            return False
        else:
            return True

    def populate_column_names(self):
        # Read the Excel file
        self.df = pd.read_excel("Data/attendance.xlsx")

        # Extract column names from the third column till the last column
        column_names = self.df.columns[2:].astype(str).tolist()  # Convert to strings

        # Add "Select All" to the beginning of the combo box items
        if self.report_date_cb.count() == 0 or self.report_date_cb.itemText(0) != "Select All":
            self.report_date_cb.clear()
            self.report_date_cb.addItem("Select All")
            self.report_date_cb.addItems(column_names)

    def handle_tab2_action(self):
        try:
            # Get the selected dates from the combo box
            selected_dates = [date for date in self.report_date_cb.items() if date != "Select All"]

            # Check if at least one date is selected
            if not selected_dates:
                # Show a message box if no date is selected
                self.show_message_box("Please select at least one date.")
                return

            # Check the selected condition
            selected_condition = self.report_condition_cb.currentText()

            if selected_condition == "تفاصيل المخدومين":
                # Handle the "تفاصيل المخدومين" condition
                self.handle_students_details(selected_dates)
                return

            if selected_condition == "غياب اكثر من 4 بروفات":
                self.handle_absences_more_than_4(selected_dates)
                return

            # For "الاعذار" condition, filter based on excuses for all selected dates
            if selected_condition == "الاعذار":
                # Load the Excel file
                excel_file_path = "Data/attendance.xlsx"
                df = pd.read_excel(excel_file_path)

                # Filter the DataFrame based on selected dates
                selected_columns = ['Name', 'Serial Number'] + selected_dates
                filtered_df = df[selected_columns]

                # Show only students who have excuses (cell value = "Excuse") on all selected dates
                excuse_mask = filtered_df[selected_dates].apply(lambda row: all(cell == "Excuse" for cell in row),
                                                                axis=1)
                filtered_df = filtered_df[excuse_mask]

                # Update the table view with the filtered data
                self.update_table_view(filtered_df)
                return

            # For other conditions, proceed with the existing logic
            # Load the Excel file
            excel_file_path = "Data/attendance.xlsx"
            df = pd.read_excel(excel_file_path)

            # Filter the DataFrame based on selected dates
            selected_columns = ['Name', 'Serial Number'] + selected_dates
            filtered_df = df[selected_columns]

            # Apply filtering based on the selected condition
            if selected_condition == "الحضور":
                # Show only students who attended on all selected dates
                attendance_mask = filtered_df[selected_dates].apply(lambda row: all(cell == "*" for cell in row),
                                                                    axis=1)
                filtered_df = filtered_df[attendance_mask]
            elif selected_condition == "الغياب":
                # Show only students who were absent (have empty cells) on all selected dates
                absent_mask = filtered_df[selected_dates].apply(lambda row: all(pd.isna(cell) for cell in row), axis=1)
                filtered_df = filtered_df[absent_mask]

            # Update the table view with the filtered data
            self.update_table_view(filtered_df)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            # Print the traceback for more details
            import traceback
            traceback.print_exc()

    def handle_students_details(self, selected_dates):
        try:
            # Load the Excel file
            excel_file_path = "Data/attendance.xlsx"
            df = pd.read_excel(excel_file_path)

            # Replace "nan" values with "Absent" in the DataFrame
            df = df.fillna("Absent")

            # Filter the DataFrame based on selected dates
            selected_columns = ['Name', 'Serial Number'] + selected_dates
            filtered_df = df[selected_columns]

            # Calculate total attendance, absence, and excuses for each student
            total_attendance = filtered_df[selected_dates].apply(
                lambda row: row.apply(lambda cell: 1 if cell == "*" else 0).sum(), axis=1)
            total_absence = filtered_df[selected_dates].apply(
                lambda row: row.apply(lambda cell: 1 if cell == "Absent" else 0).sum(), axis=1)
            total_excuses = filtered_df[selected_dates].apply(
                lambda row: row.apply(lambda cell: 1 if cell == "Excuse" else 0).sum(), axis=1)

            # Clear the existing model
            self.model.clear()

            # Add new columns to the DataFrame
            filtered_df['Total Attendance'] = total_attendance
            filtered_df['Total Absence'] = total_absence
            filtered_df['Total Excuses'] = total_excuses

            # Set the new horizontal header labels based on the DataFrame columns
            self.model.setHorizontalHeaderLabels(filtered_df.columns)

            # Populate the model with the DataFrame data
            for row in range(filtered_df.shape[0]):
                for col in range(filtered_df.shape[1]):
                    item = QStandardItem(str(filtered_df.iat[row, col]))
                    self.model.setItem(row, col, item)

            # Adjust column widths to fit the content
            for column in range(self.model.columnCount()):
                self.tableView_2.resizeColumnToContents(column)

            # # Update the table view with the filtered data
            # self.update_table_view(df)


        except Exception as e:
            print(f"An error occurred in handle_students_details: {str(e)}")
            # Print the traceback for more details
            import traceback
            traceback.print_exc()

    def update_table_view(self, data_frame):
        # Clear the existing model
        self.model.clear()

        # Add the new columns to the DataFrame
        data_frame['رقم موبايل المخدوم'] = ''
        data_frame['رقم موبايل الأم'] = ''
        data_frame['رقم موبايل الأب'] = ''

        # Set the new horizontal header labels based on the DataFrame columns
        self.model.setHorizontalHeaderLabels(data_frame.columns)

        # Read data from the external JSON file with explicit encoding
        with open('Data/data.json', encoding='utf-8') as json_file:
            data_json = json.load(json_file)

            # Print debug information
        data_frame_serial_numbers = data_frame['Serial Number'].astype(str).tolist()
        json_file_serial_numbers = list(data_json.keys())
        print("DataFrame Serial Numbers:", data_frame_serial_numbers)
        print("JSON File Serial Numbers:", json_file_serial_numbers)

        # Find the common serial numbers between the DataFrame and JSON file
        common_serial_numbers = set(data_frame_serial_numbers).intersection(json_file_serial_numbers)
        print("Common Serial Numbers:", common_serial_numbers)

        # Populate the new columns with data from the JSON file
        for index, row in data_frame.iterrows():
            serial_number = str(row['Serial Number'])  # Convert to string
            if serial_number in common_serial_numbers:
                # Update column names to match the keys in the JSON file
                data_frame.at[index, 'رقم موبايل المخدوم'] = data_json[serial_number].get(' رقم موبايل المخدوم ', '')
                data_frame.at[index, 'رقم موبايل الأم'] = data_json[serial_number].get(' رقم موبايل الأم', '')
                data_frame.at[index, 'رقم موبايل الأب'] = data_json[serial_number].get(' رقم موبايل الأب ', '')

        # Replace "nan" values with "Absent" in the DataFrame
        data_frame = data_frame.fillna("Absent")

        # Populate the model with the DataFrame data
        for row in range(data_frame.shape[0]):
            for col in range(data_frame.shape[1]):
                item = QStandardItem(str(data_frame.iat[row, col]))
                self.model.setItem(row, col, item)

        # Adjust column widths to fit the content
        for column in range(self.model.columnCount()):
            self.tableView_2.resizeColumnToContents(column)

    def condition_type(self):
        self.list = ["الحضور","الغياب","الاعذار", "تفاصيل المخدومين" , "غياب اكثر من 4 بروفات"]
        if self.report_condition_cb.count() == 0:
            self.report_condition_cb.clear()
            self.report_condition_cb.addItems(self.list)

    def handle_absences_more_than_4(self, selected_dates):
        try:
            # Load the Excel file
            excel_file_path = "Data/attendance.xlsx"
            df = pd.read_excel(excel_file_path)

            # Filter the DataFrame based on selected dates
            selected_columns = ['Name', 'Serial Number'] + selected_dates
            filtered_df = df[selected_columns]

            # Find students with more than 3 absences
            absences_count = filtered_df[selected_dates].apply(lambda row: sum(pd.isna(cell) for cell in row), axis=1)
            students_more_than_4_absences = filtered_df[absences_count > 4]

            # Clear the existing model
            self.model.clear()

            # Add the new column to the DataFrame
            students_more_than_4_absences['رقم موبايل المخدوم'] = ''
            students_more_than_4_absences['رقم موبايل الأم'] = ''
            students_more_than_4_absences['رقم موبايل الأب'] = ''

            # Set the new horizontal header labels based on the DataFrame columns
            self.model.setHorizontalHeaderLabels(students_more_than_4_absences.columns)

            # Read data from the external JSON file with explicit encoding
            with open('Data/data.json', encoding='utf-8') as json_file:
                data_json = json.load(json_file)

                # Populate the new columns with data from the JSON file
                for index, row in students_more_than_4_absences.iterrows():
                    serial_number = str(row['Serial Number'])  # Convert to string
                    if serial_number in data_json:
                        students_more_than_4_absences.at[index, 'رقم موبايل المخدوم'] = data_json[serial_number].get(
                            ' رقم موبايل المخدوم ', '')
                        students_more_than_4_absences.at[index, 'رقم موبايل الأم'] = data_json[serial_number].get(
                            ' رقم موبايل الأم', '')
                        students_more_than_4_absences.at[index, 'رقم موبايل الأب'] = data_json[serial_number].get(
                            ' رقم موبايل الأب ', '')

                # Replace "nan" values with "Absent" in the DataFrame
                students_more_than_4_absences = students_more_than_4_absences.fillna("Absent")

                # Populate the model with the DataFrame data
                for row in range(students_more_than_4_absences.shape[0]):
                    for col in range(students_more_than_4_absences.shape[1]):
                        item = QStandardItem(str(students_more_than_4_absences.iat[row, col]))
                        self.model.setItem(row, col, item)

                # Adjust column widths to fit the content
                for column in range(self.model.columnCount()):
                    self.tableView_2.resizeColumnToContents(column)

        except Exception as e:
            print(f"An error occurred in handle_absences_more_than_3: {str(e)}")
            # Print the traceback for more details
            import traceback
            traceback.print_exc()

    def calculate_total_attendance(self, selected_date):
        # Load the Excel file
        excel_file_path = "Data/attendance.xlsx"
        df = pd.read_excel(excel_file_path)

        # Filter the DataFrame for the selected date
        selected_columns = ['Name', 'Serial Number', selected_date]
        date_df = df[selected_columns]

        # Count the number of students with "*" (attendance) on the selected date
        total_attendance = date_df[selected_date].apply(lambda cell: 1 if cell == "*" else 0).sum()

        return total_attendance

    def calculate_total_absence(self, selected_date):
        # Load the Excel file
        df = pd.read_excel("Data/attendance.xlsx")

        # Count the number of students absent on the selected date
        total_absence = df[selected_date].apply(lambda cell: 1 if pd.isna(cell) else 0).sum()

        return total_absence

    def calculate_total_excuses(self, selected_date):
        # Load the Excel file
        df = pd.read_excel("Data/attendance.xlsx")

        # Count the number of students with excuses on the selected date
        total_excuses = df[selected_date].apply(lambda cell: 1 if cell == "Excuse" else 0).sum()

        return total_excuses

    def add_total_attendance_row(self, total_attendance):
        # Create a new item with the label "Total Number of Attended" and the calculated value
        total_attendance_item = QStandardItem(str(total_attendance))

        # Add the item to the model in the first column (you can adjust the column as needed)
        self.model.setItem(0, 0, total_attendance_item)

    def add_total_absence_row(self, total_absence):
        # Create a new item with the label "Total Number of Absent" and the calculated value
        total_absence_item = QStandardItem(str(total_absence))

        # Add the item to the model in the first column (you can adjust the column as needed)
        self.model.setItem(0, 0, total_absence_item)

    def add_total_excuses_row(self, total_excuses):
        # Create a new item with the label "Total Number of Excuses" and the calculated value
        total_excuses_item = QStandardItem(str(total_excuses))

        # Add the item to the model in the first column (you can adjust the column as needed)
        self.model.setItem(0, 0, total_excuses_item)

    def add_filtered_students_row(self, filtered_students):
        # Create a new item with the label "Students with More than 3 Absences" and the filtered data
        filtered_students_item = QStandardItem('\n'.join(filtered_students.index))

        # Add the item to the model in the first column (you can adjust the column as needed)
        self.model.setItem(0, 0, filtered_students_item)

    def calculate_total_absences(self):
        # Load the Excel file
        df = pd.read_excel("Data/attendance.xlsx")

        # Count the total number of absences for each student
        total_absences = df.set_index('Serial Number').apply(
            lambda row: row.apply(lambda cell: 1 if pd.isna(cell) else 0).sum(), axis=1)

        return total_absences

    def handle_save_button(self):
        try:
            # Prompt the user to choose a location and name for the CSV file
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            file_name, _ = QFileDialog.getSaveFileName(self, "Save CSV File", "", "CSV Files (*.csv);;All Files (*)",
                                                       options=options)

            # Check if the user canceled the dialog
            if file_name:
                # Ensure the file has the .csv extension
                if not file_name.lower().endswith(".csv"):
                    file_name += ".csv"

                # Save the data from the table view to the chosen file in CSV format
                self.save_table_data_to_csv(file_name)
        except Exception as e:
            print(f"An error occurred while saving: {str(e)}")
            # Print the traceback for more details
            import traceback
            traceback.print_exc()

    def save_table_data_to_csv(self, file_name):
        try:
            # Get the data from the table view
            data = []
            for row in range(self.model.rowCount()):
                row_data = [self.model.item(row, col).text() for col in range(self.model.columnCount())]
                data.append(row_data)

            # Get the header from the table view
            header = [self.model.headerData(col, Qt.Horizontal) for col in range(self.model.columnCount())]

            # Save the data to the CSV file
            with open(file_name, 'w', newline='', encoding='utf-8-sig') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(header)
                csv_writer.writerows(data)

            self.show_message_box(f"Data saved to {file_name}")
        except Exception as e:
            print(f"An error occurred while saving to CSV: {str(e)}")
            # Print the traceback for more details
            import traceback
            traceback.print_exc()

    def handle_search_button(self):
        try:
            # Check if a condition is selected
            if not self.report_condition_cb.currentText():
                self.show_message_box("Please select a condition first before searching.")
                return

            # Check if the table view is empty
            if self.model.rowCount() == 0:
                self.show_message_box("The table view is empty. Please perform a search after selecting a condition.")
                return

            # Get the entered serial number from the search_edit QLineEdit
            search_serial_number = self.search_edit.text().strip()

            # Check if the entered serial number is empty
            if not search_serial_number:
                self.show_message_box("Please enter a serial number for search.")
                return

            # Get the column index for 'Serial Number' in the table view
            serial_number_column = self.tableView_2.horizontalHeader().logicalIndex(1)

            # Iterate over the rows in the model to find the serial number
            for row in range(self.model.rowCount()):
                item = self.model.item(row, serial_number_column)
                if item and item.text() == search_serial_number:
                    # Select the row in the table view
                    self.tableView_2.selectRow(row)
                    return

            # If the serial number is not found
            self.show_message_box(f"No data found for serial number: {search_serial_number}")
        except Exception as e:
            print(f"An error occurred while searching: {str(e)}")
            # Print the traceback for more details
            import traceback
            traceback.print_exc()

    def show_message_box(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText(message)
        msg.setWindowTitle("Warning")
        msg.exec_()