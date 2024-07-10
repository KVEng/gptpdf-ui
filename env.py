from dotenv import load_dotenv
import os

load_dotenv()

OpenAI_Key     = os.environ['OPENAI_API_KEY']
OpenAI_BaseUrl = os.environ['OPENAI_BASE_URL']
Host           = os.environ['HOST']
Port           = int(os.environ['PORT'])