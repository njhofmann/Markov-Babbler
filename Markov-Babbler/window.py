from tkinter import filedialog
import tkinter as tk

from mc_generator import MarkovChain
from babbler import Markov_Babbler


class Window:
    # Creates a GUI to use for generating Markov Chains and Babbler text from a .txt file"""

    def __init__(self, master):
        self.master = master
        master.title("Markov Babbler")

        # Constants
        self.button_height = 3
        self.button_width = 10
        self.button_off_color = "Light Grey"
        self.button_on_color = "Grey"

        # Displays babbler output
        self.display = tk.Label(master, height=18, width=80, textvariable="", bg="White", borderwidth=3,
                                relief="groove")
        self.display.grid(row=0, rowspan=10, column=1, columnspan=10)

        # Selects .txt file to make a babbler out of
        self.select_file = tk.Button(master, text="Select File", height=self.button_height, width=self.button_width,
                                     bg=self.button_off_color, activebackground=self.button_on_color,
                                     command=self.find_file)
        self.select_file.grid(row=0, column=0)

        # Generates babbler text
        self.generate = tk.Button(master, text="Generate Text", height=self.button_height, width=self.button_width,
                                  bg=self.button_off_color, activebackground=self.button_on_color,
                                  command=self.generate_babble_text)
        self.generate.grid(row=1, column=0)

        # Saves babbbler text in a .txt file
        self.save_file = tk.Button(master, text="Save Text", height=self.button_height, width=self.button_width,
                                   bg=self.button_off_color, activebackground=self.button_on_color,
                                   command=self.save_babble)
        self.save_file.grid(row=2, column=0)

        # Placeholders for selected file's markov chain and babbler output
        self.markov_chain = {}
        self.babble_output = ""

    # Find the .txt file the user is wants to read from
    def find_file(self):
        selected_file = tk.filedialog.askopenfilename(initialdir="/", title="Select File",
                                                      filetypes=(("txt Files", "*.txt"), ("All Files", "*.*")))
        mc = MarkovChain(selected_file)
        self.markov_chain = mc.output_mc

    # From the file's generated markokv chain, produces 10 lines of babbler text
    def generate_babble_text(self):
        self.babble_output = ""
        for n in range(10):
            bab = Markov_Babbler(self.markov_chain)
            self.babble_output += bab.sentence + "\n"
        self.display.config(text=self.babble_output)

    # Saves the last generated babble text as a .txt file under a file name and directory of user's choice
    def save_babble(self):
        save_file = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
        if save_file is None:
            return
        save_file.write(self.babble_output)
        save_file.close()


if __name__ == '__main__':
    root = tk.Tk()
    my_window = Window(root)
    root.mainloop()
