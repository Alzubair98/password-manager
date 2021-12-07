import tkinter as tk
from tkinter import messagebox
import random
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(6, 8)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    letter_list = [random.choice(letters) for i in range(nr_letters)]
    number_list = [random.choice(numbers) for i in range(nr_letters)]
    symbol_list = [random.choice(numbers) for i in range(nr_letters)]

    password_list = letter_list + number_list + symbol_list
    random.shuffle(password_list)

    password = "".join(password_list)
    pass_box.delete(0, 1000)
    pass_box.insert(0, password)  # 0 is the position , password is the string(text)
    pyperclip.copy(password)  # to copy the password just after the click of the button


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save_password():
    website = website_box.get()
    info = info_box.get()
    passs = pass_box.get()
    dict = {website: {"email": info,
                      "password": passs,

                      }

            }
    if len(website) == 0 or len(passs) == 0:
        messagebox.showerror(title="Oops", message="pleas do not leave any filed empty")
    else:
        # is_ok = messagebox.askokcancel(title=website,
        # message=f"These are the details entered: \nEmail: {info}\nPassword: {passs} ")  # to show a pop up msg to the user
        # with open("data.txt", "a") as file:  # normal txt file (hard to work with)
        try:
            with open("data.json", "r") as file:
                # reading old data
                data_file = json.load(file)
                # updating old data with new data (dict)
                data_file.update(dict)
        except FileNotFoundError:
            with open("data.json",
                      "w") as file:  # json file much easier to work with to read from json we use json.load(), write, json.dump(), updata, json.update()
                # the data we want to dump it into json should be dict , and we should provide where we want to dump this data in which file
                json.dump(dict, file, indent=4)  # indent used to add space to the json file to make it easy to read
        else:
            with open("data.json", "w") as file:
                json.dump(data_file, file, indent=4)

        finally:
            website_box.delete(0,
                               1000)  # the delete method will delete the text inside the box after pressing the add button
            pass_box.delete(0,
                            1000)  # the parameters mean from the first letter to the 1000 letter delete every thing


# ---------------------------- Search setup ------------------------------- #
def search():
    global the_email, the_password
    website = website_box.get()
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
            # print(data)
        for key in data:  # loop inside the json file to get hold of all the components
            for i in data[website]:  # loop inside the dict of data but with the value of the(website) key
                the_email = data[website]['email']  # get hold of the email
                the_password = data[website]["password"]  # get hold of the password
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="you did not create any passwords yet 😥  ")
    except KeyError:
        messagebox.showerror(title="error", message="please make sure you entered a valid website 🤗")
    else:
        messagebox.showinfo(title=website,
                            message=f"your e-mail is {the_email}\nyour password is {the_password}")  # send them as msg-box


# ---------------------------- UI SETUP ------------------------------- #


window = tk.Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = tk.Canvas(width=200, height=200, highlightthickness=0)
Image = tk.PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=Image)
canvas.grid(column=1, row=0)

website_label = tk.Label(text="Website:")
website_label.grid(column=0, row=1)

info_label = tk.Label(text="Email/Username:")
info_label.grid(column=0, row=2)

pass_label = tk.Label(text="Password:")
pass_label.grid(column=0, row=3)

website_box = tk.Entry(width=25)
website_box.grid(column=1, row=1)
website_box.focus()  # focus method is to start the program with curser in this entery

info_box = tk.Entry(width=43)
info_box.grid(column=1, row=2, columnspan=2)  # the CS make the box take space of 2 columns
info_box.insert(0, "your e-mail")  # insert allows you to start the program with some text inside the box

pass_box = tk.Entry(width=25)
pass_box.grid(column=1, row=3)

Generate_button = tk.Button(text="Generate Password", highlightthickness=0, command=generate_password)
Generate_button.grid(column=2, row=3)

add_button = tk.Button(text="add", highlightthickness=0, width=37, command=save_password)
add_button.grid(column=1, row=4, columnspan=2)

search_button = tk.Button(text="Search", highlightthickness=0, width=15, command=search)
search_button.grid(column=2, row=1)

window.mainloop()
