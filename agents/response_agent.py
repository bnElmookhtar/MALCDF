import json
from openai import OpenAI


class ResponseAgent:

    def __init__(self, api_key):

        self.client = OpenAI(
            base_url="https://backend.sovereigneg.com/v1",
            api_key=api_key
        )

        self.system_prompt = """
You are a Cybersecurity Response Coordination Agent.

Based on the detected threat and intelligence,
recommend defensive actions.

DO NOT perform the actions.

Return JSON:

{
    "priority": "...",
    "recommended_actions": [],
    "reason": "..."
}
"""

    def generate_response(
        self,
        event,
        detection,
        intelligence
    ):

        payload = {
            "event": event,
            "detection": detection,
            "intelligence": intelligence
        }

        response = self.client.chat.completions.create(

            model="gpt-oss-20b",

            messages=[
                {
                    "role": "system",
                    "content": self.system_prompt
                },
                {
                    "role": "user",
                    "content": json.dumps(payload)
                }
            ],

            temperature=0
        )

        return json.loads(
            response.choices[0].message.content
        )