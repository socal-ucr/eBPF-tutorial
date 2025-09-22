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
        start_time = time.time()
        response = requests.post(target_url, json=data)
        
        if response.status_code == 200:
            response_time = time.time()
            latency = round((response_time - start_time) * 1000, 5)
            print(latency)
    except Exception:
        pass 

def send_requests_for_duration(target_url, duration, rps):
    end_time = time.time() + duration
    interval = 1 / rps
    t_count = 0
    while time.time() < end_time:
        t_count += 1
        thread = threading.Thread(target=send_request, args=(target_url,))
        thread.start()
        time.sleep(interval)
    print(f"Total threads: {t_count}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 http.py <Duration_in_seconds> <Requests_per_second>")
        sys.exit(1)

    duration = int(sys.argv[1])
    rps = float(sys.argv[2])
    target_url = "http://localhost:8000/v2/models/densenet_onnx/infer"
    send_requests_for_duration(target_url, duration, rps)