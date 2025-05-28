#!/bin/bash

methodlist=('DeepFool' 'Forgetting' 'Glister' 'GraNd' 'Submodular' 'Uncertainty')

for method in "${methodlist[@]}"; do
    # for weight in 1.0100; do
    for weight in $(seq 1.0200 0.0100 1.0500); do
        # mkdir -p log/makefig
        NAME="${method:0:5}-${weight:3:3}"
        LOGNAME="${method:0:5}-${weight:3:3}"
        qsub -N "$NAME" -o log/$data/$LOGNAME "makefig.sh" $weight $method
    done
done