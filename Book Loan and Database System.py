 #Book Loan database system
#from pylab import figure, axes, pie, title, show
from tkinter import *
from tkinter.messagebox import *
from tkinter import ttk
import sqlite3
import re
import os
from functools import partial
import subprocess
from reportlab.graphics.barcode import eanbc
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.graphics.shapes import Drawing
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.graphics import renderPDF
import time
import datetime
from datetime import datetime, date
import email
import smtplib


studentLoggedIn = False
recover = False


#STUFF TO REMEMBER
#For button classes use fixed numbers9780748782963


#Use the button classes for login stuff
#Remove conn and cursor thing and make GLOBAL


#245392hi435nk3jb43h5hk34bnnj3v4jkv35j4l35v3jk45v43i349y534iubt3i4b3o HAX HAX t643towtngwlng
class SetupAndLogin(Frame):
    def ProgressBar(self):
        root.geometry("200x50")
        self.progress.grid()
        self.progress.config(cursor = "@cursor.cur")
        progressb = ttk.Progressbar(self.progress, orient = "horizontal", length = 200, mode = "determinate")
        progressb.grid()
        progressb["maximum"] = 100
        progressb["value"] = 0
        label = Label(self.progress, text = "")
        label.grid(sticky = "nesw")
        label.config(text = "Loading for first time use....")
        value = 0
        def changetext(value):
            value = value + 0.5
            progressb["value"] = value
            if progressb["value"] == 20:
                label.config(text = "Loading Assets...")
            if progressb["value"] == 40:
                label.config(text = "Making you wait...")
            if progressb["value"] == 60:
                label.config(text = "Deleting System32...")
            if progressb["value"] == 80:
                label.config(text = "Loading complete...")
            if progressb["value"] == 100:
                progressb.stop()
                os.remove("firstTimeUse.txt")
                self.Continue()
            self.after(50, changetext, (value))
        changetext(value)
            
            
    def __init__(self, master):
        super(SetupAndLogin,self).__init__(master)
        self.grid()
        self.progress = Frame(self)
        self.loginWindow = Frame(self)
        self.setupWindow = Frame(self)
        self.userWindow = Frame(self)
        self.userWindow2 = Frame(self)
        self.userWindow3 = Frame(self)
        #Checking if the database exists
        if (os.path.exists("database.db")):          
            if (os.path.exists("firstTimeUse.txt")):
                self.ProgressBar()
            else:
                self.Continue()
        else:
            file = open("firstTimeUse.txt", "w")
            file.close()
            self.setupWindow.grid()
            root.title("Book Loan System and Database Setup")
            root.geometry("400x350")
            root.wm_iconbitmap("favicon.ico")
            self.setupWindow.configure(bg = "SystemWindow", cursor = "@cursor.cur")

            #The book stack image to show professionalism
            backG = PhotoImage(file = "bookstack.gif")
            BackGlabel = Label(self.setupWindow, image = backG, height = 300, width = 90)
            BackGlabel.image = backG
            BackGlabel.grid(sticky = "nw")

            #Labels and btns
            welcomeLabel = Label(self.setupWindow, bg = "SystemWindow", justify = "left", text = "Welcome to Book Loan System\nand Database Setup Wizard", font = ("Arial", 10, "bold"), height = 2)
            welcomeLabel.grid(row =0, padx = 100, pady = 10, sticky = "nw")
            guideLabel = Label(self.setupWindow, bg = "SystemWindow", justify = "left", text = "This wizard will guide you through the setup of\nBook Loan System and Database.\n\n It is recommended you close all other applications\n before starting Setup. This will make it possible to update\n relevant system files without having to reboot your\n computer.", font = ("Arial", 8, "normal"))
            guideLabel.grid(row = 0, padx = 100, pady = 70, sticky = "nw")
            sep = ttk.Separator(self.setupWindow, orient = "horizontal")
            sep.grid(row = 0, pady = 303, sticky = "new")
            clickNext = Label(self.setupWindow, bg = "SystemWindow", text = "Click Next to continue.", font = ("Arial", 8, "normal"), justify = "left")
            clickNext.grid(row = 0, padx = 100, pady = 180, sticky = "nw")
            #Need a fake grey label
            fakelabel = Label(self.setupWindow, text = "", height = 100, width = 350, bg = "SystemMenu")
            fakelabel.grid(row = 0, pady = 304, sticky = "nw")

            nextbtn = ttk.Button(self.setupWindow, text = "Next >", command = lambda:self.Newuser())
            nextbtn.grid(row = 0, pady = 315, sticky = "nw", padx = 220)
            cancelbtn = ttk.Button(self.setupWindow, text = "Cancel", command = lambda:self.CloseOrCancel(root))
            cancelbtn.grid(row = 0, pady = 315, sticky = "nw", padx = 310)

    def Continue(self):
        conn=sqlite3.connect("database.db")
        cur=conn.cursor()
        self.progress.grid_remove()
        self.loginWindow.grid()
        root.title("Login")
        root.geometry("400x350")
        root.config(cursor = "@cursor.cur")
        root.wm_iconbitmap("favicon.ico")
        self.loginWindow.columnconfigure(0,weight=1)
        self.loginWindow.rowconfigure(0, weight=1)


        #the photo in the login window
        photo = PhotoImage(file = "Book.gif")
        plabel = Label(self.loginWindow, image = photo, height = 170)
        plabel.image = photo
        plabel.grid()

        #creating the labels and Entry and buttons also binding the enter key to the login button
        titleL = ttk.Label(text = "Book and Student Database", font = ("Arial", 20,"bold"))
        usernameLabel = ttk.Label(text = "Username: ")
        passwordLabel = ttk.Label(text = "Password: ")
        usernameEntry = ttk.Entry()
        passwordEntry = ttk.Entry(show = "*")
        usernameEntry.focus()
        incorrectLabel = Label()
        cancel = ttk.Button(text = "Cancel", command = lambda:self.CloseOrCancel(root))
        forgotDetails = ttk.Button(text = "Request Details", command = lambda:recoverDetails())
        def recoverDetails():
            cur.execute("SELECT userName, passWord, email  FROM User")
            details = cur.fetchall()
            user = str(details[0][0])
            passW = str(details[0][1])
            email2 = str(details[0][2])
            message = ("Your username is: "+"'"+user+"'"+"\n"+"'"+"Your password is: "+"'"+passW)
            s = smtplib.SMTP("smtp.mail.yahoo.com", 25)
            msg = email.message_from_string(message)
            msg['From'] = "DatabaseSystem@Recover.co.uk"
            msg['To'] = str(email2)
            msg['Subject'] = "Details recover"
            s.ehlo()
            s.starttls() 
            s.ehlo()
            global root
            global recover
            recover = True
            cls = System(root)
            cls2 = cls.emailPart(email2, msg, s, email2)


        #Once login is clicked or enter is pressed it will6 check if any of the requirements match, if so then login sucessfull.
        loginButton = ttk.Button(text = "Login",command=lambda:self.getPassword(passwordEntry, usernameEntry, incorrectLabel))
        usernameEntry.bind("<Return>", lambda wasteevent:self.getPassword(passwordEntry, usernameEntry, incorrectLabel))
        passwordEntry.bind("<Return>", lambda wasteevent:self.getPassword(passwordEntry, usernameEntry, incorrectLabel))
        
        #Griding all the labels and buttons
        titleL.grid(row = 0, column = 0)
        usernameLabel.grid(row = 1, column = 0, sticky = "sw", padx = 90, pady = 20)
        usernameEntry.grid(row = 1, column = 0, sticky = "se", padx = 100, pady = 20)
        passwordLabel.grid(row = 2, column = 0, sticky = "w", padx = 93)
        passwordEntry.grid(row = 2, column = 0, sticky = "e", padx = 100)
        
        fake = Label()
        fake.grid(row = 3, sticky = "w", pady = 15)
        loginButton.grid(row = 4, column =0, sticky = "e", padx = 100, pady = 10)
        incorrectLabel.grid(row = 4, column = 0, sticky = "sw", padx = 100, pady = 10)
        cancel.grid(row = 4, column = 0, padx = 15, pady = 10, sticky = "e")
        forgotDetails.grid(row = 4, column = 0, sticky = "w", padx = 10, pady = 10)

        
    def CloseOrCancel(self, x):
        x.destroy()

#verify the password
    def getPassword(self, passwordEntry, usernameEntry, incorrectLabel):
        loggedIn = False
        conn=sqlite3.connect("database.db")
        cur=conn.cursor()
        cur.execute("SELECT teacherCode FROM User")
        teacherCode = str(cur.fetchall())
        #This basically removes the brackets and the commas in the string
        teacherCode = re.sub('[(,)]',"", teacherCode)
        #this removes the quotes at the start and at the end
        teacherCode = teacherCode[1:-1]
        teacherCode = teacherCode[1:-1]
        if passwordEntry.get() != "" and usernameEntry.get() != "":
            userValue = usernameEntry.get()
            try:
                cur.execute("SELECT passWord FROM User WHERE userName =?", (userValue,))
                passwords = str(cur.fetchall())
                #This basically removes the brackets and the commas in the string
                passwords = re.sub('[(,)]',"", passwords)
                #this removes the quotes at the start and at the end
                passwords = passwords[1:-1]
                passwords = passwords[1:-1]
                if passwords == passwordEntry.get():
                    if teacherCode == "8989":
                        loggedIn = True #CHANGE THIS TO studentLoggedIn = True TO LOG IN AS A STUDENT
                        root.destroy()
                        MainProg(loggedIn)
                        
                    else:
                        global studentLoggedIn
                        studentLoggedIn = True #IF YOU CHANGE THE TOP CHANGE THIS ONE TO loggedIn = True
                        root.destroy()
                        MainProg(loggedIn)
                else:
                    incorrectLabel.config(text = "*Incorrect details", fg = "red")
                    print("That is not the correct username or password, please try again!")
                    
            except sqlite3.Error as e:
                print("An error occured: "+ e.args[0])

        elif usernameEntry.get() == "" and passwordEntry.get() == "":
            incorrectLabel.config(text = "*Fields are empty", fg = "red")
  
