from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
from git_client import push_client_code
from git_api import push_server_code

# Initialize FastAPI app
app = FastAPI()

# Pydantic models for request and response
class PushCodeRequest(BaseModel):
    payload: str

class PushCodeResponse(BaseModel):
    response: str

# Define the PushCode endpoint
@app.post("/push-code", response_model=PushCodeResponse)
def push_code(request: PushCodeRequest):
    try:
        # Parse the JSON payload
        data = json.loads(request.payload)
        print(data)

        # Call the appropriate function based on the "is_server" flag
        if data.get("is_server"):
            push_server_code(data["code_json"])
        else:
            push_client_code(data["code_json"], data["path"], data["remote_push"])

        # Return a success response
        return PushCodeResponse(response="Hello! This is a FastAPI response.")
    except Exception as e:
        # Log the exception and return an error response
        print(e)
        raise HTTPException(status_code=500, detail="An error occurred while processing the request.")

# Run the server using Uvicorn (if needed)
if __name__ == "__main__":
    import uvicorn
    print("FastAPI server is running on port 8000...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
