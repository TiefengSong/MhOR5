gmx='docker run --gpus all --rm -e CUDA_MPS_PIPE_DIRECTORY=/tmp/nvidia-mps -e CUDA_MPS_LOG_DIRECTORY=/tmp/nvidia-log --rm --gpus all -v $PWD:/workdir -v /tmp/nvidia-mps:/tmp/nvidia-mps -v /tmp/nvidia-log:/tmp/nvidia-log --ipc host -w /workdir registry.cn-hangzhou.aliyuncs.com/linjiahao/gromacs:2023-plumed-avx2-u2204-cu124 gmx'
for i in {1..3}
	do
	for j in {18..21}
	do
		echo 1 $j | $gmx rms -s step7.tpr -f nopbc_${i}.xtc -o rmsd${i}_${j}.xvg -n ligand.ndx
	done
done

