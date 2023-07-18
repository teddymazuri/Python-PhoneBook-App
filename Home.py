import sqlite3
import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
import io
import contacts_report


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("Phonebookapp.ui", self)
        # Position Center
        self.center()
        # QTABLE WIDGET ATTRIBUTES
        self.contactTable.setColumnWidth(0, 50)
        self.contactTable.setColumnWidth(1, 100)
        self.contactTable.setColumnWidth(2, 100)
        self.contactTable.setColumnWidth(3, 170)
        self.contactTable.setColumnWidth(4, 130)
        self.contactTable.setHorizontalHeaderLabels(["ID", "First Name", "Last Name", "Email", "Phone Number"])
        self.load_data()
        self.txtId.setEnabled(False)
        # Search and Clear Search Buttons
        self.search_button.clicked.connect(self.load_search)
        self.clear_button.clicked.connect(self.clear_search)
        # Menu Buttons
        # File Menu
        self.actionSave.triggered.connect(self.save_data)
        self.actionUpdate.triggered.connect(self.update_data)
        self.actionDelete.triggered.connect(self.delete_data)
        self.actionCancel.triggered.connect(self.clear_fields)
        self.actionExit_Prog.triggered.connect(self.exit_program)
        # Edit Menu
        self.actionBackup_Database.triggered.connect(self.backup_db)
        self.actionExport_pdf.triggered.connect(self.write_pdf)
        self.actionLoad_Backup.triggered.connect(self.restore_db)
        # listener for table view click
        self.contactTable.cellClicked.connect(self.selected_row)

    # CENTER WINDOW
    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def load_data(self):
        # Create Database Connection & Cursor
        conn = sqlite3.connect('phonebook.db')
        cur = conn.cursor()
        # SQL Query String
        my_query = "SELECT * FROM contacts LIMIT 50"
        # Set Table Row Count
        self.contactTable.setRowCount(50)
        # Initialise Table Row
        table_row = 0

        for row in cur.execute(my_query):
            self.contactTable.setItem(table_row, 0, QtWidgets.QTableWidgetItem(str(row[0])))
            self.contactTable.setItem(table_row, 1, QtWidgets.QTableWidgetItem(row[1]))
            self.contactTable.setItem(table_row, 2, QtWidgets.QTableWidgetItem(row[2]))
            self.contactTable.setItem(table_row, 3, QtWidgets.QTableWidgetItem(row[3]))
            self.contactTable.setItem(table_row, 4, QtWidgets.QTableWidgetItem(row[4]))
            # Increment Table Row Values
            table_row += 1
        # Close Database Connection
        conn.close()

    def load_search(self):
        # Clear Table
        self.contactTable.setRowCount(0)
        # Create New Connection & Cursor
        conn = sqlite3.connect('phonebook.db')
        cur = conn.cursor()
        # Get Text From Search Field
        search_field = self.search_contact.text()
        # Sql Query String
        search_query = "SELECT * FROM contacts WHERE first_name =? LIMIT 10"
        # Set Row Count
        self.contactTable.setRowCount(10)
        # Initialise Table Row
        table_row = 0

        for row in cur.execute(search_query, [search_field]):
            self.contactTable.setItem(table_row, 0, QtWidgets.QTableWidgetItem(str(row[0])))
            self.contactTable.setItem(table_row, 1, QtWidgets.QTableWidgetItem(row[1]))
            self.contactTable.setItem(table_row, 2, QtWidgets.QTableWidgetItem(row[2]))
            self.contactTable.setItem(table_row, 3, QtWidgets.QTableWidgetItem(row[3]))
            self.contactTable.setItem(table_row, 4, QtWidgets.QTableWidgetItem(row[4]))
            # Increment Row Values
            table_row += 1
        # Close Database Connection
        conn.close()

    # SELECTED ROWS
    def selected_row(self):
        whole_row = self.contactTable.currentRow()  # Index of Row
        first_column_in_row = self.contactTable.item(whole_row, 0)  # returns QTableWidgetItem
        second_column_in_row = self.contactTable.item(whole_row, 1)
        third_column_in_row = self.contactTable.item(whole_row, 2)
        fourth_column_in_row = self.contactTable.item(whole_row, 3)
        fifth_column_in_row = self.contactTable.item(whole_row, 4)

        if first_column_in_row or second_column_in_row or third_column_in_row or fourth_column_in_row or \
                fifth_column_in_row is not None:
            # Store data in defined variables
            contact_id = first_column_in_row.text()  # content of this
            f_name = second_column_in_row.text()
            l_name = third_column_in_row.text()
            e_mail = fourth_column_in_row.text()
            p_number = fifth_column_in_row.text()

            # Append data to fields
            self.txtId.setText(contact_id)
            self.txtFname.setText(f_name)
            self.txtLname.setText(l_name)
            self.txtEmail.setText(e_mail)
            self.txtPhone.setText(p_number)

    def clear_search(self):
        self.search_contact.setText("")
        self.contactTable.setRowCount(0)
        self.load_data()

    # MENU BAR ITEMS

    # Save Action
    def save_data(self):
        # Create Database Connection & Cursor
        conn = sqlite3.connect('phonebook.db')
        cur = conn.cursor()
        # The Text Fields
        firstname = self.txtFname.text()
        lastname = self.txtLname.text()
        email = self.txtEmail.text()
        phonenumber = self.txtPhone.text()
        save_query = "INSERT INTO contacts VALUES(NULL,?,?,?,?)"

        if firstname == "":
            # Message
            self.message_box.setText("First Name Cannot Be Empty!")
            conn.close()
        if lastname == "":
            # Message
            self.message_box.setText("Last Name Empty!")
            conn.close()
        if email == "":
            # Message
            self.message_box.setText("E-mail Empty!")
            conn.close()
        if phonenumber == "":
            # Message
            self.message_box.setText("Phone Number Empty!")
            conn.close()
        else:
            check_query = "SELECT phone_number FROM contacts WHERE phone_number=?"
            cur.execute(check_query, [phonenumber])
            items = cur.fetchall()
            if len(items) == 0:
                cur.execute(save_query, [firstname, lastname, email, phonenumber])
                # conn.commit()
                rply = QMessageBox.question(self, 'Perform Action', "Save Contact?", QMessageBox.Yes | QMessageBox.No,
                                            QMessageBox.No)
                if rply == QMessageBox.Yes:
                    conn.commit()
                    QMessageBox.critical(self, 'Success', 'Contact Has Been Saved!')
                    self.message_box.setText("Saved Successfully!")
                    # reload table
                    self.load_data()
                    conn.close()
                    # Clear fields
                    self.clear_fields()
                else:
                    conn.close()
                    QMessageBox.critical(self, 'Aborted', 'Action Aborted!')
                    self.message_box.setText("Save Aborted!")

            else:
                QMessageBox.critical(self, 'Error', 'Contact Exists!')
                self.message_box.setText("Contact Exists!")
                conn.close()

    # Update Data
    def update_data(self):
        # Create Connection
        conn = sqlite3.connect('phonebook.db')
        cur = conn.cursor()
        # Text Fields
        contactid = self.txtId.text()
        firstname = self.txtFname.text()
        lastname = self.txtLname.text()
        email = self.txtEmail.text()
        phonenumber = self.txtPhone.text()
        # update query
        update_query = """UPDATE contacts 
                        SET first_name=?, last_name=?, email_address=?, phone_number=? WHERE contact_id=?"""
        # Check if ID field is empty
        if contactid == "":
            QMessageBox.critical(self, 'Error', 'Select Contact to Update!')
            self.message_box.setText("Please Select Contact to Update!")
            conn.close()
        else:
            cur.execute(update_query, [firstname, lastname, email, phonenumber, int(contactid)])
            rply = QMessageBox.question(self, 'Perform Action', "Update Contact?", QMessageBox.Yes | QMessageBox.No,
                                        QMessageBox.No)
            if rply == QMessageBox.Yes:
                conn.commit()
                QMessageBox.critical(self, 'Success', 'Contact Has Been Updated!')
                self.message_box.setText("Updated Successfully!")
                conn.close()
                # reload table
                self.load_data()
                # Clear fields
                self.clear_fields()
            else:
                conn.close()
                QMessageBox.critical(self, 'Aborted', 'Update Aborted!')
                self.message_box.setText("Update Aborted!")

    # Delete Data
    def delete_data(self):
        # Create Connection
        conn = sqlite3.connect('phonebook.db')
        cur = conn.cursor()
        # Text Fields
        contactid = self.txtId.text()
        # Delete Query
        delete_query = "DELETE FROM contacts WHERE contact_id=?"
        # Check if ID field is empty
        if contactid == "":
            QMessageBox.critical(self, 'Error', 'Select Contact to Delete!')
            self.message_box.setText("Please Select Contact to Delete!")
            conn.close()
        else:
            cur.execute(delete_query, [int(contactid)])
            rply = QMessageBox.question(self, 'Perform Action', "Delete Contact?", QMessageBox.Yes | QMessageBox.No,
                                        QMessageBox.No)
            if rply == QMessageBox.Yes:
                conn.commit()
                QMessageBox.critical(self, 'Success', 'Contact Has Been Deleted!')
                self.message_box.setText("Deleted Successfully!")
                # reload table
                self.load_data()
                conn.close()
                # Clear fields
                self.clear_fields()
            else:
                conn.close()
                QMessageBox.critical(self, 'Aborted', 'Delete Aborted!')
                self.message_box.setText("Delete Aborted!")
                self.clear_fields()

    # Clear Fields Action
    def clear_fields(self):
        self.txtId.setText("")
        self.txtFname.setText("")
        self.txtLname.setText("")
        self.txtEmail.setText("")
        self.txtPhone.setText("")

    # Back Up Database
    def backup_db(self):
        rply = QMessageBox.question(self, 'Perform Backup', "Create Database Backup?", QMessageBox.Yes | QMessageBox.No,
                                    QMessageBox.No)
        if rply == QMessageBox.Yes:
            conn = sqlite3.connect('phonebook.db')
            with io.open('BACKUP/phonebook_dump.sql', 'w') as p:
                # iterdump() function
                for line in conn.iterdump():
                    p.write('%s\n' % line)
            conn.close()
            QMessageBox.critical(self, 'Success', 'Database Backed Up! As BACKUP/phonebook_dump.sql')
            self.message_box.setText(' Backup Successful! Saved as BACKUP/phonebook_dump.sql')
        else:
            QMessageBox.critical(self, 'Aborted', 'Backup Aborted!')
            self.message_box.setText("Backup Aborted!")

    # DATABASE RESTORE
    def restore_db(self):
        rply = QMessageBox.question(self, 'Restore Backup', "Restore From Backup?", QMessageBox.Yes | QMessageBox.No,
                                    QMessageBox.No)
        if rply == QMessageBox.Yes:
            conn = sqlite3.connect('phonebook.db')
            f = open('BACKUP/phonebook_dump.sql', 'r')
            sql = f.read()
            conn.executescript(sql)
            QMessageBox.critical(self, 'Success', 'Database Restored!')
            self.message_box.setText("Database Restore Successful!")
        else:
            QMessageBox.critical(self, 'Aborted', 'Database Restore Aborted!')
            self.message_box.setText("Database Restore Aborted!")

    # REPORT GENERATION
    def write_pdf(self):
        rply = QMessageBox.question(self, 'Export', "Export to PDF?", QMessageBox.Yes | QMessageBox.No,
                                    QMessageBox.No)
        if rply == QMessageBox.Yes:
            contacts_report.pdf.output('REPORTS/Contacts.pdf')
            QMessageBox.critical(self, 'Success', 'Phonebook Exported! As REPORTS/Contacts.pdf')
            self.message_box.setText("Phonebook Exported to REPORTS/Contacts.pdf")
        else:
            QMessageBox.critical(self, 'Aborted', 'Export to PDF Aborted!')
            self.message_box.setText("Export Aborted!")

    # EXIT PROGRAM
    def exit_program(self):
        rply = QMessageBox.question(self, 'Close App', "Close Phone Book?", QMessageBox.Yes | QMessageBox.No,
                                    QMessageBox.No)
        if rply == QMessageBox.Yes:
            sys.exit(0)
        else:
            QMessageBox.critical(self, 'Aborted', 'Exit App Aborted!')
            self.message_box.setText("Exit Aborted!")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = MainWindow()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(ui)
    widget.setFixedHeight(409)
    widget.setFixedWidth(859)
    widget.show()
    sys.exit(app.exec_())


