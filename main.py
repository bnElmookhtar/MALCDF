"""
===============================================================================
MALCDF - Main Application Orchestrator
===============================================================================

File:
    main.py

Project:
    Multi-Agent LLM Cyber Defense Framework (MALCDF)

Description:
    This module is the main entry point for the MALCDF cybersecurity system.
    It coordinates the complete threat detection and incident response
    pipeline.

    The system receives network events, processes them through the threat
    detection stage, and, when suspicious activity is detected, forwards the
    event through the multi-agent cybersecurity workflow:

        Network Event
              |
              v
        Threat Detection Agent (TDA)
              |
              v
        Threat Intelligence Agent (TIA)
              |
              v
        Response Coordination Agent (RCA)
              |
              v
        Analyst Agent (AA)
              |
              v
        Final SOC Incident Report

Responsibilities:
    - Initialize the system components.
    - Load environment variables and configuration.
    - Initialize cybersecurity agents.
    - Receive/process network events.
    - Coordinate communication between agents.
    - Collect agent outputs.
    - Generate final incident reports.
    - Store results for dashboard visualization.

Input:
    - Network flow/event data.
    - Environment configuration.
    - LLM API credentials.

Output:
    - Threat classification.
    - Threat intelligence information.
    - MITRE ATT&CK mapping.
    - Response recommendations.
    - Analyst incident report.

Research Context:
    This module implements the orchestration layer of the MALCDF-inspired
    multi-agent cybersecurity architecture and serves as the central execution
    point for experiments.

Security Note:
    API keys must never be hard-coded in this file. Credentials must be loaded
    from environment variables or a secure secrets manager.

Author:
    Karim Mokhtar

Status:
    Research Prototype

===============================================================================
"""

from dotenv import load_dotenv
import os 
from agents.detection_agent import DetectionAgent
from agents.analyst_agent import AnalystAgent
from agents.intelligence_agent import IntelligenceAgent
from agents.response_agent import ResponseAgent

import time


load_dotenv()

API_KEY = os.getenv("OPEN_AI_KEY")


start_time = time.perf_counter()

detection_agent = DetectionAgent(api_key=API_KEY)
analyst_agent = AnalystAgent(API_KEY)
response_agent = ResponseAgent(API_KEY)
intelligence_agent = IntelligenceAgent(API_KEY)


event = {

    "src_ip": "192.168.1.199",

    "dst_ip": "10.0.0.57",

    "port": 18530,

    "protocol": "UDP",

    "bytes_sent": 162548
}

detection = detection_agent.analyse(event)
print(detection)

intelligence = intelligence_agent.analyze(event,detection)
print(intelligence)

response = response_agent.generate_response(event,detection,intelligence)
print(response)

report = analyst_agent.analyse(event,detection,intelligence,response)
print(report)

end_time = time.perf_counter()

print(f"Execution time: {end_time - start_time:.2f} seconds")
