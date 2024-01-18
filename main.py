# main.py
from PyQt5.QtCore import Qt, QFile, QTextStream, QRect
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QTabWidget, QSplashScreen, QLabel
from qt_material import apply_stylesheet

from attendance import Attendance
from report import Report
from edit import Edit


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(673, 351)
        self.centralwidget = QTabWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Adjust the geometry to fill the available space
        self.centralwidget.setGeometry(0, 0, 671, 331)

        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")

        # Set the tabWidget to fill the centralwidget
        self.tabWidget.setGeometry(self.centralwidget.geometry())

        # Create instances of the tab classes
        self.attendance = Attendance()
        self.report = Report()
        self.edit = Edit()

        # Add each tab to the QTabWidget
        self.tabWidget.addTab(self.attendance, "Attendance")
        self.tabWidget.addTab(self.report, "Report")
        self.tabWidget.addTab(self.edit, "Edit")

        self.watermark_lbl = QLabel(self.centralwidget)
        self.watermark_lbl.setObjectName(u"label_20")
        self.watermark_lbl.setGeometry(QRect(390, 330, 270, 21))
        self.watermark_lbl.setText("Developed by: Amir Ezzat   tel/ +201201266124")
        MainWindow.setCentralWidget(self.centralwidget)



class MyMainWindow(QMainWindow):
    def __init__(self):
        super(MyMainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Set central widget to your tab widget
        self.setCentralWidget(self.ui.centralwidget)

        # Set main title
        self.setWindowTitle("VOA Attendance System")

        # Set icon for the main window
        self.setWindowIcon(QIcon('Images/logo.png'))
        # Set fixed size to prevent resizing
        self.setFixedSize(self.size())





class SplashScreen(QSplashScreen):
    def __init__(self, logo_path):
        super(SplashScreen, self).__init__(QPixmap(logo_path))
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)



if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)

    # Show the splash screen
    logo = QPixmap('Images/logo.png')
    scaled_logo = logo.scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    splash = QSplashScreen(scaled_logo, Qt.WindowStaysOnTopHint)
    splash.show()

    apply_stylesheet(app, theme='light_blue.xml', css_file='custom.css')


    # Create the main window
    MainWindow = MyMainWindow()

    # Close the splash screen when the main window is shown
    splash.finish(MainWindow)

    MainWindow.show()
    sys.exit(app.exec_())