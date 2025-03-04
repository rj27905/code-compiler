import sys
import platform

print("Python Version:", sys.version)
print("Platform:", platform.platform())

try:
    import tkinter
    print("Tkinter imported successfully")
    print("Tkinter version:", tkinter.TkVersion)
except ImportError as e:
    print("Tkinter import failed:", e)
except Exception as e:
    print("Unexpected error:", e)

try:
    import _tkinter
    print("_tkinter imported successfully")
except ImportError as e:
    print("_tkinter import failed:", e)
except Exception as e:
    print("Unexpected error:", e)