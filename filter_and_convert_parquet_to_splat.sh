#!/bin/bash
set -eux

: "${X:=0.0}"
: "${Y:=0.0}"
: "${Z:=0.0}"
: "${RADIUS:=1.0}"
: "${PCD_OUT:=none}"
IN_PARQUET="$1"
OUT_SPLAT="$2"

TMP_PARQ=$(mktemp)

python filter_parquet.py -x=$X -y=$Y -z=$Z --radius=$RADIUS "$IN_PARQUET" "$TMP_PARQ"
python parquet_to_splat.py "$TMP_PARQ" "$OUT_SPLAT"

if [ "$PCD_OUT" != "none" ]; then
    python splat_to_parquet.py "$OUT_SPLAT" "$TMP_PARQ"
    python parquet_to_pcd.py "$TMP_PARQ" "$PCD_OUT" --rgb
fi

rm "$TMP_PARQ"
