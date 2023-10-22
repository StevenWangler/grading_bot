"""
Email Communication Module

This module provides functionalities related to sending emails to users.
It encapsulates the SMTP logic and provides a cleaner interface for email communication.

Dependencies:
- email.mime.text: To construct MIME text messages.
- smtplib: To handle SMTP communication.
- time: To introduce delays for retries.
- socket: To handle socket-related errors.
- logging: To log application events and errors.
- settings.settings: To access application-specific settings.
"""

from email.mime.text import MIMEText
import smtplib
import time
import socket
import logging
from settings import settings


def send_email_to_user(message):
    '''
    Sends an email with the given message to multiple users.

    Parameters:
    - email_addresses (dict): A dictionary where keys are email addresses and values are user names.
    - message (str): The message content to be sent to the users.

    Uses the sender's email from settings.SENDER_EMAIL.
    
    Raises:
    - smtplib.SMTPException: If there's an error during the SMTP communication.
    - socket.gaierror: If there's a socket-related error.

    Note:
    - Logging is done for informational and error scenarios.
    '''
    logging.info(f'Sending our grading results to {settings.RESULTS_EMAIL}')
    try:
        username = settings.SENDER_EMAIL
        smtp_connection = create_smtp_connection(username)
        send_email(smtp_connection, message)
        close_smtp_connection(smtp_connection)
    except smtplib.SMTPException as _e:
        logging.error('An SMTP error occurred: %s', {_e})
    except socket.gaierror as _e:
        logging.error('A socket error occurred: %s', {_e})


def send_email(smtp_connection, message, max_retries: int = 3):
    '''
    Sends a snow day prediction email to a single recipient. If delivery fails, it will retry
    up to the specified maximum number of retries.

    Parameters:
    - smtp_connection: The active SMTP connection object to use for sending the email.
    - message (str): The main content of the email.
    - email (str): The recipient's email address.
    - first_name (str): The recipient's first name for personalizing the email subject.
    - username (str): The sender's email address.
    - max_retries (int, optional): Maximum number of delivery retries if an SMTP exception 
    occurs. Default is 3.

    Note:
    - If the delivery fails after the maximum number of retries, an error will be logged.
    - On each failed delivery attempt, a warning will be logged and the function will wait 
    for 2 seconds before retrying.
    '''
    recipient = f'{settings.RESULTS_EMAIL}'
    message = f'{message}\n\nBest,\nGrading Bot'
    msg = MIMEText(message)
    msg['From'] = settings.SENDER_EMAIL
    msg['To'] = recipient
    msg['Subject'] = f'{settings.FIRST_NAME}, your grading is done!'
    retries = 0
    while retries < max_retries:
        try:
            smtp_connection.send_message(msg)
            status = smtp_connection.noop()[0]
            if status == 250:
                logging.info('Message delivered to %s', recipient)
                break

            retries += 1
            logging.warning('Delivery failed for %s. Retrying... (retry %s of %s)', recipient, retries, max_retries)
        except smtplib.SMTPException as _e:
            retries += 1
            logging.warning('SMTPException occurred when delivering message to %s. Retrying... (retry %s of %s) (%s)',recipient, retries, max_retries, str(_e))
            time.sleep(2)  # delay before retrying
    if retries == max_retries:
        logging.error('Delivery failed for %s after %s retries', recipient, max_retries)


def create_smtp_connection(username):
    '''
    Creates and returns an authenticated SMTP connection for sending emails.

    Parameters:
    - username (str): The email address used for authentication with the SMTP server.

    Returns:
    - smtplib.SMTP: An authenticated SMTP connection object.

    Notes:
    - This function uses SMTP server settings (server address and port) from the settings module.
    - It also uses the sender's email password from the settings module for authentication.
    - The function initiates a secure TLS connection with the server.
    - Designed primarily for Gmail servers, but can be adapted for other SMTP servers by updating the settings module.
    '''
    # Here we are going to login to our mail server
    # In this particular case, it's a gmail server hooked to the bots email
    smtp_server = settings.SMTP_SERVER
    smtp_port = settings.SMTP_PORT
    smtp_connection = smtplib.SMTP(smtp_server, smtp_port)
    smtp_connection.starttls()
    smtp_connection.login(username, settings.SENDER_EMAIL_PASSWORD)
    return smtp_connection


def close_smtp_connection(smtp_connection):
    '''
    Closes an active SMTP connection gracefully.

    Parameters:
    - smtp_connection (smtplib.SMTP): An active SMTP connection object that needs to be closed.

    Note:
    - The function calls the 'quit' method, which logs out and closes the connection gracefully.
    '''
    # Close the SMTP connection
    smtp_connection.quit()
