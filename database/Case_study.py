from cgitb import text
from datetime import datetime
from operator import index
import matplotlib.pyplot as plt
from tkinter import ttk
from cProfile import label
from distutils.cmd import Command
from doctest import master
import sqlite3
from tkinter import *
from random import randint, random
import re
from tkinter import messagebox
from tkinter import ttk
from tkinter.tix import Tree
from turtle import clear, left, right, width
from typing_extensions import Self
from webbrowser import get
from Database_class import*
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)

Data_={"A1":('Vu Anh Tuan','1'),"A2":("Do van hung","2")}

class Sign_Up(Toplevel):
    
    def __init__(self,master): 
        super().__init__(master)
        self.geometry('400x150')
        self.title('Registion')
        # Row of user name
        lbl_username = Label(self,text="User Name").grid(row=0,column=0)
        self.add_us=StringVar()
        ent_username = Entry(self,textvariable=self.add_us).grid(row=0,column=1)

        # Row of Password
        lbl_pw = Label(self,text="Enter the password").grid(row =1,column =0)
        self.add_pw =StringVar()
        ent_pw = Entry(self,textvariable=self.add_pw).grid(row=1,column=1)

        # Login button
        Butt_sign=Button(self,text='Sign-up',command=self.add).grid(row=4, column=0)
    
    def reset(self):
        self.add_us.set('')
        Label(self,text="Wrong").grid(row =4,column =1) 

    def valid_pw(self,PW):  
    # Check exist_Uppercase:
        for i in range(0,len(PW)):
            if PW[i].isupper() == True: 
                Txt = True
                break
    # Password contains:Just 08 chars; at least a number, an uppercase; non-white-space
        if len(PW)==8 and Txt and re.findall('\d',PW) and PW.count(" ")==0:
            return False
        else: return True  

    def add(self):
        global  Data_
    #  Name
        name_ = self.add_us.get()
        if not name_:
            self.reset()       
    # ID
        add_ID = f"ARSENAL{randint(1,22)}"     
        while True:
            if add_ID in Data_: 
                True
                add_ID = f"ARSENAL{randint(1,22)}"
            else: break
    # Password
        pw_ = self.add_pw.get()
    # Adding....
        if self.valid_pw(pw_):
            self.reset()
        else:
            Data_[add_ID] = name_,pw_
            print(Data_)
            messagebox.showinfo('Infor',f'Success!\n-ID:{add_ID}\n-User name: {name_}')
            
            login_=Login(window)
            
            self.destroy()
                   
class Login(Toplevel):
    def __init__(self,master): 
        super().__init__(master)
        self.geometry('400x150')
        self.title('Login')
        lbl_id = Label(self,text="ID").grid(row=0,column=0)
        self.ID=StringVar()
        Entry(self,textvariable=self.ID).grid(row=0,column=1)
        
        Label(self,text="Enter the password").grid(row =1,column =0)
        self.pw =StringVar()
        Entry(self,textvariable=self.pw,show="*").grid(row=1,column=1)
        
        Button(self,text='Login',command=self.validateLogin).grid(row=4, column=0)
    
    def close_log(self):
        self.destroy()

    def reset(self,ms):
        self.ID.set('')
        self.ID.set('')
        Label(self,text=ms).grid(row =4,column =1)  

    def validateLogin(self):
        global Table_
        a = self.ID.get().upper()
        if a in Data_ and self.pw.get() == Data_[a][1]: 
            self.close_log()
    # Connecting to The table of DataBase
            Table_ = DB(a)
            messagebox.showinfo('Welcome!',f'Success!\n-ID:{a}')
    # To show database by The tree_view(Main_window)
            view()
    # Showing ID and name of the user on main_window
            Label(window, text=f'ID:{a}\n \nName:{Data_[a][0]}' ).grid(row=0, column=0,rowspan=2)
        else: self.reset("wrong")

class DB:                          
    def __init__(self, Table):  
        self.data = Table
        self.conn = sqlite3.connect("mybooks.db")  
        self.cur = self.conn.cursor()            
        self.cur.execute(f"CREATE TABLE IF NOT EXISTS {self.data} (id INTEGER PRIMARY KEY, title TEXT, genre TEXT,author TEXT)")
        self.conn.commit() 
#closes the connection with the database
    def __del__(self):        
        self.conn.close()   
        
#To view all the rows present in the table
    def view(self):                
        self.cur.execute(f"SELECT * FROM {self.data}") 
        rows = self.cur.fetchall() 
        return rows
