"""
===============================================================================
MALCDF - Response Coordination Agent (RCA)
===============================================================================

File:
    agents/response_agent.py

Agent:
    Response Coordination Agent (RCA)

Description:
    This module implements the Response Coordination Agent responsible for
    generating defensive recommendations based on detected threats and
    threat-intelligence information.

Primary Responsibilities:
    - Evaluate the detected threat.
    - Determine response priority.
    - Generate defensive recommendations.
    - Recommend containment actions.
    - Recommend investigation and evidence-collection actions.
    - Provide a structured response plan.

Input:
    - Network event.
    - Threat Detection Agent result.
    - Threat Intelligence Agent result.

Output:
    Structured response recommendation containing:
        - Priority
        - Recommended actions
        - Response reasoning

Example:

    {
        "priority": "HIGH",
        "recommended_actions": [
            "Isolate source endpoint",
            "Block suspicious connection",
            "Collect endpoint evidence"
        ]
    }

Safety:
    The research prototype generates recommendations only.
    It must not automatically execute potentially disruptive defensive
    commands without explicit authorization and appropriate safeguards.

Architecture Role:

    Threat Intelligence
            |
            v
    [ Response Coordination Agent ]
            |
            v
    Response Recommendation
            |
            v
       Analyst Agent

Research Purpose:
    This agent investigates whether an LLM/SLM can generate useful,
    structured incident-response recommendations.

Author:
    Karim Mokhtar

Status:
    Research Prototype

===============================================================================
"""


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