"""
------------------------------------------------------------------------
[program description]
------------------------------------------------------------------------
Author: Branden Wheeler
ID:     190197360
Email:  whee7360@mylaurier.ca
__updated__ = "2019-09-27"
------------------------------------------------------------------------
"""
from tkinter import *
from tkinter import messagebox
from finance_scraper import AddCompany
from sql_implementation import DB
import os

TITLE_FONT = ("Bookman Old Style", 22, "bold")


class FinScraperUI(Tk):
    
    def __init__ (self, *args, **kwargs):
        
        Tk.__init__(self, *args, **kwargs)
        container = Frame(self)
        
        container.pack(side="top", fill="both", expand=True)
        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        
        for F in (MenuScreen, AddScreen, DeleteScreen, DisplayScreen, NotImplemented):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(MenuScreen)
        
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        
    def refresh(self):
        self.destroy()
        os.system('user_interface.py')
        
class MenuScreen(Frame):
    
    def __init__ (self, parent, controller):

        add_img = PhotoImage(file='resources/AddButton.png')
        display_img = PhotoImage(file='resources/DisplayButton.png')
        delete_img = PhotoImage(file='resources/DeleteButton.png')
        search_img = PhotoImage(file='resources/SearchButton.png')
        quit_img = PhotoImage(file='resources/QuitButton.png')
        
        Frame.__init__(self, parent)
        
        self.configure(bg="white")
        label = Label(image=add_img)
        label.image = add_img
        
        label = Label(image=display_img)
        label.image = display_img
        
        label = Label(image=delete_img)
        label.image = delete_img
        
        label = Label(image=search_img)
        label.image = search_img
        
        label = Label(image=quit_img)
        label.image = quit_img
        
        title = Label(self, text="Yahoo Finance Database", font=TITLE_FONT, fg="green", bg="white")
        title.place(x=75, y=10)

        add_button = Button(self, image=add_img, command=lambda: controller.show_frame(AddScreen), borderwidth=0, bg="white")
        add_button.place(height=55, width=425, x=50, y=60)
        
        view_button = Button(self, image=display_img, command=lambda: controller.show_frame(DisplayScreen), borderwidth=0, bg="white")
        view_button.place(height=55, width=425, x=50, y=125)
        
        delete_button = Button(self, image=delete_img, command=lambda: controller.show_frame(DeleteScreen), borderwidth=0, bg="white")
        delete_button.place(height=55, width=425, x=50, y=190)
        
        search_button = Button(self, image=search_img, command=lambda: controller.show_frame(NotImplemented), borderwidth=0, bg="white")
        search_button.place(height=55, width=425, x=50, y=255)
        
        quit_button = Button(self, image=quit_img, command=quit, borderwidth=0, bg="white")
        quit_button.place(height=55, width=425, x=50, y=320)
        
        refresh_button = Button(self, text="Refresh", command=lambda: controller.refresh())
        refresh_button.pack()
        

        
        
class AddScreen(Frame):
    
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.configure(bg="white")
        
        title = Label(self, text="Add Company", font=TITLE_FONT, fg="green", bg="white")
        title.place(x=140, y=10)
            
        description = Label(self, text="Enter the stock symbol of the company to be added", bg="white")
        description.place(x=10, y=60)
        
        e = Entry(self, font=TITLE_FONT, highlightcolor="blue", highlightthickness=2)
        e.place(x=10, y=80, width=400, height=50)
        
        enter_button = Button(self, text="Add", font=TITLE_FONT, command=lambda: self.add_company(e.get().lower()))
        enter_button.place(x=405, y=80, width=85, height=50)
        
        return_button = Button(self, text="Return to main", font=TITLE_FONT, command=lambda: controller.show_frame(MenuScreen))
        return_button.place(x=175, y=140, width=150, height=30)
        
    def add_company(self, name):
        
        db = DB()
        answer = True;
        if db.tableExists(name):
            answer = messagebox.askyesno("Already Exists", "A table with this name already exists. Would you like to overwrite?")
            if answer:
                db.deleteTable(name)
        
        if answer:
            adder = AddCompany(name.upper())
            try:
                adder.use()
                db.createTable(name, adder)
                db.addRow(name, 'Income Headers', adder.income_data[0][0], adder.income_data[0][1], adder.income_data[0][2], 'Income')
                db.addRows(name, adder.income_data[1:], "Income")
                
                db.addRow(name, 'Balance Headers', adder.balance_data[0][0], adder.balance_data[0][1], adder.balance_data[0][2], 'Income')
                db.addRows(name, adder.balance_data[1:], "Balance")
                
                db.addRow(name, 'Cash Headers', adder.cash_data[0][0], adder.cash_data[0][1], adder.cash_data[0][2], 'Income')
                db.addRows(name, adder.cash_data[1:], "Cash")
                
                self
                
            except Exception as e:
                print(e)
                adder.test()
                adder.quit()
                messagebox.showerror("Error!", 
                         "An error has occurred. Please check your input and internet connection")
        
class DeleteScreen(Frame):
    
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.configure(bg="white")
        
        db = DB()

        title = Label(self, text="Delete Company", font=TITLE_FONT, bg="white")
        title.place(x=140, y=10)
            
        description = Label(self, text="Enter the stock symbol of the company to be deleted", bg="white")
        description.place(x=10, y=60)
        
        e = Entry(self, font=TITLE_FONT, highlightcolor="blue", highlightthickness=2)
        e.place(x=10, y=80, width=400, height=50)
        
        enter_button = Button(self, text="Delete", command=lambda: self.delete_company(e.get(), db))
        enter_button.place(x=405, y=80, width=85, height=50)
        
        return_button = Button(self, text="Return to main", command=lambda: controller.show_frame(MenuScreen))
        return_button.place(x=175, y=140, width=150, height=30)
        
        
        
    def delete_company(self, name, db):     
        db.deleteTable(name)
        
class DisplayScreen(Frame):
    
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
            
        db = DB()
        
        tables = db.get_tables()
        for table in tables:
            label = Label(self, text=table[0].upper())
            label.pack()
            
        return_button = Button(self, text="Return to main", command=lambda: controller.show_frame(MenuScreen))
        return_button.place(x=175, y=140, width=150, height=30)
            
        
        
class NotImplemented(Frame):
    
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        
        label = Label(self, text="Not yet implemented")
        label.pack()
        
        return_button = Button(self, text="Return to main", command=lambda: controller.show_frame(MenuScreen))
        return_button.pack()
        
        
root = FinScraperUI()
root.geometry("500x400+300+100")
root.resizable(False, False)
root.title("Yahoo Finance Database")
root.iconbitmap('resources/stockicon.ico')

def update(frame):
    root.destroy()
    root.show_frame(frame)
    os.system('user_interface.py')
    
root.mainloop()

