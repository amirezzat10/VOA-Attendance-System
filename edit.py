# edit.py
import json
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator, QIcon
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QLineEdit, QTabWidget, QHBoxLayout, QGridLayout, \
    QMessageBox, QToolButton


class Edit(QWidget):
    def __init__(self):
        super(Edit, self).__init__()

        # add all widgets
        # self.home_btn = QPushButton('Home', self)
        self.add_btn = QToolButton(self)
        self.add_btn.setIcon(QIcon('Images/add.png'))
        self.add_btn.setIconSize(self.add_btn.sizeHint())
        self.add_btn.setStyleSheet("QToolButton { border: none; }")

        self.update_btn = QToolButton(self)
        self.update_btn.setIcon(QIcon('Images/update.png'))
        self.update_btn.setIconSize(self.update_btn.sizeHint())
        self.update_btn.setStyleSheet("QToolButton { border: none; }")

        self.delete_btn = QToolButton(self)
        self.delete_btn.setIcon(QIcon('Images/delete.png'))
        self.delete_btn.setIconSize(self.delete_btn.sizeHint())
        self.delete_btn.setStyleSheet("QToolButton { border: none; }")

        # self.home_btn.clicked.connect(self.home_btn_clicked)
        self.add_btn.clicked.connect(self.add_btn_clicked)
        self.update_btn.clicked.connect(self.update_btn_clicked)
        self.delete_btn.clicked.connect(self.delete_btn_clicked)

        # add tabs
        # self.home_tab = self.home_screen()
        self.add_tab = self.add_screen()
        self.update_tab = self.update_screen()
        self.delete_tab = self.delete_screen()


        # Load existing data from the JSON file
        with open('Data/data.json', 'r', encoding='utf-8') as json_file:
            self.data = json.load(json_file)

        self.setup_ui()

    def setup_ui(self):
        sidebar_layout = QVBoxLayout()

        # sidebar_layout.addWidget(self.home_btn)
        sidebar_layout.addWidget(self.add_btn)
        sidebar_layout.addWidget(self.update_btn)
        sidebar_layout.addWidget(self.delete_btn)

        sidebar_layout.addStretch(5)
        sidebar_layout.setSpacing(20)

        sidebar_widget = QWidget()
        sidebar_widget.setStyleSheet("background-color: #cfcfcf;")
        sidebar_widget.setLayout(sidebar_layout)

        self.right_screen_widget = QTabWidget()
        self.right_screen_widget.tabBar().setObjectName("mainTab")

        # self.right_screen_widget.addTab(self.home_tab, 'Home')
        self.right_screen_widget.addTab(self.add_tab, 'Add')
        self.right_screen_widget.addTab(self.update_tab, 'Update')
        self.right_screen_widget.addTab(self.delete_tab, 'Delete')

        self.right_screen_widget.setCurrentIndex(0)
        self.right_screen_widget.setStyleSheet('''QTabBar::tab{width: 50; \
                    height: 20; margin: 0; padding: 0; border: none;}''')

        main_layout = QHBoxLayout()
        main_layout.addWidget(sidebar_widget, 1)  # Stretch factor 1 for left_widget
        main_layout.addWidget(self.right_screen_widget, 9)  # Stretch factor 9 for right_widget
        main_widget = QWidget()
        main_widget.setLayout(main_layout)

        # Add a member variable to track whether search button is clicked
        self.search_button_clicked = False

        # Initialize the QIntValidator for SN_add_lineedit
        self.int_val_only = QIntValidator(self)

        self.SN_add_lineedit.setValidator(self.int_val_only)
        self.second_add_lineedit.setValidator(self.int_val_only)
        self.third_add_lineedit.setValidator(self.int_val_only)
        self.fourth_add_lineedit.setValidator(self.int_val_only)
        self.ten_add_lineedit.setValidator(self.int_val_only)
        self.eleven_add_lineedit.setValidator(self.int_val_only)

        self.second_update_lineedit.setValidator(self.int_val_only)
        self.third_update_lineedit.setValidator(self.int_val_only)
        self.fourth_update_lineedit.setValidator(self.int_val_only)
        self.ten_update_lineedit.setValidator(self.int_val_only)
        self.eleven_update_lineedit.setValidator(self.int_val_only)


        # Connect the returnPressed signal of SN_add_lineedit to check_existing_SN
        self.SN_add_lineedit.returnPressed.connect(self.check_existing_SN)
        self.search_update_lineedit.returnPressed.connect(self.search_person)
        self.search_delete_lineedit.returnPressed.connect(self.search_delete_person)

        # Connect the buttons to functions
        self.SN_add_btn.clicked.connect(self.check_existing_SN)
        self.add_value_btn.clicked.connect(self.add_person)

        self.search_update_btn.clicked.connect(self.search_person)
        self.save_update_btn.clicked.connect(self.update_person)
        self.clear_update_btn.clicked.connect(self.clear_update_line_eidt)

        self.search_delete_btn.clicked.connect(self.search_delete_person)
        self.delete_method_btn.clicked.connect(self.delete_person)

        self.setLayout(main_layout)  # Add this line

    # -----------------
    # buttons

    # def home_btn_clicked(self):
    #     self.right_screen_widget.setCurrentIndex(0)

    def add_btn_clicked(self):
        self.right_screen_widget.setCurrentIndex(0)

    def update_btn_clicked(self):
        self.right_screen_widget.setCurrentIndex(1)

    def delete_btn_clicked(self):
        self.right_screen_widget.setCurrentIndex(2)

    # -----------------
    # pages

    # ...

    # def home_screen(self):
    #     main_layout = QVBoxLayout()
    #     main_layout.addWidget(QLabel('page 1'))
    #     main_layout.addStretch(5)
    #     main = QWidget()
    #     main.setLayout(main_layout)
    #     return main

    # ...

    def add_screen(self):
        main_layout = QGridLayout()

        self.SN_add_lbl = QLabel("Enter Serial Number: ")
        self.SN_add_lineedit = QLineEdit()
        self.SN_add_lineedit.setFixedSize(220, 20)
        self.SN_add_btn = QPushButton("Create")
        self.SN_add_btn.setFixedSize(80, 20)

        self.first_add_lbl = QLabel("اسم المخدوم: ")
        self.first_add_lineedit = QLineEdit()
        self.first_add_lineedit.setFixedSize(90, 20)

        self.second_add_lbl = QLabel("رقم موبايل المخدوم: ")
        self.second_add_lineedit = QLineEdit()
        self.second_add_lineedit.setFixedSize(90, 20)

        self.third_add_lbl = QLabel("رقم موبايل الأب: ")
        self.third_add_lineedit = QLineEdit()
        self.third_add_lineedit.setFixedSize(90, 20)

        self.fourth_add_lbl = QLabel("رقم موبايل الأم: ")
        self.fourth_add_lineedit = QLineEdit()
        self.fourth_add_lineedit.setFixedSize(90, 20)

        self.fifth_add_lbl = QLabel("المنطقة: ")
        self.fifth_add_lineedit = QLineEdit()
        self.fifth_add_lineedit.setFixedSize(90, 20)

        self.sixth_add_lbl = QLabel("اسم الشارع: ")
        self.sixth_add_lineedit = QLineEdit()
        self.sixth_add_lineedit.setFixedSize(90, 20)

        self.seventh_add_lbl = QLabel("متفرع من: ")
        self.seventh_add_lineedit = QLineEdit()
        self.seventh_add_lineedit.setFixedSize(90, 20)

        self.eight_add_lbl = QLabel("علامة مميزة: ")
        self.eight_add_lineedit = QLineEdit()
        self.eight_add_lineedit.setFixedSize(90, 20)

        self.nine_add_lbl = QLabel("رقم العمارة: ")
        self.nine_add_lineedit = QLineEdit()
        self.nine_add_lineedit.setFixedSize(90, 20)

        self.ten_add_lbl = QLabel("الدور: ")
        self.ten_add_lineedit = QLineEdit()
        self.ten_add_lineedit.setFixedSize(90, 20)

        self.eleven_add_lbl = QLabel("الشقة: ")
        self.eleven_add_lineedit = QLineEdit()
        self.eleven_add_lineedit.setFixedSize(90, 20)

        self.twelve_add_lbl = QLabel("المخدوم في سنة كام دلوقتي: ")
        self.twelve_add_lineedit = QLineEdit()
        self.twelve_add_lineedit.setFixedSize(90, 20)

        self.thirteen_add_lbl = QLabel("تاريخ الميلاد: ")
        self.thirteen_add_lineedit = QLineEdit()
        self.thirteen_add_lineedit.setFixedSize(90, 20)

        self.fourteen_add_lbl = QLabel("لينك الصورة: ")
        self.fourteen_add_lineedit = QLineEdit()
        self.fourteen_add_lineedit.setFixedSize(90, 20)

        self.fifteen_add_lbl = QLabel("كم طول المخدوم ؟ ")
        self.fifteen_add_lineedit = QLineEdit()
        self.fifteen_add_lineedit.setFixedSize(90, 20)

        self.add_value_btn = QPushButton("Add")
        self.add_value_btn.setFixedSize(80, 20)

        main_layout.addWidget(self.SN_add_lbl, 1, 0, 1, 3)  # Span 3 columns
        main_layout.addWidget(self.SN_add_lineedit, 1, 2)
        main_layout.addWidget(self.SN_add_btn, 1, 5)

        main_layout.addWidget(self.first_add_lbl, 2, 3, 1, 3)
        main_layout.addWidget(self.first_add_lineedit, 2, 2)
        main_layout.addWidget(self.second_add_lbl, 2, 1)
        main_layout.addWidget(self.second_add_lineedit, 2, 0)

        main_layout.addWidget(self.third_add_lbl, 3, 3, 1, 3)
        main_layout.addWidget(self.third_add_lineedit, 3, 2)
        main_layout.addWidget(self.fourth_add_lbl, 3, 1)
        main_layout.addWidget(self.fourth_add_lineedit, 3, 0)

        main_layout.addWidget(self.fifth_add_lbl, 4, 3, 1, 3)
        main_layout.addWidget(self.fifth_add_lineedit, 4, 2)
        main_layout.addWidget(self.sixth_add_lbl, 4, 1)
        main_layout.addWidget(self.sixth_add_lineedit, 4, 0)

        main_layout.addWidget(self.seventh_add_lbl, 5, 3, 1, 3)
        main_layout.addWidget(self.seventh_add_lineedit, 5, 2)
        main_layout.addWidget(self.eight_add_lbl, 5, 1)
        main_layout.addWidget(self.eight_add_lineedit, 5, 0)

        main_layout.addWidget(self.nine_add_lbl, 6, 5, 1, 3)
        main_layout.addWidget(self.nine_add_lineedit, 6, 4)
        main_layout.addWidget(self.ten_add_lbl, 6, 3)
        main_layout.addWidget(self.ten_add_lineedit, 6, 2)
        main_layout.addWidget(self.eleven_add_lbl, 6, 1)
        main_layout.addWidget(self.eleven_add_lineedit, 6, 0)

        main_layout.addWidget(self.twelve_add_lbl, 7, 3, 1, 3)  # Span 2 columns
        main_layout.addWidget(self.twelve_add_lineedit, 7, 2)
        main_layout.addWidget(self.thirteen_add_lbl, 7, 1)
        main_layout.addWidget(self.thirteen_add_lineedit, 7, 0)

        main_layout.addWidget(self.fourteen_add_lbl, 8, 3, 1, 3)  # Span 2 columns
        main_layout.addWidget(self.fourteen_add_lineedit, 8, 2)
        main_layout.addWidget(self.fifteen_add_lbl, 8, 1)
        main_layout.addWidget(self.fifteen_add_lineedit, 8, 0)

        main_layout.addWidget(self.add_value_btn, 9, 5)



        main = QWidget()
        main.setLayout(main_layout)
        return main

    def update_screen(self):
        main_layout = QGridLayout()

        self.search_update_lbl = QLabel("Search by Name or Serial Number: ")
        self.search_update_lineedit = QLineEdit()
        self.search_update_lineedit.setFixedSize(150, 20)
        self.search_update_btn = QPushButton("Search")
        self.search_update_btn.setFixedSize(80, 20)

        self.first_update_lbl = QLabel("اسم المخدوم: ")
        self.first_update_lineedit = QLineEdit()
        self.first_update_lineedit.setFixedSize(90, 20)

        self.second_update_lbl = QLabel("رقم موبايل المخدوم: ")
        self.second_update_lineedit = QLineEdit()
        self.second_update_lineedit.setFixedSize(90, 20)

        self.third_update_lbl = QLabel("رقم موبايل الأب: ")
        self.third_update_lineedit = QLineEdit()
        self.third_update_lineedit.setFixedSize(90, 20)

        self.fourth_update_lbl = QLabel("رقم موبايل الأم: ")
        self.fourth_update_lineedit = QLineEdit()
        self.fourth_update_lineedit.setFixedSize(90, 20)

        self.fifth_update_lbl = QLabel("المنطقة: ")
        self.fifth_update_lineedit = QLineEdit()
        self.fifth_update_lineedit.setFixedSize(90, 20)

        self.sixth_update_lbl = QLabel("اسم الشارع: ")
        self.sixth_update_lineedit = QLineEdit()
        self.sixth_update_lineedit.setFixedSize(90, 20)

        self.seventh_update_lbl = QLabel("متفرع من: ")
        self.seventh_update_lineedit = QLineEdit()
        self.seventh_update_lineedit.setFixedSize(90, 20)

        self.eight_update_lbl = QLabel("علامة مميزة: ")
        self.eight_update_lineedit = QLineEdit()
        self.eight_update_lineedit.setFixedSize(90, 20)

        self.nine_update_lbl = QLabel("رقم العمارة: ")
        self.nine_update_lineedit = QLineEdit()
        self.nine_update_lineedit.setFixedSize(90, 20)

        self.ten_update_lbl = QLabel("الدور: ")
        self.ten_update_lineedit = QLineEdit()
        self.ten_update_lineedit.setFixedSize(90, 20)

        self.eleven_update_lbl = QLabel("الشقة: ")
        self.eleven_update_lineedit = QLineEdit()
        self.eleven_update_lineedit.setFixedSize(90, 20)

        self.twelve_update_lbl = QLabel("المخدوم في سنة كام دلوقتي: ")
        self.twelve_update_lineedit = QLineEdit()
        self.twelve_update_lineedit.setFixedSize(90, 20)

        self.thirteen_update_lbl = QLabel("تاريخ الميلاد: ")
        self.thirteen_update_lineedit = QLineEdit()
        self.thirteen_update_lineedit.setFixedSize(90, 20)

        self.fourteen_update_lbl = QLabel("لينك الصورة: ")
        self.fourteen_update_lineedit = QLineEdit()
        self.fourteen_update_lineedit.setFixedSize(90, 20)

        self.fifteen_update_lbl = QLabel("كم طول المخدوم ؟ ")
        self.fifteen_update_lineedit = QLineEdit()
        self.fifteen_update_lineedit.setFixedSize(90, 20)

        self.save_update_btn = QPushButton("Save")
        self.save_update_btn.setFixedSize(80, 20)

        self.clear_update_btn = QPushButton("Clear")
        self.clear_update_btn.setFixedSize(80,20)


        main_layout.addWidget(self.search_update_lbl, 1, 0, 1, 3)  # Span 3 columns
        main_layout.addWidget(self.search_update_lineedit, 1, 2)
        main_layout.addWidget(self.search_update_btn, 1, 4)  # Adjusted column for search_update_btn
        main_layout.addWidget(self.clear_update_btn, 1, 5)  # Added clear_update_btn

        main_layout.addWidget(self.first_update_lbl, 2, 3, 1, 3)
        main_layout.addWidget(self.first_update_lineedit, 2, 2)
        main_layout.addWidget(self.second_update_lbl, 2, 1)
        main_layout.addWidget(self.second_update_lineedit, 2, 0)

        main_layout.addWidget(self.third_update_lbl, 3, 3, 1, 3)
        main_layout.addWidget(self.third_update_lineedit, 3, 2)
        main_layout.addWidget(self.fourth_update_lbl, 3, 1)
        main_layout.addWidget(self.fourth_update_lineedit, 3, 0)

        main_layout.addWidget(self.fifth_update_lbl, 4, 3, 1, 3)
        main_layout.addWidget(self.fifth_update_lineedit, 4, 2)
        main_layout.addWidget(self.sixth_update_lbl, 4, 1)
        main_layout.addWidget(self.sixth_update_lineedit, 4, 0)

        main_layout.addWidget(self.seventh_update_lbl, 5, 3, 1, 3)
        main_layout.addWidget(self.seventh_update_lineedit, 5, 2)
        main_layout.addWidget(self.eight_update_lbl, 5, 1)
        main_layout.addWidget(self.eight_update_lineedit, 5, 0)

        main_layout.addWidget(self.nine_update_lbl, 6, 5, 1, 3)
        main_layout.addWidget(self.nine_update_lineedit, 6, 4)
        main_layout.addWidget(self.ten_update_lbl, 6, 3)
        main_layout.addWidget(self.ten_update_lineedit, 6, 2)
        main_layout.addWidget(self.eleven_update_lbl, 6, 1)
        main_layout.addWidget(self.eleven_update_lineedit, 6, 0)

        main_layout.addWidget(self.twelve_update_lbl, 7, 3, 1, 3)  # Span 2 columns
        main_layout.addWidget(self.twelve_update_lineedit, 7, 2)
        main_layout.addWidget(self.thirteen_update_lbl, 7, 1)
        main_layout.addWidget(self.thirteen_update_lineedit, 7, 0)

        main_layout.addWidget(self.fourteen_update_lbl, 8, 3, 1, 3)  # Span 2 columns
        main_layout.addWidget(self.fourteen_update_lineedit, 8, 2)
        main_layout.addWidget(self.fifteen_update_lbl, 8, 1)
        main_layout.addWidget(self.fifteen_update_lineedit, 8, 0)

        main_layout.addWidget(self.save_update_btn, 9, 5)

        main = QWidget()
        main.setLayout(main_layout)
        return main


    def delete_screen(self):
        main_layout = QGridLayout()

        self.search_delete_lbl = QLabel("Search by Name or Serial Number: ")
        self.search_delete_lineedit = QLineEdit()
        self.search_delete_lineedit.setFixedSize(220, 20)
        self.search_delete_btn = QPushButton("Search")
        self.search_delete_btn.setFixedSize(80, 20)

        self.first_delete_lbl = QLabel("اسم المخدوم: ")
        self.first_delete_lineedit = QLineEdit()
        self.first_delete_lineedit.setFixedSize(90, 20)

        self.second_delete_lbl = QLabel("رقم موبايل المخدوم: ")
        self.second_delete_lineedit = QLineEdit()
        self.second_delete_lineedit.setFixedSize(90, 20)

        self.third_delete_lbl = QLabel("رقم موبايل الأب: ")
        self.third_delete_lineedit = QLineEdit()
        self.third_delete_lineedit.setFixedSize(90, 20)

        self.fourth_delete_lbl = QLabel("رقم موبايل الأم: ")
        self.fourth_delete_lineedit = QLineEdit()
        self.fourth_delete_lineedit.setFixedSize(90, 20)

        self.fifth_delete_lbl = QLabel("المنطقة: ")
        self.fifth_delete_lineedit = QLineEdit()
        self.fifth_delete_lineedit.setFixedSize(90, 20)

        self.sixth_delete_lbl = QLabel("اسم الشارع: ")
        self.sixth_delete_lineedit = QLineEdit()
        self.sixth_delete_lineedit.setFixedSize(90, 20)

        self.seventh_delete_lbl = QLabel("متفرع من: ")
        self.seventh_delete_lineedit = QLineEdit()
        self.seventh_delete_lineedit.setFixedSize(90, 20)

        self.eight_delete_lbl = QLabel("علامة مميزة: ")
        self.eight_delete_lineedit = QLineEdit()
        self.eight_delete_lineedit.setFixedSize(90, 20)

        self.nine_delete_lbl = QLabel("رقم العمارة: ")
        self.nine_delete_lineedit = QLineEdit()
        self.nine_delete_lineedit.setFixedSize(90, 20)

        self.ten_delete_lbl = QLabel("الدور: ")
        self.ten_delete_lineedit = QLineEdit()
        self.ten_delete_lineedit.setFixedSize(90, 20)

        self.eleven_delete_lbl = QLabel("الشقة: ")
        self.eleven_delete_lineedit = QLineEdit()
        self.eleven_delete_lineedit.setFixedSize(90, 20)

        self.twelve_delete_lbl = QLabel("المخدوم في سنة كام دلوقتي: ")
        self.twelve_delete_lineedit = QLineEdit()
        self.twelve_delete_lineedit.setFixedSize(90, 20)

        self.thirteen_delete_lbl = QLabel("تاريخ الميلاد: ")
        self.thirteen_delete_lineedit = QLineEdit()
        self.thirteen_delete_lineedit.setFixedSize(90, 20)

        self.fourteen_delete_lbl = QLabel("لينك الصورة: ")
        self.fourteen_delete_lineedit = QLineEdit()
        self.fourteen_delete_lineedit.setFixedSize(90, 20)

        self.fifteen_delete_lbl = QLabel("كم طول المخدوم ؟ ")
        self.fifteen_delete_lineedit = QLineEdit()
        self.fifteen_delete_lineedit.setFixedSize(90, 20)

        self.delete_method_btn = QPushButton("Delete")
        self.delete_method_btn.setFixedSize(80, 20)

        # Set other QLineEdit widgets as read-only
        self.first_delete_lineedit.setReadOnly(True)
        self.second_delete_lineedit.setReadOnly(True)
        self.third_delete_lineedit.setReadOnly(True)
        self.fourth_delete_lineedit.setReadOnly(True)
        self.fifth_delete_lineedit.setReadOnly(True)
        self.sixth_delete_lineedit.setReadOnly(True)
        self.seventh_delete_lineedit.setReadOnly(True)
        self.eight_delete_lineedit.setReadOnly(True)
        self.nine_delete_lineedit.setReadOnly(True)
        self.ten_delete_lineedit.setReadOnly(True)
        self.eleven_delete_lineedit.setReadOnly(True)
        self.twelve_delete_lineedit.setReadOnly(True)
        self.thirteen_delete_lineedit.setReadOnly(True)
        self.fourteen_delete_lineedit.setReadOnly(True)
        self.fifteen_delete_lineedit.setReadOnly(True)

        main_layout.addWidget(self.search_delete_lbl, 1, 0, 1, 3)  # Span 3 columns
        main_layout.addWidget(self.search_delete_lineedit, 1, 2)
        main_layout.addWidget(self.search_delete_btn, 1, 5)

        main_layout.addWidget(self.first_delete_lbl, 2, 3, 1, 3)
        main_layout.addWidget(self.first_delete_lineedit, 2, 2)
        main_layout.addWidget(self.second_delete_lbl, 2, 1)
        main_layout.addWidget(self.second_delete_lineedit, 2, 0)

        main_layout.addWidget(self.third_delete_lbl, 3, 3, 1, 3)
        main_layout.addWidget(self.third_delete_lineedit, 3, 2)
        main_layout.addWidget(self.fourth_delete_lbl, 3, 1)
        main_layout.addWidget(self.fourth_delete_lineedit, 3, 0)

        main_layout.addWidget(self.fifth_delete_lbl, 4, 3, 1, 3)
        main_layout.addWidget(self.fifth_delete_lineedit, 4, 2)
        main_layout.addWidget(self.sixth_delete_lbl, 4, 1)
        main_layout.addWidget(self.sixth_delete_lineedit, 4, 0)

        main_layout.addWidget(self.seventh_delete_lbl, 5, 3, 1, 3)
        main_layout.addWidget(self.seventh_delete_lineedit, 5, 2)
        main_layout.addWidget(self.eight_delete_lbl, 5, 1)
        main_layout.addWidget(self.eight_delete_lineedit, 5, 0)

        main_layout.addWidget(self.nine_delete_lbl, 6, 5, 1, 3)
        main_layout.addWidget(self.nine_delete_lineedit, 6, 4)
        main_layout.addWidget(self.ten_delete_lbl, 6, 3)
        main_layout.addWidget(self.ten_delete_lineedit, 6, 2)
        main_layout.addWidget(self.eleven_delete_lbl, 6, 1)
        main_layout.addWidget(self.eleven_delete_lineedit, 6, 0)

        main_layout.addWidget(self.twelve_delete_lbl, 7, 3, 1, 3)  # Span 2 columns
        main_layout.addWidget(self.twelve_delete_lineedit, 7, 2)
        main_layout.addWidget(self.thirteen_delete_lbl, 7, 1)
        main_layout.addWidget(self.thirteen_delete_lineedit, 7, 0)

        main_layout.addWidget(self.fourteen_delete_lbl, 8, 3, 1, 3)  # Span 2 columns
        main_layout.addWidget(self.fourteen_delete_lineedit, 8, 2)
        main_layout.addWidget(self.fifteen_delete_lbl, 8, 1)
        main_layout.addWidget(self.fifteen_delete_lineedit, 8, 0)

        main_layout.addWidget(self.delete_method_btn, 9, 5)

        main = QWidget()
        main.setLayout(main_layout)


        return main

    def check_existing_SN(self):
        serial_number = self.SN_add_lineedit.text()

        # Check if the serial number already exists
        if serial_number in self.data:
            QMessageBox.warning(self, "Error",
                                f"Serial number {serial_number} already exists. Use a unique serial number.")
        else:
            QMessageBox.information(self, "Success",
                                    f"Person with serial number {serial_number} added successfully.")

    def add_person(self):
        serial_number = self.SN_add_lineedit.text()

        # Check if the serial number is empty
        if not serial_number:
            QMessageBox.warning(self, "Error", "Please enter a serial number.")
            return

        # Check if the serial number already exists
        if serial_number in self.data:
            QMessageBox.warning(self, "Error",
                                f"Serial number {serial_number} already exists. Use a unique serial number.")
        else:
            # Create a new entry in the data dictionary
            self.data[serial_number] = {
                "اسم المخدوم رباعى": self.first_add_lineedit.text(),
                " رقم موبايل المخدوم ": self.second_add_lineedit.text(),
                " رقم موبايل الأب ": self.third_add_lineedit.text(),
                " رقم موبايل الأم": self.fourth_add_lineedit.text(),
                "المنطقة": self.fifth_add_lineedit.text(),
                "رقم العمارة": int(self.nine_add_lineedit.text()) if self.nine_add_lineedit.text() else "",
                "اسم الشارع ": self.sixth_add_lineedit.text(),
                "متفرع من": self.seventh_add_lineedit.text(),
                "علامة مميزة ": self.eight_add_lineedit.text(),
                "الدور ": int(self.ten_add_lineedit.text()) if self.ten_add_lineedit.text() else "",
                "الشقة": int(self.eleven_add_lineedit.text()) if self.eleven_add_lineedit.text() else "",
                "المخدوم فى سنة كام دلوقتى وليس العام الدراسى القادم": self.twelve_add_lineedit.text(),
                "تاريخ الميلاد": self.thirteen_add_lineedit.text(),
                "برجاء رفع صورة واضحة لوجه المخدوم ": self.fourteen_add_lineedit.text(),
                "كم طول المخدوم؟": self.fifteen_add_lineedit.text()
            }

            # Save the updated data to the JSON file
            with open('Data/data.json', 'w', encoding='utf-8') as json_file:
                json.dump(self.data, json_file, ensure_ascii=False, indent=4)

            # Clear all line edits
            self.SN_add_lineedit.clear()
            self.first_add_lineedit.clear()
            self.second_add_lineedit.clear()
            self.third_add_lineedit.clear()
            self.fourth_add_lineedit.clear()
            self.fifth_add_lineedit.clear()
            self.sixth_add_lineedit.clear()
            self.seventh_add_lineedit.clear()
            self.eight_add_lineedit.clear()
            self.nine_add_lineedit.clear()
            self.ten_add_lineedit.clear()
            self.eleven_add_lineedit.clear()
            self.twelve_add_lineedit.clear()
            self.thirteen_add_lineedit.clear()
            self.fourteen_add_lineedit.clear()
            self.fifteen_add_lineedit.clear()

            QMessageBox.information(self, "Success",
                                    f"Person with serial number {serial_number} added successfully.")

    def search_person(self):
        try:
            # Get the entered serial number or name for searching
            search_input = self.search_update_lineedit.text()

            # Check if the search input is empty
            if not search_input:
                QMessageBox.warning(self, "Error", "Please enter a serial number or name for searching.")
                return

            # Check if the search input exists in the data
            person_data = None
            if search_input in self.data:
                person_data = self.data[search_input]
            else:
                # If not found by serial number, try to find by name
                for serial_number, data in self.data.items():
                    if data.get("اسم المخدوم رباعى", "") == search_input:
                        person_data = data
                        break

            if person_data is None:
                QMessageBox.warning(self, "Error", f"No person found with serial number or name: {search_input}")
                return

            # Update the line edits with the retrieved data
            self.first_update_lineedit.setText(person_data.get("اسم المخدوم رباعى", ""))
            self.second_update_lineedit.setText(person_data.get(" رقم موبايل المخدوم ", ""))
            self.third_update_lineedit.setText(person_data.get(" رقم موبايل الأب ", ""))
            self.fourth_update_lineedit.setText(person_data.get(" رقم موبايل الأم", ""))
            self.fifth_update_lineedit.setText(person_data.get("المنطقة", ""))
            self.sixth_update_lineedit.setText(person_data.get("اسم الشارع ", ""))
            self.seventh_update_lineedit.setText(person_data.get("متفرع من", ""))
            self.eight_update_lineedit.setText(person_data.get("علامة مميزة ", ""))
            self.nine_update_lineedit.setText(str(person_data.get("رقم العمارة", "")))
            self.ten_update_lineedit.setText(str(person_data.get("الدور ", "")))
            self.eleven_update_lineedit.setText(str(person_data.get("الشقة", "")))
            self.twelve_update_lineedit.setText(
                person_data.get("المخدوم في سنة كام دلوقتى وليس العام الدراسى القادم", ""))
            self.thirteen_update_lineedit.setText(person_data.get("تاريخ الميلاد", ""))
            self.fourteen_update_lineedit.setText(person_data.get("برجاء رفع صورة واضحة لوجه المخدوم ", ""))
            self.fifteen_update_lineedit.setText(person_data.get("كم طول المخدوم؟", ""))

            # Set the flag to True indicating that search button is clicked
            self.search_button_clicked = True

        except Exception as e:
            print(f"An error occurred in search_person: {str(e)}")
            # Print the traceback for more details
            import traceback
            traceback.print_exc()

    def update_person(self):
        try:
            # Check if the search button is clicked before allowing the update
            if not self.search_button_clicked:
                QMessageBox.warning(self, "Error", "Please click on the 'Search' button first.")
                return

            # Get the entered serial number for searching
            serial_number = self.search_update_lineedit.text()
            # Retrieve data for the found serial number
            person_data = self.data[serial_number]
            # Update the person's data
            person_data["اسم المخدوم رباعى"] = self.first_update_lineedit.text()
            person_data[" رقم موبايل المخدوم "] = self.second_update_lineedit.text()
            person_data[" رقم موبايل الأب "] = self.third_update_lineedit.text()
            person_data[" رقم موبايل الأم"] = self.fourth_update_lineedit.text()
            person_data["المنطقة"] = self.fifth_update_lineedit.text()
            person_data["رقم العمارة"] = int(self.nine_update_lineedit.text()) if self.nine_update_lineedit.text() else ""
            person_data["اسم الشارع "] = self.sixth_update_lineedit.text()
            person_data["متفرع من"] = self.seventh_update_lineedit.text()
            person_data["علامة مميزة "] = self.eight_update_lineedit.text()
            person_data["الدور "] = int(self.ten_update_lineedit.text()) if self.ten_update_lineedit.text() else ""
            person_data["الشقة"] = int(self.eleven_update_lineedit.text()) if self.eleven_update_lineedit.text() else ""
            person_data["المخدوم في سنة كام دلوقتى وليس العام الدراسى القادم"] = self.twelve_update_lineedit.text()
            person_data["تاريخ الميلاد"] = self.thirteen_update_lineedit.text()
            person_data["برجاء رفع صورة واضحة لوجه المخدوم "] = self.fourteen_update_lineedit.text()
            person_data["كم طول المخدوم؟"] = self.fifteen_update_lineedit.text()

            # Save the updated data to the JSON file
            with open('Data/data.json', 'w', encoding='utf-8') as json_file:
                json.dump(self.data, json_file, ensure_ascii=False, indent=4)

            # Clear all line edits
            self.search_update_lineedit.clear()
            self.first_update_lineedit.clear()
            self.second_update_lineedit.clear()
            self.third_update_lineedit.clear()
            self.fourth_update_lineedit.clear()
            self.fifth_update_lineedit.clear()
            self.sixth_update_lineedit.clear()
            self.seventh_update_lineedit.clear()
            self.eight_update_lineedit.clear()
            self.nine_update_lineedit.clear()
            self.ten_update_lineedit.clear()
            self.eleven_update_lineedit.clear()
            self.twelve_update_lineedit.clear()
            self.thirteen_update_lineedit.clear()
            self.fourteen_update_lineedit.clear()
            self.fifteen_update_lineedit.clear()

            QMessageBox.information(self, "Success", f"Person with {serial_number} updated successfully.")

            # Clear the flag after updating the person's data
            self.search_button_clicked = False
        except Exception as e:
            print(f"An error occurred in handle_absences_more_than_3: {str(e)}")
            # Print the traceback for more details
            import traceback
            traceback.print_exc()

    def clear_update_line_eidt(self):
        # Clear all line edits
        self.search_update_lineedit.clear()
        self.first_update_lineedit.clear()
        self.second_update_lineedit.clear()
        self.third_update_lineedit.clear()
        self.fourth_update_lineedit.clear()
        self.fifth_update_lineedit.clear()
        self.sixth_update_lineedit.clear()
        self.seventh_update_lineedit.clear()
        self.eight_update_lineedit.clear()
        self.nine_update_lineedit.clear()
        self.ten_update_lineedit.clear()
        self.eleven_update_lineedit.clear()
        self.twelve_update_lineedit.clear()
        self.thirteen_update_lineedit.clear()
        self.fourteen_update_lineedit.clear()
        self.fifteen_update_lineedit.clear()

    def search_delete_person(self):
        try:
            # Get the entered serial number or name for searching
            search_input = self.search_delete_lineedit.text()

            # Check if the search input is empty
            if not search_input:
                QMessageBox.warning(self, "Error", "Please enter a serial number or name for searching.")
                return

            # Check if the search input exists in the data
            person_data = None
            if search_input in self.data:
                person_data = self.data[search_input]
            else:
                # If not found by serial number, try to find by name
                for serial_number, data in self.data.items():
                    if data.get("اسم المخدوم رباعى", "") == search_input:
                        person_data = data
                        break

            if person_data is None:
                QMessageBox.warning(self, "Error", f"No person found with serial number or name: {search_input}")
                return

            # Update the line edits with the retrieved data
            self.first_delete_lineedit.setText(person_data.get("اسم المخدوم رباعى", ""))
            self.second_delete_lineedit.setText(person_data.get(" رقم موبايل المخدوم ", ""))
            self.third_delete_lineedit.setText(person_data.get(" رقم موبايل الأب ", ""))
            self.fourth_delete_lineedit.setText(person_data.get(" رقم موبايل الأم", ""))
            self.fifth_delete_lineedit.setText(person_data.get("المنطقة", ""))
            self.sixth_delete_lineedit.setText(person_data.get("اسم الشارع ", ""))
            self.seventh_delete_lineedit.setText(person_data.get("متفرع من", ""))
            self.eight_delete_lineedit.setText(person_data.get("علامة مميزة ", ""))
            self.nine_delete_lineedit.setText(str(person_data.get("رقم العمارة", "")))
            self.ten_delete_lineedit.setText(str(person_data.get("الدور ", "")))
            self.eleven_delete_lineedit.setText(str(person_data.get("الشقة", "")))
            self.twelve_delete_lineedit.setText(
                person_data.get("المخدوم في سنة كام دلوقتى وليس العام الدراسى القادم", ""))
            self.thirteen_delete_lineedit.setText(person_data.get("تاريخ الميلاد", ""))
            self.fourteen_delete_lineedit.setText(person_data.get("برجاء رفع صورة واضحة لوجه المخدوم ", ""))
            self.fifteen_delete_lineedit.setText(person_data.get("كم طول المخدوم؟", ""))

            # Set the flag to True indicating that search button is clicked
            self.search_button_clicked = True

        except Exception as e:
            print(f"An error occurred in search_person: {str(e)}")
            # Print the traceback for more details
            import traceback
            traceback.print_exc()

    def delete_person(self):
        try:
            # Check if the search button is clicked before allowing the delete
            if not self.search_button_clicked:
                QMessageBox.warning(self, "Error", "Please click on the 'Search' button first.")
                return

            # Get the entered serial number or name for searching
            search_input = self.search_delete_lineedit.text()

            # Retrieve the name of the person to include in the confirmation message
            person_name = self.first_delete_lineedit.text()

            # Display a confirmation message box
            confirmation = QMessageBox.question(
                self,
                "Confirmation",
                f"Are you sure you want to delete {person_name}?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )

            if confirmation == QMessageBox.Yes:
                # Delete the person's data from the JSON file
                del self.data[search_input]
                with open('Data/data.json', 'w', encoding='utf-8') as json_file:
                    json.dump(self.data, json_file, ensure_ascii=False, indent=4)

                # Clear all line edits
                self.search_delete_lineedit.clear()
                self.first_delete_lineedit.clear()
                self.second_delete_lineedit.clear()
                self.third_delete_lineedit.clear()
                self.fourth_delete_lineedit.clear()
                self.fifth_delete_lineedit.clear()
                self.sixth_delete_lineedit.clear()
                self.seventh_delete_lineedit.clear()
                self.eight_delete_lineedit.clear()
                self.nine_delete_lineedit.clear()
                self.ten_delete_lineedit.clear()
                self.eleven_delete_lineedit.clear()
                self.twelve_delete_lineedit.clear()
                self.thirteen_delete_lineedit.clear()
                self.fourteen_delete_lineedit.clear()
                self.fifteen_delete_lineedit.clear()

                QMessageBox.information(self, "Success", f"{person_name} deleted successfully.")
            else:
                QMessageBox.information(self, "Deletion Cancelled", f"{person_name} was not deleted.")

        except Exception as e:
            print(f"An error occurred in delete_person: {str(e)}")
            # Print the traceback for more details
            import traceback
            traceback.print_exc()