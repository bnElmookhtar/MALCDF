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
