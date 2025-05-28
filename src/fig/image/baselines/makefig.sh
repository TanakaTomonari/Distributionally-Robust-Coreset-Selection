#!/bin/sh
#$ -cwd
#$ -V -S /bin/bash
# Above two lines are settings for shell scripts (bash)

# the standard error stream of the job is merged into the standard output stream.
#$ -j y

# specify the memory that can be used (5 GB is the total amount for 2 CPUs)
#$ -l h_vmem=100.0G

# specify the computation nodes (queues) to submit. We can use wildcard (*) and logical_or (|) to specify multiple nodes.
#$ -q cpu-*.q@cpu-d*

# specify the number of CPU
#$ -pe smp 1

# activate virtual environment of conda
conda activate jax

# $@ is the all arguments of this job script
python makefig.py $@
