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
            # Adding two new lines for separation, the student's name, and their grade
            file.write(f'\n\nStudent: {student_name}\nGrade: {grade_response}')

    except Exception as ex:
        logging.error(f"An error occurred while writing to the file: {ex}")


def combine_contents_into_message(grading_criteria, assignment_content):
    """
    Combine the contents of two strings and format the message.

    Args:
    - grading_criteria (str): Content of the first string.
    - assignment_content (str): Content of the second string.

    Returns:
    - list: A list containing a dictionary with the combined and formatted message.
    """
    try:
        logging.info('Creating chat message for open ai')

        # Combine the contents
        message = f'''{grading_criteria}\n{assignment_content}'''

        # Prepare the message
        message = message.replace("\n", "\\n")
        message = message.strip()

        # Format the message as per the structure you showed
        message_object = [{"role": "user", "content": message}]

        return message_object
    except Exception as ex:
        logging.error(f'An error occurred in combine_contents_into_message. Error: {ex}')
        return None
