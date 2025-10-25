from google import genai
import os, json

api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    print('NO_API_KEY')
    raise SystemExit(1)

client = genai.Client(api_key=api_key)

try:
    resp = client.models.embed_content(
        model="embedding-001",
        contents=["hello world"]
    )
    print('OK')
    try:
        print('keys:', resp.__dict__.keys())
    except Exception:
        pass
    print(resp)
except Exception as e:
    print('ERR:', type(e).__name__, str(e))
