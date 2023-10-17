'''
The open ai api calls file handles the chat completion
request to open ai. Also will handle any other api cals
to open ai.
'''
import logging
import openai
from settings import settings
openai.api_key = settings.OPENAI_API_KEY


def generate_chat_completions(grading_criteria):
    '''
    This method calls the chat completion endpoint from openai using the openai Python package.
    '''
    try:
        logging.info('Generating the chat completion message')

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=grading_criteria
        )

        completion_message = response.choices[0].message.content
        logging.info('Returning the completed message')
        return completion_message

    except openai.error.OpenAIError as ex:
        logging.error('An error occurred while calling the OpenAI chat completion endpoint: %s', ex)
        return None
