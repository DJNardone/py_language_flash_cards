from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
rand_word = {}
word_dict = {}

# Get Words to Translate
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    word_dict = original_data.to_dict(orient="records")
else:
    word_dict = data.to_dict(orient="records")


# Choose Flash Card Words
def random_card():
    global rand_word, flip_timer
    window.after_cancel(flip_timer)
    rand_word = random.choice(word_dict)
    canvas.itemconfig(flash_title, text="French", fill='black')
    canvas.itemconfig(flash_word, text=rand_word['French'], fill="black")
    canvas.itemconfig(card_image, image=flash_card_front)
    flip_timer = window.after(3000, func=flip_card)


# Flip the Flash Card
def flip_card():
    canvas.itemconfig(flash_title, text="English", fill="white")
    canvas.itemconfig(flash_word, text=rand_word['English'], fill="white")
    canvas.itemconfig(card_image, image=flash_card_back)


# Create a "words to learn" database
def word_known():
    word_dict.remove(rand_word)
    data = pandas.DataFrame(word_dict)
    data.to_csv("data/words_to_learn.csv", index=False)
    random_card()


# ---------- UI SETUP ---------- #
window = Tk()
window.title("Language Flash Cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

# Flash Cards
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
flash_card_front = PhotoImage(file="images/card_front.png")
flash_card_back = PhotoImage(file="images/card_back.png")
card_image = canvas.create_image(400, 263, image=flash_card_front)

flash_title = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
flash_word = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

# Buttons
wrong_button_img = PhotoImage(file="../flash-card-app/images/wrong.png")
wrong_button = Button(image=wrong_button_img, highlightthickness=0, command=random_card)
wrong_button.grid(column=0, row=1)
correct_button_img = PhotoImage(file="../flash-card-app/images/right.png")
correct_button = Button(image=correct_button_img, highlightthickness=0, command=word_known)
correct_button.grid(column=1, row=1)

random_card()
window.mainloop()