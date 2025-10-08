import sys
import time
import threading
import numpy as np
import tritonclient.grpc as grpcclient
from tritonclient.utils import InferenceServerException

# Default requests per second
DEFAULT_RPS = 1  # You can adjust this as needed

def send_request(grpc_client, model_name):
    inputs = grpcclient.InferInput("data_0", [3, 224, 224], "FP32")
    input_data = np.zeros([3, 224, 224], dtype=np.float32)
    inputs.set_data_from_numpy(input_data)
    
    outputs = grpcclient.InferRequestedOutput("fc6_1")
    
    try:
        print("Sending request...")
        response = grpc_client.infer(model_name, inputs=[inputs], outputs=[outputs])
        print("Response received successfully.")
    except InferenceServerException as e:
        print(f"Failed to send request: {str(e)}")

def send_requests_for_duration(grpc_client, model_name, duration, rps=DEFAULT_RPS):
    end_time = time.time() + duration
    interval = 1 / rps
    t_count = 0
    while time.time() < end_time:
        t_count += 1
        thread = threading.Thread(target=send_request, args=(grpc_client, model_name))
        thread.start()
        time.sleep(interval)
    print(f"Total threads created: {t_count}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 grpc_client.py <Duration_in_seconds>")
        sys.exit(1)

    duration = int(sys.argv[1])
    model_name = "densenet_onnx"

    ip = "localhost"
    port = "8001"

    try:
        grpc_client = grpcclient.InferenceServerClient(url=f"{ip}:{port}")
        print(f"Connected to Triton server at {ip}:{port}")
    except Exception as e:
        print(f"Failed to create gRPC client: {str(e)}")
        sys.exit(1)

    print(f"Running for {duration} seconds at {DEFAULT_RPS} requests/second...")
    send_requests_for_duration(grpc_client, model_name, duration)

