import tkinter as tk
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
import psycopg2
import os

user_id = os.environ.get("USER_ID")
if user_id is not None:
    user_id = int(user_id)
    print("Received user_id:", user_id)

# Database connection parameters
DB_NAME = "assignments"
DB_USER = "postgres"
DB_PASSWORD = "password"
DB_HOST = "localhost"
DB_PORT = "5432"

def scrape_and_save():
    product_url = url_entry.get()

    try:
        scraped_data = scrape_product_details(product_url)
        save_to_database(scraped_data)
        display_scraped_data(scraped_data)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def scrape_product_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    title = soup.find("span", class_="B_NuCI").get_text()
    price = soup.find("div", class_="_30jeq3").get_text()

    description = ""
    description_element = soup.find("div", class_="_3WHvuP")
    if description_element:
        description = description_element.get_text()

    reviews_count = soup.find("span", class_="_2_R_DZ").get_text()
    rating = soup.find("div", class_="_3LWZlK").get_text()

    media_count = len(soup.find_all("div", class_="_2mLllQ"))

    return {
        "title": title,
        "price": price,
        "description": description,
        "reviews_count": reviews_count,
        "rating": rating,
        "media_count": media_count
    }

def save_to_database(data):
    connection = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

    cursor = connection.cursor()

    try:
        cursor.execute("INSERT INTO products (user_id, title, price, description, reviews_count, rating, media_count) "
                       "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                       (user_id, data["title"], data["price"], data["description"], data["reviews_count"], data["rating"], data["media_count"]))
        connection.commit()
        messagebox.showinfo("Success", "Data saved to database!")
    except psycopg2.Error as e:
        print(e)
        connection.rollback()
        messagebox.showerror("Error", f"An error occurred while saving to database: {e}")
    finally:
        connection.close()

def display_scraped_data(data):
    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)
    for key, value in data.items():
        result_text.insert(tk.END, f"{key}: {value}\n")
    result_text.config(state=tk.DISABLED)

# GUI setup
root = tk.Tk()
root.title("Flipkart Product Scraper")
root.geometry("500x500")

url_label = tk.Label(root, text="Enter Flipkart Product URL:", font=("arial", 15, 'bold'))
url_label.place(x=80,y=50)

url_entry = tk.Entry(root,width=50)
url_entry.place(x=70,y=90)

scrape_button = tk.Button(root, text="Scrape & Save", font=("arial", 15, 'bold'),command=scrape_and_save)
scrape_button.place(x=130,y=130)

result_text = tk.Text(root, height=15, width=50, state=tk.DISABLED)
result_text.place(x=50,y=180)

root.mainloop()
