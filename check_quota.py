from dotenv import load_dotenv
load_dotenv()
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv('GEMINI_API_KEY'), base_url='https://generativelanguage.googleapis.com/v1beta/openai/')
try:
    r = client.chat.completions.create(model='gemini-2.5-flash', messages=[{'role':'user','content':'ping'}], max_tokens=2)
    print('SUCCESS - quota is clear')
except Exception as e:
    print('FULL ERROR BELOW:')
    print(str(e))
