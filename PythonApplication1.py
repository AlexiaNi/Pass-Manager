    Password Manager-keeping your passwords safe and easy to access
    Copyright (C) <2022>  <Niculae Alexia>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.




import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import font  as tkfont
import tkinter as GUI
from tkinter import messagebox
from tkinter.ttk import *
import sqlite3
from PIL import *
from PIL import ImageTk, Image
import os
import hashlib
import webbrowser


os.system("python Password_Database_2.py")
os.system("python Main_Database_2.py")

class Application(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Calibri', size=30, weight="bold")
        self.button_font = tkfont.Font(family='Calibri', size=15, weight="bold")

        master = tk.Frame(self)
        master.pack(side="top", fill="both", expand=True)
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Frame_Login, Frame_Register, Frame_Verify, Frame_1, Frame_2, Frame_3, Frame_4, Frame_5):
            frame_name = F.__name__
            frame = F(parent=master, controller=self)
            self.frames[frame_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Frame_Login")

    def show_frame(self, frame_name):
        frame = self.frames[frame_name]
        frame.tkraise()


class Frame_Login(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        def verify():
            connectivity = sqlite3.connect('Master_2.db')
            cursor = connectivity.cursor()

            cursor.execute("""SELECT *, oid from Master_password_2""")
            your_mom = cursor.fetchall()
            if len(your_mom)==0:
                messagebox.showwarning("Warning", "Please configure master password")
            else:
                 controller.show_frame("Frame_Verify")


            connectivity.commit()
            connectivity.close()

        def register():
            connectivity = sqlite3.connect('Master_2.db')
            cursor = connectivity.cursor()

            cursor.execute("""Select *, oid from Master_password_2""")
            your_mom2 = cursor.fetchall()
            if len (your_mom2)==0:
                 controller.show_frame("Frame_Register")
            else:
                messagebox.showinfo("Info", "Master password already exists. Please verify password.")

        def exit_2():
            app.destroy()


        label_password = tk.Label(self, text="Master Window", font=controller.title_font)
        label_password.pack()
        button_login = tk.Button(self, text="Verify password", pady=10, font=controller.button_font, command=verify)
        button_login.pack()
        button_register = tk.Button(self, text="Register",padx=34, pady=10, font=controller.button_font, command=register)
        button_register.pack()
        button_exit2 = tk.Button(self, text="Exit", padx=52, pady=10, font=controller.button_font, command=exit_2)
        button_exit2.pack()
        def callback2():
            webbrowser.open_new("https://eww.pass.panasonic.co.jp/pro-av/support/content/download/EN/user/GPLLGPL.pdf")

        button_license = tk.Button(self, text="License", command=callback2)
        button_license.pack()


class Frame_Register(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label_big = tk.Label(self, text="Configure master password", font=controller.title_font).pack()
        label_enter = tk.Label(self, text="Create new password: ", font=controller.button_font).pack()
        entry_enter = tk.Entry(self, borderwidth=2.5, width=40, show='*')
        entry_enter.pack()
        label_2 = tk.Label(self, text="Enter new password again: ", font=controller.button_font).pack()
        entry_2 = tk.Entry(self, borderwidth=2.5, width=40, show='*')
        entry_2.pack()

        def configure():
            global hash_value
            hash_value = hashlib.sha256(entry_enter.get().encode('utf-8')).hexdigest()
            connectivity = sqlite3.connect('Master_2.db')
            cursor = connectivity.cursor()

            if len(entry_enter.get())==0 or len(entry_2.get())==0:
                messagebox.showwarning("Warning", "Must complete all available fields")
                question=0
            elif len(entry_enter.get())<10:
                messagebox.showwarning("Warning", "Password must be at least 10 characters long")
                question=0
            elif entry_enter.get() != entry_2.get():
                messagebox.showwarning("Warning", "Passwords do not match")
                question=0
            else:
                question = messagebox.askyesno("Proceed", "Are you sure you would like to proceed? The master password cannot be recovered or reset.")
                
            if question == 1:
                cursor.execute("INSERT INTO Master_password_2 VALUES (:Password_1)",
                {
                    'Password_1': hash_value
                }
                )
                controller.show_frame("Frame_Login")   
                messagebox.showinfo("Succes", "Master password successfully configured. I hope you enjoy the program!")


            connectivity.commit()
            connectivity.close()

        button_register2 = tk.Button(self, text="Configure password", pady=10, font=controller.button_font, width=20, command=configure).pack()


class Frame_Verify(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label_verify = tk.Label(self, text="Verify master password", font=controller.title_font).pack()
        label_enter2 = tk.Label(self, text="Enter master password: ", font=controller.button_font).pack()
        entry_enter2 = tk.Entry(self, borderwidth=2.5, width=40, show='*')
        entry_enter2.pack()

        def verify_2():
            hash_value_2 = hashlib.sha256(entry_enter2.get().encode('utf-8')).hexdigest()
            connectivity = sqlite3.connect('Master_2.db')
            cursor = connectivity.cursor()

            if len(entry_enter2.get())==0:
                messagebox.showwarning("Warning", "Must complete all available fields")
            else:
                entry_copyl = []
                entry_copyl.append(hash_value_2)
                entry_copyt = tuple(entry_copyl)

                select_3 = """SELECT * from Master_password_2"""
                cursor.execute(select_3)
                your_mom3 = cursor.fetchall()
                for moms in your_mom3:
                    if moms == entry_copyt:
                        controller.show_frame("Frame_1")
                    else:
                        messagebox.showwarning("Warning", "Incorrect password")

            connectivity.commit()
            connectivity.close()

        button_enter = tk.Button(self, text="Verify", pady=10, width=15, font=controller.button_font, command=verify_2).pack()
        button_back3 = tk.Button(self, text="Back", pady=10, width=15, font=controller.button_font, command=lambda:controller.show_frame("Frame_Login"))
        button_back3.pack()


class Frame_1(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        def exit_program():
            app.destroy()

        label_title = tk.Label(self, text="Password Manager",padx=0, pady=10, font=controller.title_font)
        label_title.pack()
        img = ImageTk.PhotoImage(Image.open("mimi.jpeg"))
        label_image = tk.Label(self, image=img)
        label_image.image = img
        label_image.pack()


        button_menu = tk.Button(self, text="Menu", padx=47,pady=10,font=controller.button_font, command=lambda:controller.show_frame("Frame_2"))
        button_menu.pack()
        def callback():
            webbrowser.open_new("https://github.com/AlexiaNi/Pass-Manager")
        button_exit = tk.Button(self, text="Exit", padx=55, pady=10,font=controller.button_font,  command=exit_program)
        button_exit.pack()
        button_link = tk.Button(self, text="GitHub Repository", command=callback)
        button_link.pack()


class Frame_2(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label_1 = tk.Label(self, text="Options", font=controller.title_font)
        label_1.pack()
        button_1 = tk.Button(self, text="Add record", font=controller.button_font, padx=68, pady=10, command=lambda:controller.show_frame("Frame_3"))
        button_1.pack()
        button_2 = tk.Button(self, text="Delete record", padx=58, pady=10, font=controller.button_font, command=lambda:controller.show_frame("Frame_4"))
        button_2.pack()
        button_3  = tk.Button(self,text="Show records", padx=60, pady=10, font=controller.button_font, command=lambda:controller.show_frame("Frame_5"))
        button_3.pack()
        button_back = tk.Button(self, text="Back to title screen",padx=38, pady=10, font=controller.button_font, command=lambda:controller.show_frame("Frame_1"))
        button_back.pack()


class Frame_3(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label_master1 = tk.Label(self, text="Add record", font=controller.title_font)
        label_master1.pack()

        label_platform = tk.Label(self, text="Enter Platform: ", font=controller.button_font)
        label_platform.pack()
        entry_platform = tk.Entry(self, borderwidth=2.5, width=40)
        entry_platform.pack()

        label_URL= tk.Label(self, text="Enter URL: ", font=controller.button_font)
        label_URL.pack()
        entry_URL = tk.Entry(self, borderwidth=2.5, width=40)
        entry_URL.pack()

        label_pass = tk.Label(self, text="Enter password: ", font=controller.button_font)
        label_pass.pack()
        entry_pass = tk.Entry(self, borderwidth=2.5, width=40, show='*')
        entry_pass.pack()

        def insert():
            connectivity = sqlite3.connect('Pass.db')

            cursor = connectivity.cursor()
 
            if len(entry_platform.get())==0 or len(entry_URL.get())==0 or len(entry_pass.get())==0:
                 messagebox.showwarning("Warning", "Must complete all available fields!")
            else:
                 cursor.execute("INSERT INTO Passes VALUES (:Platform, :URL, :Password)",
                     {
                         'Platform': entry_platform.get(),
                         'URL': entry_URL.get(),
                         'Password': entry_pass.get()
                     })

                 entry_platform.delete(0, 'end')
                 entry_URL.delete(0, 'end')
                 entry_pass.delete(0, 'end')

                 messagebox.showinfo("Info", "Successfully added to database")

            connectivity.commit()
            connectivity.close()

        label_space1 = tk.Label(self, text="    ", padx=105, pady=1)
        label_space1.pack()
        button_insert = tk.Button(self, text="Add record to database", font=controller.button_font, padx=30, pady=10, command=insert)
        button_insert.pack()
        button_back = tk.Button(self, text="Back", font=controller.button_font, padx=111, pady=10, command=lambda:controller.show_frame("Frame_2"))
        button_back.pack()

        
class Frame_4(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        def show_records():
            connectivity = sqlite3.connect('Pass.db')

            cursor = connectivity.cursor()

            select = """SELECT *, oid from Passes"""
            cursor.execute(select)
            values = cursor.fetchall()
            global label_show_records
            label_show_records = tk.Label(self, text="Number of records: " + str(len(values)), font=controller.button_font)
            label_show_records.pack()
            button_show_records['state'] = GUI.DISABLED

            cursor.close()

            connectivity.commit()
            connectivity.close()


        def delete():
            connectivity = sqlite3.connect('Pass.db')

            cursor = connectivity.cursor()

            select1 = """SELECT oid from Passes"""
            cursor.execute(select1)
            values1 = cursor.fetchall()
            if entry_select.get().isnumeric() == True:
                test = int(entry_select.get())
                test_list=[]
                test_list.append(test)
                test_tuple = tuple(test_list)   
                bool_select = False
                for value in values1:
                    if sorted(test_tuple) == sorted(value):
                        bool_select = True
                        break
          


            if len(entry_select.get()) == 0:
                 messagebox.showwarning("Warning", "Must specify record ID")
            elif entry_select.get().isnumeric() == False: 
                 messagebox.showwarning("Warning", "Input must be a positive integer")
            elif bool_select == False:
                 messagebox.showwarning("Warning", "Record ID outside of range")
            else:
                 delete = "DELETE from Passes WHERE oid= " + entry_select.get()
                 cursor.execute(delete)
                 messagebox.showinfo("Info", "Record successfully deleted")

            cursor.close()

            entry_select.delete(0, 'end')

            connectivity.commit()
            connectivity.close()


        def hide_records():
            label_show_records.pack_forget()
            button_show_records['state'] = GUI.NORMAL

        label_master2 = tk.Label(self, text="Delete or modify record", font=controller.title_font)
        label_master2.pack()
        label_select = tk.Label(self, text="Record ID: ", font=controller.button_font)
        label_select.pack()
        entry_select = tk.Entry(self, borderwidth=2.5, width=40 )
        entry_select.pack()
        label_space1 = tk.Label(self, text="    ", padx=105, pady=1, font=controller.button_font)
        label_space1.pack()

        button_delete = tk.Button(self, text="Delete record", padx=67, pady=10, font=controller.button_font, command=delete)
        button_delete.pack()
        button_show_records = tk.Button(self, text="Show number of records", padx=22, pady=10, font=controller.button_font, command=show_records)
        button_show_records.pack()
        button_hide_records  = tk.Button(self, text="Hide number of records", padx=25, pady=10, font=controller.button_font, command=hide_records)
        button_hide_records.pack()
        button_back1 = tk.Button(self, text="Back", padx=105, pady=10, font=controller.button_font, command=lambda:controller.show_frame("Frame_2"))
        button_back1.pack()

class Frame_5(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        def show_all():
            top = tk.Toplevel()
            top.geometry("1000x400")
            top.resizable(False, False)
            top.title("All records")
            top.iconbitmap('bunny.ico')

            frame_scrollbar = tk.Frame(top)
            frame_scrollbar.pack(fill=BOTH, expand=1)
            canvas_scrollbar = tk.Canvas(frame_scrollbar)
            canvas_scrollbar.pack(side=LEFT, fill=BOTH, expand=1)
            scrollbar = ttk.Scrollbar(frame_scrollbar, orient=VERTICAL, command=canvas_scrollbar.yview)
            scrollbar.pack(side=RIGHT, fill=Y)
            canvas_scrollbar.configure(yscrollcommand=scrollbar.set)
            canvas_scrollbar.bind('<Configure>', lambda e: canvas_scrollbar.configure(scrollregion = canvas_scrollbar.bbox("all")))
            frame_scrollbar2 = tk.Frame(canvas_scrollbar)
            canvas_scrollbar.create_window((0,0), window=frame_scrollbar2, anchor="nw")

            connectivity = sqlite3.connect('Pass.db')

            cursor = connectivity.cursor()

    
            select_all = """SELECT *, oid from Passes"""
            cursor.execute(select_all)
            values3 = cursor.fetchall()

            print_value3 = ''
            for value in values3:
                print_value3 = ''
                print_value3 +=  "Platform/Username: " + str(value[0]) + ", " + "URL: " + str(value[1]) + ", " + "Password: " + str(value[2]) + ", "  + "ID Number: " + str(value[3])
                label_value3 = tk.Label(frame_scrollbar2, text=print_value3, pady=10)
                label_value3.pack() 

            cursor.close()
            connectivity.commit()
            connectivity.close()

            global label_value
        def show_one():
            connectivity = sqlite3.connect('Pass.db')

            cursor = connectivity.cursor()

            select_copy = """SELECT oid from Passes"""
            cursor.execute(select_copy)
            values = cursor.fetchall()
            if entry_show_ID.get().isnumeric() == True:
                test2 = int(entry_show_ID.get())
                test2_list=[]
                test2_list.append(test2)
                test2_tuple = tuple(test2_list)
                bool2_select = False
                for value in values:
                    if sorted(test2_tuple) == sorted(value):
                        bool2_select = True
                        break
                cursor.close()

                connectivity.commit()
                connectivity.close()        

                if len(entry_show_ID.get()) == 0:
                    messagebox.showwarning("Warning", "Must complete all fields")
                elif entry_show_ID.get().isnumeric() == False:
                    messagebox.showwarning("Warning", "Input must be a positive integer")
                elif bool2_select == False:
                    messagebox.showwarning("Warning", "Record ID outside of range")
                else:
                    connectivity = sqlite3.connect('Pass.db')

                    cursor = connectivity.cursor()

                    select = ("SELECT *, oid from Passes WHERE oid = " + entry_show_ID.get())
                    cursor.execute(select)
                    values2 = cursor.fetchall()
                    global label_value
                    print_value = ''
                    for value in values2:
                        print_value += "Platform/Username: " + str(value[0]) + ", " + "URL: " + str(value[1]) + ", " + "Password: " + str(value[2]) + "\n" + "ID Number: " + str(value[3]) + "\n" 
                        global label_value
                        label_value = tk.Label(self, text=print_value, pady=10, font=controller.button_font)
                        label_value.pack()

                    cursor.close()

                    connectivity.commit()
                    connectivity.close()
                    button_show_one['state'] = GUI.DISABLED
                    button_hide_one['state'] = GUI.NORMAL


        def hide_one():
            button_show_one['state'] = GUI.NORMAL
            label_value.pack_forget()

        label_master3 = tk.Label(self, text="View records", font=controller.button_font)
        label_master3.pack()

        button_show_all = tk.Button(self, text="Show all records", padx=10, pady=10, font=controller.button_font, command=show_all)
        button_show_all.pack()
        label_select1 = tk.Label(self, text="Record ID:", font=controller.button_font)
        label_select1.pack()
        entry_show_ID = tk.Entry(self)
        entry_show_ID.pack()

        label_space2 = tk.Label(self, text="    ", padx=64, pady=0, font=controller.button_font)
        label_space2.pack()
        button_show_one = tk.Button(self, text="Show record", padx=30, pady=10, font=controller.button_font, command=show_one)
        button_show_one.pack()
        button_hide_one = tk.Button(self, text="Hide record", padx=34, pady=10, font=controller.button_font, command=hide_one)
        button_hide_one['state'] = GUI.DISABLED
        button_hide_one.pack()
        button_back2 = tk.Button(self, text="Back", padx=64, pady=10, font=controller.button_font, command=lambda:controller.show_frame("Frame_2"))
        button_back2.pack()


if __name__ == "__main__":
    app = Application()
    style = ttk.Style(app)
    style.theme_use("clam")
    app.title("Password Manager")
    app.iconbitmap('bunny.ico')
    app.geometry('750x500')
    app.resizable(False, False)
    print("<Password Manager>  Copyright (C) <2022>  <Alexia Niculae> This program comes with ABSOLUTELY NO WARRANTY; for details click the About License on the home screen")
    app.mainloop()

