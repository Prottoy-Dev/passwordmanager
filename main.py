"""
Password Manager Application

This is a simple password manager application that allows users to generate and store passwords for different websites.
It provides functionality to generate strong passwords, store them along with website and email details,
and retrieve saved passwords.


"""
from random import choice, randint, shuffle
import pyperclip
from tkinter import messagebox
import json
from tkinter import *


# ---------------------------- GENERATE PASSWORD ------------------------------- #
def generate_pass():
    """
        Generate a strong password with a mix of letters, numbers, and symbols.

    """
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
    pass_letters = [choice(letters) for _ in range(randint(8, 10))]
    pass_numbers = [choice(numbers) for _ in range(randint(2, 4))]
    pass_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_list = pass_letters + pass_numbers + pass_symbols
    shuffle(password_list)
    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    """
        Retrieve and display the password associated with a given website.

    """
    user_search = website_entry.get().lower()
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
            password = data[user_search]["Password"]
            messagebox.showinfo(title="Info", message=f"Website: {user_search}\n Password: {password}")
    except:
        messagebox.showinfo(title="Error", message="No Data File Found")


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    """
        Save website, email, and password details to a data file.

    """
    email_name = email_entry.get().lower()
    website_name = website_entry.get().lower()
    password_name = password_entry.get()
    if len(password_name) == 0:
        messagebox.askretrycancel(title="ERROR", message="Password is empty")
    elif len(website_name) == 0:
        messagebox.askretrycancel(title="ERROR", message="Website is empty")
    else:
        its_ok = messagebox.askokcancel(title="Check", message=f"These are the details entered:\n "
                                                               f"Website:{website_name}\n Email:{email_name}\n "
                                                               f"Password:{password_name}\n")
        new_data = {
            website_name: {
                "Email": email_name,
                "Password": password_name,
            }
        }
        if its_ok:
            try:
                with open("data.json", "r") as file:
                    data = json.load(file)
            except FileNotFoundError:
                with open("data.json", "w") as file:
                    json.dump(new_data, file, indent=4)
            else:
                data.update(new_data)
                with open("data.json", "w") as file:
                    json.dump(data, file, indent=4)
            finally:
                # email_entry.delete(0, END)
                website_entry.delete(0, END)
                password_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #

# ... (UI setup code using tkinter)

# Entry point of the program


window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(height=200, width=200)
locker_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=locker_img)
canvas.grid(column=1, row=0)

website_label = Label(text="Website :")
website_label.grid(column=0, row=1)

email_label = Label(text="Email/Username :")
email_label.grid(column=0, row=2)

password_label = Label(text="Password :")
password_label.grid(column=0, row=3)

gen_button = Button(text="Generate Password", command=generate_pass)
gen_button.grid(column=2, row=3)

add_button = Button(text="Add", width=45, command=save)
add_button.grid(column=1, row=4, columnspan=2)

search_button = Button(text="Search", width=15, command=find_password)
search_button.grid(column=2, row=1)

website_entry = Entry(width=34)
website_entry.grid(row=1, column=1)
website_entry.focus()

email_entry = Entry(width=53)
email_entry.grid(column=1, row=2, columnspan=2)
email_entry.insert(0, "your email")

password_entry = Entry(width=34)
password_entry.grid(column=1, row=3)

window.mainloop()
