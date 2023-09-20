'''
The general_functions file handles basic functions and
actions for the app
'''
import datetime
import logging
import os


def configure_logging():
    '''
    This method configures our log file
    '''
    log_file_path = os.path.join('settings', 'application_log.log')
    logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')
    current_time = datetime.datetime.now()
    logging.info('---- APPLICATION START (current date/time is: %s) ----', current_time)


def write_results_to_file(grade_response):
    '''
    This function writes the given prediction to a text file as a record
    '''
    logging.info('Writing grades to a file...')

    # Detecting the operating system and setting the downloads folder path accordingly
    if os.name == 'nt':  # Windows
        downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
    elif os.uname().sysname == 'Darwin':  # macOS
        downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
    else:  # Linux and other UNIX-like OS
        downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
    
    # Create the "Grading Results" folder inside the Downloads folder if it doesn't exist
    grading_results_folder = os.path.join(downloads_folder, 'Grading Results')
    if not os.path.exists(grading_results_folder):
        os.makedirs(grading_results_folder)
    
    # Set the file path within the "Grading Results" folder
    file_path = os.path.join(grading_results_folder, 'grading_results.txt')

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(f'{grade_response}\n')


def combine_contents_into_message(grading_criteria, assignment_content):
    """
    Combine the contents of two strings and format the message.

    Args:
    - grading_criteria (str): Content of the first string.
    - assignment_content (str): Content of the second string.

    Returns:
    - list: A list containing a dictionary with the combined and formatted message.
    """
    logging.info('Creating chat message for open ai')

    # Combine the contents
    message = f'''{grading_criteria}\n{assignment_content}'''

    # Prepare the message
    message = message.replace("\n", "\\n")
    message = message.strip()

    # Format the message as per the structure you showed
    message_object = [{"role": "user", "content": message}]

    return message_object
