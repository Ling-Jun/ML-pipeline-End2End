echo $0 
file_path=$(realpath $0)
echo $file_path
dir_path=$(dirname $file_path)
echo $dir_path

echo $dir_path/monitor.py
while true; do python $dir_path/monitor.py; echo SLEEPING 8 seconds; sleep 8; echo SLEEPING is DONE; done