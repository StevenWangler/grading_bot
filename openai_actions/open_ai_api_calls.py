'''
The open ai api calls file handles the chat completion
request to open ai. Also will handle any other api cals
to open ai.
'''
import json
import logging
import requests
from settings import settings


def generate_chat_completion(grading_criteria):
    '''
    This method calls the chat completion endpoint from openai
    '''
    try:
        logging.info('Generating the chat completion message')
        url = settings.CHAT_COMPLETIONS_URL
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {settings.OPENAI_API_KEY}'
        }
        data = {
            'model': settings.ENGINE_NAME,
            'messages': grading_criteria,
        }
        response = requests.post(url,
                                 headers=headers,
                                 data=json.dumps(data),
                                 timeout=30)
        response_data = json.loads(response.text)
        completion_message = response_data['choices'][0]['message']['content']
        logging.info('Returning the completed message')
        return completion_message
    except (requests.exceptions.RequestException, json.JSONDecodeError) as ex:
        logging.error('An error occurred while calling the OpenAI chat completion endpoint: %s', ex)
        return None
    