#if it's a new user, new username is created

    def Newuser(self):
        self.setupWindow.grid_remove()
        self.userWindow.grid()
        self.userWindow.config(bg = "SystemMenu", cursor = "@cursor.cur")
        backG = PhotoImage(file = "bookstack.gif")
        BackGlabel = Label(self.userWindow, image = backG, height = 50, width = 400)
        BackGlabel.image = backG
        BackGlabel.grid(row = 0, sticky = "nw")
        sep = ttk.Separator(self.userWindow, orient = "horizontal")
        sep.grid(row = 1, sticky = "nwe")
        continuel = Label(self.userWindow, text = "Please enter your details: ")
        continuel.grid(row = 2, pady = 10, sticky = "w", padx = 5)
        fNameL = Label(self.userWindow, text = "First name: ")
        self.fNameE = ttk.Entry(self.userWindow, width = 45)
        lNameL = Label(self.userWindow, text = "Last name: ")
        self.lNameE = ttk.Entry(self.userWindow, width = 45)
        emailL = Label(self.userWindow, text = "Yahoo e-mail: ")
        self.emailE = ttk.Entry(self.userWindow, width = 40)
        fNameL.grid(row = 3, sticky = "w", padx = 10, pady = 10)
        self.fNameE.grid(row = 3, sticky = "ne", padx = 100, pady = 10)
        lNameL.grid(row = 4, sticky = "w", padx = 10, pady = 10)
        self.lNameE.grid(row = 4, sticky = "ne", padx = 100, pady = 10)
        emailL.grid(row = 5, sticky = "w", padx = 10, pady = 10)
        self.emailE.grid(row = 5, sticky = "e", padx = 100, pady = 10)

        teacherCode = Label(self.userWindow, text = "Teacher code: ")
        self.teacherCodeEnt = ttk.Entry(self.userWindow, width = 40)
        teacherCode.grid(row = 6, sticky = "w", padx = 10, pady = 10)
        self.teacherCodeEnt.grid(row = 6, sticky = "e", padx = 100, pady = 10)
        fakelabel1 = Label(self.userWindow, text = "", bg = "SystemMenu")
        fakelabel1.grid(row = 7, sticky = "w")
        self.incompFields = Label(self.userWindow, text = "", fg = "red")
        self.incompFields.grid(row = 8, sticky = "w", padx = 10)
        self.warningLbl = Label(self.userWindow, text = "*Enter 0 for unknown teachercode \\ Yahoo email only", fg = "red")
        self.warningLbl.grid(row = 8, sticky = "sw", padx = 10)
        sep2 = ttk.Separator(self.userWindow, orient = "horizontal")
        sep2.grid(row = 9, sticky = "sew")
        self.ListP1 = [self.fNameE, self.lNameE, self.emailE, self.teacherCodeEnt]
        nextb = ttk.Button(self.userWindow, text = "Next >", command = lambda:self.checkEmail())
        cancel = ttk.Button(self.userWindow, text = "Cancel", command = lambda:self.CloseOrCancel(root))
        nextb.grid(row = 10, sticky = "ne", padx = 180, pady = 9)
        cancel.grid(row = 10, sticky = "ne", padx = 90, pady = 9)

    def checkEmail(self):
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", self.emailE.get()) != None:
            self.warningLbl.config(text = "")
            self.Newuser2()
        else:
            self.warningLbl.config(text = "Email is not valid, please try again")

    def Newuser2(self):
        if self.forumComplete(self.ListP1) == True:
            self.userWindow.grid_remove()
            self.userWindow2.grid()
            self.userWindow2.config(bg = "SystemMenu", cursor = "@cursor.cur")
            backG = PhotoImage(file = "bookstack.gif")
            BackGlabel = Label(self.userWindow2, image = backG, height = 50, width = 400)
            BackGlabel.image = backG
            BackGlabel.grid(row = 0, sticky = "nw")
            sep = ttk.Separator(self.userWindow2, orient = "horizontal")
            sep.grid(row = 1, sticky = "nwe")
            continuel = Label(self.userWindow2, text = "Please enter your desired password: ")
            continuel.grid(row = 2, pady = 10, sticky = "w", padx = 5)
            uNameL = Label(self.userWindow2, text = "User name: ")

            uNameE = ttk.Label(self.userWindow2, width = 45)
            userpart1 = self.ListP1[0].get()
            userpart1 = userpart1[0:3]
            userpart2 = self.ListP1[1].get()
            userpart2 = userpart2[0:3]
            userpart3 = self.ListP1[2].get()
            userpart3 = userpart3[0:3]
            self.username = userpart1 + userpart2 + userpart3
            uNameE.configure(text = self.username)
            
            pWordL = Label(self.userWindow2, text = "Password: ")
            pWordE = ttk.Entry(self.userWindow2, show = "*", width = 40)
            conpWordL = Label(self.userWindow2, text = "Confirm password: ")
            conpWordE = ttk.Entry(self.userWindow2, show = "*", width = 40)
            uNameL.grid(column = 0, row = 3, sticky = "w", padx = 10, pady = 15)
            uNameE.grid(column = 0, row = 3, sticky = "e", padx = 100, pady = 15)
            pWordL.grid(column = 0, row = 4, sticky = "w", padx = 10, pady = 15)
            pWordE.grid(column = 0, row = 4, sticky = "e", padx = 100, pady = 15)
            conpWordL.grid(column = 0, row = 5, sticky = "w", padx= 10, pady = 15)
            conpWordE.grid(column = 0, row = 5, sticky = "e", padx=100, pady = 15)
            fakelabel1 = Label(self.userWindow2, text = "", bg = "SystemMenu")
            fakelabel1.grid(row = 6, pady = 7, sticky = "w")
            self.passwordNoMatch = Label(self.userWindow2, fg = "red")
            self.passwordNoMatch.grid(column = 0, row = 7, sticky = "w", padx = 10)
            sep2 = ttk.Separator(self.userWindow2, orient = "horizontal")
            sep2.grid(row = 8, sticky = "sew")
            self.ListP2 = [pWordE, conpWordE]
            self.widgetList = [pWordE, self.fNameE, self.lNameE, self.emailE, self.teacherCodeEnt]
            nextb = ttk.Button(self.userWindow2, text = "Next >", command = lambda:self.Newuser3())
            cancel = ttk.Button(self.userWindow2, text = "Cancel", command = lambda:self.CloseOrCancel(root))
            nextb.grid(row = 9, sticky = "ne", padx = 180, pady = 9)
            cancel.grid(row =9, sticky = "ne", padx = 90, pady = 9)
        else:
           self.incompFields.config(text = "*Incomplete fields, please fill in all the information.")

    def Newuser3(self):
        if self.forumComplete(self.ListP2) == True:
            if self.ListP2[0].get() == self.ListP2[1].get():
                #Labels and btns
                self.userWindow2.grid_remove()
                self.userWindow3.grid()
                self.userWindow3.configure(bg = "SystemWindow", cursor = "@cursor.cur")

                #The book stack image to show professionalism
                backG = PhotoImage(file = "bookstack.gif")
                BackGlabel = Label(self.userWindow3, image = backG, height = 300, width = 90)
                BackGlabel.image = backG
                BackGlabel.grid(sticky = "nw")

                finishLabel = Label(self.userWindow3, bg = "SystemWindow", justify = "left", text = "Setup Complete", font = ("Arial", 10, "bold"), height = 2)
                finishLabel.grid(row =0, padx = 100, pady = 10, sticky = "nw")
                guideLabel = Label(self.userWindow3, bg = "SystemWindow", justify = "left", text = "Book Loan System and Database was succesfully setup. ", font = ("Arial", 8, "normal"))
                guideLabel.grid(row = 0, padx = 100, pady = 70, sticky = "nw")
                sep = ttk.Separator(self.userWindow3, orient = "horizontal")
                sep.grid(row = 0, pady = 303, sticky = "new")
                clickNext = Label(self.userWindow3, bg = "SystemWindow", text = "Click Finish to complete Setup.", font = ("Arial", 8, "normal"), justify = "left")
                clickNext.grid(row = 0, padx = 100, pady = 90, sticky = "nw")
                #Need a fake grey label
                fakelabel = Label(self.userWindow3, text = "", height = 100, width = 350, bg = "SystemMenu")
                fakelabel.grid(row = 0, pady = 304, sticky = "nw")

                cancelbtn = ttk.Button(self.userWindow3, text = "Finish", command = lambda:self.crTbleUser())
                cancelbtn.grid(row = 0, pady = 315, sticky = "nw", padx = 310)
            else:
                self.passwordNoMatch.configure(text = "*Passwords do not match!") 
        else:
            self.passwordNoMatch.configure(text = "*Incomplete fields, please fill in all the information.")

    #This checks if all the fields in the newUser window are filled out
    def forumComplete(self, x):
        complete = True
        debounce = True
        while complete == True and debounce == True:
            for i in range(len(x)):
                if x[i].get() == "":
                    complete = False
            if complete == True:
                debounce = False
        print(complete)
        return complete



    #this creates the table if it doesnt exist and then adds the new user       
    def crTbleUser(self):
        #If the table doesn't exist already create one!
        conn=sqlite3.connect("database.db")
        cur=conn.cursor()
        try:
           cur.execute("""CREATE TABLE User(
               userName VARCHAR(20) PRIMARY KEY,
               passWord VARCHAR(20),
               firstName VARCHAR (15),
               lastname VARCHAR (15),
               email VARCHAR(30),
               teacherCode CHAR(7)
                )""")
        except sqlite3.Error as e:
            print("An error occurred: " + e.args[0])
            
 
        #Make a new list as a tuple
        newUserData = []
        newUserData.append(self.username)
        for i in range(5):
            newUserData.append(self.widgetList[i].get())

        newUserData = tuple(newUserData)

        #insert the values
        SQL = "INSERT INTO User(userName, passWord, firstName, lastName, email, teacherCode) "
        SQL = SQL + "VALUES(?,?,?,?,?,?)"
        try:
            cur.execute(SQL,newUserData)
            conn.commit()
            root.destroy()
        except sqlite3.Error as e:
            print("An error occured: "+ e.args[0])

def MainProg(loggedIn):
    global root
    if loggedIn == True:
        root = Tk()
        root.title("Book Loan System and Database")
        root.geometry("1080x500")
        root.wm_iconbitmap("favicon.ico")
        BookLoan = System(root)

    if studentLoggedIn == True:
        if (os.path.exists("CannotUseAgain.txt")):
            print("ACCESS DENIED, Data from this machine has already been added")
            sys.exit()
        else:
            root = Tk()
            root.title("Book Loan System and Database")
            root.geometry("1080x700")
            root.wm_iconbitmap("favicon.ico")
            cls = System(root)
            BookLoanStudent = cls.EnterStudentInfo()

    
