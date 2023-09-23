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
    try:
        log_dir = 'settings'
        log_file = 'application_log.log'

        # Create the log directory if it doesn't exist
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        log_file_path = os.path.join(log_dir, log_file)

        logging.basicConfig(filename=log_file_path, 
                            level=logging.INFO, 
                            format='%(asctime)s:%(levelname)s:%(message)s')

        current_time = datetime.datetime.now()
        logging.info('---- APPLICATION START (current date/time is: %s) ----', current_time)
    except Exception as ex:
        print(f"An error occurred while configuring logging: {ex}")


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
