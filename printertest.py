import usb.core
import usb.util
import win32print
import sqlite3
import win32ui

#printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL,None,1)

#for printer in printers:
#    print(printer[2])
#<< DEFAULT VARIABLES >>#
cut_command = b'\x1B\x69' 
file_path='C:\\Users\\myagmardorj\\Git\\test.txt'
printer_name ='THERMAL Receipt Printer'

#### PRINT ZONE

filehandle = open(file_path, 'rb')
printer_handle = win32print.OpenPrinter(printer_name)
JobInfo = win32print.StartDocPrinter(printer_handle,1,(file_path,None,"RAW"))
win32print.StartPagePrinter(printer_handle)
win32print.WritePrinter(printer_handle,filehandle.read())
win32print.EndPagePrinter(printer_handle)
win32print.EndDocPrinter(printer_handle)
win32print.ClosePrinter(printer_handle)
filehandle.close()

#### CUT ZONE 

hdc = win32ui.CreateDC()
hdc.CreatePrinterDC(printer_name)

        # Send the cut command (ESC/POS command for partial cut)
cut_command = b'\x1B\x69'  # ESC i command for cutting paper
hdc.StartDoc("Cut Command")
hdc.StartPage()
hdc.WritePrinter(cut_command)
hdc.EndPage()
hdc.EndDoc()

import openpyxl

# Sample data in a list of lists
data = [
    ["Name", "Age", "City"],
    ["Alice", 30, "New York"],
    ["Bob", 25, "Chicago"],
    ["Eve", 35, "Los Angeles"]
]
for i in range(10000):
    value1 = "name" + str(i)
    value2 = "city" + str(i)
    data.append([value1, str(i), value2])
# Create a new Excel workbook and select the active worksheet
workbook = openpyxl.Workbook()
sheet = workbook.active

# Iterate through the data and write it to the worksheet
for row in data:
    sheet.append(row)

# Save the workbook to a file
workbook.save("output.xlsx")

print("Data has been written to output.xlsx")
