from settings import app_secrets

# OpenAI data
OPENAI_API_KEY = app_secrets.OPENAI_API_KEY
ENGINE_NAME = 'gpt-3.5-turbo'
ENGINE_TEMPERATURE = 1
ENGINE_TOP_P = 1
ENGINE_N = 1
ENGINE_STREAM = False
ENGINE_STOP = None
ENGINE_MAX_TOKENS = float('inf')
ENGINE_PRESENCE_PENALTY = 0
ENGINE_FREQUENCY_PENALTY = 0
ENGINE_LOGIT_BIAS = None
ENGINE_USER = None
CHAT_COMPLETIONS_URL = 'https://api.openai.com/v1/chat/completions'
IMAGE_GENERATION_URL = 'https://api.openai.com/v1/images/generations'
