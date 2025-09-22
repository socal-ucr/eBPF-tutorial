root@danwong-bpf-testing:/workspace/client/src/python/examples# cat my_test_grpc.py
import sys
import time
import threading
from datetime import datetime
import numpy as np
import tritonclient.grpc as grpcclient
from tritonclient.utils import InferenceServerException

def send_request(grpc_client, model_name, rps):
    # Prepare input data
    inputs = grpcclient.InferInput("data_0", [3, 224, 224], "FP32")
    input_data = np.zeros([3, 224, 224], dtype=np.float32)
    inputs.set_data_from_numpy(input_data)
    
    # Prepare the request
    outputs = grpcclient.InferRequestedOutput("fc6_1")
    
    try:
        # Record start time
        start_time = time.time()

        # Send the inference request
        response = grpc_client.infer(model_name, inputs=[inputs], outputs=[outputs])
        
        # Record response receive time
        response_time = time.time()

        # Calculate latency
        latency = round((response_time - start_time) * 1000, 5)
        print(f"Latency: {latency} ms")

    except InferenceServerException as e:
        print(f"Failed to send request: {str(e)}")

def send_requests_for_duration(grpc_client, model_name, duration, rps):
    end_time = time.time() + duration
    interval = 1 / rps
    t_count = 0
    while time.time() < end_time:
        t_count = t_count + 1
        thread = threading.Thread(target=send_request, args=(grpc_client, model_name, rps))
        thread.start()
        time.sleep(interval)
    print(f"Total threads: {t_count}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python my_test.py <Duration_in_seconds> <Requests_per_second>")
        sys.exit(1)

    duration = int(sys.argv[1])
    rps = float(sys.argv[2])
    model_name = "densenet_onnx"

    # Hardcoded IP and Port
    ip = "localhost"
    port = "8001"

    # Create a gRPC client
    try:
        grpc_client = grpcclient.InferenceServerClient(url=f"{ip}:{port}")
    except Exception as e:
        print(f"Failed to create gRPC client: {str(e)}")
        sys.exit(1)

    # Send requests for the specified duration
    send_requests_for_duration(grpc_client, model_name, duration, rps)