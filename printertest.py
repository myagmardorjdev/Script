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

