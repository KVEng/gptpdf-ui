from dotenv import load_dotenv
import os

load_dotenv()

def _load(env, if_none=""):
    _v = os.environ[env]
    if _v == "":
        _v = if_none
    return _v

OpenAI_Key     = os.environ['OPENAI_API_KEY']
OpenAI_BaseUrl = os.environ['OPENAI_BASE_URL']
Host           = _load('HOST', '127.0.0.1')
Port           = int(_load('PORT', '5000'))
Model          = _load('MODEL', 'gpt-4o')
MaxThread      = int(_load('MAX_THREAD', '8'))