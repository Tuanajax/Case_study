from datetime import datetime
from tkinter import ttk
import sqlite3
from tkinter import *
from random import randint, random
import re
from tkinter import messagebox
from tkinter import ttk
from Database_class import*
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)

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
        Label(self,text="Wrong Password'format or Blanked Field of name").grid(row =4,column =1) 

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
            self.destroy()
                   
class Login(Toplevel):
    def __init__(self,master): 
        super().__init__(master)
        self.geometry('400x150')
        self.title('Login')
        lbl_id = Label(self,text="ID").grid(row=0,column=0)
        self.ID=StringVar()
        ent_username = Entry(self,textvariable=self.ID).grid(row=0,column=1)
        
        lbl_pw = Label(self,text="Enter the password").grid(row =1,column =0)
        self.pw =StringVar()
        ent_pw = Entry(self,textvariable=self.pw,show="*").grid(row=1,column=1)
        
        Butt_login=Button(self,text='Login',command=self.validateLogin).grid(row=4, column=0)
    
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
    def  close(self):        
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
        self.view()
#to update the values of the selected row with the values passed by the user
    def update(self, id, title, genre,author):    
        self.cur.execute(f"UPDATE {self.data} SET title=?, genre=?, author=? WHERE id=?", (title,genre,author,id,))
        self.conn.commit()
        self.view()
#to delete the row from the table given of the id of the selected row.
    def delete(self, id):                   
        self.cur.execute(f"DELETE FROM {self.data} WHERE id=?", (id,))
        self.conn.commit()
        self.view()
#to search for a given entry in the table given either the value of the title or author name
    def search(self, title="",genre="" ,author=""):  
        self.cur.execute(f"SELECT * FROM {self.data} WHERE title=? OR genre=? OR author=?", (title, genre,author,))
        rows = self.cur.fetchall()
        return rows

    def Top3_Author(self):
        self.cur.execute(f'SELECT author, COUNT(ID) column FROM {self.data} GROUP BY author order by column DESC limit 3') 
        rows = self.cur.fetchall()
        return rows
window = Tk()
window.title("My Books!!!!")

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
    ent_title.insert(END,selected_item[1])
    ent_genre.insert(END,selected_item[2])
    ent_author.insert(END,selected_item[3])

# def check_data_exist():
#     count_=0
#     for row in Table_.view():
#         if row[1]==title_text.get(): 
#             count_+=1
#     if count_>=1 or not title_text.get():
#         return True
#     else:
        # return messagebox.askokcancel("Quit", "The title  not already exists!")    
        
def clear_field():
    ent_title.delete(0,END)
    ent_genre.delete(0,END)
    ent_author.delete(0,END)

def clear_treev():
    for item in tree.get_children():
        tree.delete(item)
def view():    
    clear_field()      
    clear_treev()
    for row in Table_.view():   
        tree.insert('',END,values = row)
    for i in range(3):
        (f'Author {Table_.Top3_Author()[i][0]}: {Table_.Top3_Author()[i][1]}')

def search():     
    clear_treev()
    for row in Table_.search(title_text.get(), genre_text.get(), author_text.get()): 
        tree.insert('',END, values = row) 

def insert_field():
    tree.insert('',END,values=(title_text.get(), genre_text.get(), author_text.get()))
def check_blanked_field():
    if  not ent_title.get() or  not ent_genre.get() or not ent_author.get():
        return messagebox.askokcancel("Quit", "There are several blanked fields?")

def add():      
    global a  
    global now_
    if check_blanked_field():True
    else:        
        Table_.insert(title_text.get(), genre_text.get(), author_text.get()) 
        now_=datetime.now()
        a = f"{now_}.ADD:{title_text.get()},{genre_text.get()},{author_text.get()}"
        logfile(a)
        view()
def delete(): 
        global b
        if tree.focus()!='':
            if messagebox.askokcancel("Quit", "Are you sure?"): 
                b =selected_item[1]
                Table_.delete(selected_item[0])
                tree.delete(tree.selection()[0])
                logfile(f"DELETE:{b}")
                view()
            else: clear_field() 
        else: messagebox.showwarning("showwarning", "Lookout, Have selected yet! ")
    

def update():
    if check_blanked_field() and tree.focus()!='': True
    else:
        Table_.update(selected_item[0], title_text.get(), genre_text.get(), author_text.get()) 
        now_=datetime.now()
        c = f"{now_}.UPDate:{title_text.get()},{genre_text.get()},{author_text.get()}"
        # clear_field()
        logfile(c)
        view()

def Histogram():
    fig = Figure(figsize=(5.5),dpi=100)
    canvas = FigureCanvasTkAgg(fig,window)
    canvas.draw()

def ask_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"): 
                window.destroy()      
                Table_.close()        
window.protocol("WM_DELETE_WINDOW", ask_closing)


lbl_title = Label(window, text="Title",width=20).grid(row=0, column=1,sticky='nsew')

lbl_genre = Label(window, text="genre", width=20).grid(row=1, column=1,sticky='nsew')

lbl_author = Label(window, text="author", width=20).grid(row=2, column=1,sticky='nsew')

title_text = StringVar()
ent_title = Entry(window, textvariable=title_text,width=20)
ent_title.grid(row=0, column=2,sticky='nsew')

genre_text = StringVar() 
ent_genre = Entry(window, textvariable=genre_text,width=20)
ent_genre.grid(row=1, column=2,sticky='nsew')

author_text = StringVar() 
ent_author = Entry(window, textvariable=author_text,width=20)
ent_author.grid(row=2, column=2,sticky='nsew')

#  Tree 
columns = ('1', '2', '3','4')
tree = ttk.Treeview(columns=columns, show='headings')
tree.heading('1', text='ID')
tree.heading('2', text='Title')
tree.heading('3', text='genre')
tree.heading('4', text='Author')
tree.grid(row=3,column=1,rowspan=6,columnspan=2,sticky='nsew')

tree.bind('<<TreeviewSelect>>', item_selected)

scrollbar = ttk.Scrollbar(window,orient=VERTICAL,command=tree.yview)
tree.config(yscrollcommand=scrollbar.set)
scrollbar.grid(row=3,column=3,rowspan=6,sticky='ne')



butt_view = Button(window, text="View all", width=12, command=view).grid(row=3, column=0)

butt_search = Button(window, text="Search ", width=12, command=search).grid(row=4, column=0)

butt_Add = Button(window, text="Add Items", width=12, command=add).grid(row=5, column=0)

butt_Update = Button(window, text="Update selected", width=12, command=update).grid(row=6, column=0)

butt_Delete = Button(window, text="Delete selected", width=12, command=delete).grid(row=7, column=0)

button_Histogram = Button(window, text = 'Histogram',command=Histogram, width=12).grid(row=8,column=0)

# Menu bar placed on the left-side of the window, which consists: login; sign-up;
menubar =Menu(window)
acount = Menu(menubar,tearoff=0)
menubar.add_cascade(label=f"My account", menu=acount)
acount.add_command(label = 'login/switch', comman = lambda:Login(master))
acount.add_command(label = 'Sign-up', comman = lambda:Sign_Up(master))
acount.add_separator()
acount.add_command(label = 'Exit', comman = ask_closing)

window.config(menu=menubar)

window.mainloop() #carry the functioning o







