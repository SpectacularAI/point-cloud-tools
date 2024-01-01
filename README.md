# Point cloud tools
_Miscellaneous tools for point cloud file manipulation_


## Installation

Clone the repo and install the dependencies:

    git clone https://github.com/SpectacularAI/point-cloud-tools
    cd point-cloud-tools
    # optional but recommended: activate a virtual environment at this point
    pip install -r requirements.txt

## Examples

Convert PLY to PCD

    python convert.py input_file.ply output_file.pcd

### Gaussian Splatting

**Converting `.ply` file to `.splat`**.

    # Example of Gaussian Splatting training
    ns-train gaussian-splatting --data /PATH/TO/my-input
    ns-export gaussian-splat --load-config outputs/my-input/gaussian-splatting/DATE/config.yaml --output-dir exports/splat

    python convert.py \
        exports/splat/point_cloud.ply \
        /OUT/PATH/my-splat.splat

**Converting `.ply` file to a standalone `.html`** (powered by [gsplat.js](https://github.com/dylanebert/gsplat.js)).

    python convert.py \
        exports/splat/point_cloud.ply \
        /OUT/PATH/my-splat.html

**Creating Gaussian Splatting `.ply` from smartphone data**: See [Spectacular AI Mapping Tools](https://github.com/SpectacularAI/sdk-examples/tree/main/python/mapping)
