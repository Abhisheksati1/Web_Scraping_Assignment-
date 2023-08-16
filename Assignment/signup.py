import tkinter as tk
import psycopg2
import subprocess

# Database connection parameters
DB_NAME = "assignments"
DB_USER = "postgres"
DB_PASSWORD = "password"
DB_HOST = "localhost"
DB_PORT = "5432"

def signup():
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
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        connection.commit()
        result_label.config(text="Signup successful!", fg="green")
        root.destroy()
        subprocess.Popen(['python', 'signin.py'])

    except psycopg2.Error as e:
        print(e)
        if "duplicate key value" in str(e):
            result_label.config(text="username already exist", fg="red")
        else:
            connection.rollback()
            result_label.config(text="An error occurred while signing up.", fg="red")

    finally:
        connection.close()

root = tk.Tk()
root.title("Sign_Up Page")
root.geometry("500x500")


username_label = tk.Label(root, text="Username:", font=("arial", 15, 'bold'))
username_label.place(x=80, y=50)

username_entry = tk.Entry(root)
username_entry.place(x=210, y=60)

password_label = tk.Label(root, text="Password:", font=("arial", 15, 'bold'))
password_label.place(x=75, y=120)

password_entry = tk.Entry(root, show="*")
password_entry.place(x=210, y=130)

signup_button = tk.Button(root, text="Signup", font=('arial', 15, 'bold'), width=10, height=1, command=signup)
signup_button.place(x=140, y=200)

result_label = tk.Label(root, text="", fg="black")
result_label.place(x=150, y=250)

root.mainloop()
