"""
===============================================================================
MALCDF - Analyst Agent (AA)
===============================================================================

File:
    agents/analyst_agent.py

Agent:
    Analyst Agent (AA)

Description:
    This module implements the Analyst Agent responsible for consolidating
    outputs from the other cybersecurity agents into a human-readable
    incident report.

Primary Responsibilities:
    - Consolidate detection results.
    - Consolidate threat intelligence.
    - Consolidate MITRE ATT&CK mappings.
    - Consolidate response recommendations.
    - Produce a structured SOC incident report.
    - Present the incident in a form suitable for human analyst review.

Input:
    - Network event.
    - Detection Agent output.
    - Intelligence Agent output.
    - Response Agent output.

Output:
    Incident report containing:
        - Incident summary
        - Threat classification
        - Severity
        - Source/destination information
        - MITRE ATT&CK technique
        - Recommended response
        - Supporting explanation

Architecture Role:

    Detection
        |
    Intelligence
        |
    Response
        |
        v
    [ Analyst Agent ]
        |
        v
    SOC Incident Report

Research Purpose:
    The Analyst Agent represents the human-facing reasoning and reporting
    layer of the multi-agent cybersecurity system.

Author:
    Karim Mokhtar

Status:
    Research Prototype

===============================================================================
"""
import json 
from openai import OpenAI
from prompts.prompts import ANALYST_SYSTEM_PROMPT

class AnalystAgent:
    def __init__(self,api_key):
        self.client =OpenAI(
                base_url="https://backend.sovereigneg.com/v1",
            api_key=api_key)

        self.system_prompt = ANALYST_SYSTEM_PROMPT
        
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

    