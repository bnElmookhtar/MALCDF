from openai import OpenAI
import json
class DetectionAgent:

    def __init__(self,api_key):
        self.client = OpenAI(    
            base_url="https://backend.sovereigneg.com/v1",
            api_key=api_key)

        self.system_prompt = """
You are a cybersecurity Threat Detection Agent.

Analyze network events and determine whether
the event is benign or malicious.

Return ONLY valid JSON.

Required fields:

{
    "is_attack": true/false,
    "threat_type": "...",
    "severity": "low/medium/high",
    "confidence": 0.0,
    "reason": "..."
}
"""


    def analyse(self , event):
        response = self.client.chat.completions.create(
            model = "gpt-oss-20b",
            messages = [
                {
                    "role":"system",
                    "content":self.system_prompt
                },
                {
                    "role":"user",
                    "content":json.dumps(event)

                }
            ],
            temperature = 0.0,
        )
        result = response.choices[0].message.content
        return json.loads(result)

