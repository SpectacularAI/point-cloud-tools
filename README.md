# Point cloud tools
_Miscellaneous tools for point cloud file manipulation_

Example. Merge and decimate point clouds, then convert CSV->PCD

    mkdir data
    CELL_SIZE=0.1 ./merge_and_convert.sh \
      /PATH/TO/points.sparse.csv \
      /PATH/TO/points.dense.csv \
      data/points-merged.pcd
