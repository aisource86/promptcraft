from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import grpc
import json
import service_pb2
import service_pb2_grpc

# Initialize FastAPI
app = FastAPI()

# Define the request and response models using Pydantic
class TestMessageRequest(BaseModel):
    payload: str

class TestMessageResponse(BaseModel):
    response: str

# Helper function to get deploy agent (gRPC client)
def get_deploy_agent():
    channel = grpc.insecure_channel("localhost:50055")
    return service_pb2_grpc.MyServiceStub(channel)

# Endpoint to handle TestMessage
@app.post("/test-message", response_model=TestMessageResponse)
def test_message(request: TestMessageRequest):
    try:
        # Parse the payload from the request
        data = json.loads(request.payload)

        # Call the gRPC client
        deploy_agent = get_deploy_agent()
        grpc_request = service_pb2.Request4(payload=json.dumps(data))
        deploy = deploy_agent.PushCode(grpc_request).response

        print(deploy)

        return TestMessageResponse(response="success pushed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Another helper function for push_grpc_client_code
def push_grpc_client_code(code_json, path, remote_push=False):
    try:
        testing_client = get_deploy_agent()  # Use the same deploy agent
        grpc_request = service_pb2.Request3(
            payload=json.dumps({"code_json": code_json, "path": path, "remote_push": remote_push})
        )
        testing = testing_client.TestMessage(grpc_request).response
        return testing
    except Exception as e:
        raise Exception(f"Error pushing gRPC client code: {e}")

# Run the server using Uvicorn (if needed)
if __name__ == "__main__":
    import uvicorn
    print("FastAPI server is running on port 8000...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
