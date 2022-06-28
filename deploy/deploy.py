from pyexpat import model
import uvicorn
from joblib import load
from fastapi import FastAPI
import os



app = FastAPI(title="Remote Community Power Usage")

model_unvailable_msg="Model NOT Available"


# ================================ Test Code =============================================================
# file_path = os.path.realpath(__file__)
# dir_path = os.path.dirname(file_path)
# root_path = os.path.dirname(dir_path)
# model_path = root_path+"/artifacts/models/pickled_model.pkl"
# model = load(model_path)
# results = model.predict(fh=2)
# print(results)
# ================================ Test Code =============================================================

@app.get("/")
async def root():
    return {"message": "Remote Community Power Usage"}

@app.post("/predict", status_code=200)
async def predict(fh: int):
    """
    Make predictions with the model
    """
    try:
        file_path = os.path.realpath(__file__)
        dir_path = os.path.dirname(file_path)
        # root_path = os.path.dirname(dir_path)
        # we can also download the model from a remote location and load it
        # model_path = root_path+"/artifacts/models/pickled_model.pkl"
        model_path = dir_path+"/pickled_model.pkl"
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
