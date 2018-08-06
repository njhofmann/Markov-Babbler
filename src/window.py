from tkinter import filedialog
import tkinter as tk
import random

from src.markov_chain import MarkovChain


class Window:
    # Creates a GUI to use for generating Markov Chains and Babbler text from a .txt file"""

    def __init__(self, master):
        self.master = master
        self.markov_chain = MarkovChain()
        master.title("Markov Babbler")

        # Constants
        self.button_height = 2
        self.button_width = 10
        self.button_off_color = "Light Grey"
        self.button_on_color = "Grey"
        self.number_of_sentences = 1

        # Displays babbler output
        self.display = tk.Label(master, height=18, width=80, textvariable="", bg='WHITE', borderwidth=3,
                                relief="groove", anchor='w', justify='left')
        self.display.grid(row=0, rowspan=12, column=0, columnspan=10)

        # Selects .txt file to make a babbler out of
        self.select_file = tk.Button(master, text="Select File", height=self.button_height, width=self.button_width,
                                     bg=self.button_off_color, activebackground=self.button_on_color,
                                     command=self.find_file)
        self.select_file.grid(row=0, column=11)

        # Generates babbler text
        self.generate = tk.Button(master, text="Generate Text", height=self.button_height, width=self.button_width,
                                  bg=self.button_off_color, activebackground=self.button_on_color,
                                  command=self.generate_babble_text)
        self.generate.grid(row=1, column=11)

        # Select the number sentences to generate.
        self.num_of_sentences_selection = tk.Spinbox(master, values=tuple(range(1, 50)),
                                                     command=self.set_number_of_sentences)

        self.num_of_sentences_selection.grid(row=4, column=11)

        # Select the markov chain's order
        self.order_selection = tk.Spinbox(master, values=tuple(range(1, 11)), command=self.recompute_markov_chain)
        self.order_selection.grid(row=3, column=11)

        # Saves babbler text in a .txt file
        self.save_file = tk.Button(master, text="Save Text", height=self.button_height, width=self.button_width,
                                   bg=self.button_off_color, activebackground=self.button_on_color,
                                   command=self.save_babble)
        self.save_file.grid(row=5, column=11)

        # Placeholders for selected file's markov chain and babbler output
        self.babble_output = ""

    def find_file(self):
        """
        Finds the .txt file the user is wants to read from
        :return: None
        """
        selected_file = tk.filedialog.askopenfilename(initialdir="/", title="Select File",
                                                      filetypes=(("txt Files", "*.txt"), ("All Files", "*.*")))
        self.markov_chain.add_file(selected_file)

    def generate_babble_text(self):
        """
        From the file's generated markov chain, produces X sentences.
        :return: X sentences from generated markov chain
        """
        self.babble_output = ""
        for n in range(self.number_of_sentences):
            sentence_length = random.randint(10, 20)
            self.babble_output += self.markov_chain.generate_sentence(sentence_length)
        self.display.config(text=self.babble_output)

    def set_number_of_sentences(self):
        """

        :return:
        """
        self.number_of_sentences = int(self.num_of_sentences_selection.get())

    def recompute_markov_chain(self):
        """

        :return:
        """
        new_order = int(self.order_selection.get())
        if new_order != self.markov_chain.order:
            self.markov_chain.recompute_markov_chain(new_order)

    def save_babble(self):
        """
        Saves the last generated babble text as a .txt file under a file name and directory of user's choice.
        :return: None
        """
        save_file = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
        if save_file is None:
            return
        save_file.write(self.babble_output)
        save_file.close()


if __name__ == '__main__':
    root = tk.Tk()
    my_window = Window(root)
    root.mainloop()
