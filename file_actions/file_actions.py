'''
The file actions file contains various
functions that handle/read/write files.
'''
import logging
import time
import os
from tkinter import filedialog, messagebox, simpledialog
import tkinter
from general_functions import general_functions
from openai_actions import open_ai_api_calls


def prompt_user_for_input():
    """
    Prompt the user to select the assignments folder and grading criteria file.

    This function performs the following steps:
    1. Initialize a hidden Tkinter root window.
    2. Show a message box prompting the user to select the assignments folder.
    3. Show a file dialog allowing the user to select the assignments folder.
    4. Show a message box prompting the user to select the grading criteria file.
    5. Show a file dialog allowing the user to select the grading criteria file.

    Returns:
        assignments_folder (str): The path to the selected assignments folder.
        grading_criteria_file (str): The path to the selected grading criteria file.

    Raises:
        ValueError: If the user cancels either of the file dialogs.
    """
    try:
        root = tkinter.Tk()
        root.withdraw()
        messagebox.showinfo('Select Assignments Folder', '''Please select
                            the folder containing all assignments.''')
        assignments_folder = filedialog.askdirectory()
        if not assignments_folder:
            raise ValueError("No assignments folder selected.")

        logging.info(f"Selected folder: {assignments_folder}")
        messagebox.showinfo('Select Criteria File', 'Please select the grading criteria text file.')
        grading_criteria_file = filedialog.askopenfilename()
        if not grading_criteria_file:
            raise ValueError("No grading criteria file selected.")

        logging.info(f"Selected file: {grading_criteria_file}")
        return assignments_folder, grading_criteria_file
    except ValueError as ex:
        logging.error(f"User input error: {ex}")
        messagebox.showerror('Error!', f'Error: {ex}')
        raise


def read_grading_criteria(file_path):
    """
    Read the grading criteria from a specified file.

    Args:
        file_path (str): The path to the grading criteria file.

    Returns:
        str: The contents of the grading criteria file.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        UnicodeDecodeError: If the file is not encoded in UTF-8.
        IOError: For other I/O errors like permission issues.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as grading_file:
            return grading_file.read()
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        messagebox.showerror('Error!', f'File not found: {file_path}')
        raise
    except UnicodeDecodeError:
        logging.error(f"File not encoded in UTF-8: {file_path}")
        messagebox.showerror('Error!', f'File not encoded in UTF-8: {file_path}')
        raise
    except IOError as ex:
        logging.error(f"I/O error occurred while reading the file: {ex}")
        messagebox.showerror('Error!', f'I/O error occurred: {ex}')
        raise


def write_results_to_file(grade_response, student_name, first_run):
    '''
    This function writes the given prediction to a text file as a record
    '''
    try:
        logging.info('Writing grades to a file...')
        # Detecting the operating system and setting the downloads folder path accordingly
        downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads')

        # Create the "Grading Results" folder inside the Downloads folder if it doesn't exist
        grading_results_folder = os.path.join(downloads_folder, 'Grading Results')
        if not os.path.exists(grading_results_folder):
            os.makedirs(grading_results_folder)

        # Set the file path within the "Grading Results" folder
        file_path = os.path.join(grading_results_folder, 'grading_results.txt')

        # Delete the existing file if first_run is True
        if first_run and os.path.exists(file_path):
            logging.info('Deleting prior grading file')
            os.remove(file_path)

        with open(file_path, "a", encoding="utf-8") as file:
            # Adding four new lines for separation, the student's name, and their grade
            file.write(f'\n\n\n\nStudent: {student_name}\nGrade: {grade_response}')

    except Exception as ex:
        logging.error(f"An error occurred while writing to the file: {ex}")


def grade_assignments(assignments_folder, grading_criteria, allowed_extensions, first_run=True):
    """
    Grades assignments based on given criteria.

    Args:
        assignments_folder (str): Path to the folder containing student assignment folders.
        grading_criteria (str): The criteria to use for grading.
        first_run (bool): Flag to indicate if this is the first run.

    This function iterates over each student folder within the main assignments folder,
    reads each assignment, and grades it based on the given criteria.

    Exceptions are handled for each assignment individually, so an error in one file
    will not terminate the entire process.
    """
    try:
        for student_folder in os.listdir(assignments_folder):
            student_folder_path = os.path.join(assignments_folder, student_folder)

            if os.path.isdir(student_folder_path):
                if not os.listdir(student_folder_path):
                    logging.info(f"The folder for {student_folder} is empty. Skipping...")
                    write_results_to_file("No assignment submitted", student_folder, first_run)
                    continue

                for assignment_file in os.listdir(student_folder_path):
                    if not any(assignment_file.lower().endswith(ext) for ext in allowed_extensions):
                        logging.warning(f"Skipping file {assignment_file} for {student_folder} as it's not a recognized text file.")
                        continue
                    try:
                        assignment_file_path = os.path.join(student_folder_path, assignment_file)
                        with open(assignment_file_path, 'r', encoding='utf-8') as f:
                            assignment_content = f.read()

                        message = general_functions.combine_contents_into_message(grading_criteria, assignment_content)
                        ai_response = open_ai_api_calls.generate_chat_completions(message)
                        write_results_to_file(ai_response, student_folder, first_run)
                        logging.info(f"Graded {assignment_file} for {student_folder}")
                    except UnicodeDecodeError:
                        logging.error(f"The file {assignment_file} for {student_folder} is not UTF-8 encoded.")
                        messagebox.showinfo('Error!', f'The file {assignment_file} for {student_folder} is not UTF-8 encoded. Click "OK" to continue grading.')
                        continue
                    except FileNotFoundError:
                        logging.error(f"The file {assignment_file} for {student_folder} was not found.")
                        continue
                    except Exception as ex:
                        logging.error(f"An unexpected error occurred while grading {assignment_file} for {student_folder}: {ex}")
                        messagebox.showinfo('Error!', f'I ran into an error grading the assignment for {student_folder}. Error: {ex}. Click "OK" to continue grading.')
                        continue

                first_run = False
    except Exception as ex:
        logging.error(f"An unexpected error occurred in grade_assignments. Error: {ex}")
        messagebox.showerror('Error!', f'The grading process failed. Error: {ex}')


def get_file_extension():
    """
    Prompt the user to input a file extension using a tkinter dialog.

    Returns:
        str or None: The provided file extension (e.g., ".xlsx") 
        or None if the user cancels the dialog.

    Raises:
        ValueError: If the provided string does not start with a 
        dot (e.g., "xlsx" instead of ".xlsx").
    """
    try:
        root = tkinter.Tk()
        root.withdraw()  # Hide the main window
        file_extension = simpledialog.askstring("Input", 'Please enter the file extension. (e.g., .xlsx):')

        if file_extension and not file_extension.startswith('.'):
            raise ValueError("The provided file extension should start with a dot (e.g., '.xlsx').")

        root.quit()
        root.destroy()
        return file_extension
    except Exception as ex:
        logging.error(f"An unexpected error occurred in get_file_extension. Error: {ex}")
        return None
