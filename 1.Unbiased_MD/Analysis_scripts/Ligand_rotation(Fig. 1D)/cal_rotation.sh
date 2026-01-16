
for i in {1..3}
do
		for j in {1..4}
		do
			plumed="docker run --gpus all --rm -e CUDA_MPS_PIPE_DIRECTORY=/tmp/nvidia-mps -e CUDA_MPS_LOG_DIRECTORY=/tmp/nvidia-log --rm --gpus all -v $PWD:/workdir -v /tmp/nvidia-mps:/tmp/nvidia-mps -v /tmp/nvidia-log:/tmp/nvidia-log --ipc host -w /workdir registry.cn-hangzhou.aliyuncs.com/linjiahao/gromacs:2025-plumed-avx2-u2204-cu128 plumed"
			$plumed driver --plumed rotationl$j.dat --mf_xtc nopbc_$i.xtc
			mv rotation_l$j rotation_${i}_l${j}
		done
done

