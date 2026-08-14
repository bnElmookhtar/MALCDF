"""
===============================================================================
MALCDF - Threat Intelligence Agent (TIA)
===============================================================================

File:
    agents/intelligence_agent.py

Agent:
    Threat Intelligence Agent (TIA)

Description:
    This module implements the Threat Intelligence Agent responsible for
    enriching detected security events with additional cybersecurity context.

Primary Responsibilities:
    - Analyze detection results.
    - Interpret the detected threat.
    - Identify relevant attack techniques.
    - Map threats to MITRE ATT&CK techniques.
    - Provide contextual threat intelligence.
    - Identify relevant indicators and behavioral evidence.

Input:
    - Original network event.
    - Threat Detection Agent result.

Output:
    Structured threat intelligence information containing:
        - Threat type
        - MITRE ATT&CK technique
        - Threat context
        - Indicators
        - Supporting explanation

Example:

    {
        "threat_type": "Data Exfiltration",
        "mitre_attack": "T1041",
        "context": "Possible outbound data transfer",
        "indicators": []
    }

Architecture Role:

    Detection Agent
          |
          v
    [ Threat Intelligence Agent ]
          |
          v
    Threat Intelligence
          |
          v
    Response Agent

Research Purpose:
    This agent provides contextual reasoning and cybersecurity knowledge
    enrichment before a response recommendation is generated.

Author:
    Karim Mokhtar

Status:
    Research Prototype

===============================================================================
"""

import json 
from openai import OpenAI
from prompts.prompts import INTELLIGENCE_SYSTEM_PROMPT

class IntelligenceAgent:

    def __init__(self,api_key):
        self.client = OpenAI(
                base_url="https://backend.sovereigneg.com/v1",

            api_key=api_key)

        self.system_prompt =INTELLIGENCE_SYSTEM_PROMPT
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
    