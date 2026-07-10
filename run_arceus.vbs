Set WshShell = CreateObject("WScript.Shell")
' The 0 at the end forces the terminal window to hide completely
WshShell.Run "pythonw.exe ""D:\Projects\ARCEUS\main.py""", 0, False