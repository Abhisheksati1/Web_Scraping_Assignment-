import tkinter as tk
import psycopg2
import subprocess

# Database connection parameters
DB_NAME = "assignments"
DB_USER = "postgres"
DB_PASSWORD = "password"
DB_HOST = "localhost"
DB_PORT = "5432"

root = tk.Tk()
root.title("Forget Page")
root.geometry("500x500")

def forget():
    username = username_entry.get()
    connection = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT password FROM users WHERE username = %s ", (username,))
        password = cursor.fetchone()
        if password:
            result_label.config(text=password, fg="green")
    except psycopg2.Error as e:
        print(e)
        result_label.config(text="An error occurred while logging in.", fg="red")




    
def home():
    root.destroy()
    subprocess.Popen(['python', 'signin.py'])

username_label = tk.Label(root, text="Username:",font=("arial",15,'bold'))
username_label.place(x=80,y=50)

username_entry = tk.Entry(root,width=40)
username_entry.place(x=210,y=60)


submit_button = tk.Button(root, text="submit",font=('arial',15,'bold'),width=8,height=1, command=forget)
submit_button.place(x=100,y=120)

Home_button = tk.Button(root, text="Home",font=('arial',15,'bold'),width=8,height=1, command=home)
Home_button.place(x=250,y=120)

label=tk.Label(root,text = "password",fg="black",font=('arial',15,'bold'))
label.place(x=110,y=200)
result_label = tk.Label(root, text="", fg="black",font=('arial',15,'bold'))
result_label.place(x=250, y=200)

root.mainloop()