#create the root window
class System(Frame):
    def __init__(self, master):
        super(System,self).__init__(master)
        if recover == True:
            print("Details reover mode")
        else:
            print("Not recover")
            self.grid()
            if studentLoggedIn == False:
                print("Not student logged in")
                self.Menu = Frame(self)
                self.displayWelcomeMessage()
                self.DisplayMenu()
            else:
                print("Student logged in")



    #display the welcome message
    def displayWelcomeMessage(self):
        messagebox.showinfo(
            message = "Welcome to the Book Loan and Database System",
            icon = "info", title = "Welcome", detail = "Press OK to continue")

    def goHome(self, x):
        x.destroy()
        self.Menu = Frame(self)
        self.DisplayMenu()


    def tick(self):
        time2 = time.strftime("%H:%M:%S")
        if time2!=self.time1:
            self.time1 = time2
            self.clock.config(text = time2)
        self.clock.after(200, self.tick)
        
    #this displays the menu       
    def DisplayMenu(self):
        print("Menu")
        conn=sqlite3.connect("database.db")
        cur=conn.cursor()
        self.Menu.grid()
        self.Menu.config(cursor = "@cursor.cur")
        root.geometry("700x300")
        self.TitleLBL = Label(self.Menu, text = "Book Loan and Database System", font = ("Arial", 20,"bold"))
        self.TitleLBL.grid(row = 0, padx = 140, sticky = "w")
        self.time1 = ""
        self.clock = Label(self.Menu, font = ("Arial", 14,"bold"))
        self.clock.grid(row = 1, padx = 310, stick = "w")
        self.tick()
        self.bookTitle = StringVar()
        NotesLbl = Label(self.Menu, text = "Notes: ")
        NotesLbl.grid(row = 2, padx = 10, sticky = "nw")
        Notes = Text(self.Menu, height = 4, width = 50)
        Notes.grid(row =3, padx = 10, sticky = "w")
        Save = ttk.Button(self.Menu, text = "Save to text file", command = lambda:self.saveNotes(Notes))
        Save.grid(row = 4, padx = 10, sticky = "w")
        Load = ttk.Button(self.Menu, text = "Load text file", command = lambda:self.loadNotes(Notes))
        Load.grid(row = 4, padx = 120, sticky = "w")
        Clear = ttk.Button(self.Menu, text = "Clear", command = lambda:self.clear(Notes))
        Clear.grid(row = 4, padx = 220, sticky = "w")
        self.comboBook = ttk.Combobox(self.Menu, textvariable = self.bookTitle)
        self.comboBook.grid(row =5, padx = 10, pady = 10, sticky = "w")
        self.CreatingBookTables()
        valueList = []
        LblBook = ttk.Label(self.Menu, text = "Number of books: ")
        LblBook.grid(row = 5, padx = 170, sticky = "w")
        Entbook = Entry(self.Menu)
        Entbook.grid(row = 5, padx = 290, sticky = "w")
        self.counter = 0
        self.comboBook.bind("<<ComboboxSelected>>", lambda wasteevent:self.valueInCombo(Entbook))
        Entbook.bind("<Return>", lambda wasteevent:self.updateNoOfBooks(Entbook))
        BookLoanB = Button(self.Menu, text = "Book Loan", command = lambda:self.BookLoan(), height = 2, width = 20)
        StudentInfo = Button(self.Menu, text = "Student information", command = lambda:self.EnterStudentInfo(), height = 2, width = 20)
        StudentInfo.grid(row = 3, padx = 530, sticky = "sw")
        BookLoanB.grid(row = 4, padx = 530, pady = 10, sticky = "nw")
        StatisticView = Button(self.Menu, text = "View Statistics", command = lambda:self.Statistics(), height = 2, width = 20)
        StatisticView.grid(row = 5, padx = 530, sticky = "nw")
        self.warningLbl = Label(self.Menu, text = "", fg = "red")
        self.warningLbl.grid(row =6, padx = 10, pady = 20, sticky = "sw")
        try:
            cur.execute("SELECT Title FROM Book")
            titles = cur.fetchall()
            for i in titles:
                temp = str(i)
                temp = re.sub('[(,)]',"", temp)
                #this removes the quotes at the start and at the end
                temp = temp[1:-1]
                temp = str(temp)
                valueList.append(temp)
            self.comboBook.configure(values = valueList)
            self.comboBook.set(str(valueList[0]))
            self.comboBook.current()
            self.valueInCombo(Entbook)
        except:
            self.warningLbl.config(text = "*No books to display, enter book details in book loan screen")

    def updateNoOfBooks(self, Ent):
        conn=sqlite3.connect("database.db")
        cur=conn.cursor()
        def integerChecker(ent):
            try:
                int(ent)
                return True
            except ValueError:
                return False
        print(self.comboBook.get())
        print(Ent.get())
        ent = Ent.get()
        def clear():
            self.warningLbl.config(text = "")
        if self.comboBook.get() == "":
            self.warningLbl.config(text = "*Please select a book to update")
        else:
            if integerChecker(ent) == False:
                self.warningLbl.config(text = "*Please enter a number")
            else:
                if int(ent) < 500 and int(ent) > -1:
                    try:
                        cur.execute("UPDATE Book SET NoOfBooks ="+"'"+Ent.get()+"'"+"WHERE Title ="+"'"+self.comboBook.get()+"'")
                        print("here")
                        conn.commit()
                    except sqlite3.Error as e:
                        print("An error occurred: " + e.args[0]) 
                    self.warningLbl.config(text = "*Number of books for "+self.comboBook.get()+" has been updated!")
                    self.after(5000, clear)
                else:
                    if int(ent) >= 500:
                        self.warningLbl.config(text = "*Please enter a book number less than 500")
                    else:
                        self.warningLbl.config(text = "*Please enter a book number higher than -1")
                    self.after(5000, clear)
            

    def clear(self, Notes):
        Notes.delete("1.0", END)

    def saveNotes(self, Notes):
        self.counter +=1
        text = Notes.get("1.0", END)
        if self.counter == 1:
            self.firstTimeSave = True
            date = str(time.strftime("%d-%m-%Y"))
            time2 = str(time.strftime("%H-%M-%S"))
            self.sameSave = (date+" at "+time2+".txt")
            file = open(self.sameSave, "w")
            file.write(self.sameSave+"\n"+"\n")
            file.write(text+"\n")
            file.close()

        if self.counter != 1:    
            answer = messagebox.askyesno(message='Would you like to save to the same note text file?', icon='question', title='Text file option')
            if answer == True:
                file = open(self.sameSave, "w")
                file.write(self.sameSave+"\n"+"\n")
                file.write(text+"\n")
                file.close()
            else:    
                date = str(time.strftime("%d-%m-%Y"))
                time2 = str(time.strftime("%H-%M-%S"))
                dateAndTime = (date+" at "+time2+".txt")
                file = open(dateAndTime, "w")
                file.write(dateAndTime+"\n"+"\n")
                file.write(text+"\n")
                file.close()
    
    def loadNotes(self, Notes):
        filename = str(filedialog.askopenfilename())
        if filename[-4:] != ".txt":
            Notes.delete("1.0", END)
            self.warningLbl.config(text = "*This is not a text file, please open a file with an extension, '.txt'.")
        else:
            self.warningLbl.config(text = "")
            Notes.delete("1.0", END)
            with open(filename, 'r') as content_file:
                content = str(content_file.read())
                Notes.insert("1.0", content)
        
    def Statistics(self):
        conn=sqlite3.connect("database.db")
        cur=conn.cursor()
        dialogBox=Tk()
        dialogBox.title("Statistics")
        dialogBox.geometry("280x110")
        dialogBox.wm_iconbitmap("favicon.ico")
        dialogBox.config(cursor = "@cursor.cur")
        subject = StringVar()
        selectType = Label(dialogBox, text = "Select cource type: ")
        selectType.grid(row = 0, padx = 5, pady = 5, sticky = "w")
        comboBox = ttk.Combobox(dialogBox, textvariable = subject, values = ["A-Level Subject", "GCSE Subject"])
        comboBox.grid(row = 0, padx = 120, pady =5, sticky = "w")
        LabelS = Label(dialogBox, text = "Enter Subject: ")
        LabelS.grid(row = 1, padx = 5, pady = 5, sticky = "w")
        LabelEnt = Entry(dialogBox)
        LabelEnt.grid(row = 1, padx = 120, pady = 5, sticky = "w")
        self.LblWarningStat = Label(dialogBox, text = "", fg = "red")
        self.LblWarningStat.grid(row = 2, padx = 5, sticky = "ws")
        ButtonG = ttk.Button(dialogBox, text = "Generate Graph", command = lambda:self.DisplayStatistics(LabelEnt, comboBox))
        ButtonG.grid(row = 3, padx = 5, sticky = "w")
        close = ttk.Button(dialogBox, text = "Close", command = lambda:self.CloseOrCancel(dialogBox))
        close.grid(row = 3, padx = 100, sticky = "w")
        
    def DisplayStatistics(self, Ent, combo):
        conn=sqlite3.connect("database.db")
        cur=conn.cursor()
        self.LblWarningStat.config(text = "")
        figure(1, figsize = (6,6))
        ax = axes([0.1, 0.1, 0.8, 0.8])
        labelVal = str(Ent.get())
        print(combo.get())
        try:
            cur.execute("SELECT * FROM studentData")
            noOfRecs = len(cur.fetchall())
        except sqlite3.Error as e:
            print("An error occurred: " + e.args[0])

        if combo.get() == "GCSE Subject":
            labels = labelVal+"\n"+" taken"+"\n"+"at GCSE", labelVal+"\n"+" not taken"+"\n"+"at GCSE"
            title(labelVal+' taken at GCSE', bbox={'facecolor':'0.8', 'pad':5})
            print("In GCSE")
            print(combo.get())
            try:
                enteries = ["GCSESub1", "GCSESub2", "GCSESub3", "GCSESub4"]
                results = 0
                for i in enteries:
                    cur.execute("SELECT "+i+" FROM studentData WHERE "+i+"="+"'"+Ent.get()+"'")
                    temp = len(cur.fetchall())
                    results = temp + results
                print(results, "Results")
                print("No of recs: ", noOfRecs)
            except sqlite3.Error as e:
                print("An error occurred: " + e.args[0]) 

        if combo.get() == "A-Level Subject":
            labels = labelVal+"\n"+" taken"+"\n"+"at A-Level", labelVal+"\n"+" not taken"+"\n"+"at A-Level"
            title(labelVal+' taken at A-Level', bbox={'facecolor':'0.8', 'pad':5})
            print("In Alevel")
            print(combo.get())
            try:
                enteries = ["otherSubs1", "otherSubs2", "otherSubs3", "otherSubs4", "year2Sub1", "year2Sub2", "year2Sub3", "year2Sub4"]
                results = 0
                for i in enteries:
                    cur.execute("SELECT "+i+" FROM studentData WHERE "+i+"="+"'"+Ent.get()+"'")
                    temp = len(cur.fetchall())
                    results = temp + results
                print(results, "Results")
                print("No of recs: ", noOfRecs)
            except sqlite3.Error as e:
                print("An error occurred: " + e.args[0])

        if (combo.get() == ""):
            self.LblWarningStat.config(text = "*Select a course type!")
        else:
            self.LblWarningStat.config(text = "")
            if results == 0 or Ent.get() == "":
                self.LblWarningStat.config(text = "*Subject not found!")
            else:
                partPie = ((results/noOfRecs)*100)
                partPie2 = 100 - partPie
                fracs = [partPie, partPie2]
                pie(fracs, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
                show()
    def valueInCombo(self, Ent):
        conn=sqlite3.connect("database.db")
        cur=conn.cursor()
        bookSelected = self.comboBook.get()
        print(bookSelected)
        cur.execute("SELECT NoOfBooks FROM Book WHERE Title ="+"'"+bookSelected+"'")
        bookNO = cur.fetchall()
        bookNO = str(bookNO[0])
        bookNO = re.sub('[(,)]', "", bookNO)
        print(bookNO)
        Ent.delete(0, END)
        Ent.insert(0, bookNO)

    #this is a frame that allows books to be loaned and returned
    def BookLoan(self):
        root.geometry("650x420")
        self.Menu.grid_remove()
        self.BookLoanFrme = Frame(self)
        self.BookLoanFrme.grid()
        self.BookLoanFrme.config(cursor = "@cursor.cur")
        self.BookLoanFrme.columnconfigure(0,weight=1)       
        bookID = allLabels(self.BookLoanFrme, "Enter book ID: ", ("Arial", 12,"normal"))
        self.bookIDent = ttk.Entry(self.BookLoanFrme)
        bookID.grid_mel(0, 0, "nw", 20, 20)
        self.bookIDent.grid(column =0, row = 0, sticky = "nw", pady =20, padx = 135)
        studentIDLbl = allLabels(self.BookLoanFrme, "Student ID: ", ("Arial", 12,"normal"))
        studentIDLbl.grid_mel(0,0, "nw", 410, 20)
        self.studentIDEnt = ttk.Entry(self.BookLoanFrme)
        self.studentIDEnt.grid(column = 0, row = 0, sticky = "nw", pady = 20, padx = 500)
        self.loanInformationTree = ttk.Treeview(self.BookLoanFrme, selectmode = "extended", columns=("LoanNo", "Book Title", "Student Name", "Date Borrowed", "Return Date"))
        self.loanInformationTree.column("LoanNo", width = 50)
        self.loanInformationTree.column("Book Title", width = 100)
        self.loanInformationTree.column("Student Name", width = 100)
        self.loanInformationTree.column("Date Borrowed", width = 100)
        self.loanInformationTree.column("Return Date", width = 100)
        self.loanInformationTree.heading("LoanNo", text = "LoanNo")
        self.loanInformationTree.heading("Book Title", text = "Book Title")
        self.loanInformationTree.heading("Student Name", text = "Student Name")
        self.loanInformationTree.heading("Date Borrowed", text = "Date Borrowed")
        self.loanInformationTree.heading("Return Date", text = "Return Date")
        self.loanInformationTree['show'] = 'headings'
        self.loanInformationTree.grid(column = 0, row = 0, sticky = "nw", pady = 110, padx = 100)
        self.warningLbl = Label(self.BookLoanFrme, text = "", fg = "red")
        self.warningLbl.grid(column = 0, row = 0, sticky = "wn", padx = 50, pady = 360)
        BorrowBtn = ttk.Button(self.BookLoanFrme, text = "Borrow", command = lambda:self.bookBorrowed())
        BorrowBtn.grid(column = 0, row = 0, sticky = "ws", padx = 50, pady = 380)
        ReturnBtn = ttk.Button(self.BookLoanFrme, text = "Return", command = lambda:self.bookReturned())
        ReturnBtn.grid(column = 0, row = 0, sticky = "ws", padx = 160, pady = 380)
        OverdueBtn = ttk.Button(self.BookLoanFrme, text = "Overdue Books", command = lambda:self.highlightOverdue())
        OverdueBtn.grid(column = 0, row = 0, sticky = "ws", padx = 390, pady = 380)
        Sendwarning = ttk.Button(self.BookLoanFrme, text = "Send Warning", command = lambda:self.SendEmail())
        Sendwarning.grid(column = 0, row = 0, sticky = "ws", padx = 520, pady = 380)
        bookData = ttk.Button(self.BookLoanFrme, text = "Add book Data", command = lambda:self.AddBookData())
        bookData.grid(column = 0, row = 0, sticky = "ws", padx = 270, pady = 380)
        generateBarc = ttk.Button(self.BookLoanFrme, text = "Print Barcodes", command = lambda:self.printBarcodes())
        generateBarc.grid(column = 0, row = 0, sticky = "wn", padx = 330, pady = 350)
        Home = ttk.Button(self.BookLoanFrme, text = "Home", command = lambda:self.goHome(self.BookLoanFrme))
        Home.grid(row = 0, column = 0, sticky = "wn", padx = 215, pady = 350)
        self.CreatingBookTables()
        self.treeShowData()
        #self.loanInformationTree.bind("<<TreeviewSelect>>", lambda wasteevent:self.SendEmail())

    def CreatingBookTables(self):
        conn=sqlite3.connect("database.db")
        cur=conn.cursor()
        try:
            cur.execute("""CREATE TABLE if not exists Book(
                        ISBN VARCHAR (20) PRIMARY KEY,
                        Title VARCHAR (40),
                        NoOfBooks INTEGER,
                        authFirstN VARCHAR (30),
                        authSurN VARCHAR (30)
                        )""")
                
        
            cur.execute("""CREATE TABLE if not exists BookCopy(
                        bookCopyNo VARCHAR (2) PRIMARY KEY,
                        ISBN VARCHAR (20),
                        FOREIGN KEY (ISBN) REFERENCES Book(ISBN)
                        )""")


            cur.execute("""CREATE TABLE if not exists Loan(
                        loanNo VARCHAR(4) PRIMARY KEY,
                        studID CHAR (8),
                        bookCopyNo VARCHAR (2),
                        returnDate DATE,
                        borrowDate DATE,
                        FOREIGN KEY (studID) REFERENCES studentData(studID),
                        FOREIGN KEY (bookCopyNo) REFERENCES BookCopy(bookCopyNo)
                        )""")
        except sqlite3.Error as e:
            print("An error occurred: " + e.args[0])
    


    def SendEmail(self):
        conn=sqlite3.connect("database.db")
        cur=conn.cursor()
        global DetailRecover
        DetailRecover = False
        self.EmailScreen = Tk()
        self.EmailScreen.title("Send Alert")
        self.EmailScreen.geometry("400x200")
        self.EmailScreen.wm_iconbitmap("favicon.ico")
        self.EmailScreen.config(cursor = "@cursor.cur")
        To = ttk.Label(self.EmailScreen, text = "To: ")
        To.grid(row = 0, sticky = "w", padx = 10, pady = 5)
        self.ToEnt = ttk.Entry(self.EmailScreen, width = 52)
        self.ToEnt.grid(row = 0, sticky = "w", padx = 70, pady = 5)
        From = ttk.Label(self.EmailScreen, text = "From: ")
        From.grid(row = 1, sticky = "w", padx = 10)
        self.FromEnt = ttk.Entry(self.EmailScreen, width = 52)
        self.FromEnt.grid(row = 1, sticky = "w", padx = 70)
        Subject = ttk.Label(self.EmailScreen, text = "Subject: ")
        Subject.grid(row = 2, sticky = "w", padx = 10, pady = 5)
        self.SubjectEnt = ttk.Entry(self.EmailScreen, width = 52)
        self.SubjectEnt.grid(row = 2, sticky = "w", padx = 70, pady = 5)
        MessageLbl = Label(self.EmailScreen, text = "Message: ")
        MessageLbl.grid(row = 3, sticky = "nw", padx = 10)
        self.Message = Text(self.EmailScreen, height = 5, width = 39)
        self.Message.grid(row = 3, sticky = "w", padx = 70)
        Send = ttk.Button(self.EmailScreen, text = "Send", command = lambda:self.sendTheMail())
        Send.grid(row = 4, sticky = "sw", padx = 305, pady = 5)
        item = self.loanInformationTree.selection()
        print(item)
        NamesList = []
        self.emailSendingTo = []
        for i in item:
            i = str(i)
            print("you clicked on", self.loanInformationTree.item(i,"text"))
            x = 0
            for value in self.loanInformationTree.item(i)['values']:
                x +=1
                if x > 2 and x < 4:
                    firstName = value
                    firstName = str(firstName)
                    firstName = firstName.split()
                    lastName = firstName[1]
                    print(lastName)
                    firstName = firstName[0]
                    print(firstName)
                    NamesList.append((str(firstName)+" "+str(lastName)))
                    try:
                        cur.execute("SELECT studID FROM studentData WHERE studNameF = "+"'"+firstName+"'"+"AND studNameL = "+"'"+lastName+"'")
                        studID = str(cur.fetchall())
                        studID = re.sub('[(,)]',"", studID)
                        #this removes the quotes at the start and at the end
                        studID = studID[1:-1]
                        studID = studID[1:-1]
                        print(studID)
                        studID = str(studID)
                        studID = studID+"@strodes.ac.uk"
                        print(studID, "stud id")
                        self.emailSendingTo.append(studID)
                        print(self.emailSendingTo)
                        print(NamesList)
                    except sqlite3.Error as e:
                        print("An error occurred: " + e.args[0])
        try:
            cur.execute("SELECT firstName, lastname, email FROM User")
            details = str(cur.fetchall())
            details = re.sub('[(,)]',"", details)
            #this removes the quotes at the start and at the end
            details = details[1:-1]
            details = details[1:-1]
            details = details.split()
            firstName = ""
            lastName = ""
            self.Email = ""
            x = 0
            for i in details:
                x =x+1
                if x == 1:
                    firstName = i[0:-1]
                if x == 2:
                    lastName = i[1:-1]
                if x == 3:
                    self.Email = i[1:]
        except:
            print()
        self.Name = (str(firstName)+" "+str(lastName))
        self.FromEnt.insert(0, self.Name)
        x = len(NamesList)
        x = int(x)
        NamesList = self.QuickSort(NamesList)
        print(NamesList)
        for i in NamesList:
            self.ToEnt.insert(END, i)
            if x%2 == 0:
                self.ToEnt.insert(END, ", ")
            x = x - 1
            
        self.EmailScreen.mainloop()
        
    def QuickSort(self, li):
        if li == []: 
            return []
        else:
            piv = li[0]
            less = self.QuickSort([x for x in li[1:] if x < piv])
            bigger = self.QuickSort([x for x in li[1:] if x >= piv])
            return less + [piv] + bigger

    def sendTheMail(self):
        conn=sqlite3.connect("database.db")
        cur=conn.cursor()
        self.s = smtplib.SMTP("smtp.mail.yahoo.com", 25)
        msg = email.message_from_string(str(self.Message.get("1.0", END)))
        if len(self.emailSendingTo) == 0:
            msg['To'] = ",".join(str(self.ToEnt.get()))
            To = []
            To.append(self.ToEnt.get())
            print(To)
        else:
            print("List")
            msg['To'] = ",".join(self.emailSendingTo)
        msg['From'] = str(self.Email)
        print(len(self.emailSendingTo), "email sending to")
        print(self.emailSendingTo, "inside")
        msg['Subject'] = str(self.SubjectEnt.get())
        self.PasswordSaved = None
        self.s.ehlo()
        self.s.starttls() 
        self.s.ehlo()
        if len(self.emailSendingTo) == 0:
            self.emailPart(To, msg, self.s, self.Email)
        else:
            self.emailPart(self.emailSendingTo, msg, self.s, self.Email)
    
    def emailPart(self, emailSendingTo, msg, s, Email):
        print("here")
        if (os.path.exists("EmailPass.txt")):
            showMessage = False
            global recover
            if recover == True:
                recover = False
                showMessage = True
            file = open("EmailPass.txt", "r")
            password = str(file.readline())
            password = self.decrypt(password)
            print(password, "Password")
            print(Email, "Email")
            s.login(str(Email), str(password))
            s.sendmail(str(Email), emailSendingTo, msg.as_string())
            s.quit()
            if showMessage == True:
                messagebox.showinfo(
                message = "Email has been sent to you with your details",
                icon = "info", title = "Details Recover", detail = "Press OK to continue")
                recover = False
            else:
                messagebox.showinfo(
                message = "Email has been sent!",
                icon = "info", title = "Book Loan System", detail = "Press OK to continue")
                self.EmailScreen.destroy()
            
        else:
            print("No pass")
            self.loginPrompt = Toplevel()
            self.loginPrompt.title("Email login")
            self.loginPrompt.geometry("250x85")
            self.loginPrompt.wm_iconbitmap("favicon.ico")
            self.loginPrompt.config(cursor = "@cursor.cur")
            EmailLbl = ttk.Label(self.loginPrompt, text = "E-mail: ")
            EmailLbl.grid(row = 0, sticky = "w", padx = 10, pady = 5)
            EmailEnt = ttk.Entry(self.loginPrompt)
            EmailEnt.grid(row = 0, sticky = "w", padx = 110, pady = 5)
            PasswordLbl = ttk.Label(self.loginPrompt, text = "E-mail Password: ")
            PasswordLbl.grid(row = 1, sticky = "w", padx = 10)
            self.PasswordEnt = ttk.Entry(self.loginPrompt, show = "*")
            self.PasswordEnt.grid(row = 1, sticky = "w", padx = 110)
            Login = ttk.Button(self.loginPrompt, text = "Login", command = lambda:self.SaveAndLogin())
            Login.grid(row =2, sticky = "sw", padx = 160, pady = 5)
            self.loginPrompt.mainloop()
        

    def SaveAndLogin(self):
        self.EmailPassword = str(self.PasswordEnt.get())
        print(self.EmailPassword)
        file = open("EmailPass.txt", "w")
        self.EmailPassword = str(self.EmailPassword)
        text = self.encrypt(self.EmailPassword)
        file.write(text)
        file.close()
        self.loginPrompt.destroy()
        global recover
        if recover == True:
            messagebox.showinfo(
                message = "Sign in complete, click request details to request details",
                icon = "info", title = "Details Recover", detail = "Press OK to continue")

    def encrypt(self, message):                                                                     
        encrypted = []
        key = "Encryption"
        for i, c in enumerate(message):
            key_c = ord(key[i % len(key)])
            message_c = ord(c)
            encrypted.append(chr((message_c+key_c) % 127))
        return "".join(encrypted)

    def decrypt(self, message):
        decrypted = []
        key = "Encryption"
        for i, c in enumerate(message):
            key_c = ord(key[i % len(key)])
            enc_c = ord(c)
            decrypted.append(chr((enc_c - key_c) %127))
        return "".join(decrypted)
            
    
    def highlightOverdue(self):
        self.clearSelection()
        y = 0
        print("Length", len(self.loanInformationTree.get_children()))
        if len(self.loanInformationTree.get_children()) != 0:
            for line in self.loanInformationTree.get_children():
                print(line)
                x = 0
                for value in self.loanInformationTree.item(line)['values']: 
                    x +=1
                    if x > 4 and x < 6:
                        print(self.loanInformationTree.item(line))
                        item = self.loanInformationTree.item(line)
                        import time
                        import datetime
                        todaysDate = datetime.date.today()
                        from datetime import date
                        print(value)
                        temp = str(value)
                        print(temp, "temp1", todaysDate, "todays Date")
                        if temp[1:2] == "/":
                            tempday = str("0"+temp[0:1])
                        else:
                            tempday = str(temp[0:2])
                        if temp[3:4] == "/":
                            tempmonth = str("0"+temp[2:3])
                        else:
                            tempmonth = str(temp[3:5])
                        tempyear = temp[-2:]
                        tempdate = tempday+"/"+tempmonth+"/"+tempyear
                        tempdate = datetime.datetime.strptime(tempdate, "%d/%m/%y").date()
                        

                        if tempdate < todaysDate:
                            print(temp)
                            self.loanInformationTree.selection_add(line)
                            y = y+1
                        else:
                            if y == 0:
                                self.warningLbl.config(text = "*There are no overdue books")
                            else:
                                print()
        else:
            self.warningLbl.config(text = "*There are no loaned out books")
    def clearSelection(self):
        for line in self.loanInformationTree.get_children():
            self.loanInformationTree.selection_remove(line)

    
    def clearTreeView(self):
        print("deleting")
        for i in self.loanInformationTree.get_children():
            self.loanInformationTree.delete(i)

    def treeShowData(self):
        conn=sqlite3.connect("database.db")
        cur=conn.cursor()
        self.clearTreeView()
        try:
            cur.execute("SELECT * FROM Loan")
            recs = cur.fetchall()
        except sqlite3.Error as e:
            print("An error occurred: " + e.args[0])
        self.iidNum = 0
        for i in recs:
            self.iidNum +=1
            i = list(i)
            loanNo = i[0]
            studentID = i[1]

            studentID = str(studentID)
            bookCopy = str(i[2])
            print(bookCopy)
            returnDate = i[3]
            borrowDate = i[4]
            try:
                firstName = cur.execute("SELECT studNameF FROM studentData WHERE studID = ?", [studentID])
                firstName =str(cur.fetchall())
                firstName = re.sub('[(,)]',"",firstName)
                firstName = firstName[1:-1]
                firstName = firstName[1:-1]
                lastName = cur.execute("SELECT studNameL FROM studentData WHERE studID = ?", [studentID])
                lastName = str(cur.fetchall())
                lastName = re.sub('[(,)]',"",lastName)
                lastName = lastName[1:-1]
                lastName = lastName[1:-1]
                name = (str(firstName)+" "+ str(lastName))
            except sqlite3.Error as e:
                print("An error occurred: " + e.args[0])
            try:
                title = cur.execute("SELECT Title FROM Book, BookCopy WHERE bookCopyNo = "+"'"+bookCopy+"'"+" AND BookCopy.ISBN = Book.ISBN")
                title = str(cur.fetchall())
                title = re.sub('[(,)]',"",title)
                title = title[1:-1]
                title = title[1:-1]
            except sqlite3.Error as e:
                print("An error occurred: " + e.args[0])
            self.loanInformationTree.insert("" ,"end",iid = self.iidNum,text = str(self.iidNum), values=(str(loanNo), str(title), name, str(borrowDate), str(returnDate)))


    def printBarcodes(self):
        conn=sqlite3.connect("database.db")
        cur=conn.cursor()
        self.barcodesFrme = Tk()
        self.barcodesFrme.title("Generate barcodes")
        self.barcodesFrme.geometry("250x125")
        self.barcodesFrme.wm_iconbitmap("favicon.ico")
        self.barcodesFrme.config(cursor = "@cursor.cur")
        ComboLbl = Label(self.barcodesFrme, text = "Select book: ")
        ComboLbl.grid(row = 0, padx = 0, sticky = "w")
        variable = StringVar()
        comboBox = ttk.Combobox(self.barcodesFrme, textvariable = variable)
        comboBox.grid(row = 0, padx = 100, sticky = "w")
        valueList = []
        try:
            cur.execute("SELECT Title FROM Book")
            titles = cur.fetchall()
        except sqlite3.Error as e:
            print("An error occurred: " + e.args[0])
        for i in titles:
            temp = str(i)
            temp = re.sub('[(,)]',"", temp)
            #this removes the quotes at the start and at the end
            temp = temp[1:-1]
            temp = str(temp)
            valueList.append(temp)
        comboBox.configure(values = valueList)
        comboBox.bind("<<ComboboxSelected>>", lambda wasteevent:self.comboValue(comboBox))
        orLbl = Label(self.barcodesFrme, text = "OR")
        orLbl.grid(row = 1, padx = 100, pady = 5, sticky = "w")
        ISBN = Label(self.barcodesFrme, text = "Enter ISBN: ")
        ISBN.grid(row = 2, padx = 0, sticky = "w")
        self.ISBNEntB = ttk.Entry(self.barcodesFrme)
        self.ISBNEntB.grid(row = 2, padx = 100)
        self.warningLblBar = Label(self.barcodesFrme, text = "", fg = "red")
        self.warningLblBar.grid(row = 3, sticky = "w", padx = 0)
        generateBtn = ttk.Button(self.barcodesFrme, text = "Generate", command = lambda:self.PDFPrintBarcodes(comboBox))
        generateBtn.grid(row = 4, sticky = "w", padx = 0, pady = 5)
        Close = ttk.Button(self.barcodesFrme, text = "Close", command = lambda:self.CloseOrCancel(self.barcodesFrme))
        Close.grid(row = 4, sticky = "w", padx = 100, pady = 5)

    def comboValue(self, combo):
        conn=sqlite3.connect("database.db")
        cur=conn.cursor()
        value = str(combo.get())
        print(value)
        try:
            cur.execute("SELECT ISBN FROM Book WHERE Title ="+"'"+value+"'")
            isbn = str(cur.fetchall())
            isbn = str(isbn[3:-4])
            self.ISBNEntB.delete(0, END)
            self.ISBNEntB.insert(0,isbn)
        except sqlite3.Error as e:
            print("An error occurred: " + e.args[0])
            

    def PDFPrintBarcodes(self, combo):
        if str(self.ISBNEntB.get()) != "" and str(combo.get()) != "":
            try:
                self.warningLblBar.configure(text = "")
                c = canvas.Canvas("barcodes.pdf")

                print(self.ISBNEntB.get())
                print(str(combo.get()))
                barcodeList = ["barcode_value1", "barcode_value2", "barcode_value3", "barcode_value4", "barcode_value5", "barcode_value6", "barcode_value7", "barcode_value8", "barcode_value9", "barcode_value10", "barcode_value11", "barcode_value12", "barcode_value13", "barcode_value14", "barcode_value15", "barcode_value16", "barcode_value17", "barcode_value18", "barcode_value19", "barcode_value20", "barcode_value21"]
                count = ["1000", "2000", "3000", "4000", "5000", "6000", "7000", "8000", "9000", "1001", "1100", "1200", "1300", "1400", "1500", "1600", "1700", "1800", "1900", "2001", "2100"]
                Ent = str(self.ISBNEntB.get()[4:])
                barcodeList2 = ["barcode1", "barcode2", "barcode3", "barcode4", "barcode5", "barcode6", "barcode7", "barcode8", "barcode9", "barcode10", "barcode11", "barcode12", "barcode13", "barcode14", "barcode15", "barcode16", "barcode17", "barcode18", "barcode19", "barcode20", "barcode21"]
                Drawings = ["d1", "d2", "d3","d4", "d5", "d6", "d7", "d8", "d9","d10","d11","d12","d13","d14","d15","d16","d17","d18","d19","d20","d21"]
                checkList = []
                barcodesNo = []
                TheDList = []
                x =0
                for i in barcodeList:
                    globals()[i] = str(count[x]+Ent)
                    checkList.append(globals()[i])
                    print(checkList)
                    x = x+1
                self.barcodesFrme.destroy()

                x = 0
                for z in barcodeList2:
                    globals()[z] = eanbc.Ean13BarcodeWidget(checkList[x])
                    barcodesNo.append(globals()[z])
                    print(barcodesNo)
                    x = x + 1

                
                for y in Drawings:
                    globals()[y] = Drawing(20, 10)
                    TheDList.append(globals()[y])
                    print(TheDList)

                x =0
                for m in TheDList:
                    m.add(barcodesNo[x])
                    x = x+1

                l = 55
                n = 0
                for x in range(0, 7):
                    renderPDF.draw(TheDList[n], c, 60, l)
                    renderPDF.draw(TheDList[n+1], c, 240, l)
                    renderPDF.draw(TheDList[n+2], c, 420, l)
                    l  = l + 110
                    n = n+3

                c.save()
                #Opens up PDF
                subprocess.Popen("barcodes.pdf",shell=True)
            except:
                self.warningLbl.config(text = "*Please close the PDF file to generate new ones!")
        else:
            self.warningLblBar.configure(text = "*Please select book or enter ISBN") 

    def bookReturned(self):
        conn=sqlite3.connect("database.db")
        cur=conn.cursor()
        try:
            cur.execute("SELECT studID FROM studentData WHERE studID =?", [str(self.studentIDEnt.get())])
            idlength = len(cur.fetchall())
            print(idlength, "idlength")
        except sqlite3.Error as e:
            print("An error occurred: " + e.args[0])
            
        if self.bookIDent.get() != "" and self.studentIDEnt.get() != "":
            if idlength !=0:
                studID = self.studentIDEnt.get()
                self.warningLbl.config(text = "")
                copyNo = self.bookIDent.get()[0:4]
                copyNo = str(copyNo)
                print(copyNo[3:4])
                if copyNo[3:4] == "0":
                    print("CopyNo is not 10 or 20")
                    if copyNo[1:2] == "0":
                        print("One digit copyNo")
                        copyNo = copyNo[0:1]
                    else:
                        copyNo =copyNo[0:2]
                else:
                    copyNo = copyNo[0:2]
                    print("CopyNo is 10 or 20")
                print(copyNo)
                try:
                    cur.execute("DELETE FROM Loan WHERE studID = "+"'"+studID+"'"+"AND bookCopyNo = "+"'"+copyNo+"'")
                    cur.execute("DELETE FROM BookCopy WHERE bookCopyNo = ?", [copyNo]) 
                    conn.commit()
                    print("Deleting from database")
                    self.treeShowData()
                except:
                    self.warningLbl.config(text = "*Student ID or book ID incorrect!")
            else:
                self.warningLbl.config(text = "*Student ID incorrect") 
        else:
            self.warningLbl.config(text = "*Please fill in the fields") 
        
        
                    
    def bookBorrowed(self):
        bookNo = None
        ISBNFound = None
        conn=sqlite3.connect("database.db")
        cur=conn.cursor()
        try:
            cur.execute("SELECT studID FROM studentData WHERE studID =?", [str(self.studentIDEnt.get())])
            idlength = len(cur.fetchall())
            print(idlength, "idlength")
        except sqlite3.Error as e:
            print("An error occurred: " + e.args[0])
        if self.bookIDent.get() != "" and self.studentIDEnt.get() != "":
            if idlength != 0:
                try:
                    cur.execute("SELECT ISBN FROM Book")
                    compareISBN = cur.fetchall()
                    compareISBN = list(compareISBN)
                except:
                    self.warningLbl.config(text = "*No book data found! Enter book data by clicking 'Add book Data'")
                for i in range(0, len(compareISBN)):
                    Temp = compareISBN[i]
                    Temp = str(Temp)
                    Temp = Temp[1:-1]
                    Temp = Temp[1:-1]
                    Temp = Temp[0:-1]
                    print(Temp)
                    if len(Temp) == 13 and Temp[7:-1] == self.bookIDent.get()[7:-1]:
                        print("Here")
                        print(Temp[7:-1])
                        print(self.bookIDent.get()[7:-1])
                        print("ISBN found")
                        fullISBN = Temp
                        ISBNFound = True
                        break
                    else:
                        print("ISBNT not same")
                        ISBNFound = False
                
                if ISBNFound == True:
                    self.warningLbl.config(text = "")
                    copyNo = self.bookIDent.get()[0:4]
                    copyNo = str(copyNo)
                    print(copyNo[3:4])
                    if copyNo[3:4] == "0":
                        print("CopyNo is not 10 or 20")
                        if copyNo[1:2] == "0":
                            print("One digit copyNo")
                            copyNo = copyNo[0:1]
                        else:
                            copyNo =copyNo[0:2]
                    else:
                        copyNo = copyNo[0:2]
                        print("CopyNo is 10 or 20")
                    print(copyNo)
                    bookList = [copyNo, fullISBN]
                    bookList = tuple(bookList)
                    try:
                        fullISBN = str(fullISBN)
                        cur.execute("SELECT NoOfBooks FROM Book WHERE ISBN =?", [fullISBN])
                        No = cur.fetchall()
                        No = No[0]
                        No = str(No)
                        No = No[1:-1]
                        No = No[0:-1]
                        No = int(No)
                        No = No - 1
                        No = str(No)
                        cur.execute("UPDATE Book SET NoOfBooks ="+"'"+No+"'"+"WHERE ISBN ="+"'"+fullISBN+"'")
                    except sqlite3.Error as e:
                        print("An error occurred: " + e.args[0])
                    SQL = "INSERT INTO BookCopy(bookCopyNo, ISBN) "
                    SQL = SQL + "VALUES(?,?)"
                    print("fullISBN", fullISBN)
                    try:
                        cur.execute(SQL, bookList)
                        conn.commit()
                        bookNo = True
                    except sqlite3.Error as e:
                        self.warningLbl.config(text = "*There is a book already loaned out with that copy number")
                        bookNo = False
                        print("An error occurred: " + e.args[0])
                else:
                    self.warningLbl.config(text = "*The entered book ID is incorrect")
            else:
                self.warningLbl.config(text = "*Student ID not found")

            if bookNo == True:
                print("Book NO is true")
                self.warningLbl.config(text = "")
                try:
                    cur.execute("SELECT loanNo FROM Loan ORDER BY CAST(loanNo AS INTEGER) DESC LIMIT 1")
                    loan = str(cur.fetchall())
                    print("loan NO: ", loan)
                    if loan == "[]":
                        print("No loans currently")
                        loan = "1"
                    else:
                        loan = re.sub('[(,)]',"", loan)
                        loan = loan[1:-1]
                        loan = loan[1:-1]
                        loan = int(loan)
                        print(loan)
                        loan = loan + 1
                        loan = str(loan)
                    import datetime
                    todaysDate = datetime.date.today().strftime("%d/%m/%Y")
                    day = str(todaysDate[0:2])
                    month = str(todaysDate[3:5])
                    year = str(todaysDate[6:])
                    if day == "31" or day == "30" or day == "28" and month == "02":
                        print("First IF")
                        dueday = "07"
                        if month != "12":
                            returnDate = dueday+"/"+(str((int(month)+1)))+todaysDate[5:]
                        else:
                            month = "01"
                            year = ((int(year))+1)
                            returnDate = dueday+"/"+month+"/"+(str(year))
                               
                            
                    elif int(day) > 24 and month == "01" or month == "03" or month == "05" or month == "07" or month == "08" or month == "10" or month == "12":
                        print("Second IF")
                        if (int(day) + 7) > 31:
                            value = (int(day) + 7)
                            left = value - 31
                            left = str(left)
                            if int(left[0]) > 0:
                                dueday = str(left)
                            else:
                                dueday = "0"+str(left)
                            if month != "12":
                                returnDate = dueday+"/"+(str((int(month)+1)))+todaysDate[5:]
                            else:
                                month = "01"
                                year = ((int(year))+1)
                                returnDate = dueday+"/"+month+"/"+(str(year))
                        else:
                            value = (int(day) + 7)
                            dueday = str(value)
                            returnDate = dueday+todaysDate[2:]
                            
                    elif int(day) > 24 and month == "04" or month == "06" or month == "09" or month == "11":
                        print("THird IF")
                        if (int(day) + 7) > 30:
                            value = (int(day) + 7)
                            left = value - 30
                            left = str(left)
                            if int(left[0]) > 0:
                                dueday = str(left)
                            else:
                                dueday = "0"+str(left)
                            if month != "12":
                                returnDate = dueday+"/"+(str((int(month)+1)))+todaysDate[5:]
                            else:
                                month = "01"
                                year = ((int(year))+1)
                                returnDate = dueday+"/"+month+"/"+(str(year))
                        else:
                            value = (int(day) + 7)
                            dueday = str(value)
                            returnDate = dueday+todaysDate[2:]
                                
                    elif int(day) > 24 and month == "02":
                        print("Fourth IF")
                        if (int(day) + 7) > 28:
                            value = (int(day) + 7)
                            left = value - 28
                            left = str(left)
                            if int(left[0]) > 0:
                                dueday = str(left)
                            else:
                                dueday = "0"+str(left)
                            if month != "12":
                                returnDate = dueday+"/"+(str((int(month)+1)))+todaysDate[5:]
                            else:
                                month = "01"
                                year = ((int(year))+1)
                                returnDate = dueday+"/"+month+"/"+(str(year))

                        else:
                            value = (int(day) + 7)
                            dueday = str(value)
                            returnDate = dueday+todaysDate[2:]
                    else:
                        print("Im here mofo")
                        dueday = str(int(day) + 7)
                        if int(dueday[0]) > 0 :
                                dueday = str(int(day) + 7)
                        else:
                            dueday = "0"+str(int(day) + 7)
                        print("In")
                        returnDate = dueday+todaysDate[2:]
                    
                    loanList = [loan, self.studentIDEnt.get(), copyNo, returnDate, todaysDate]
                    loanList = tuple(loanList)
                except sqlite3.Error as e:
                    print("An error occurred: " + e.args[0])
                try:
                    SQL = "INSERT INTO Loan(loanNo, studID, bookCopyNo, returnDate, borrowDate) "
                    SQL = SQL + "VALUES(?,?,?,?,?)"
                    cur.execute(SQL, loanList)
                    conn.commit()
                except sqlite3.Error as e:
                    self.warningLbl.config(text = "*An error occured")
                    print("An error occurred: " + e.args[0])
                    print("Here")
                try:
                    title = cur.execute("SELECT Title FROM Book WHERE ISBN = ?", [fullISBN])
                    title = str(cur.fetchall())
                    print("title")
                    title = re.sub('[(,)]',"", title)
                    #this removes the quotes at the start and at the end
                    title = title[1:-1]
                    title = title[1:-1]
                except sqlite3.Error as e:
                    self.warningLbl.config(text = "*No book data found! Enter book data by clicking 'Add book Data'")
                    print("An error occurred: " + e.args[0])
                try:
                    firstName = cur.execute("SELECT studNameF FROM studentData WHERE studID = ?", [self.studentIDEnt.get()])
                    firstName =str(cur.fetchall())
                    firstName = re.sub('[(,)]',"",firstName)
                    firstName = firstName[1:-1]
                    firstName = firstName[1:-1]
                    
                    lastName = cur.execute("SELECT studNameL FROM studentData WHERE studID = ?", [self.studentIDEnt.get()])
                    lastName = str(cur.fetchall())
                    lastName = re.sub('[(,)]',"",lastName)
                    lastName = lastName[1:-1]
                    lastName = lastName[1:-1]

                    name = (str(firstName)+" "+ str(lastName))
                    print(name)
                    self.iidNum +=1
                    print("iidNum: ", self.iidNum)
                    self.loanInformationTree.insert("" ,"end",iid = self.iidNum, values=(str(loan), title, name, todaysDate, returnDate))

                except sqlite3.Error as e:
                    self.warningLbl.config(text = "*No book data found! Enter book data by clicking 'Add book Data'")
                    print("An error occurred: " + e.args[0])
        else:
            self.warningLbl.config(text = "*Please fill in the fields")
        
        
        
    def CloseOrCancel(self, x):
        x.destroy()

    def AddBookData(self):
        self.bookData = Tk()
        self.bookData.title("Add Book Data")
        self.bookData.geometry("300x155")
        self.bookData.wm_iconbitmap("favicon.ico")
        self.bookData.config(cursor = "@cursor.cur")
        ISBN = Label(self.bookData, text = "ISBN: ")
        ISBN.grid(row = 0, padx = 0, sticky = "w")
        self.ISBNEnt = Entry(self.bookData)
        self.ISBNEnt.grid(row = 0, padx = 110)
        bookTitle = Label(self.bookData, text = "Name of Book: ")
        bookTitle.grid(row = 1, padx = 0, sticky = "w")
        self.bookTitleEnt = Entry(self.bookData)
        self.bookTitleEnt.grid(row = 1, padx = 110)
        AuthorFirst = Label(self.bookData, text = "Author first name: ")
        AuthorFirst.grid(row = 2, padx = 0, sticky = "w")
        self.AuthorFirstEnt = Entry(self.bookData)
        self.AuthorFirstEnt.grid(row = 2, padx = 110)
        AuthorSecond = Label(self.bookData, text = "Author last name: ")
        AuthorSecond.grid(row = 3, padx = 0, sticky = "w")
        self.AuthorSecondEnt = Entry(self.bookData)
        self.AuthorSecondEnt.grid(row = 3, padx = 110)
        numBooks = Label(self.bookData, text = "Number of books in Class: ")
        numBooks.grid(row = 4, padx = 0, sticky = "w")
        self.numBooksEnt = Entry(self.bookData)
        self.numBooksEnt.grid(row = 4, padx = 160)
        self.warningLblB = Label(self.bookData, text = "", fg = "red")
        self.warningLblB.grid(row = 5, padx = 0, sticky = "w")
        Save = ttk.Button(self.bookData, text = "Save", command = lambda:self.saveBook())
        Save.grid(row = 6, padx = 0, pady = 5, sticky = "w")
        Cancel = ttk.Button(self.bookData, text = "Cancel", command = lambda:self.CloseOrCancel(self.bookData))
        Cancel.grid(row = 6, padx = 80, pady =5, sticky = "w")
        self.bookData.mainloop()

    def saveBook(self):
        conn=sqlite3.connect("database.db")
        cur=conn.cursor()
        check = False
        def integerChecker(ent):
            try:
                int(ent)
                return True
            except ValueError:
                return False
        bookDataList = [self.ISBNEnt.get(), self.bookTitleEnt.get(), self.numBooksEnt.get(), self.AuthorFirstEnt.get(), self.AuthorSecondEnt.get()]
        intBooks = self.numBooksEnt.get()
        for i in bookDataList:
            if str(i) == "":
                check = True
        if check == True:        
            self.warningLblB.configure(text = "*Please fill in all the fields")
        else:
            if integerChecker(intBooks) == True:
                if int(intBooks) > -1 and int(intBooks) <= 500:
                    bookDataList = tuple(bookDataList)
                    SQL = "INSERT INTO Book(ISBN, Title, NoOfBooks, authFirstN, authSurN) "
                    SQL = SQL + "VALUES(?,?,?,?,?)"
                    try:
                        print(SQL)
                        print(bookDataList)
                        cur.execute(SQL,bookDataList)
                        conn.commit()
                        question = messagebox.askyesno(message = "Would you like to enter data for another book?", icon = "question", title = "Book Data")
                        if  question == True:
                            self.bookData.destroy()
                            self.AddBookData()
                        else:
                            self.bookData.destroy()
                    except sqlite3.Error as e:
                        print("An error occurred: " + e.args[0])
                else:
                    if int(intBooks) < -1:
                        self.warningLblB.configure(text = "*Enter book number bigger than -1")
                    else:
                        self.warningLblB.configure(text = "*Enter book number less than 500")
            else:
                self.warningLblB.configure(text = "*Enter a number for number of books")
            


    def EnterStudentInfo(self):
        self.StudentInformation = Frame(self)
        #Labels and buttons
        if studentLoggedIn == False:
            self.Menu.grid_remove()
        else:
            print("Student Logged in")
        self.StudentInformation.grid()
        self.StudentInformation.config(cursor = "@cursor.cur")
        root.geometry("1300x715")
        self.StudentInformation.columnconfigure(0,weight=1)

        titleComp = allLabels(self.StudentInformation, "COMPUTING/ICT STUDENT INFORMATION RECORD", ("Arial", 20,"bold"))
        titleComp.grid_mel(0, 0, "w", 290, 10)                             

        StudNameF = allLabels(self.StudentInformation, "FIRST NAME: ", ("Arial", 12,"normal"))
        StudNameF.grid_mel(1, 0, "w", 20, 10)

        StudNameL = allLabels(self.StudentInformation, "LAST NAME: ", ("Arial", 12, "normal"))
        StudNameL.grid_mel(1, 0, "w", 380, 10)

        StudNameEntL = ttk.Entry(self.StudentInformation)
        StudNameEntL.grid(row = 1, sticky = "w", padx = 480, pady = 10)

        StudNameEntF = ttk.Entry(self.StudentInformation)
        StudNameEntF.grid(row = 1, sticky = "w", padx = 125, pady = 10)

        StudKnownAsEnt = ttk.Entry(self.StudentInformation)
        StudKnownAsEnt.grid(row = 1,sticky = "w", padx = 1155, pady = 10)

        StudKnownAs = allLabels(self.StudentInformation, "KNOWN AS: ", ("Arial", 12,"normal"))
        StudKnownAs.grid_mel(1, 0, "w", 1055, 10)

        StudID = allLabels(self.StudentInformation, "ID NO: ", ("Arial", 12,"normal"))
        StudID.grid_mel(1, 0, "w", 745, 10)

        StudIDEnt = ttk.Entry(self.StudentInformation)
        StudIDEnt.grid(row = 1, sticky = "w", padx = 800, pady = 10)

        self.FirstOrSecond = allLabels(self.StudentInformation, "IS THIS YOUR 1st OR 2nd YEAR AT STRODE'S?", ("Arial", 12, "normal"))
        self.FirstOrSecond.grid_mel(3, 0, "nw", 745, 0)

        #Radio button for is this ur first or second year at strodes
        self.FirstOrSecond = StringVar()
        FirstRad = ttk.Radiobutton(self.StudentInformation, text ="1st", variable = self.FirstOrSecond, value = "First")
        SecondRad = ttk.Radiobutton(self.StudentInformation, text = "2nd", variable = self.FirstOrSecond, value = "Second")
        self.FirstOrSecond.set("First")
        FirstRad.grid(row = 3, column = 0, sticky = "nw", padx = 1105)
        SecondRad.grid(row = 3, column = 0, sticky = "nw", padx = 1155)

        ITorComputingSub = allLabels(self.StudentInformation, "IT/COMPUTING SUBJECT (Please select one from the listbox)", ("Arial", 12,"normal"))
        ITorComputingSub.grid_mel(2, 0, "w", 20, 0)

        #List box and scroll bar
        listBoxList = ["BTEC Double", "BTEC Single", "BTEC level 2", "ICT A level", "Computing A level", "Using IT", "Java"]
        listVar = StringVar()
        self.listBoxCompSub = Listbox(self.StudentInformation, listvariable = listVar, height = 4, selectmode = SINGLE, width = 100)
        for l in listBoxList:
            self.listBoxCompSub.insert(END, l)
        self.listBoxCompSub.grid(row = 3,column = 0, sticky = "w", padx = 20)
        self.listBoxCompSub.bind('<Double-1>')
        self.listBoxCompSub.selection_set(0)
        #scrollbar = Scrollbar(orient = "vertical")
        #self.listBoxCompSub.config(yscrollcommand=scrollbar.set)
        #scrollbar.config(command = self.listBoxCompSub.yview)
        #scrollbar.grid(row = 4, column = 0,sticky = "w")

        blocksL = allLabels(self.StudentInformation, "Block (Please circle): ", ("Arial", 12,"normal"))
        blocksL.grid_mel(4, 0, "sw", 20, 0)

        #Radio Buttons for blocks
        self.Blocks = StringVar()
        A = ttk.Radiobutton(self.StudentInformation, text = "A", variable = self.Blocks, value = "A")
        B = ttk.Radiobutton(self.StudentInformation, text = "B", variable = self.Blocks, value = "B")
        C = ttk.Radiobutton(self.StudentInformation, text = "C", variable = self.Blocks, value = "C")
        D = ttk.Radiobutton(self.StudentInformation, text = "D", variable = self.Blocks, value = "D")
        E = ttk.Radiobutton(self.StudentInformation, text = "E", variable = self.Blocks, value = "E")
        F = ttk.Radiobutton(self.StudentInformation, text = "F", variable = self.Blocks, value = "F")
        G = ttk.Radiobutton(self.StudentInformation, text = "G", variable = self.Blocks, value = "G")
        H = ttk.Radiobutton(self.StudentInformation, text = "H", variable = self.Blocks, value = "H")
        self.Blocks.set("A")
        R = [A,B,C,D,E,F,G,H]
        Rx = 20
        #Generalized gridding method
        for i in range(8):
            R[i].grid(row = 5, column = 0, sticky = "w", padx = Rx, pady = 0)
            Rx += 90

        OtherSubs = allLabels(self.StudentInformation, "WHICH OTHER SUBJECTS YOU ARE STUDYING AT STRODES?", ("Arial", 12,"normal"))
        OtherSubs.grid_mel(6, 0, "sw", 20, 0)

        subjectLabel = allLabels(self.StudentInformation, "SUBJECT", ("Arial", 12, "normal"))
        subjectLabel.grid_mel(7, 0, "sw", 20, 0)
        
        levelLab = allLabels(self.StudentInformation, "LEVEL (eg A2, GCSE)", ("Arial", 12,"normal"))
        levelLab.grid_mel(7, 0, "sw", 200, 0)

        subjectLabelRight = allLabels(self.StudentInformation, "SUBJECT", ("Arial", 12, "normal"))
        subjectLabelRight.grid_mel(7, 0, "sw", 380, 0)

        levelLabRight = allLabels(self.StudentInformation, "LEVEL (eg A2, GCSE)", ("Arial", 12, "normal"))
        levelLabRight.grid_mel(7, 0, "sw", 560, 0)
        
        subjectEnt1 = ttk.Entry(self.StudentInformation)
        levelEnt1 = ttk.Entry(self.StudentInformation)
        subjectEnt2 = ttk.Entry(self.StudentInformation)
        levelEnt2 = ttk.Entry(self.StudentInformation)
        subjectEnt3 = ttk.Entry(self.StudentInformation)
        levelEnt3 = ttk.Entry(self.StudentInformation)
        subjectEnt4 = ttk.Entry(self.StudentInformation)
        levelEnt4 = ttk.Entry(self.StudentInformation)
        subjectEnt1.grid(row = 8, column = 0, sticky = "w", padx = 20, pady = 3)
        levelEnt1.grid(row = 8, column = 0, sticky = "w", padx = 200, pady = 3)
        subjectEnt2.grid(row = 9, column = 0, sticky = "nw", padx = 20, pady = 3)
        levelEnt2.grid(row = 9, column = 0, sticky = "nw", padx = 200, pady = 3)
        subjectEnt3.grid(row = 8, column = 0, sticky = "w", padx = 380, pady = 3)
        levelEnt3.grid(row = 8, column = 0, sticky = "w", padx = 560, pady = 3)
        subjectEnt4.grid(row = 9, column = 0, sticky = "nw", padx = 380, pady = 3)
        levelEnt4.grid(row = 9, column = 0, sticky = "nw", padx = 560, pady = 3)
        
        gcseSubs = allLabels(self.StudentInformation, "GCSES (Please give all your GCSE results. This will help us to advise you)", ("Arial", 12,"normal"))
        gcseSubs.grid_mel(10, 0, "w", 20, 0)
        
        subjectLabel1 = allLabels(self.StudentInformation, "SUBJECT", ("Arial", 12, "normal"))
        subjectLabel1.grid_mel(11, 0, "w", 20, 0)

        gcseLabel = allLabels(self.StudentInformation, "Grade", ("Arial", 12, "normal"))
        gcseLabel.grid_mel(11, 0, "w", 200, 0)

        subjectLabelRight1 = allLabels(self.StudentInformation, "SUBJECT", ("Arial", 12, "normal"))
        subjectLabelRight1.grid_mel(11, 0, "w", 380, 0)

        gcseLabelRight = allLabels(self.StudentInformation, "Grade", ("Arial", 12, "normal"))
        gcseLabelRight.grid_mel(11, 0, "w", 560, 0)
        
        subjectEnt5 = ttk.Entry(self.StudentInformation)
        Grade1 = ttk.Entry(self.StudentInformation)
        subjectEnt6 = ttk.Entry(self.StudentInformation)
        Grade2 = ttk.Entry(self.StudentInformation)
        subjectEnt7 = ttk.Entry(self.StudentInformation)
        Grade3 = ttk.Entry(self.StudentInformation)
        subjectEnt8 = ttk.Entry(self.StudentInformation)
        Grade4 = ttk.Entry(self.StudentInformation)
        subjectEnt5.grid(row = 12, column = 0, sticky = "w", padx = 20, pady = 3)
        Grade1.grid(row = 12, column = 0, sticky = "w", padx = 200, pady = 3)
        subjectEnt6.grid(row = 13, column = 0, sticky = "w", padx = 20, pady = 3)
        Grade2.grid(row = 13, column = 0, sticky = "w", padx = 200, pady = 3)
        subjectEnt7.grid(row = 12, column = 0, sticky = "w", padx = 380, pady = 3)
        Grade3.grid(row = 12, column = 0, sticky = "w", padx = 560, pady = 3)
        subjectEnt8.grid(row = 13, column = 0, sticky = "w", padx = 380, pady = 3)
        Grade4.grid(row = 13, column = 0, sticky = "w", padx = 560, pady = 3)
        
        ifYearTwo = allLabels(self.StudentInformation, "If you are a year 2 student, please fill in your recent AS/A2/BTEC results at Strode's.", ("Arial", 12,"normal"))
        ifYearTwo.grid_mel(15, 0, "w", 20, 10)

        blankLab = allLabels(self.StudentInformation, "",("Arial", 12, "normal"))
        blankLab.grid_mel(14, 0, "w", 20, 0)
        
        subjectLabel2 = allLabels(self.StudentInformation, "SUBJECT", ("Arial", 12, "normal"))
        subjectLabel2.grid_mel(16, 0 , "w", 20, 0)

        levelLab1 = allLabels(self.StudentInformation, "Level", ("Arial", 12, "normal"))
        levelLab1.grid_mel(16, 0, "w", 240, 0)

        gradeLabel = allLabels(self.StudentInformation, "Grade", ("Arial", 12, "normal"))
        gradeLabel.grid_mel(16, 0, "w", 460, 0)
        
        subjectEnt9 = ttk.Entry(self.StudentInformation)
        levelEnt5 = ttk.Entry(self.StudentInformation)
        Grade5 = ttk.Entry(self.StudentInformation)
        subjectEnt10 = ttk.Entry(self.StudentInformation)
        levelEnt6 = ttk.Entry(self.StudentInformation)
        Grade6 = ttk.Entry(self.StudentInformation)
        subjectEnt11 = ttk.Entry(self.StudentInformation)
        levelEnt7 = ttk.Entry(self.StudentInformation)
        Grade7 = ttk.Entry(self.StudentInformation)
        subjectEnt12 = ttk.Entry(self.StudentInformation)
        levelEnt8 = ttk.Entry(self.StudentInformation)
        Grade8 = ttk.Entry(self.StudentInformation)
        subjectEnt9.grid(row = 17, column = 0, sticky = "w", padx = 20, pady = 3)
        levelEnt5.grid(row = 17, column = 0, sticky = "w", padx = 240, pady =3)
        Grade5.grid(row = 17, column = 0, sticky = "w", padx = 460, pady = 3)
        subjectEnt10.grid(row = 18, column = 0, sticky = "w", padx = 20, pady = 3)
        levelEnt6.grid(row = 18, column = 0, sticky = "w", padx = 240, pady =3)
        Grade6.grid(row = 18, column = 0, sticky = "w", padx = 460, pady = 3)
        subjectEnt11.grid(row = 19, column = 0, sticky = "w", padx = 20, pady = 3)
        levelEnt7.grid(row = 19, column = 0, sticky = "w", padx = 240, pady =3)
        Grade7.grid(row = 19, column = 0, sticky = "w", padx = 460, pady = 3)
        subjectEnt12.grid(row = 20, column = 0, sticky = "w", padx = 20, pady = 3)
        levelEnt8.grid(row = 20, column = 0, sticky = "w", padx = 240, pady =3)
        Grade8.grid(row = 20, column = 0, sticky = "w", padx = 460, pady = 3)
        
        whyChoose = allLabels(self.StudentInformation, "Why did you choose to take this subject?", ("Arial", 12,"normal"))
        whyChoose.grid_mel(3, 0, "sw", 745, 0)
        whyChooseText = Text(self.StudentInformation, height = 2, width = 65)
        whyChooseText.grid(row = 4, column = 0, sticky = "nw", padx = 745, pady = 5)
        
        specialNeeds1 = allLabels(self.StudentInformation, "Special educational needs", ("Arial", 12,"normal"))
        specialNeeds1.grid_mel(5, 0, "sw", 745, 8)
        specialNeeds2 = allLabels(self.StudentInformation, "Please let us know if there are any factors such as dyslexia or health problems", ("Arial", 12,"normal"))
        specialNeeds3 = allLabels(self.StudentInformation, "that may affect your education or interfere with your attendace. It may help us", ("Arial", 12, "normal"))
        specialNeeds4 = allLabels(self.StudentInformation, "to help you. We will keep this information in confidence.", ("Arial", 12,"normal"))
        specialNeeds2.grid_mel(6, 0, "nw", 745, 0)
        specialNeeds3.grid_mel(7, 0, "nw", 750, 0)
        specialNeeds4.grid_mel(8, 0, "nw", 750, 0)
        specialNeedsText = Text(self.StudentInformation, height = 2, width = 65)
        specialNeedsText.grid(row = 9, column = 0, sticky = "w", padx = 745, pady = 5)

        #Options menu
        #StudentOptions = StringVar(self.StudentInformation)
        #option = OptionMenu(self.StudentInformation, StudentOptions, "stuff", "other sutff")
        #StudentOptions.set("stuff")
        self.studentDataList = [StudNameEntL, StudNameEntF, StudKnownAsEnt, StudIDEnt, self.FirstOrSecond, listVar, self.Blocks, subjectEnt1, levelEnt1, subjectEnt2, levelEnt2, subjectEnt3, levelEnt3, subjectEnt4, levelEnt4, subjectEnt5, Grade1,
        subjectEnt6, Grade2, subjectEnt7, Grade3, subjectEnt8, Grade4, subjectEnt9, levelEnt5, Grade5, subjectEnt10, levelEnt6, Grade6, subjectEnt11, levelEnt7, Grade7, subjectEnt12, levelEnt8, Grade8, whyChooseText, specialNeedsText]

        if studentLoggedIn == True:
            buttonSave = ttk.Button(self.StudentInformation, text = "Save", command = lambda:self.addCheckStudentData())
            buttonSave.grid(row = 19, column = 0, sticky = "w", padx = 700, pady = 3)
            self.warningLbl = Label(self.StudentInformation, text = "*Once save is clicked you will not be able to add any other data.", fg = "red")
            self.warningLbl.grid(row = 20, sticky = "w", padx = 745)
                        
        else:
            previousBtn = ttk.Button(self.StudentInformation, text = "Prev. Record", command = lambda:self.prevRecord())
            nextBtn = ttk.Button(self.StudentInformation, text = "Next. Record", command = lambda:self.nexRecord())
            self.recordEnt = Entry(self.StudentInformation, width = 3, justify = "center")
            previousBtn.grid(row = 15, sticky = "w", padx = 910)
            nextBtn.grid(row = 15, sticky = "w", padx = 1035)
            self.recordEnt.grid(row = 15, sticky = "w", padx = 1000)
            self.warningLbl = Label(self.StudentInformation, text = "", fg = "red")
            self.warningLbl.grid(row = 20, sticky = "w", padx = 745)
            clearbtn = ttk.Button(self.StudentInformation, text = "Clear", command = lambda:self.clearStudentDataR())
            clearbtn.grid(row = 15, sticky = "w", padx = 820)
            homebtn = ttk.Button(self.StudentInformation, text = "Home", command = lambda:self.goHome(self.StudentInformation))
            homebtn.grid(row = 15, sticky = "w", padx = 1125)
            self.searchClicked = False
            search = ttk.Button(self.StudentInformation, text = "Search", command = lambda:self.studentSearchClicked())
            search.grid(row = 16, sticky = "w", padx = 820)
            deleteStud = ttk.Button(self.StudentInformation, text = "Delete", command = lambda:self.deleteStudent())
            deleteStud.grid(row = 16, sticky = "w", padx = 910)
            updateStud = ttk.Button(self.StudentInformation, text = "Update", command = lambda:self.updateStudData())
            updateStud.grid(row = 16, sticky = "w", padx = 1035)
            buttonSave = ttk.Button(self.StudentInformation, text = "Add Record", command = lambda:self.addCheckStudentData())
            buttonSave.grid(row = 16, sticky = "w", padx = 1125)
            self.recordNumber = 0
            self.deleteClicked = False
            self.studNotFound = False
            self.ShowData()

    def addCheckStudentData(self):
        self.x = 0
        self.warningLbl.configure(text = "")
        self.addClicked = True
        self.CantAdd = False
        topfour = True
        if studentLoggedIn == True:
            messagebox.showinfo(
                message = "Please select the database to save to",
                icon = "info", title = "Select Database", detail = "Press OK to continue")
            filename = str(filedialog.askopenfilename())
            self.StudConn=sqlite3.connect(filename)
            conn=sqlite3.connect(filename)
        else:
            conn=sqlite3.connect("database.db")
        cur=conn.cursor()
        self.createTheTable()
        for i in range(0, 4):
            if self.studentDataList[i].get() != "":
                topfour = False
        for i in range(7, 35):
            if self.studentDataList[i].get() != "":
                self.CantAdd = True
        try:
            cur.execute("SELECT studID FROM studentData WHERE studID = ?", [self.studentDataList[3].get()])
            length = int(len(cur.fetchall()))

        except sqlite3.Error as e:
            print("An error occured: "+ e.args[0])

        if topfour == True and self.CantAdd == False:
            self.warningLbl.configure(text = "*Cannot add an empty student!")
        else:
            if length != 0:
                self.warningLbl.configure(text = "*This student ID is already in use!")
            else:
                self.addStudentData()
                if studentLoggedIn == False:
                    self.warningLbl.config(text = "*Student added!")

    def updateStudData(self):
        #Checks if the update is not being preformed empty
        if self.studentDataList[3].get() == "" and self.studentDataList[0].get() == "" and self.studentDataList[1].get() == "":
            self.warningLbl.configure(text = "*No student found to update")
        else:
            studentDataTuple = []
            self.warningLbl.configure(text = "")
            conn=sqlite3.connect("database.db")
            cur=conn.cursor()
            for i in range(0, 3):
                studentDataTuple.append(self.studentDataList[i].get())
            studentDataTuple.append(self.studentDataList[4].get())
            studentDataTuple.append(self.listBoxCompSub.get(ACTIVE))
            for i in range(6, 35):
                studentDataTuple.append(self.studentDataList[i].get())
            studentDataTuple.append(self.studentDataList[35].get("1.0", END))
            studentDataTuple.append(self.studentDataList[36].get("1.0", END))
            studentDataTuple = tuple(studentDataTuple)
            #Checkes if the there is a change in the primary key
            #If the changed primary key is already being used the user is notified
            try:
                cur.execute("SELECT studID FROM studentData WHERE studID = "+"'"+self.studentDataList[3].get()+"'")
                student = cur.fetchall()
            except sqlite3.Error as e: 
                    print("An error occured: "+ e.args[0])
                    self.warningLbl.config(text = "*Error")
            print(str(student))
            print("[]")
            if str(student) != "[]":
                try:
                #Even if there is a change in the primary key or not the table is updated to avoid changed lost from other fields
                    SQL = ("UPDATE studentData SET studnameL=?, studNameF=?, studKnownAs=?, year=?, subject=?, block=?, otherSubs1=?, otherSubLVL1=?, otherSubs2=?, otherSubLVL2=?, otherSubs3=?, otherSubLVL3=?, otherSubs4=?, otherSubLVL4=?, GCSESub1=?, GCSEgrade1=?, GCSESub2=?, GCSEgrade2=?, GCSESub3=?, GCSEgrade3=?, GCSESub4=?, GCSEgrade4=?, year2Sub1=?, year2LVL1=?, year2grade1=?, year2Sub2=?, year2LVL2=?, year2grade2=?, year2Sub3=?, year2LVL3=?, year2grade3=?, year2Sub4=?, year2LVL4=?, year2grade4=?, whyChoose=?, specialNeeds=? WHERE studID = "+"'"+self.studentDataList[3].get()+"'")
                    cur.execute(SQL, studentDataTuple)
                    conn.commit()
                    self.warningLbl.configure(text = "*Update successful")
                except sqlite3.Error as e: 
                    print("An error occured: "+ e.args[0])

            else:
                self.warningLbl.config(text = "*ID not found to update student data")

                       

    def deleteStudent(self):
        self.warningLbl.configure(text = "")
        conn=sqlite3.connect("database.db")
        cur=conn.cursor()
        if self.studentDataList[3].get() == "" and self.studentDataList[0].get() == "" and self.studentDataList[1].get() == "":
            self.warningLbl.configure(text = "Firstname, Lastname and StudentID needed to delete a student")
        else:
            self.deleteClicked = True
            try:
                cur.execute("DELETE FROM studentData WHERE studNameL = "+"'"+self.studentDataList[0].get()+"'"+" AND studNameF = "+"'"+self.studentDataList[1].get()+"'"+" AND studID = "+"'"+self.studentDataList[3].get()+"'")
                self.warningLbl.configure(text = "*Student deleted")
                self.clearStudentDataR()
                self.ShowData()
                conn.commit()
            except sqlite3.Error as e: 
                print("An error occured: "+ e.args[0])
                self.warningLbl.configure(text = "*Student not deleted, please enter Firstname, Lastname and StudentID correctly")
            
                   
    def studentSearchClicked(self):
        self.x = 0
        self.warningLbl.configure(text = "")
        self.searchClicked = True
        self.NotASearch = False
        for i in range(7, 35):
            if self.studentDataList[i].get() != "":
                self.NotASearch = True
                print("Searching with a full database")
        if self.NotASearch == True:
            self.searchClicked = False
            self.warningLbl.configure(text = "*Please click clear, then enter the Firstname, Lastname or StudentID of the student")
        else:
            if self.studNotFound == True:
                self.ShowData()
            else:
                self.recordNumber +=1
                self.ShowData()

    def choosingSearchPart2(self):
        conn=sqlite3.connect("database.db")
        cur=conn.cursor()
        if self.searchPart1 == True and self.searchPart2 == True:
            print("this search not valid")
        elif self.searchPart3 == True:
            cur.execute("SELECT * FROM studentData WHERE studID =?", (self.studentDataList[3].get(),))

        if self.searchPart4 == True and self.searchPart5 == True:
            cur.execute("SELECT * FROM studentData WHERE studNameL =?", (self.studentDataList[0].get(),))
        elif self.searchPart6 == True:
            cur.execute("SELECT * FROM studentData WHERE studID = "+"'"+self.studentDataList[3].get()+"'"+"AND studNameL = "+"'"+self.studentDataList[0].get()+"'")

        if self.searchPart7 == True and self.searchPart8 == True:
            cur.execute("SELECT * FROM studentData WHERE studNameF =?", (self.studentDataList[1].get(),))
        elif self.searchPart9 == True:
            cur.execute("SELECT * FROM studentData WHERE studID = "+"'"+self.studentDataList[3].get()+"'"+"AND studNameF = "+"'"+self.studentDataList[1].get()+"'")

        if self.searchPart10 == True and self.searchPart11 == True:
            cur.execute("SELECT * FROM studentData WHERE studNameF = "+"'"+self.studentDataList[1].get()+"'"+"AND studNameL = "+"'"+self.studentDataList[0].get()+"'")
        elif self.searchPart12 == True:
            cur.execute("SELECT * FROM studentData WHERE studNameF = "+"'"+self.studentDataList[1].get()+"'"+"AND studNameL = "+"'"+self.studentDataList[0].get()+"'"+"AND studID = "+"'"+self.studentDataList[3].get()+"'")
        return cur
            
    def choosingSearch(self):
        x = 0
        y = 0
        self.searchPart1 = False
        self.searchPart2 = False
        self.searchPart3 = False
        self.searchPart4 = False
        self.searchPart5 = False
        self.searchPart6 = False
        self.searchPart7 = False
        self.searchPart8 = False
        self.searchPart9 = False
        self.searchPart10 = False
        self.searchPart11 = False
        self.searchPart12 = False
        conn=sqlite3.connect("database.db")
        cur=conn.cursor()
        if self.studentDataList[0].get() != "":
            x = x+1
        if self.studentDataList[1].get() != "":
            y = y+1


        if x == 0 and y == 0:
            self.searchPart1 = True
            print("search not with lastname or firstname")
            if self.studentDataList[3].get() == "":
                print("search not valid")
                self.searchPart2 = True
            else:
                cur.execute("SELECT * FROM studentData WHERE studID =?", (self.studentDataList[3].get(),))
                self.searchPart3 = True

                
        elif x == 1 and y== 0:
            self.searchPart4 = True
            if self.studentDataList[3].get() == "":
                self.searchPart5 = True
                print("search with lastname only")
                cur.execute("SELECT * FROM studentData WHERE studNameL =?", (self.studentDataList[0].get(),))

            else:
                self.searchPart6 = True
                print("search with studentId and lastname")
                cur.execute("SELECT * FROM studentData WHERE studID = "+"'"+self.studentDataList[3].get()+"'"+"AND studNameL = "+"'"+self.studentDataList[0].get()+"'")



        elif y == 1 and x == 0:
            self.searchPart7 = True
            if self.studentDataList[3].get() == "":
                self.searchPart8 = True
                print("search with firstname only")

                cur.execute("SELECT * FROM studentData WHERE studNameF =?", (self.studentDataList[1].get(),))

            else:
                self.searchPart9 = True
                print("search with studentId and first name")
                cur.execute("SELECT * FROM studentData WHERE studID = "+"'"+self.studentDataList[3].get()+"'"+"AND studNameF = "+"'"+self.studentDataList[1].get()+"'")



        elif y == 1 and x == 1:
            self.searchPart10 = True
            if self.studentDataList[3].get() == "":
                self.searchPart11 = True
                print("search with firstname and lastname only")
                cur.execute("SELECT * FROM studentData WHERE studNameF = "+"'"+self.studentDataList[1].get()+"'"+"AND studNameL = "+"'"+self.studentDataList[0].get()+"'")
            else:
                self.searchPart12 = True
                print("Search with all 3")
                cur.execute("SELECT * FROM studentData WHERE studNameF = "+"'"+self.studentDataList[1].get()+"'"+"AND studNameL = "+"'"+self.studentDataList[0].get()+"'"+"AND studID = "+"'"+self.studentDataList[3].get()+"'")
        return cur

    def prevRecord(self):
        conn=sqlite3.connect("database.db")
        cur=conn.cursor()
        self.warningLbl.configure(text = "")
        if self.searchClicked == True:
            if self.x > 0:
                allStudents = self.choosingSearchPart2().fetchall()
            else:
                allStudents = self.choosingSearch().fetchall()
            self.x +=1
        else:
            try:
                cur.execute("SELECT * FROM studentData")
                allStudents = cur.fetchall()
            except sqlite3.Error as e:
                self.warningLbl.configure(text = "*No data found")
        if self.recordNumber - 1 >= 0:
            self.recordNumber-=1
            self.ShowData()

        else:
            if self.recordNumber == -1:
                self.warningLbl.configure(text = "*Click 'Next. Record' to view the first record")
            else:
                print("There are no previous records")
                self.warningLbl.configure(text = "*This is the First record")

                

    def nexRecord(self):
        conn=sqlite3.connect("database.db")
        cur=conn.cursor()
        print(self.recordNumber)
        self.warningLbl.configure(text = "")
        if self.searchClicked == True:
            if self.x > 0:
                allStudents = self.choosingSearchPart2().fetchall()
            else:
                allStudents = self.choosingSearch().fetchall()
            self.x +=1
        else:
            try:
                cur.execute("SELECT * FROM studentData")
                allStudents = cur.fetchall()
                print("record number: ", self.recordNumber+1)

            except sqlite3.Error as e:
                self.warningLbl.configure(text = "*No data found")
        if self.recordNumber + 1 < len(allStudents):
            self.recordNumber+=1
            self.ShowData()
        else:
            self.warningLbl.configure(text = "*This is the Last record")
            
        
       

            
            
    def ShowData(self):
        conn=sqlite3.connect("database.db")
        cur=conn.cursor()
        this = False
        self.recordEnt.delete(0, END)
        if self.deleteClicked == True and (self.recordNumber - 1) == 0:
            this = True
            self.recordEnt.insert(END, self.recordNumber-1)
        else:
            self.recordEnt.insert(END, self.recordNumber)
        if self.searchClicked == True:
            if self.x > 0:
                allStudents = self.choosingSearchPart2().fetchall()
            else:
                allStudents = self.choosingSearch().fetchall()
            self.x +=1
        else:
            try:
                cur.execute("SELECT * FROM studentData")
                allStudents = cur.fetchall()
            except sqlite3.Error as e:
                self.warningLbl.configure(text = "*No data found")
        try:
            print("Length of the list", (len(allStudents)))
            CurrentStudentData = allStudents[self.recordNumber]
            print(CurrentStudentData)
            self.clearStudentData()
            
            for i in range(0, 4):
                self.studentDataList[i].insert(END, CurrentStudentData[i])
            self.FirstOrSecond.set(str(CurrentStudentData[4]))
            self.listBoxCompSub.selection_clear(0, 7)

            if CurrentStudentData[5] == "BTEC Double":
                self.listBoxCompSub.selection_set(0)

            elif CurrentStudentData[5] == "BTEC Single":
                self.listBoxCompSub.selection_set(1)

            elif CurrentStudentData[5] == "BTEC level 2":
                self.listBoxCompSub.selection_set(2)

            elif CurrentStudentData[5] == "ICT A level":
                self.listBoxCompSub.selection_set(3)

            elif CurrentStudentData[5] == "Computing A level":
                self.listBoxCompSub.selection_set(4)

            elif CurrentStudentData[5] == "Using IT":
                self.listBoxCompSub.selection_set(5)

            else:
                self.listBoxCompSub.selection_set(6)

            self.Blocks.set(str(CurrentStudentData[6]))
            for i in range(7, 35):
                self.studentDataList[i].insert(END, CurrentStudentData[i])
            self.studentDataList[35].insert("1.0", CurrentStudentData[35])
            self.studentDataList[36].insert("1.0", CurrentStudentData[36])
            print(self.recordNumber)
            if this == True:
                self.recordNumber -=1
                this = False
            self.deleteClicked = False
        except:
            if self.searchClicked == True:
                self.studNotFound = True
                self.warningLbl.configure(text = "*Student not found")
            else:
                self.warningLbl.configure(text = "*No records to display")
    def clearStudentDataR(self):
        self.searchClicked = False
        if self.deleteClicked == False:
            self.recordNumber = -1
        else:
            if int(self.recordEnt.get()) > 0:
                self.recordNumber = self.recordNumber - 1
            else:
                self.recordNumber = 1
        if self.deleteClicked == False:
            self.recordEnt.delete(0, END)
            self.recordEnt.insert(END, self.recordNumber+1)
        self.clearStudentData()
        print(self.recordNumber)

    #To clear the data on the studentdata information frame
    def clearStudentData(self):
        self.studNotFound = False
        for i in range(0, 4):
            self.studentDataList[i].delete(0, END)
        self.studentDataList[4].set("First")
        self.listBoxCompSub.selection_clear(0, 7)
        self.listBoxCompSub.selection_set(0)
        self.studentDataList[6].set("A")
        for i in range(7, 35):
            self.studentDataList[i].delete(0, END)
        self.studentDataList[35].delete("1.0", END)
        self.studentDataList[36].delete("1.0", END)
        print(self.recordNumber)
        
    #Adding the student data to the database while creating the database simultaneously
    def addStudentData(self):
        if studentLoggedIn == True:
            conn=self.StudConn
        else:
            conn=sqlite3.connect("database.db")
        cur=conn.cursor()
        #Putting all the values into another list so it can be made into a tuple
        studentDataTuple = []
        for i in range(0, 5):
            studentDataTuple.append(self.studentDataList[i].get())
        studentDataTuple.append(self.listBoxCompSub.get(ACTIVE))
        for i in range(6, 35):
            studentDataTuple.append(self.studentDataList[i].get())
        studentDataTuple.append(self.studentDataList[35].get("1.0", END))
        studentDataTuple.append(self.studentDataList[36].get("1.0", END))

        studentDataTuple = tuple(studentDataTuple)

        SQL = "INSERT INTO studentData(studnameL, studNameF, studKnownAs, studID, year, subject, block, otherSubs1, otherSubLVL1, otherSubs2, otherSubLVL2, otherSubs3, otherSubLVL3, otherSubs4, otherSubLVL4, GCSESub1, GCSEgrade1, GCSESub2, GCSEgrade2, GCSESub3, GCSEgrade3, GCSESub4, GCSEgrade4, year2Sub1, year2LVL1, year2grade1, year2Sub2, year2LVL2, year2grade2, year2Sub3, year2LVL3, year2grade3, year2Sub4, year2LVL4, year2grade4, whyChoose, specialNeeds) "
        SQL = SQL + "VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
        try:
            cur.execute(SQL, studentDataTuple)
            conn.commit()

        except sqlite3.Error as e:
            print("An error occured: "+ e.args[0])
        if studentLoggedIn == True:
            root.destroy()
            file = open("CannotUseAgain.txt", "w")
            file.close()



    def createTheTable(self):
        if studentLoggedIn == True:
            conn = self.StudConn
        else:
            conn=sqlite3.connect("database.db")
        cur=conn.cursor()
        try:
           cur.execute("""CREATE TABLE if not exists studentData(
               studNameL VARCHAR (30),
               studNameF VARCHAR(30),
               studKnownAs VARCHAR (15),
               studID CHAR (8) PRIMARY KEY,
               year VARCHAR(10),
               subject VARCHAR(20),
               block CHAR(1),
               otherSubs1 VARCHAR(30),
               otherSubLVL1 VARCHAR(30),
               otherSubs2 VARCHAR(30),
               otherSubLVL2 VARCHAR(30),
               otherSubs3 VARCHAR(30),
               otherSubLVL3 VARCHAR(30),
               otherSubs4 VARCHAR(30),
               otherSubLVL4 VARCHAR(30),
               GCSESub1 VARCHAR(30),
               GCSEgrade1 VARCHAR(3),
               GCSESub2 VARCHAR(30),
               GCSEgrade2 VARCHAR(3),
               GCSESub3 VARCHAR(30),
               GCSEgrade3 VARCHAR(3),
               GCSESub4 VARCHAR(30),
               GCSEgrade4 VARCHAR(3),
               year2Sub1 VARCHAR(30),
               year2LVL1 VARCHAR(30),
               year2grade1 VARCHAR(30),
               year2Sub2 VARCHAR(30),
               year2LVL2 VARCHAR(30),
               year2grade2 VARCHAR(30),
               year2Sub3 VARCHAR(30),
               year2LVL3 VARCHAR(30),
               year2grade3 VARCHAR(30),
               year2Sub4 VARCHAR(30),
               year2LVL4 VARCHAR(30),
               year2grade4 VARCHAR(30),
               whyChoose CHAR(200),
               specialNeeds CHAR(200)
                )""")
        except sqlite3.Error as e:
            print("An error occurred: " + e.args[0])
        
            
        
       
#class for all buttons
class allButtons():
    def __init__(self, frme,txt):
        self.__button = ttk.Button(frme, text = txt)
        
    def grid_meb(self):
        self.__button.grid()

    def bind_meb(self,event,func):
        self.__button.bind(event,func)

    def get_button(self):
        return self.__button

#Class for all labels
class allLabels():
    def __init__(self, frme,txt, fnt):
        self.__label = ttk.Label(frme, text = txt, font = fnt)

    def grid_mel(self, ro, col, stik, pax, pay):
        self.__label.grid(row = ro, column = col, sticky = stik, padx = pax, pady = pay)


    def get_label(self):
        return self.__label


root = Tk()
root.title("Book Loan System and Database")
root.wm_iconbitmap("favicon.ico")
root.config(cursor = "@cursor.cur")
Setup = SetupAndLogin(root)
root.mainloop() 


