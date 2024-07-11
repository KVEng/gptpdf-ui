from dotenv import load_dotenv
import os
import openai

load_dotenv()

def _load(env, if_none=""):
    if env not in os.environ:
        return if_none
    _v = os.environ[env]
    if _v == "":
        _v = if_none
    return _v

OpenAI_Key     = os.environ['OPENAI_API_KEY']
OpenAI_BaseUrl = _load('OPENAI_BASE_URL', 'https://api.openai.com/v1')
Host           = _load('HOST', '127.0.0.1')
Port           = int(_load('PORT', '5000'))
Model          = _load('MODEL', 'gpt-4o')
MaxThread      = int(_load('MAX_THREAD', '8'))
TranslateModel = _load('TRANSLATE_MODEL', 'gpt-3.5-turbo')


OpenAIClient = openai.Client(api_key=OpenAI_Key, base_url=OpenAI_BaseUrl)