for i in {1..10}
do
	cd ABMD${i}
	gmps="docker run --gpus all --rm -e CUDA_MPS_PIPE_DIRECTORY=/tmp/nvidia-mps -e CUDA_MPS_LOG_DIRECTORY=/tmp/nvidia-log --rm --gpus all -v $PWD:/root -v /tmp/nvidia-mps:/tmp/nvidia-mps -v /tmp/nvidia-log:/tmp/nvidia-log --ipc host -w /root gromacs:gromaps gmx"
	$gmps maptide -f nopbc.xtc -s nopbc.pdb -select 'chain E' -spacing 0.1 -mo
	cd ../
done
