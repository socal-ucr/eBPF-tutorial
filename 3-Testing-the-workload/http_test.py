import requests
import time
import sys
import threading
import json

def send_request(target_url):
    data = {
        "inputs": [
            {
                "name": "data_0",
                "data": [0.0] * 224 * 224 * 3,
                "datatype": "FP32",
                "shape": [3, 224, 224]
            }
        ]
    }
    try:
        response = requests.post(target_url, json=data)
        if response.status_code == 200:
            print("Request successful.")
        else:
            print(f"Request failed with status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending request: {e}")

def send_requests_for_duration(target_url, duration, rps=1):
    """Send requests at a fixed rate (default 1 RPS) for the specified duration."""
    end_time = time.time() + duration
    interval = 1 / rps
    t_count = 0
    while time.time() < end_time:
        t_count += 1
        thread = threading.Thread(target=send_request, args=(target_url,))
        thread.start()
        time.sleep(interval)
    print(f"Total threads created: {t_count}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 http_client.py <Duration_in_seconds>")
        sys.exit(1)

    duration = int(sys.argv[1])
    target_url = "http://localhost:8000/v2/models/densenet_onnx/infer"
    print(f"Sending HTTP inference requests for {duration} seconds...")
    send_requests_for_duration(target_url, duration)
