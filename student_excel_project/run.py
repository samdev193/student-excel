from pyqt_generated import Ui_Dialog
from pyqt_generated import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QInputDialog, QLineEdit

import main


class MainWindow(Ui_Dialog, QInputDialog):
    def setupUi(self, Dialog):
        super().setupUi(Dialog)
        self.email_button.clicked.connect(lambda: self.email_clicked())
        self.update_db_button.clicked.connect(lambda: self.update_db())
        self.unpaid_student_button.clicked.connect(lambda: self.unpaid_students())
        self.all_students()


    def email_clicked(self):
        subject = self.subject_line.text()
        body = self.textEdit.toPlainText()
        current_students = []
        for i in range(self.list_of_students.count()):
            current_students.append(self.list_of_students.item(i).text())

        mailing_list = []
        # gets students names and emails
        student_info = main.get_students()
        for student in current_students:
            mailing_list.append((student, student_info[student]))

        confirm = QMessageBox()
        question = confirm.question(self, '', 'Are you sure you want to send an email?', confirm.Yes | confirm.No)

        if question == confirm.Yes:
            send_email = main.email_student(subject, body, mailing_list)

            # error occured
            if len(send_email) == len(current_students):
                self.show_popup("Something went wrong... None of the emails were able to be sent.", QMessageBox.Critical)

            elif len(send_email) != 0:
                self.show_popup(f"An Error has occured, the following email addresses did not receive your email.{', '.join(send_email)}",
                                QMessageBox.Critical)

            # all emails sent
            else:
                self.show_popup("All emails successfully sent.", QMessageBox.Information)

    # populates list widget with all students
    def all_students(self):
        students = main.get_students()
        for name in students:
            self.list_of_students.addItem(name)

    # overwrites and updates db
    def update_db(self):
        month = self.month_name_popup()
        sheet_name = self.sheet_name_popup()
        # handles invalid input for sheet name or month
        if month and sheet_name and not main.update_db(month, sheet_name):
            while not main.update_db(month, sheet_name):
                self.show_popup("Something went wrong! Try again.", QMessageBox.Warning)
                month = self.month_name_popup()
                sheet_name = self.sheet_name_popup()
                # when cancel is clicked.
                if not month or not sheet_name:
                    break
        self.list_of_students.clear()
        self.all_students()

    def unpaid_students(self):
        unpaid_list = main.students_not_paid()
        self.list_of_students.clear()
        if len(unpaid_list) == 0:
            self.list_of_students.addItem('All students have paid their tuition.')
        else:
            for student in unpaid_list:
                self.list_of_students.addItem(student)

    def month_name_popup(self):
        text, popup = QInputDialog.getText(self, 'Sheet Month', 'Write the current month the sheet is using')
        if popup:
            return str(text)
        else:
            return False

    def sheet_name_popup(self):
        text, popup = QInputDialog.getText(self, 'Sheet Name', "Write the name of the sheet you're going to use")
        if popup:
            return str(text)
        else:
            return False

    def show_popup(self, text: str, icon: QMessageBox):
        msg = QMessageBox()
        msg.setWindowTitle("test")
        msg.setText(text)
        msg.setIcon(icon)
        x = msg.exec_()

if __name__ =='__main__':
    import sys
    gui_app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = MainWindow()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(gui_app.exec_())