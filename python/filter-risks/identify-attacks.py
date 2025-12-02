import pandas as pd
import re
class LogAnalysis:
    errorTypes = ['secutrity','alert','warn','critical','error']
    # Keywords that define risky events
    RISK_KEYWORDS = [
        "ERROR", "CRITICAL", "SECURITY", "ALERT",
        "SQL Injection", "Brute force", "DDoS", "Malware",
        "Unauthorized", "Ransomware", "Path Traversal",
        "Suspicious", "Invalid API key", "API key leaked",
        "Exposed", "PowerShell", "attack",'api_key'
    ]

    # API key patterns (regex)
    API_KEY_PATTERNS = [
        r"AKIA[A-Z0-9]{8,}",
        r"sk_test_[a-zA-Z0-9]+",
        r"ghp_[a-zA-Z0-9]+"
    ]
    def __init__(self,path):
        self.path = path
    def getLogs(self,path):
        with open(path,'r') as file:
            for f in file:
                yield f
    def start(self):
        for log in self.getLogs(self.path):
          content = log.lower()
          for i in LogAnalysis.errorTypes:
              if i in content:
                  print("Issues detected",i,content)
                  break
    def strongSearch(self):
        risk_reports = []
        for log in self.getLogs(self.path):
            content = log.lower()
            for i in LogAnalysis.RISK_KEYWORDS:
                if re.search(i.lower(),content):
                    risk_reports.append(
                        {"type":i,
                        "logmessage":content
                        }
                    )
                    break
        print("Total Risks Reported:",len(risk_reports))  
        # print(risk_reports)
        self.save_risk(risk_reports)
    def save_risk(self,risk_reports):
        with open("risks_logs.txt","w") as f:
            for item in risk_reports:
                f.writelines(f"type:{item['type']},logmessage:{item['logmessage']}")






# logAnalysis = LogAnalysis("logs.txt")
# logAnalysis.start()
        
logAnalysis = LogAnalysis("logs1.txt")
logAnalysis.strongSearch()
            

    
