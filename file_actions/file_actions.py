"""
file_actions Module

This module provides a collection of functions designed to facilitate
the grading process of student assignments. The primary functions include:

- Prompting the user to select the assignments folder and grading criteria file.
- Reading and combining all assignment files for individual students.
- Grading the combined content of all assignment files for a single student.
- Writing the grading results to a designated file.
- Logging and user notifications for error handling and process updates.

Key Features:
- Support for different file extensions via user-defined allowed extensions.
- Error handling to ensure continuous grading even if issues arise with individual files.
- Integration with external APIs for grading.
- Tkinter-based user interface elements for folder and file selection, as well as error notifications.

Dependencies:
- logging: For recording the grading process and any potential issues.
- os: For directory and file path operations.
- tkinter: For user interface elements.
- general_functions: Custom module containing auxiliary functions.
- open_ai_api_calls: Custom module for interfacing with the external grading API.

Note: Ensure that the dependencies are properly installed and accessible.
"""

import logging
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


def read_student_files(student_folder_path, allowed_extensions):
    """
    Read and combine all assignment files for a single student.

    Args:
        student_folder_path (str): The path to the individual student's folder.
        allowed_extensions (list): List of file extensions that are considered valid for assignments.

    Returns:
        str: Combined content of all valid assignment files in the student's folder.

    This function iterates over all files in the student's folder. It skips files that do not have 
    an allowed extension. For each valid assignment file, it reads the content and appends it to 
    a combined content string, separated by two newlines. In case of any errors while reading a file 
    (e.g., not UTF-8 encoded, file not found), appropriate logging and user notifications are done.

    Note: The function continues reading other files even if an error occurs with one file.
    """
    combined_assignment_content = ""

    for assignment_file in os.listdir(student_folder_path):
        if not any(assignment_file.lower().endswith(ext) for ext in allowed_extensions):
            logging.warning(f"Skipping file {assignment_file} as it's not a recognized text file.")
            continue
        try:
            assignment_file_path = os.path.join(student_folder_path, assignment_file)
            with open(assignment_file_path, 'r', encoding='utf-8') as f:
                combined_assignment_content += f.read() + "\n\n"  # Combine content with two newlines as a separator
        except UnicodeDecodeError:
            logging.error(f"The file {assignment_file} is not UTF-8 encoded.")
            messagebox.showinfo('Error!', f'The file {assignment_file} is not UTF-8 encoded. Click "OK" to continue grading.')
        except FileNotFoundError:
            logging.error(f"The file {assignment_file} was not found.")
        except Exception as ex:
            logging.error(f"An unexpected error occurred while reading {assignment_file}: {ex}")
            messagebox.showinfo('Error!', f'I ran into an error reading the assignment. Error: {ex}. Click "OK" to continue grading.')

    return combined_assignment_content


def grade_combined_assignment(grading_criteria, combined_assignment_content, student_folder, first_run):
    """
    Grade the combined content of all assignment files for a single student.

    Args:
        grading_criteria (str): The criteria to use for grading the assignments.
        combined_assignment_content (str): The combined content of all valid assignment
        files for a student.
        student_folder (str): The name of the student's folder, used for logging and 
        result file naming.
        first_run (bool): Flag to indicate if this is the first grading run.

    This function takes the combined assignment content for a student, and grades 
    it using an external API. The grading results are then written to a file. In 
    case of any errors during the grading process, appropriate logging and user 
    notifications are done.

    Note: The function continues the grading process for other students even if 
    an error occurs with one student.
    """
    try:
        if not combined_assignment_content:
            logging.warning(f'No assignment submitted for: {student_folder}')
        else:
            message = general_functions.combine_contents_into_message(grading_criteria, combined_assignment_content)
            ai_response = open_ai_api_calls.generate_chat_completions(message)
            write_results_to_file(ai_response, student_folder, first_run)
            logging.info(f"Graded combined assignments for {student_folder}")
    except Exception as ex:
        logging.error(f"An unexpected error occurred while grading combined assignments for {student_folder}: {ex}")
        messagebox.showinfo('Error!', f'I ran into an error grading the combined assignments for {student_folder}. Error: {ex}. Click "OK" to continue grading.')


def grade_assignments(assignments_folder, grading_criteria, allowed_extensions, first_run=True):
    """
    Grade assignments for each student based on the provided criteria.

    Args:
        assignments_folder (str): Path to the main folder containing individual student 
        assignment folders.
        grading_criteria (str): The criteria to use for grading assignments.
        allowed_extensions (list): List of file extensions that are considered 
        valid for assignments.
        first_run (bool, optional): Flag to indicate if this is the initial run of the 
        grading process. Defaults to True.

    This function iterates over each student's folder within the main assignments folder. 
    For each student, it reads and combines all valid assignment files using the 
    `read_student_files` function. The combined content is then graded using the 
    `grade_combined_assignment` function. If a student's folder is empty, 
    a log message is recorded, and the result "No assignment submitted" is written to a file.

    In case of any unexpected errors during the grading process, appropriate logging 
    and user notifications are done.

    Note: The function continues the grading process for other students even if an 
    error occurs with one student.
    """
    try:
        for student_folder in os.listdir(assignments_folder):
            student_folder_path = os.path.join(assignments_folder, student_folder)

            if os.path.isdir(student_folder_path):
                if not os.listdir(student_folder_path):
                    logging.info(f"The folder for {student_folder} is empty. Skipping...")
                    write_results_to_file("No assignment submitted", student_folder, first_run)
                    continue

                combined_assignment_content = read_student_files(student_folder_path, allowed_extensions)
                grade_combined_assignment(grading_criteria, combined_assignment_content, student_folder, first_run)

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


def read_results_from_file():
    """
    Retrieve the content of the 'grading_results.txt' file from the "Grading Results" 
    folder in the user's Downloads directory.

    :return: A string containing the content of the 'grading_results.txt' file.
             If the file does not exist, it returns a message indicating so.
             If an error occurs during the reading process, an error message with 
             the exception details is returned.

    :rtype: str

    :raises Exception: Any exception raised during the reading process is caught 
    and its message is returned.
    """
    try:
        # Detecting the operating system and setting the downloads folder path accordingly
        downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads')

        # Set the path to the "Grading Results" folder inside the Downloads folder
        grading_results_folder = os.path.join(downloads_folder, 'Grading Results')

        # Set the file path within the "Grading Results" folder
        file_path = os.path.join(grading_results_folder, 'grading_results.txt')

        # Check if the file exists
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
        else:
            return "The grading_results.txt file does not exist."

    except Exception as ex:
        return f"An error occurred while reading from the file: {ex}"
