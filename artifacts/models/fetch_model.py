import os
import neptune.new as neptune


run = neptune.init(project="lingjun/Remote-Community-Power-Usage", 
    api_token="eyJhcGlfYWRkcmVzcyI6Imh0dHBzOi8vYXBwLm5lcHR1bmUuYWkiLCJhcGlfdXJsIjoiaHR0cHM6Ly9hcHAubmVwdHVuZS5haSIsImFwaV9rZXkiOiI2ZDQ3M2M3Yy0xYjNkLTRmMDYtOTYyNi00ODE4ZjgzZjA2MGMifQ==",
    # the run id of an existing run that has the model. Question is, HOW CAN WE not specify the run id but fetch the latest run?
    run="REM-19"
)  


file_path = os.path.realpath(__file__)
# get the root dir of this entire project.
dir_path = os.path.dirname(file_path)

# Download model to the specified directory
run["model/pickled_model"].download(dir_path)