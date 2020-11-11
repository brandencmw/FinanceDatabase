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
import csv
#a73737
#7a2828


TITLE_FONT = ("Bookman Old Style", 40, "bold")
DISPLAY_FONT = ("Bookman Old Style", 24, "bold")
TABLE_FONT = ("Times New Roman", 9)


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
        refresh_img = PhotoImage(file='resources/RefreshButton.png')
        quit_img = PhotoImage(file='resources/QuitButton.png')
        
        Frame.__init__(self, parent)
        
        self.configure(bg="white")
        label = Label(image=add_img)
        label.image = add_img
        
        label = Label(image=display_img)
        label.image = display_img
        
        label = Label(image=delete_img)
        label.image = delete_img
        
        label = Label(image=refresh_img)
        label.image = refresh_img
        
        label = Label(image=quit_img)
        label.image = quit_img
        
        title = Label(self, text="Yahoo Finance Database", font=TITLE_FONT, fg="green", bg="white")
        title.place(x=600, y=70, anchor="center")

        add_button = Button(self, image=add_img, command=lambda: controller.show_frame(AddScreen), borderwidth=0, bg="white")
        add_button.place(height=85, width=510, x=80, y=150)
        
        delete_button = Button(self, image=delete_img, command=lambda: controller.show_frame(DeleteScreen), borderwidth=0, bg="white")
        delete_button.place(height=85, width=510, x=610, y=150)
        
        display_button = Button(self, image=display_img, command=lambda: controller.show_frame(DisplayScreen), borderwidth=0, bg="white")
        display_button.place(height=85, width=510, x=80, y=310)
        
        refresh_button = Button(self, image=refresh_img, command=lambda: controller.refresh(), borderwidth=0, bg="white")
        refresh_button.place(height=85, width=510, x=610, y=310)
        
        quit_button = Button(self, image=quit_img, command=quit, borderwidth=0, bg="white")
        quit_button.place(height=85, width=510, x=345, y=470)

        
        
class AddScreen(Frame):
    
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.configure(bg="white")
        
        title = Label(self, text="Add Company", font=TITLE_FONT, bg="white")
        title.place(x=600, y=50, anchor="center")
            
        description = Label(self, text="Enter the stock symbol of the company to be added", bg="white")
        description.place(x=355, y=110)
        
        e = Entry(self, font=TITLE_FONT, highlightcolor="blue", highlightthickness=2)
        e.place(x=355, y=130, width=400, height=50)
        
        enter_button = Button(self, text="Add", command=lambda: self.add_company(e.get().lower()))
        enter_button.place(x=760, y=130, width=90, height=50)
        
        return_button = Button(self, text="Return to main", command=lambda: controller.show_frame(MenuScreen))
        return_button.place(x=525, y=230, width=150, height=30)
        
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
                db.createTable(name)
                db.addRow(name, 'Income Headers', adder.income_data[0][0], adder.income_data[0][1], adder.income_data[0][2], 'Income')
                db.addRows(name, adder.income_data[1:], "Income")
                
                db.addRow(name, 'Balance Headers', adder.balance_data[0][0], adder.balance_data[0][1], adder.balance_data[0][2], 'Balance')
                db.addRows(name, adder.balance_data[1:], "Balance")
                
                db.addRow(name, 'Cash Headers', adder.cash_data[0][0], adder.cash_data[0][1], adder.cash_data[0][2], 'Cash')
                db.addRows(name, adder.cash_data[1:], "Cash")
                
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
        title.place(x=600, y=50, anchor="center")
            
        description = Label(self, text="Enter the stock symbol of the company to be deleted", bg="white")
        description.place(x=355, y=110)
        
        e = Entry(self, font=TITLE_FONT, highlightcolor="blue", highlightthickness=2)
        e.place(x=355, y=130, width=400, height=50)
        
        enter_button = Button(self, text="Delete", command=lambda: self.delete_company(e.get(), db))
        enter_button.place(x=760, y=130, width=90, height=50)
        
        return_button = Button(self, text="Return to main", command=lambda: controller.show_frame(MenuScreen))
        return_button.place(x=525, y=230, width=150, height=30)
        
        
    def delete_company(self, name, db):  
        
        if not db.tableExists(name):
            messagebox.showinfo("Not Found", "This table could not be found. Perhaps it was already deleted")
        else:   
            db.deleteTable(name)
        
