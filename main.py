'''
The main.py file serves as our main entry
point to our grading bot
'''
import logging
import tkinter as tk
from tkinter import filedialog, messagebox
import os
from openai_actions import open_ai_api_calls
from general_functions import general_functions


def main():
    '''
    The main entry point into the application.
    '''
    try:
        logging.info('Main method executing')
        root = tk.Tk()
        root.withdraw()  # we don't want a full GUI, so keep the root window from appearing

        logging.info("Select the assignments folder...")
        messagebox.showinfo('Select Assignments Folder', 'Please select the folder containing all assignments.')
        assignments_folder = filedialog.askdirectory()  # open folder dialog
        logging.info(f"Selected folder: {assignments_folder}")

        logging.info("Select the grading criteria text file...")
        messagebox.showinfo('Select Criteria File', 'Please select the grading criteria text file.')
        grading_criteria_file = filedialog.askopenfilename()  # open file dialog
        logging.info(f"Selected file: {grading_criteria_file}")

        with open(grading_criteria_file, 'r', encoding='utf-8') as grading_file:
            grading_criteria = grading_file.read()

        for assignment_file in os.listdir(assignments_folder):
            with open(os.path.join(assignments_folder, assignment_file), 'r', encoding='utf-8') as f:
                assignment_content = f.read()
                message = general_functions.combine_contents_into_message(grading_criteria, assignment_content)
                ai_response = open_ai_api_calls.generate_chat_completion(message)
                general_functions.write_results_to_file(ai_response)
                logging.info(f"Graded {assignment_file}")

        messagebox.showinfo('Grading completed!', 'The grading has been completed! Please check your downloads folder for the results.')
        logging.info("Grading completed! Check downloads folder for results.")
    except Exception as ex:
        logging.error(f'An unexpected error occurred in main. Error: {ex}')
        messagebox.showerror('Error!', f'The grading process failed. Error: {ex}')


if __name__ == "__main__":
    general_functions.configure_logging()
    main()
