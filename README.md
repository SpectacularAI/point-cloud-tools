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

**Converting `.ply` file to `.splat`**. As of December 2023, there is no standard way of storing the
colors of the splats in the PLY files and different tools use different conventions. The type of the PLY file needs
to be specified with the `--ply_input_format` argument. See options below:

[**Inria format**](https://github.com/graphdeco-inria/gaussian-splatting#evaluation) (NOTE: may also work for newer versions of Nerfstudio):

    python convert.py \
        /PATH/TO/bonsai/point_cloud/iteration_30000/point_cloud.ply \
        /OUT/PATH/bonsai.splat \
       --ply_input_format=inria

[**Nerfstudio format**](https://github.com/nerfstudio-project/nerfstudio)

    # Example of Gaussian Splatting training
    ns-train gaussian-splatting --data /PATH/TO/my-input
    ns-export gaussian-splat --load-config outputs/my-input/gaussian-splatting/DATE/config.yaml --output-dir exports/splat

    python convert.py \
        exports/splat/point_cloud.ply \
        /OUT/PATH/my-splat.splat \
       --ply_input_format=nerfstudio

**Converting `.ply` file to a standalone `.html`** (powered by [gsplat.js](https://github.com/dylanebert/gsplat.js)).
The discussion on `--ply_input_format` above also applies here.

    python convert.py \
        exports/splat/point_cloud.ply \
        /OUT/PATH/my-splat.html \
       --ply_input_format=...

**Creating Gaussian Splatting `.ply` from smartphone data**: See [Spectacular AI Mapping Tools](https://github.com/SpectacularAI/sdk-examples/tree/main/python/mapping)
