#!/bin/bash
set -eux

: "${CELL_SIZE:=0.05}"
IN_SPARSE="$1"
IN_DENSE="$2"
OUT="$3"

TMP_COLORS=$(mktemp)
TMP_INTERP=$(mktemp)
TMP_DECIM=$(mktemp)

# remove points without color
grep -v ",0,0,0," $IN_DENSE > $TMP_COLORS
python interpolate_colors.py $TMP_COLORS $IN_SPARSE $TMP_INTERP
python voxel_decimate.py $TMP_COLORS $TMP_DECIM --cell_size=$CELL_SIZE
python merge_csvs.py $TMP_INTERP $TMP_DECIM $OUT

rm $TMP_COLORS $TMP_INTERP $TMP_DECIM
