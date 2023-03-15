#!/bin/bash

CPU=$4
INDIR=$2
OUTDIR=$3
SCRIPT=$1

for f in `ls $INDIR`; do
    python3 $SCRIPT $INDIR/$f $OUTDIR $CPU
done

