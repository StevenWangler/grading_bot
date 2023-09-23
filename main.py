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
        first_run = True

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

        # Loop through each student's folder in the main assignments folder
        for student_folder in os.listdir(assignments_folder):
            student_folder_path = os.path.join(assignments_folder, student_folder)
            
            # Check if it's a directory before proceeding
            if os.path.isdir(student_folder_path):
                
                # Loop through each assignment file in the student's folder
                for assignment_file in os.listdir(student_folder_path):
                    
                    try:
                        assignment_file_path = os.path.join(student_folder_path, assignment_file)
                        
                        # Open and read each assignment file
                        with open(assignment_file_path, 'r', encoding='utf-8') as f:
                            assignment_content = f.read()
                        
                        # Combine the grading criteria and assignment content
                        message = general_functions.combine_contents_into_message(grading_criteria, assignment_content)
                        
                        # Generate the AI response
                        ai_response = open_ai_api_calls.generate_chat_completion(message)
                        
                        # Write the results to a file
                        general_functions.write_results_to_file(ai_response, student_folder, first_run)
                        
                        # Log the graded assignment
                        logging.info(f"Graded {assignment_file} for {student_folder}")

                    except Exception as ex:
                        # Log the error and continue to the next iteration
                        logging.error(f"An error occurred while grading {assignment_file} for {student_folder}: {ex}")
                        messagebox.showinfo('Error!', f'I ran into an error grading the assignment for {student_folder}. Error: {ex}. Click "OK" to continue grading.')
                        continue

                    first_run = False

        messagebox.showinfo('Grading completed!', 'The grading has been completed! Please check your downloads folder for the results.')
        logging.info("Grading completed! Check downloads folder for results.")
    except Exception as ex:
        logging.error(f'An unexpected error occurred in main. Error: {ex}')
        messagebox.showerror('Error!', f'The grading process failed. Error: {ex}')


if __name__ == "__main__":
    general_functions.configure_logging()
    main()
