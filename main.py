'''
The main.py file serves as our main entry
point to our grading bot
'''
import logging
from tkinter import messagebox
from general_functions import general_functions
from file_actions import file_actions
from email_functions import email_delivery as email


def main():
    """
    The main entry point for the application.

    This function performs the following steps:
    1. Log the start of the main method.
    2. Prompt the user to select an assignments folder and a grading criteria file.
    3. Read the grading criteria from the selected file.
    4. Grade the assignments in the selected folder based on the grading criteria.
    5. Display a message box to inform the user that grading has been completed.
    6. Log the completion of grading.

    Exception handling is done to catch and log any errors that may occur during execution.
    """
    try:
        logging.info('Main method executing')
        assignments_folder, grading_criteria_file = file_actions.prompt_user_for_input()
        grading_criteria = file_actions.read_grading_criteria(grading_criteria_file)
        extension = file_actions.get_file_extension()
        if extension:
            file_actions.grade_assignments(assignments_folder, grading_criteria, extension)
            grading_results = file_actions.read_results_from_file()
            email.send_email_to_user(grading_results)
            messagebox.showinfo('Grading completed!', '''The grading has been completed!
                            Please check your downloads folder for the results.''')

            logging.info("Grading completed! Check downloads folder for results.")
        else:
            messagebox.showerror('Error!', 'You must provide a file extension. Service ending.')

    except Exception as ex:
        logging.error(f'An unexpected error occurred in main. Error: {ex}')
        messagebox.showerror('Error!', f'The grading process failed. Error: {ex}')


if __name__ == "__main__":
    general_functions.configure_logging()
    main()
   