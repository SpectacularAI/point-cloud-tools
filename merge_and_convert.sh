#!/bin/bash
set -eux

: "${CELL_SIZE:=0.05}"
IN_SPARSE="$1"
IN_DENSE="$2"
OUT="$3"

TMP_DECIMATED=$(mktemp ./decimated.XXXXXX)
TMP_MERGED=$(mktemp ./merged.XXXXXX)

python voxel_decimate.py $IN_DENSE $TMP_DECIMATED --cell_size=$CELL_SIZE
python merge_csvs.py $IN_SPARSE $TMP_DECIMATED $TMP_MERGED
python csv_to_pcd.py $TMP_MERGED $OUT

rm $TMP_DECIMATED $TMP_MERGED
