from settings import app_secrets

# Personal Data
RESULTS_EMAIL = app_secrets.RESULTS_EMAIL
FIRST_NAME = app_secrets.FIRST_NAME

# OpenAI data
OPENAI_API_KEY = app_secrets.OPENAI_API_KEY
ENGINE_NAME = 'gpt-4'
BACKUP_ENGINE_NAME = 'gpt-3.5-turbo-16k'
CHAT_COMPLETIONS_URL = 'https://api.openai.com/v1/chat/completions'

# Communication data
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SENDER_EMAIL = app_secrets.SENDER_EMAIL
SENDER_EMAIL_PASSWORD = app_secrets.SENDER_EMAIL_PASSWORD
