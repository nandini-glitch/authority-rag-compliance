from dotenv import load_dotenv
load_dotenv()
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv('GEMINI_API_KEY'), base_url='https://generativelanguage.googleapis.com/v1beta/openai/')
try:
    r = client.chat.completions.create(model='gemini-3.5-flash-lite', messages=[{'role':'user','content':'ping'}], max_tokens=2)
    print('SUCCESS - flash-lite works')
except Exception as e:
    print('FAILED:', str(e))