#inserting a new row in the table.
    def insert(self, title, genre,author):   
        self.cur.execute(f"INSERT INTO {self.data} VALUES (NULL,?,?,?)", (title, genre,author,)) 
        self.conn.commit()
        # self.view()
#to update the values of the selected row with the values passed by the user
    def update(self, id, title, genre,author):    
        self.cur.execute(f"UPDATE {self.data} SET title=?, genre=?, author=? WHERE id=?", (title,genre,author,id,))
        self.conn.commit()
        # self.view()
#to delete the row from the table given of the id of the selected row.
    def delete(self, id):                   
        self.cur.execute(f"DELETE FROM {self.data} WHERE id=?", (id,))
        self.conn.commit()
        # self.view()
#to search for a given entry in the table given either the value of the title or author name
    def search_title(self, title):  
        self.cur.execute(f"SELECT * FROM {self.data} WHERE title like ?", ("%"+title+"%",))
        rows = self.cur.fetchall()
        return rows
    
    def search_genre(self, genre):  
        self.cur.execute(f"SELECT * FROM {self.data} WHERE genre like ? ", ("%"+genre+"%",))
        rows = self.cur.fetchall()
        return rows
    
    def search_author(self,author):  
        self.cur.execute(f"SELECT * FROM {self.data} WHERE author like ? ", ("%"+author+"%",))
        rows = self.cur.fetchall()
        return rows

    def Top_Author(self):
        self.cur.execute(f'SELECT author, COUNT(ID) column FROM {self.data} GROUP BY author order by column DESC limit 1') 
        rows = self.cur.fetchall()
        return rows
    
    def genre_(self):
        self.cur.execute(f'SELECT genre, COUNT(ID) column FROM {self.data} GROUP BY genre')
        rows =self.cur.fetchall()
        return rows
    
    def report(self):
        report_label =[]
        report_list=[]
        for i in Data_.keys():
            self.cur.execute(f'SELECT genre, COUNT(ID) Column FROM {i} GROUP BY genre')
            rows =self.cur.fetchall()
            for j in range(len(rows)):
                report_list.append(rows[j])
        for i in report_list:
            report_label.append(i[0])
        report_label=list(dict.fromkeys(report_label))
        Dict = {}
        for i in report_label:
            count = 0
            for j in report_list:
                if i == j[0]: count+=j[1]
            Dict[i]=count
        return Dict
        
            
window = Tk()
window.title("My Books!!!!")

def get_value():
    return (title_text.get().capitalize().strip(),genre_text.get().capitalize(),author_text.get().capitalize(),)

log_file=list()
def logfile(record):
    # global log_file
    log_file.append(record)
    txt_History = Text(window, height=5, width=80)
    txt_History.grid(row=8, column=1,columnspan=2,sticky='nsew') 
    txt_History.insert(END,log_file)

def item_selected(event):
    global selected_item
    selected = tree.focus()
    selected_item = tree.item(selected,'values')
    clear_field()
    for i in range(3):
        entry_text[i].set(selected_item[1+i])

def check_data_exist():
    count_=0
    for row in Table_.view():
        if row[1]==title_text.get().capitalize().strip(): 
            count_+=1
            # print(row[1])
    if count_>=1 :
        return messagebox.askokcancel("Quit", "The title already exists!")
    
          
def clear_field():
    for i in entry_text:
        i.set("")   
    
def clear_treev():
    for item in tree.get_children():
        tree.delete(item)

def view():    
    clear_field()      
    clear_treev()
    for row in Table_.view():   
        tree.insert('',END,values = row)
    chart()

def search_title():     
    clear_treev()
    for row in Table_.search_title(title_text.get()): 
        tree.insert('',END, values = row) 

def search_genre():     
    clear_treev()
    for row in Table_.search_genre(genre_text.get()): 
        tree.insert('',END, values = row) 

def search_author():   
    clear_treev()
    for row in Table_.search_author(author_text.get()): 
        tree.insert('',END, values = row) 

def insert_field():
    tree.insert('',END,values=get_value())

def check_blanked_field():
    if entry_text[0].get=="" or entry_text[1].get()=="" or entry_text[2].get()=="":
        return messagebox.askokcancel("Quit", "There are several blanked fields ?")

def add():      
    global a  
    global now_
    if check_blanked_field(): True
    elif check_data_exist():True
    else:        
        Table_.insert(*get_value()) 
        now_=datetime.now()
        a = f"{now_}.ADD:{get_value()}"
        logfile(a)
        view()
        chart()

