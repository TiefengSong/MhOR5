gmx='docker run --gpus all --rm -e CUDA_MPS_PIPE_DIRECTORY=/tmp/nvidia-mps -e CUDA_MPS_LOG_DIRECTORY=/tmp/nvidia-log --rm --gpus all -v $PWD:/workdir -v /tmp/nvidia-mps:/tmp/nvidia-mps -v /tmp/nvidia-log:/tmp/nvidia-log --ipc host -w /workdir registry.cn-hangzhou.aliyuncs.com/linjiahao/gromacs:2023-plumed-avx2-u2204-cu124 gmx'
$gmx select -f nopbc.xtc -s step7.tpr -select ' group 17 and within 0.3 of group 20' -n cal_hydra.ndx -os Deet5.xvg

