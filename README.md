# Point cloud tools
_Miscellaneous tools for point cloud file manipulation_

Example. Merge and decimate point clouds, then convert CSV->Parquet

    mkdir data
    CELL_SIZE=0.1 ./merge_and_decimate_csvs.sh \
      /PATH/TO/points.sparse.csv \
      /PATH/TO/points.dense.csv \
      data/points-merged.csv
    python csv_to_parquet.py data/points-merged.csv data/points-merged.parquet
