import logging
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Configuration for Data Generation ---
NUM_RECORDS = 500
OUTPUT_DIR = "cybersecurity_agentic_rag/data/processed"
OUTPUT_FILENAME = "synthetic_cyber_events.csv"

# --- Sample Data Pools ---
USERS = ['admin', 'jdoe', 'asmith', 'guest', 'system_svc']
IPS = [f"192.168.1.{i}" for i in range(10, 50)] + [f"10.0.0.{i}" for i in range(5, 20)]
MALICIOUS_IPS = [f"185.220.101.{i}" for i in range(1, 10)] + [f"203.0.113.{i}" for i in range(1, 10)]
HOSTS = [f"workstation-{i:02d}.corp.local" for i in range(1, 21)]
CVES = ['CVE-2023-1234', 'CVE-2023-5678', 'CVE-2024-9101', 'CVE-2024-1121']
MALWARE_SIGS = ['Trojan.Generic.12345', 'Ransom.WannaCry.v2', 'Spy.ZeuS.54321', 'Dropper.Emotet.8']

EVENT_TEMPLATES = [
    {"template": "Successful login for user '{user}' from IP {ip}", "is_malicious": 0, "type": "Authentication"},
    {"template": "Failed login for user '{user}' from IP {ip}", "is_malicious": 0, "type": "Authentication"},
    {"template": "Multiple failed login attempts for user '{user}' from IP {ip}", "is_malicious": 1, "type": "Brute-force"},
    {"template": "Connection to known malicious C2 server {malicious_ip} from host {host}", "is_malicious": 1, "type": "C2 Communication"},
    {"template": "Malware signature '{malware_sig}' detected on host {host}", "is_malicious": 1, "type": "Malware Detection"},
    {"template": "Exploitation of vulnerability {cve} detected on host {host}", "is_malicious": 1, "type": "Exploitation"},
    {"template": "Anomalous network traffic detected from {ip} to {host}", "is_malicious": 0, "type": "Network Anomaly"},
    {"template": "User '{user}' accessed a sensitive file.", "is_malicious": 0, "type": "File Access"},
]

def generate_synthetic_data():
    """Generates a synthetic dataset of cybersecurity events and saves it to a CSV file."""
    logging.info(f"Generating {NUM_RECORDS} synthetic records...")

    records = []
    start_time = datetime.now() - timedelta(days=1)

    for i in range(NUM_RECORDS):
        event_spec = random.choice(EVENT_TEMPLATES)

        # 50% chance to override and make a malicious-looking event benign (false positive)
        is_truly_malicious = event_spec['is_malicious']
        if is_truly_malicious and random.random() < 0.5:
            is_truly_malicious = 0

        description = event_spec['template'].format(
            user=random.choice(USERS),
            ip=random.choice(IPS),
            malicious_ip=random.choice(MALICIOUS_IPS),
            host=random.choice(HOSTS),
            cve=random.choice(CVES),
            malware_sig=random.choice(MALWARE_SIGS)
        )

        timestamp = start_time + timedelta(seconds=i * 10)

        records.append({
            'timestamp': timestamp.isoformat(),
            'event_id': f"EVENT-{i:04d}",
            'description': description,
            'event_type': event_spec['type'],
            'is_malicious_ground_truth': is_truly_malicious
        })

    df = pd.DataFrame(records)

    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILENAME)

    df.to_csv(output_path, index=False)
    logging.info(f"Synthetic data successfully saved to {output_path}")

if __name__ == '__main__':
    generate_synthetic_data()
