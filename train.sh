full_path=$(realpath $0)
root_path=$(dirname $full_path)
data_path=$root_path/df1_processed.csv
# echo $data_path

pip install -r $root_path/requirements.txt

python $root_path/train.py -d $data_path -mr $root_path -fr $root_path