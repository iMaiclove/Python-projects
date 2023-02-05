from tkinter import *
import sqlite3 # sqlite3 to connect to the database
import os #for operating system related task
import datetime #to right the adte and time in the datadase
import re # re for checking regular expressions
from random import randint #to make random wallet numbers
import pandas as pd # pandas for saving files to csv

# If database is not present create a db
if not os.path.isfile('database.db'):
    db = sqlite3.connect('database.db') # create a connection between the program and the database
    # create user table
    db.cursor().execute('''
    CREATE TABLE IF NOT EXISTS users 
    (student_id INTEGER(10) UNIQUE, 
    first_name varchar(32),
    last_name varchar(32),
    password varchar(32),
    email varchar(32) UNIQUE,
    phone_number INTEGER(10) UNIQUE,
    wallet_number INTEGER(10),
    account_created timestamp,
    wallet_type varchar(32),
    balance FLOAT,
    is_admin INTEGER(1) DEFAULT 0
    )
    ''')

    ### Create Admin User
    #time = datetime.datetime.now()
    student_id = 1111111111
    first_name = 'admin'
    last_name = 'user'
    password = 'admin@123'
    email = 'admin@ksu.edu.sa'
    phone_number = "0523456789"
    wallet_number = '1234567890'
    time = datetime.datetime.now()
    is_admin = 1
    # insert into db admin
    db.cursor().execute(
        """INSERT INTO users VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
         (student_id, first_name,last_name,password,email,phone_number, wallet_number, time, 'ksu',0,is_admin ))

    # commit to db
    db.commit()

    # create a transactions table
    db.cursor().execute('''
    CREATE TABLE IF NOT EXISTS transactions 
    (
    wallet_number INTEGER(10),
    sender INTEGER(10),
    reciever INTEGER(10),
    type varchar(32),
    amount FLOAT,
    transaction_time timestamp
    )
    ''')
else:
    # if database is already created connect to db.
    db = sqlite3.connect('database.db')
###########################################################

def finish_Signup():
    # variables
    first_name = temp_first_name.get()
    last_name = temp_last_name.get()
    student_id = temp_student_id.get()
    password = temp_password.get()
    email = temp_email.get()
    phone_number = temp_phone_number.get()

    # validate all fields are not empty
    if first_name.strip() == "" or last_name.strip() == "" or email.strip() == "" or phone_number.strip() == "" or student_id.strip() == "" or password.strip() == "":
        notify.config(fg="red", text="All fields requried * ")
        return
    # notify is student is is not 10 digit number
    if not len(student_id) == 10:
        notify.config(fg="red", text="Please enter a valid 10 digit number for student id")
        return

    # validate first name contains all alphabetic characters
    if not first_name.isalpha():
        notify.config(fg="red", text="Please enter a valid first name for student")
        return

    # validate last name contains all alphabetic characters
    if not last_name.isalpha():
        notify.config(fg="red", text="Please enter a valid last name for student")
        return

    # validate password length is not less than 6
    if len(password) < 6:
        notify.config(fg="red", text="Password length must be at least 6")
        return
    # validate email is email contains @ and ends with ksu.edu.sa
    if "@" in email and not email.split('@')[1] == "ksu.edu.sa":
        notify.config(fg="red", text="Please enter a valid email address")
        return

    # validate phone number that it is 10 digit and starts with 05
    if not phone_number.startswith('05'):
        notify.config(fg="red", text="Please enter a valid phone number")
        return

    if not len(phone_number) == 10:
        notify.config(fg="red", text="Please enter a valid phone number")
        return

    # Generate wallet_number
    while True:
        wallet_number = randint(1000000000, 9999999999)
        # Get all wallet_numbers
        wallet_numbers = list(map(lambda x: x[0], db.cursor().execute("SELECT wallet_number FROM users").fetchall()))
        # See if wallet_numbers is not present in db
        if wallet_number not in wallet_numbers:
            break
    # insert values into db if everything is correct
    try:
        timing = datetime.datetime.now()  # get time
        db.cursor().execute(
            """INSERT INTO users VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
            (student_id, first_name, last_name, password, email, phone_number, wallet_number, timing, 'student', 1000,0))
        db.commit()
        notify.config(fg="Green", text=f"Account Created.\nThis is your wallet number : {wallet_number}")
        return
    except Exception as e:
        # Give error if something went wrong.
        notify.config(fg="Red", text=f"{str(e)} \n it's already exists")
        return


# destroy the Sign up window
def back_Signup():
    global Signup_screen
    Signup_screen.destroy()


