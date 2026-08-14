import json 
from groq import Groq
from openai import OpenAI

class IntelligenceAgent:

    def __init__(self,api_key):
        self.client = OpenAI(
                base_url="https://backend.sovereigneg.com/v1",

            api_key=api_key)

        self.system_prompt = """
You are a Cyber Threat Intelligence Agent.

Analyze the detection result and network event.

Identify:
- threat context
- MITRE ATT&CK technique
- relevant indicators
- attack explanation

Return ONLY JSON.

{
    "threat_type": "...",
    "mitre_attack": "...",
    "context": "...",
    "indicators": []
}
"""

    def analyze(self,event,detection):
        payload = {
            "event":event,
            "detection":detection
        }

        response = self.client.chat.completions.create(
            model = "gpt-oss-20b",
            messages =[
                {
                    "role":"system",
                     "content":self.system_prompt
                },
                {
                    "role":"user",
                    "content":json.dumps(payload)
                }
            ],
            temperature=0
        )
        return json.loads(response.choices[0].message.content)
    