class DisplayScreen(Frame):
    
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.configure(bg="white")
            
        db = DB()
                
        tables = db.get_tables()
        self.statement = "Income"
        self.i = 0
        self.labels = []
        
        if len(tables) > 0:
            self.company_label = Label(self, text=tables[self.i][0].upper(), font=DISPLAY_FONT, bg="white", borderwidth=2, relief="solid")
            self.company_label.place(x=600, y=30, width=550, height=40, anchor="center")
        
            self.statement_label = Label(self, text="Income Statement", font=DISPLAY_FONT, bg="white", borderwidth=2, relief="solid")
            self.statement_label.place(x=600, y=80, width=550, height=40, anchor="center")
            
            self.data = db.get_by_doc_type(tables[self.i][0], self.statement)
            
            self.create_table()
            
            company_left = Button(self, text="<", command=lambda: self.scroll_company_left(tables, db))
            company_left.place(x=310, y=30, width=40, height=40, anchor="center")
        
            company_right = Button(self, text=">", command=lambda: self.scroll_company_right(tables, db))
            company_right.place(x=895, y=30, width=40, height=40, anchor="center")
        
            statement_right = Button(self, text=">", command=lambda: self.scroll_statement_right(tables, db))
            statement_right.place(x=895, y=80, width=40, height=40, anchor="center")
        
            statement_left = Button(self, text="<", command=lambda: self.scroll_statement_left(tables, db))
            statement_left.place(x=310, y=80, width=40, height=40, anchor="center")
            
            return_button = Button(self, text="Return to main", command=lambda: controller.show_frame(MenuScreen))
            return_button.place(x=85, y=100, width=150, height=30, anchor="center") 
            
            excel_button = Button(self, text="Export to Excel", command=lambda: self.export_to_excel(tables))
            excel_button.place(x=85, y=60, width=150, height=30, anchor="center")
            
        else:
            info_label = Label(self, text="There are no tables currently in the database\n try using the refresh button on the home screen")
            info_label.pack()
            
    def scroll_company_right(self, tables, db):
        
        if len(tables) > 0:
            if self.i == len(tables)-1:
                self.i = 0
            else:
                self.i += 1
            
            self.data = db.get_by_doc_type(tables[self.i][0], self.statement)
            self.create_table()
            
            self.company_label.destroy()
            self.company_label = Label(self, text=tables[self.i][0].upper(), font=DISPLAY_FONT, bg="white", borderwidth=2, relief="solid")
            self.company_label.place(x=600, y=30, width=550, height=40, anchor="center")
        
        
        
    def scroll_company_left(self, tables, db):
        
        if len(tables) > 0:
            if self.i == 0:
                self.i = len(tables)-1
            else:
                self.i -= 1
            
            self.data = db.get_by_doc_type(tables[self.i][0], self.statement)
            self.create_table()
            
            self.company_label.destroy()
            self.company_label = Label(self, text=tables[self.i][0].upper(), font=DISPLAY_FONT, bg="white", borderwidth=2, relief="solid")
            self.company_label.place(x=600, y=30, width=550, height=40, anchor="center")
        
    def scroll_statement_right(self, tables, db):
        
        if len(tables) > 0:
            self.statement_label.destroy()
            
            if self.statement == "Income":
                self.statement = "Balance"
                label_text = "Balance Sheet"
            elif self.statement == "Balance":
                self.statement = "Cash"
                label_text = "Cash Flow"
            else:
                self.statement = "Income"
                label_text = "Income Statement"
                
            self.data = db.get_by_doc_type(tables[self.i][0], self.statement)
            self.create_table()
                
            self.statement_label = Label(self, text=label_text, font=DISPLAY_FONT, bg="white", borderwidth=2, relief="solid")
            self.statement_label.place(x=600, y=80, width=550, height=40, anchor="center")
        
    def scroll_statement_left(self, tables, db):
        
        if len(tables) > 0:
            self.statement_label.destroy()
            
            if self.statement == "Income":
                self.statement = "Cash"
                label_text = "Cash Flow"
            elif self.statement == "Balance":
                self.statement = "Income"
                label_text = "Income Statement"
            else:
                self.statement = "Balance"
                label_text = "Balance Sheet"
                
            self.data = db.get_by_doc_type(tables[self.i][0], self.statement)
            self.create_table()
            
            self.statement_label = Label(self, text=label_text, font=DISPLAY_FONT, bg="white", borderwidth=2, relief="solid")
            self.statement_label.place(x=600, y=80, width=550, height=40, anchor="center")
            
    def create_table(self):
        
        for l in self.labels:
            l.destroy()
        
        for i in range(len(self.data)):
            for j in range(len(self.data[0])):
                if "Header" not in self.data[i][j]:
                    label = Label(self, text=self.data[i][j], font=TABLE_FONT, bg="white")
                    if j == 0:
                        label.place(x=j*300+270, y=i*16+105)
                    else:
                        label.place(x=j*100+570, y=i*16+105)
                    self.labels.append(label)
                    
    def export_to_excel(self, tables):
        
        title = "ExportedFiles/" + tables[self.i][0].upper() + self.statement + ".csv"
        with open(title, "w+") as this_csv:
            csvWriter = csv.writer(this_csv, delimiter=",")
            csvWriter.writerows(self.data)
            
        os.system('start "EXCEL.EXE" ' + title)
        
        
class NotImplemented(Frame):
    
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        
        label = Label(self, text="Not yet implemented")
        label.pack()
        
        return_button = Button(self, text="Return to main", command=lambda: controller.show_frame(MenuScreen))
        return_button.pack()
        
        
root = FinScraperUI()
root.geometry("1200x650+0+0")
root.resizable(False, False)
root.title("Yahoo Finance Database")
root.iconbitmap('resources/stockicon.ico')

def update(frame):
    root.destroy()
    root.show_frame(frame)
    os.system('user_interface.py')
    
root.mainloop()