# Sign up screen
def Signup():
    # Variables
    global temp_first_name
    global temp_last_name
    global temp_student_id
    global temp_password
    global temp_email
    global temp_phone_number
    global notify
    global Signup_screen
    temp_first_name = StringVar()
    temp_last_name = StringVar()
    temp_student_id = StringVar()
    temp_password = StringVar()
    temp_email = StringVar()
    temp_phone_number = StringVar()

    # Signup Screen
    Signup_screen = Toplevel(master)
    Signup_screen.title('Sign up')            #file='(image path)'
    Signup_screen.iconphoto(False, PhotoImage(file='KSUpay logo.png'))


    # Labels
    Label(Signup_screen, text="Please enter your details below to Sign up", font=('Calibri', 12)).grid(row=0, sticky=N, pady=10)
    Label(Signup_screen, text="First Name", font=('Calibri', 12)).grid(row=1, sticky=W)
    Label(Signup_screen, text="Last Name", font=('Calibri', 12)).grid(row=2, sticky=W)
    Label(Signup_screen, text="Student ID", font=('Calibri', 12)).grid(row=3, sticky=W)
    Label(Signup_screen, text="Password", font=('Calibri', 12)).grid(row=4, sticky=W)
    Label(Signup_screen, text="Email Address", font=('Calibri', 12)).grid(row=5, sticky=W)
    Label(Signup_screen, text="Phone Number", font=('Calibri', 12)).grid(row=6, sticky=W)

    # notify label
    notify = Label(Signup_screen, font=('Calibri', 12,))
    notify.grid(row=9, sticky=N, pady=10)

    # Entry to enter text
    Entry(Signup_screen, textvariable=temp_first_name).grid(row=1, column=0, padx=150)
    Entry(Signup_screen, textvariable=temp_last_name).grid(row=2, column=0, padx=150)
    Entry(Signup_screen, textvariable=temp_student_id).grid(row=3, column=0, padx=150)
    Entry(Signup_screen, textvariable=temp_password, show="*").grid(row=4, column=0, padx=150)
    Entry(Signup_screen, textvariable=temp_email).grid(row=5, column=0, padx=150)
    Entry(Signup_screen, textvariable=temp_phone_number).grid(row=6, column=0, padx=150)

    # Buttons
    Button(Signup_screen, text="Sign up", command=finish_Signup, font=('Calibri', 12)).grid(row=7, sticky=N, pady=10)
    Button(Signup_screen, text="Back", command=back_Signup, font=('Calibri', 12)).grid(row=8, sticky=N, pady=10)


# Destroy student screen when back button is clicked.
def back_student():
    global student_screen
    student_screen.destroy()


# Destroy send money when back button is clicked.
def back_send_money():
    global send_money_screen
    send_money_screen.destroy()


# Transfer money
def transfer_money():
    # variables
    global notify_money_screen
    global user_id
    global student_screen
    student_screen.destroy()
    reciever = temp_reciever_wallet_number.get()
    amount = temp_amount.get()

    # validate that fields are not empty.
    if reciever.strip() == "" or amount.strip() == "":
        notify_money_screen.config(fg="red", text="All fields required * ")
        return

    # see if reciever wallet_number is already exist and have 10 digits number.
    if re.search("^[0-9]{10}$", reciever):
        reciever = int(reciever)
        recievers = list(map(lambda x: x[0], db.execute('select wallet_number from users').fetchall()))
        if not (reciever in recievers):
            notify_money_screen.config(fg="red", text="Account Does not exists")
            return
    else:
        notify_money_screen.config(fg="red", text="Account Does not exists")
        return

    # validate if sender and receiver are not the same.
    if user_id == reciever:
        notify_money_screen.config(fg="red", text="Money cannot be send to own account")
        return

        # get exists balance for sender
    db_amount = db.execute(f'select balance from users where wallet_number={user_id}').fetchall()
    db_amount = db_amount[0][0]
    amount = float(amount)

    # check if enough amount is available to send.
    if db_amount < amount:
        notify_money_screen.config(fg="red", text="There is not enough money")
        return
    else:
        # update database.
        db.cursor().execute(f"UPDATE users SET balance={db_amount - amount} WHERE wallet_number={user_id}")
        reciever_balance = db.execute(f'select balance from users where wallet_number={reciever}').fetchall()
        reciever_balance = reciever_balance[0][0]
        db.cursor().execute(f"UPDATE users SET balance={reciever_balance + amount} WHERE wallet_number={reciever}")
        time = datetime.datetime.now()
        db.cursor().execute("""INSERT INTO transactions values (?,?,?,?,?,?)""",
                            (user_id, user_id, reciever, "outgoing", amount, time))
        db.cursor().execute("""INSERT INTO transactions values (?,?,?,?,?,?)""",
                            (reciever, user_id, reciever, "incoming", amount, time))
        db.commit()
        notify_money_screen.config(fg="green", text=f"{amount} transfer successful to {reciever}")
        return


