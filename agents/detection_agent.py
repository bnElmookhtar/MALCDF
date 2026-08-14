"""
===============================================================================
MALCDF - Threat Detection Agent (TDA)
===============================================================================

File:
    agents/detection_agent.py

Agent:
    Threat Detection Agent (TDA)

Description:
    This module implements the Threat Detection Agent responsible for analyzing
    network events and determining whether observed activity is potentially
    malicious or benign.

Primary Responsibilities:
    - Analyze network events.
    - Identify suspicious behavior.
    - Classify potential attack types.
    - Estimate threat severity.
    - Generate a confidence score.
    - Provide an initial explanation for the classification.

Input:
    Network event containing features such as:
        - Source IP
        - Destination IP
        - Protocol
        - Destination port
        - Packet/flow statistics
        - Byte counts
        - Timing information

Output:
    Structured detection result containing:
        - Attack/benign classification
        - Threat type
        - Severity
        - Confidence
        - Reasoning/explanation

Example Output:

    {
        "is_attack": true,
        "threat_type": "Data Exfiltration",
        "severity": "medium",
        "confidence": 0.82
    }

Architecture Role:

    Network Event
          |
          v
    [ Threat Detection Agent ]
          |
          v
    Detection Result
          |
          v
    Threat Intelligence Agent

Research Purpose:
    The TDA represents the first intelligent decision-making stage in the
    multi-agent cybersecurity architecture.

Author:
    Karim Mokhtar

Status:
    Research Prototype

===============================================================================
"""


from openai import OpenAI
import json

from prompts.prompts import DETECTION_SYSTEM_PROMPT
class DetectionAgent:

    def __init__(self,api_key):
        self.client = OpenAI(    
            base_url="https://backend.sovereigneg.com/v1",
            api_key=api_key)

        self.system_prompt = DETECTION_SYSTEM_PROMPT

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

