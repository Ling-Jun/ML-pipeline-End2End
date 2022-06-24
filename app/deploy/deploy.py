from pyexpat import model
import uvicorn
from joblib import load
from fastapi import FastAPI
import os
import neptune.new as neptune

app = FastAPI(title="Remote Community Power Usage")

model_unvailable_msg="Model NOT Available"

@app.get("/")
async def root():
    return {"message": "Remote Community Power Usage"}

file_path = os.path.realpath(__file__)
dir_path = os.path.dirname(file_path)
root_path = os.path.dirname(dir_path)

def fetch_model(path):
    run = neptune.init(project="lingjun/Remote-Community-Power-Usage", 
    api_token="eyJhcGlfYWRkcmVzcyI6Imh0dHBzOi8vYXBwLm5lcHR1bmUuYWkiLCJhcGlfdXJsIjoiaHR0cHM6Ly9hcHAubmVwdHVuZS5haSIsImFwaV9rZXkiOiI2ZDQ3M2M3Yy0xYjNkLTRmMDYtOTYyNi00ODE4ZjgzZjA2MGMifQ==",
    run="REM-19")
    run["model/pickled_model"].download(root_path+path)
    print("MODEL FETCHED!")

fetch_model(path="/artifacts/models")

@app.post("/predict", status_code=200)
async def predict(fh: int):
    try:
        # we can also download the model from a remote location and load it
        model_path = root_path+"/artifacts/models/pickled_model.pkl"
        # joblib can load .pkl model
        model = load(model_path)
    except:
        print("Model not available")
        return model_unvailable_msg
    results = model.predict(fh=fh)

    return results



if __name__ == "__main__":
    # Use this for debugging purposes only
    # reload=True appears to be broken in uvicorn.run(), but not in CLI
    uvicorn.run(app, host="localhost", port=8001, log_level="debug", reload=False)