def delete(): 
        global b
        if tree.focus()!='':
            if messagebox.askokcancel("Quit", "Are you sure?"): 
                b =selected_item[1]
                Table_.delete(selected_item[0])
                tree.delete(tree.selection()[0])
                logfile(f"DELETE:{b}")
                view()
                chart()
            else: clear_field() 
        else: messagebox.showwarning("Warning", "Lookout, Have selected yet! ")
    

def update():
    if check_blanked_field() and tree.focus()!='': True
    elif check_data_exist(): True
    else:
        Table_.update(selected_item[0],*get_value()) 
        now_=datetime.now()
        c = f"{now_}.UPdate:{get_value()}"
        # clear_field()
        logfile(c)
        view()
        chart()

def chart():
    frame_chart=Frame(window)
    frame_chart.grid(row=9,column=0, columnspan= 3)
    for i in range(3):  
        Label(frame_chart, text="All of the Users").grid(row=0, column=i)
    lst_y =[]
    lst_label =[]
    for row in Table_.genre_():
        lst_label.append(row[0])
        lst_y.append(row[1])
    fig1 = Figure(figsize=(2,2))
    ax = fig1.add_subplot()
    ax.pie(lst_y, radius=1, labels=lst_label,autopct='%0.2f%%', shadow=True,)
    chart1 = FigureCanvasTkAgg(fig1,frame_chart)
    chart1.get_tk_widget().grid(column=1,row=1)
    # pie_chart_allusers():
    label = []
    axis_y = []
    for x,y in Table_.report().items():
        label.append(x)
        axis_y.append(y)
    fig2 = Figure(figsize=(2,2))
    ax = fig2.add_subplot()
    ax.pie(axis_y, radius=1, labels=label,autopct='%0.2f%%', shadow=True,)
    chart2 = FigureCanvasTkAgg(fig2,frame_chart)
    chart2.get_tk_widget().grid(column=0,row=1)
 
 # Top_List_author_person():
    lst_Top = Listbox(frame_chart)
    lst_Top.grid(column=2,row=1)
    for row in Table_.Top_Author():
        lst_Top.insert(END,row)

def ask_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"): 
                window.destroy()      
                Table_.__del__()  
window.protocol("WM_DELETE_WINDOW", ask_closing)

frame1=Frame(window)
frame1.grid(row=0,column=1,columnspan=3)
title_text, genre_text,author_text =StringVar(),StringVar(),StringVar()
entry_text = (title_text,genre_text,author_text) 

butt_txt = ("View/Reset","Add Item","Update Item","Delete Item")

lbl_text = ("Title","Genre","Author",)

butt_def =(view,add,update,delete)

lst_def =(search_title,search_genre,search_author)

for i in range(3):
    Label(frame1, text=lbl_text[i],width=20).grid(row=i, column=0)

    Button_search=Button(frame1, text="Search ", width=12, command=lst_def[i]).grid(row=i, column=2)

    Entry(frame1, textvariable=entry_text[i],width=20).grid(row=i, column=1)

    Button(window, text=butt_txt[i], width=12, command=butt_def[i]).grid(row=i+3, column=0)
else:Button(window, text=butt_txt[3], width=12, command=butt_def[3]).grid(row=6, column=0)   
#  Tree 
columns = ('1', '2', '3','4')
columns_text=('ID',"Title","Genre","Author")
tree = ttk.Treeview(columns=columns, show='headings')
for i in range(4):
    tree.heading(f'{i+1}', text=columns_text[i])
tree.grid(row=3,column=1,rowspan=6,sticky='nsew')
tree.bind('<<TreeviewSelect>>', item_selected)

scrollbar = ttk.Scrollbar(window,orient=VERTICAL,command=tree.yview)
tree.config(yscrollcommand=scrollbar.set)
scrollbar.grid(row=3,column=3,rowspan=6,sticky='ne')

# Menu bar placed on the left-side of the window, which consists: login; sign-up;
menubar =Menu(window)
acount = Menu(menubar,tearoff=0)
menubar.add_cascade(label="My account", menu=acount)
acount.add_command(label = 'login/switch', comman = lambda:Login(master))
acount.add_command(label = 'Sign-up', comman = lambda:Sign_Up(master))
acount.add_separator()
acount.add_command(label = 'Exit', comman = ask_closing)

window.config(menu=menubar)


window.mainloop()







