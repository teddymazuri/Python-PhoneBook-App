from fpdf import FPDF
from fpdf.enums import XPos, YPos
import sqlite3


# Create Database Connection
conn = sqlite3.connect('phonebook.db')
cur = conn.cursor()
query = "SELECT * FROM contacts"
cur.execute(query)
results = cur.fetchall()


class PDF(FPDF):
    # Page header
    def header(self):
        # Font
        self.set_font('courier', 'BU', 20)
        # Title
        self.cell(0, 10, 'CONTACTS', border=False, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        # Line Break
        self.ln(10)

    # Page footer
    def footer(self):
        # Set position
        self.set_y(-15)
        # Set Font
        self.set_font('courier', 'I', 10)
        # Page number
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')


TABLE_DATA = []
headers = "Id", "First Name", "Last Name", "E-Mail", "Phone Number"
TABLE_DATA.append(headers)
for result in results:
    result_f = str(result[0]), result[1], result[2], result[3], result[4]
    TABLE_DATA.append(result_f)

pdf = PDF()
pdf.add_page()
pdf.set_font("Courier", size=11)
with pdf.table(width=170, col_widths=(10, 20, 20, 45, 25), text_align="CENTER") as table:
    for data_row in TABLE_DATA:
        row = table.row()
        for datum in data_row:
            row.cell(datum)
# pdf.output('table.pdf')
