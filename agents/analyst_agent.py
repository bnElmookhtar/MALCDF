import json 
from openai import OpenAI

class AnalystAgent:
    def __init__(self,api_key):
        self.client =OpenAI(
                base_url="https://backend.sovereigneg.com/v1",
            api_key=api_key)

        self.system_prompt = """
You are a Cybersecurity Analyst Agent.
Create a concise incident report.

Include:

- threat
- severity
- source
- destination
- protocol
- port
- MITRE ATT&CK technique
- recommended response
- explanation

Return valid JSON.
"""

    def analyse(self,event,detection,intelligence,report):
        payload = {
            "event":event,
            "detection":detection,
            "intelligence":intelligence,
            "report":report
        }

        result = self.client.chat.completions.create(
            model = "gpt-oss-20b",
            messages=[{
                "role":"system",
                "content":self.system_prompt
            },
            {
                "role":"user",
                "content":json.dumps(payload)
            }

            ],
            temperature = 0,
        )
        return result.choices[0].message.content 

    