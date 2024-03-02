from tkinter import Tk
from src.main_window import MyApp

def main():
    root = Tk()
    app = MyApp(root)
    root.resizable(False, False)
    root.mainloop()

if __name__ == "__main__":
    main()