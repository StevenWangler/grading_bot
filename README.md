# Grading Bot

Grading Bot is a Python application designed to automate the grading process for student assignments. It provides functionality for grading individual student assignments based on specified grading criteria. This README provides an overview of the main components and functionality of the application.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Dependencies](#dependencies)
- [Usage](#usage)
- [File Structure](#file-structure)
- [Configuration](#configuration)
- [License](#license)

## Introduction

The Grading Bot application simplifies the process of grading student assignments by offering the following key features:

- **Automated Grading**: The application automatically grades student assignments based on specified grading criteria.

- **Flexible Input**: Users can select the assignments folder and grading criteria file through a user-friendly interface.

- **Error Handling**: The application includes robust error handling to ensure that grading continues even if issues arise with individual files or during the grading process.

- **Logging**: Detailed logging of the grading process is available to track progress and troubleshoot any problems.

- **API Integration**: The application interfaces with external APIs, such as OpenAI, for grading assignments.

## Features

### Main Entry Point

The main entry point to the Grading Bot application is the `main.py` file.

## File Actions Module
The file_actions module provides a collection of functions to facilitate the grading process:

- Prompting the user to select the assignments folder and grading criteria file.
- Reading and combining all assignment files for individual students.
- Grading the combined content of all assignment files for a single student.
- Writing the grading results to a designated file.
- Logging and user notifications for error handling and process updates.
- General Functions Module
- The general_functions module includes functions for configuring logging and combining contents into a formatted message for the external grading API.

## OpenAI API Calls Module
The open_ai_api_calls module handles chat completion requests to the OpenAI API. It provides the following functionality:

- Generating chat completions using OpenAI's chat completion endpoint.
- Handling retries with a different model if the rate limit is reached.
- Logging and error handling for API calls.
- Settings File
- The settings.py file contains configuration settings, including personal data, OpenAI API credentials, communication data (for sending grading results via email), and engine names.

## Dependencies
The Grading Bot application depends on the following Python libraries and modules:

- logging: For recording the grading process and any potential issues.
- os: For directory and file path operations.
- tkinter: For user interface elements.
- general_functions: Custom module containing auxiliary functions.
- open_ai_api_calls: Custom module for interfacing with the external grading API.
- Make sure to install these dependencies to run the application successfully.

## Usage
To use the Grading Bot application, follow these steps:

- Clone the repository or download the source code.

- Install the required Python libraries and modules mentioned in the Dependencies section.

- Configure the settings in the settings.py file, including personal data, API credentials, and communication settings.

- Run the application by executing main.py:

The application will automatically grade assignments based on the provided criteria and send grading results via email (if configured).

## File Structure
The file structure of the Grading Bot application is as follows:

grading-bot/
│   main.py
│   README.md
│   settings.py
│
├── file_actions.py
├── general_functions.py
├── open_ai_api_calls.py
│
└── settings/
    │   app_secrets.py
    │
    └── application_log.log

- main.py: The main entry point of the application.
- file_actions.py: Module containing functions for file handling and grading.
- general_functions.py: Module with general utility functions.
- open_ai_api_calls.py: Module for interfacing with the OpenAI API.
- settings/: Directory containing configuration files and logs.

## Configuration
The Grading Bot application requires configuration settings, including API keys and personal data. These settings are stored in the settings.py file within the settings directory. You should configure the following settings:

- Personal Data: Specify your email address and first name.
- OpenAI Data: Set your OpenAI API key, engine names, and API endpoint URL.
- Communication Data: Configure SMTP server settings for email delivery.
- Please ensure that you keep your API keys and sensitive information secure.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

### Note: 
Ensure that you have reviewed and configured the application settings before running the Grading Bot. If you encounter any issues or errors during the grading process, refer to the log file (application_log.log) for details.

### Happy grading!