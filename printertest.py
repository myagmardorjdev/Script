import usb.core
import usb.util
import win32print

printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL,None,1)

for printer in printers:
    print(printer[2])

file_path='C:\\Users\\myagmardorj\\Git\\test.txt'
printer_name ='THERMAL Receipt Printer'
filehandle = open(file_path, 'rb')
printer_handle = win32print.OpenPrinter(printer_name)

JobInfo = win32print.StartDocPrinter(printer_handle,1,(file_path,None,"RAW"))

win32print.StartPagePrinter(printer_handle)

win32print.WritePrinter(printer_handle,filehandle.read())

win32print.EndPagePrinter(printer_handle)

win32print.EndDocPrinter(printer_handle)
win32print.ClosePrinter(printer_handle)
win32print.ClosePrinter()