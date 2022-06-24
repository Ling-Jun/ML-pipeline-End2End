full_path=$(realpath $0)
dir_path=$(dirname $full_path)
root_path=$(dirname $dir_path)
# data_path=$(dirname $root_path)/data/df2_processed.csv
# # echo $data_path

# python deploy/deploy.py
cd $root_path/deploy
uvicorn deploy:app --reload --port 8001