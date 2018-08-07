from tkinter import filedialog
import tkinter as tk
import random
from src.markov_chain import MarkovChain


class Window:
    """
    Creates foobar
    """

    def __init__(self, master):
        """

        :param master:
        """
        self.master = master
        self.master.resizable(False, False)
        self.markov_chain = MarkovChain()
        master.title("Markov Babbler")

        # Constants
        self.button_height = 2
        self.button_width = 20
        self.button_off_color = 'Light Grey'
        self.button_on_color = 'Grey'
        self.button_column_span = 2
        self.spinbox_length = 3
        self.number_of_sentences = 12
        self.options_column = 11
        self.min_sentence_length = 10
        self.max_sentence_length = 20

        # Displays babbler output
        self.display_frame = tk.Frame(master)
        self.display_frame.grid(row=0, rowspan=12, column=0, columnspan=10)

        self.display_scrollbar = tk.Scrollbar(self.display_frame)

        self.display = tk.Text(self.display_frame, height=18, width=80, bg='WHITE', borderwidth=3,
                               relief="groove", wrap='word')
        self.display.config(yscrollcommand=self.display_scrollbar.set)
        self.display_scrollbar.config(command=self.display.yview)
        self.display.pack(side='left')
        self.display_scrollbar.pack(side='right', fill='y')

        # Selects .txt file to add to this Markov Chain
        self.select_file = tk.Button(master, text='Add File', height=self.button_height, width=self.button_width,
                                     bg=self.button_off_color, activebackground=self.button_on_color,
                                     command=self.find_file)
        self.select_file.grid(row=0, column=self.options_column, columnspan=self.button_column_span)

        # Add user entered text to this Markov Chain
        self.user_string_row = 1

        self.user_string_entry = tk.Entry(self.master)
        self.user_string_entry.grid(row=self.user_string_row, column=self.options_column)

        self.user_string_button = tk.Button(self.master, text='Enter', bg=self.button_off_color,
                                            activebackground=self.button_on_color, command=self.add_user_text)
        self.user_string_button.grid(row=self.user_string_row, column=self.options_column+1)

        # Select the markov chain's order
        self.order_row = 2
        self.order_selection_label = tk.Label(master, text='Markov Chain Order')
        self.order_selection_label.grid(row=self.order_row, column=self.options_column)

        self.initial_order_value = tk.StringVar(master)
        self.initial_order_value.set(str(self.markov_chain.order))

        self.order_selection = tk.Spinbox(master, values=tuple(range(1, 10)),
                                          width=self.spinbox_length,
                                          command=self.recompute_markov_chain)
        self.order_selection.config(textvariable=self.initial_order_value)
        self.order_selection.grid(row=self.order_row, column=self.options_column + 1)

        # Select the number sentences to generate.
        self.num_sentences_row = 3
        self.num_sentences_label = tk.Label(master, text='Number of Sentences')
        self.num_sentences_label.grid(row=self.num_sentences_row, column=self.options_column)

        self.initial_num_sentences = tk.StringVar(master)
        self.initial_num_sentences.set(str(self.number_of_sentences))

        self.num_sentences = tk.Spinbox(master, values=tuple(range(1, 51)),
                                        width=self.spinbox_length,
                                        command=self.set_number_of_sentences)
        self.num_sentences.config(textvariable=self.initial_num_sentences)
        self.num_sentences.grid(row=self.num_sentences_row, column=self.options_column + 1)

        # Set minimum sentence length
        self.min_sentence_row = 4

        self.min_sentence_label = tk.Label(master, text='Min Sentence Length')
        self.min_sentence_label.grid(row=self.min_sentence_row, column=self.options_column)

        self.initial_min_sentence = tk.StringVar(master)
        self.initial_min_sentence.set(str(self.min_sentence_length))

        self.set_min_sentence = tk.Spinbox(master, values=tuple(range(1, 100)),
                                           width=self.spinbox_length,
                                           command=self.set_min_sentence_length)
        self.set_min_sentence.config(textvariable=self.initial_min_sentence)
        self.set_min_sentence.grid(row=self.min_sentence_row, column=self.options_column+1)

        # Set maximum sentence length
        self.max_sentence_row = 5

        self.max_sentence_label = tk.Label(master, text='Max Sentence Length')
        self.max_sentence_label.grid(row=self.max_sentence_row, column=self.options_column)

        self.initial_max_sentence = tk.StringVar(master)
        self.initial_max_sentence.set(str(self.max_sentence_length))

        self.set_max_sentence = tk.Spinbox(master, values=tuple(range(2, 101)),
                                           width=self.spinbox_length,
                                           command=self.set_max_sentence_length)
        self.set_max_sentence.config(textvariable=self.initial_max_sentence)
        self.set_max_sentence.grid(row=self.max_sentence_row, column=self.options_column+1)

        # Generates babbler text
        self.generate = tk.Button(master, text="Generate Text", height=self.button_height, width=self.button_width,
                                  bg=self.button_off_color, activebackground=self.button_on_color,
                                  command=self.generate_babble_text)
        self.generate.grid(row=6, column=self.options_column, columnspan=self.button_column_span)

        # Saves babbler text in a .txt file
        self.save_file = tk.Button(master, text='Save Text', height=self.button_height, width=self.button_width,
                                   bg=self.button_off_color, activebackground=self.button_on_color,
                                   command=self.save_babble)
        self.save_file.grid(row=7, column=self.options_column, columnspan=self.button_column_span)

    def find_file(self):
        """
        Finds the .txt file the user is wants to read from and adds it to this GUI's Markov Chain
        :return: None
        """
        selected_file = tk.filedialog.askopenfilename(initialdir='/', title='Select File',
                                                      filetypes=(('txt Files', '*.txt'), ('All Files', '*.*')))
        self.markov_chain.add_file(selected_file)

    def generate_babble_text(self):
        """
        From the GUI's Markov Chain, produces X sentences from user selected files and entered strings, where X is some
        random number between the minimum sentence length and the maximum sentence length.
        :return: X sentences from generated markov chain
        """
        markov_chain_output = []
        for n in range(self.number_of_sentences):
            sentence_length = random.randint(self.min_sentence_length, self.max_sentence_length)
            markov_chain_output.append(self.markov_chain.generate_sentence(sentence_length))

        random.shuffle(markov_chain_output)

        to_display = ''
        for i in markov_chain_output:
            to_display += i + '\n'

        self.display.delete('1.0', tk.END)
        self.display.insert('1.0', to_display)

    def add_user_text(self):
        """

        :return:
        """
        text_to_add = self.user_string_entry.get()
        self.user_string_entry.delete(0, tk.END)
        self.markov_chain.add_string(text_to_add)

    def set_number_of_sentences(self):
        """

        :return:
        """
        self.number_of_sentences = int(self.num_sentences.get())


    def set_min_sentence_length(self):
        """

        :return:
        """
        new_min = int(self.set_min_sentence.get())
        cur_max = self.max_sentence_length

        if new_min < cur_max:
            self.min_sentence_length = new_min
        else:
            old_min = self.min_sentence_length
            old_min_var = tk.StringVar(self.master)
            old_min_var.set(str(old_min))
            self.set_min_sentence.config(textvariable=old_min_var)

    def set_max_sentence_length(self):
        """

        :return:
        """
        new_max = int(self.set_max_sentence.get())
        cur_min = self.min_sentence_length

        if new_max > cur_min:
            self.max_sentence_length = new_max
        else:
            old_max = self.max_sentence_length
            old_max_var = tk.StringVar(self.master)
            old_max_var.set(str(old_max))
            self.set_max_sentence.config(textvariable=old_max_var)

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
        save_file = filedialog.asksaveasfile(mode='w', defaultextension='.txt')
        if save_file is None:
            return
        save_file.write(self.babble_output)
        save_file.close()


if __name__ == '__main__':
    root = tk.Tk()
    my_window = Window(root)
    root.mainloop()
