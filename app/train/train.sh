full_path=$(realpath $0)
dir_path=$(dirname $full_path)
root_path=$(dirname $dir_path)
data_path=$root_path/data/df1_processed.csv
# echo $data_path

pip install -r $root_path/requirements/requirements.txt

python $root_path/train/train.py -d $data_path -mr $root_path/artifacts/models/ -fr $root_path/artifacts/figures/

# python $dir_path/fetch_model.py