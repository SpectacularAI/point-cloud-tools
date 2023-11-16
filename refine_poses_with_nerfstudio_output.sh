#!/bin/bash
set -eux

INPUT_FOLDER=$1
NERFSTUDIO_CONFIG_FILE=$2
REFINED_FOLDER=$3

TMP_POSES=$(mktemp -d)

ns-export cameras --load-config "$NERFSTUDIO_CONFIG_FILE" --output-dir "$TMP_POSES"

cp -R "$INPUT_FOLDER" "$REFINED_FOLDER"
python nerfstudio_cameras_to_colmap.py \
    "$INPUT_FOLDER" \
    "$REFINED_FOLDER"/colmap/sparse/0/images.txt \
    --colmap_reference "$INPUT_FOLDER"/colmap/sparse/0/images.txt

rm -rf "$TMP_POSES"