# send money screen
def send_money():
    # Variables
    global temp_reciever_wallet_number
    global notify_money_screen
    global temp_amount
    global send_money_screen
    global master
    temp_reciever_wallet_number = StringVar()
    temp_amount = StringVar()

    # Screen
    send_money_screen = Toplevel(master)          #file='(image path)'
    send_money_screen.iconphoto(False, PhotoImage(file='KSUpay logo.png'))

    # Labels
    Label(send_money_screen, text="Please enter your details below to send money", font=('Calibri', 12)).grid(row=0, sticky=N,pady=10)
    Label(send_money_screen, text="Wallet Number", font=('Calibri', 12)).grid(row=1, sticky=W)
    Label(send_money_screen, text="Amount", font=('Calibri', 12)).grid(row=2, sticky=W)

    # notify label
    notify_money_screen = Label(send_money_screen, font=('Calibri', 12))
    notify_money_screen.grid(row=9, sticky=N, pady=10)

    # Entry to enter text
    Entry(send_money_screen, textvariable=temp_reciever_wallet_number).grid(row=1, column=0, padx=150)
    Entry(send_money_screen, textvariable=temp_amount).grid(row=2, column=0, padx=150)

    # Button
    Button(send_money_screen, text="Send", command=transfer_money, font=('Calibri', 12)).grid(row=7, sticky=N, pady=10)
    Button(send_money_screen, text="Back", command=back_send_money, font=('Calibri', 12)).grid(row=8, sticky=N, pady=10)


# Login
def login_finish():
    # variables
    global db
    global login_screen
    global notify_login
    global notify_student_login
    global student_screen
    global admin_screen
    global user_id
    global student_id
    student_id = temp_student_id.get()
    password = temp_password.get()

    # validate that all fields are enterd.
    if student_id.strip() == "" or password.strip() == "":
        notify_login.config(fg="red", text="All fields requried * ")
        return

    # validate that if wallet number is present in db
    if re.search("^[0-9]{10}$", student_id):
        student_id = int(student_id)
        student_ids = db.execute('select student_id from users').fetchall()
        student_ids = list(map(lambda x: x[0], student_ids))
        if not (student_id in student_ids):
            notify_login.config(fg="red", text="Please Enter a valid student id")
            return
    else:
        notify_login.config(fg="red", text="Please Enter a valid student id")
        return

    user_id = db.execute(f'select wallet_number from users where student_id={student_id}').fetchall()
    user_id = user_id[0][0]
    # get current password from db
    db_password = db.execute(f'select password from users where wallet_number={user_id}').fetchall()
    db_password = db_password[0][0]

    # check if password matches
    if password == db_password:
        # get admin wallet_number
        admin_user = db.execute(f'select wallet_number from users where is_admin={1}').fetchall()
        admin_user = admin_user[0][0]
        login_screen.destroy()

        # check if the  user is admin.
        if admin_user == user_id:
            # admin screen
            admin_screen = Toplevel(master)
            admin_screen.title('Admin Screen')     #file='(image path)'
            admin_screen.iconphoto(False,PhotoImage(file='KSUpay logo.png'))

            # variables
            global notify_admin_screen
            global temp_ksu_entity
            temp_ksu_entity = StringVar()

            ## Labels
            Label(admin_screen, text="Welcome to the admin dashboard", font=('Calibri', 12)).grid(row=0, sticky=W)
            Label(admin_screen, text="Entity", font=('Calibri', 12)).grid(row=1, pady=10, sticky=W)

            ## Entry
            Entry(admin_screen, textvariable=temp_ksu_entity).grid(row=1, column=0, padx=50, sticky=W)
            notify_admin_screen = Label(admin_screen, font=('Calibri', 12))
            notify_admin_screen.grid(row=7, sticky=N, pady=10)

            ## Buttons
            Button(admin_screen, text="Submit", command=admin_submit, font=('Calibri', 12)).grid(row=2, sticky=N,pady=10, )
            Button(admin_screen, text="Pay Stipend", command=admin_pay_stipend, font=('CalibCalibri', 12)).grid(row=3,sticky=N,pady=10)
            Button(admin_screen, text="Cash out", command=admin_cashout, font=('CalibCalibri', 12)).grid(row=4,sticky=N,pady=10 )
            Button(admin_screen, text="Back up Data", command=admin_backup, font=('CalibCalibri', 12)).grid(row=5,sticky=N,pady=10)
            Button(admin_screen, text="Back", command=admin_back, font=('CalibCalibri', 12)).grid(row=6, sticky=N,pady=10 )
        else:
            # Student Screen.
            student_screen = Toplevel(master)
            student_screen.title('Student Screen')    #file='(image path)'
            student_screen.iconphoto(False,PhotoImage(file='KSUpay logo.png'))

            # Labels
            Label(student_screen, text=f"Wallet Number : {user_id}", font=('Calibri', 12)).grid(row=1, sticky=W)
            current_balance = db.execute(f'select balance from users where wallet_number={user_id}').fetchall()
            current_balance = current_balance[0][0]
            Label(student_screen, text=f"Current Balance : {current_balance}", font=('Calibri', 12)).grid(row=2,sticky=W)
            notify_student_login = Label(student_screen, font=('Calibri', 12))
            notify_student_login.grid(row=6, sticky=N, pady=10)

            # Button
            Button(student_screen, text="Send Money", command=send_money, font=('Calibri', 12)).grid(row=3, sticky=N,pady=10)
            Button(student_screen, text="Save Transactions", command=transactions, font=('Calibri', 12)).grid(row=4,sticky=N,pady=10)
            Button(student_screen, text="Back", command=back_student, font=('Calibri', 12)).grid(row=5, sticky=N,pady=10)
    else:
        notify_login.config(fg="red", text="Incorrect Password")
        return


