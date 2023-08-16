import tkinter as tk
import psycopg2
import subprocess
import os

# Database connection parameters
DB_NAME = "assignments"
DB_USER = "postgres"
DB_PASSWORD = "password"
DB_HOST = "localhost"
DB_PORT = "5432"

def login():
    username = username_entry.get()
    password = password_entry.get()

    connection = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user_data = cursor.fetchone()

        if user_data:
            result_label.config(text="Login successful!", fg="green")

            cursor.execute("SELECT user_id FROM users WHERE username = %s;", (username,))
            userid = cursor.fetchone()

            if userid:
                os.environ["USER_ID"] = str(userid[0])
                root.destroy()
                subprocess.Popen(['python', 'web_scap.py'])
            else:
                result_label.config(text="User ID not found.", fg="red")
        else:
            result_label.config(text="Login failed.", fg="red")

    except psycopg2.Error as e:
        print(e)
        result_label.config(text="An error occurred while logging in.", fg="red")

    finally:
        connection.close()
def Signup():
    root.destroy()
    subprocess.Popen(['python', 'signup.py'])

def forget():
    root.destroy()
    subprocess.Popen(['python', 'froget.py'])
root = tk.Tk()
root.title("Login Page")
root.geometry("500x500")

# Create and place widgets on the GUI
username_label = tk.Label(root, text="Username:",font=("arial",15,'bold'))
username_label.place(x=80,y=50)

username_entry = tk.Entry(root)
username_entry.place(x=210,y=60)

password_label = tk.Label(root, text="Password:",font=("arial",15,'bold'))
password_label.place(x=75,y=120)

password_entry = tk.Entry(root, show="*")
password_entry.place(x=210,y=130)

login_button = tk.Button(root, text="Login",font=('arial',15,'bold'),width=5,height=1, command=login)
login_button.place(x=75,y=200)

signup_button = tk.Button(root, text="Sign up",font=('arial',15,'bold'),width=8,height=1, command=Signup)
signup_button.place(x=180,y=200)

forget_button = tk.Button(root, text="forget",font=('arial',15,'bold'),width=8,height=1, command=forget)
forget_button.place(x=310,y=200)

result_label = tk.Label(root, text="", fg="black")
result_label.place(x=150, y=250)

root.mainloop()
