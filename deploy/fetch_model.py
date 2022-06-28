import os
import neptune.new as neptune
from joblib import load

env_vars = os.environ
# print(env_vars)

run = neptune.init(project="lingjun/Remote-Community-Power-Usage", 
    api_token=env_vars['NEPTUNE_API_TOKEN'],
    # the run id of an existing run that has the model. Question is, HOW CAN WE not specify the run id but fetch the latest run?
    run="REM-50"
)  


file_path = os.path.realpath(__file__)
# get the root dir of this entire project.
dir_path = os.path.dirname(file_path)

run["model/pickled_model"].download(dir_path)
print("Model is successfully downloaded to "+dir_path+"!")

# we can also download the model from a remote location and load it
model_path = dir_path+"/pickled_model.pkl"
model = load(model_path)
print("Model is successfully loaded!")