# Takes back of database.
def admin_backup():
    global db
    global notify_admin_screen
    # save users table
    db_df = pd.read_sql_query("SELECT * FROM users", db)
    db_df.to_csv('users.csv', index=False)
    # save transactions table
    db_df = pd.read_sql_query("SELECT * FROM transactions", db)
    db_df.to_csv('transactions.csv', index=False)
    # notify message.
    notify_admin_screen.config(fg="green", text="Backup Successful!!!")
    return



#  Save Transactions logs
def transactions():
    global user_id
    global notify_student_login
    db_df = pd.read_sql_query(f"select * from transactions where wallet_number={user_id} ORDER BY transaction_time", db)
    db_df.to_csv(f'{user_id}_transactions.csv', index=False)
    notify_student_login.config(fg="green", text=f"Transactions saved\n successfully in \n{user_id}_transactions.csv")


# Destroy admin_screen when back button is clicked.
def admin_back():
    global admin_screen
    admin_screen.destroy()


# Admin Cashout
def admin_cashout():
    # variables
    global notify_admin_screen
    global db
    wallet_numbers = db.cursor().execute("SELECT wallet_number FROM users WHERE wallet_type='ksu'").fetchall()
    wallet_numbers = list(map(lambda x: x[0], wallet_numbers))
    time = datetime.datetime.now()
    # update db
    for number in wallet_numbers:
        current_balance = db.cursor().execute(f"SELECT balance FROM users WHERE wallet_number={number}").fetchall()
        current_balance = current_balance[0][0]
        db.cursor().execute("""INSERT INTO transactions values (?,?,?,?,?,?)""",
                            (number, 1234567890, number, "outgoing", current_balance, time))

    db.cursor().execute(f"UPDATE users SET balance={0} WHERE wallet_type='ksu'")
    db.commit()
    notify_admin_screen.config(fg="green", text="Cashed out\nSuccessfully!!!")
    return


# Student Stipend
def admin_pay_stipend():
    global notify_admin_screen
    # Increment all balance by 1000
    db.cursor().execute(f"UPDATE users SET balance=balance+1000 WHERE wallet_type='student'")
    time = datetime.datetime.now()
    wallet_numbers = db.cursor().execute("SELECT wallet_number FROM users WHERE wallet_type='student'").fetchall()
    wallet_numbers = list(map(lambda x: x[0], wallet_numbers))
    # Update transactions table
    for number in wallet_numbers:
        db.cursor().execute("""INSERT INTO transactions values (?,?,?,?,?,?)""",
                            (1234567890, 1234567890, number, "outgoing", 1000, time))
        db.cursor().execute("""INSERT INTO transactions values (?,?,?,?,?,?)""",
                            (number, 1234567890, number, "incoming", 1000, time))
    db.commit()
    notify_admin_screen.config(fg="green", text="Stipend Sent\nSuccessfully!!!")
    return


