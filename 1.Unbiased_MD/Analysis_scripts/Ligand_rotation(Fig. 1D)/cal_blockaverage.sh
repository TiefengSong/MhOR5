rm rotation_all rotation_all_sort
cat rotation_* > rotation_all
sort -n -k1,1 -s rotation_all > rotation_all_sort
sed -i '1s/^/#! FIELDS time ligand\n/' rotation_all_sort
python="docker run --gpus all --rm -e CUDA_MPS_PIPE_DIRECTORY=/tmp/nvidia-mps -e CUDA_MPS_LOG_DIRECTORY=/tmp/nvidia-log --rm --gpus all -v $PWD:/workdir -v /tmp/nvidia-mps:/tmp/nvidia-mps -v /tmp/nvidia-log:/tmp/nvidia-log --ipc host -w /workdir deeptime_torch_pmx:latest"
$python bash -c " python /root/FES_from_Reweighting.py -f rotation_all_sort -o FES --temp 310 --cv ligand --bias NO --blocks 50 -s 0.0314 --min -3.14 --max 3.14"
