import os
import neptune.new as neptune
from joblib import load
import sys  

# get the absolute path of this file
real_path = os.path.realpath(__file__)
# get the root dir of this entire project.
dir_path = os.path.dirname(real_path)
dir_path = os.path.dirname(dir_path)
root_path = os.path.dirname(dir_path)
print("Root path is "+root_path)


# adding deploy dir to the system path so that we can import the model_unvailable_msg 
sys.path.insert(0, root_path+'/deploy')
from deploy import model_unvailable_msg

run = neptune.init(project="lingjun/Remote-Community-Power-Usage", 
    api_token="eyJhcGlfYWRkcmVzcyI6Imh0dHBzOi8vYXBwLm5lcHR1bmUuYWkiLCJhcGlfdXJsIjoiaHR0cHM6Ly9hcHAubmVwdHVuZS5haSIsImFwaV9rZXkiOiI2ZDQ3M2M3Yy0xYjNkLTRmMDYtOTYyNi00ODE4ZjgzZjA2MGMifQ==",
    # the run id of an existing run that has the model. Question is, HOW CAN WE not specify the run id but fetch the latest run?
    run="REM-50"
)  


file_path = os.path.realpath(__file__)
# get the root dir of this entire project.
dir_path = os.path.dirname(file_path)

# Download model to the specified directory
run["model/pickled_model"].download(dir_path)
print("Model is successfully downloaded!")

# we can also download the model from a remote location and load it
model_path = root_path+"/artifacts/models/pickled_model.pkl"
model = load(model_path)
print("Model is successfully loaded!")