# Admin submit button
def admin_submit():
    # variables
    global temp_ksu_entity
    global notify_admin_screen
    global db
    entities = ['bookstore', 'housing', 'restaurant', ]
    ksu_entity = temp_ksu_entity.get()

    # validate entities
    if ksu_entity.strip() == '':
        notify_admin_screen.config(fg="red", text="Entity cannot be empty")
        return

    if ksu_entity not in entities:
        notify_admin_screen.config(fg="red", text="Entity not found\nEntity must be housing, bookstore or restaurant")
        return

    # Check if account exists.
    all_names = db.cursor().execute(f"SELECT first_name FROM users where wallet_type='ksu'")
    all_names = list(map(lambda x: x[0], all_names))
    if ksu_entity in all_names:
        notify_admin_screen.config(fg="red", text=f"{ksu_entity.title()} Account exists")
        return

    # Generate random wallet number
    while True:
        wallet_number = randint(1000000000, 9999999999)
        wallet_numbers = db.cursor().execute("SELECT wallet_number FROM users").fetchall()
        wallet_numbers = list(map(lambda x: x[0], wallet_numbers))
        if wallet_number not in wallet_numbers:
            break

    # INSERT into db
    phone_numberRE = "0500000000"
    phone_numberHU = "0500000001"
    phone_numberBS = "0500000002"
    email_RE = "restaurant@ksu.edu.sa"
    email_HU = "housing@ksu.edu.sa"
    email_BS = "bookstore@ksu.edu.sa"

    #for x in range(3):
    if ksu_entity =="bookstore":
            phone_number=phone_numberBS
            email=email_BS
    if ksu_entity == "housing":
            phone_number = phone_numberHU
            email = email_HU
    if ksu_entity == "restaurant":
            phone_number = phone_numberRE
            email = email_RE

    time = datetime.datetime.now()
    db.cursor().execute(
         """INSERT INTO users VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
         (wallet_number, ksu_entity, '', '', email, phone_number, wallet_number, time, 'ksu', 0, 0))
    db.commit()
    notify_admin_screen.config(fg="green",text=f"Account Created for {ksu_entity}.\nThis is your wallet number : {wallet_number}")
    return



# destroy login screen when back button is clicked.
def back_login():
    global login_screen
    login_screen.destroy()


# Login screen
def login():
    # Variables
    global temp_student_id
    global temp_password
    global login_screen
    global notify_login
    temp_student_id = StringVar()
    temp_password = StringVar()

    # Login Screen
    login_screen = Toplevel(master)
    login_screen.title('Login')            #file='(image path)'
    login_screen.iconphoto(False,PhotoImage(file='KSUpay logo.png'))

    # Labels
    Label(login_screen, text="Please enter your details to Login", font=('Calibri', 12)).grid(row=0, sticky=N, pady=10)
    Label(login_screen, text="ID", font=('Calibri', 12)).grid(row=1, sticky=W)
    Label(login_screen, text="Password", font=('Calibri', 12)).grid(row=2, sticky=W)

    notify_login = Label(login_screen, font=('Calibri', 12))
    notify_login.grid(row=5, sticky=N, pady=10)

    # Entry to enter text
    Entry(login_screen, textvariable=temp_student_id).grid(row=1, column=0, padx=100)
    Entry(login_screen, textvariable=temp_password, show="*").grid(row=2, column=0, padx=100)

    # Button
    Button(login_screen, text="Login", command=login_finish, font=('Calibri', 12)).grid(row=3,  pady=10 )
    Button(login_screen, text="Back", command=back_login, font=('Calibri', 12)).grid(row=4,  pady=10)


# Main Screen
master = Tk()
master.title('(KSUpay)')
master.geometry('310x400')
                                 #file='(image path)'
master.iconphoto(False,PhotoImage(file='KSUpay logo.png'))
#put an image inside the app
photo = PhotoImage(file = r"C:\Users\gglol\OneDrive\Desktop\KSUpayImage.png")#file = r"(image path)"
#resize the image to fit the app geometry
photo = photo.subsample(5,5)

# Labels
Label(master, text='KSUpay', font=('Calibiri', 14)).grid(row=0, column=5, pady=10)
Label(master, image=photo).grid(row=2, column=5, pady=15)

# Buttons
Button(master, text="Sign up", font=('Calibri', 12), width=20, command=Signup).grid(row=3, column=5,pady=10)
Button(master, text="Login", font=('Calibri', 12), width=20, command=login).grid(row=4, column=5, pady=10)

# RUN GUI for ever.
master.mainloop()




