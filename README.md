# DiffPose

<!-- WARNING: THIS FILE WAS AUTOGENERATED! DO NOT EDIT! -->

> Intraoperative 2D/3D registration via differentiable X-ray rendering

[![CI](https://github.com/eigenvivek/DiffPose/actions/workflows/test.yaml/badge.svg)](https://github.com/eigenvivek/DiffPose/actions/workflows/test.yaml)
[![License:
MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Docs](https://github.com/eigenvivek/DiffPose/actions/workflows/deploy.yaml/badge.svg)](https://vivekg.dev/DiffPose)
[![Code style:
black](https://img.shields.io/badge/Code%20style-black-black.svg)](https://github.com/psf/black)

![](experiments/test_time_optimization.gif)

## Install

To install `DiffPose` and the requirements in
[`environment.yml`](https://github.com/eigenvivek/DiffPose/blob/main/environment.yml),
run:

``` zsh
pip install diffpose
```

The differentiable X-ray renderer that powers the backend of `DiffPose`
is available at [`DiffDRR`](https://github.com/eigenvivek/DiffDRR).

## Datasets

We evaluate `DiffPose` networks on the following open-source datasets:

| **Dataset**                                                                | **Anatomy**        | **\# of Subjects** | **\# of 2D Images** | **CTs** | **X-rays** | Fiducials |
|----------------------------------------------------------------------------|--------------------|:------------------:|:-------------------:|:-------:|:----------:|:---------:|
| [`DeepFluoro`](https://github.com/rg2/DeepFluoroLabeling-IPCAI2020)        | Pelvis             |         6          |         366         |   ✅    |     ✅     |    ❌     |
| [`Ljubljana`](https://lit.fe.uni-lj.si/en/research/resources/3D-2D-GS-CA/) | Cerebrovasculature |         10         |         20          |   ✅    |     ✅     |    ✅     |

<!-- | [`2D-3D-GS`](https://lit.fe.uni-lj.si/en/research/resources/2D-3D-GS/)     | Lumbar Spine       |          1         |          18         |    ✅    |      ✅     |     ✅     |
| [`VerSe`](https://github.com/anjany/verse)                                 | Spine              |         355        |         N/A         |    ✅    |      ❌     |     ❌     | -->

- `DeepFluoro` ([**Grupp et al.,
  2020**](https://link.springer.com/article/10.1007/s11548-020-02162-7))
  provides paired X-ray fluoroscopy images and CT volume of the pelvis.
  The data were collected from six cadaveric subjects at John Hopkins
  University. Ground truth camera poses were estimated with an offline
  registration process. A visualization of one X-ray / CT pair in the
  `DeepFluoro` dataset is available
  [here](https://vivekg.dev/DiffPose/experiments/render.html).

``` zsh
mkdir -p data/
wget --no-check-certificate -O data/ipcai_2020_full_res_data.zip "http://archive.data.jhu.edu/api/access/datafile/:persistentId/?persistentId=doi:10.7281/T1/IFSXNV/EAN9GH"
unzip -o data/ipcai_2020_full_res_data.zip -d data
rm data/ipcai_2020_full_res_data.zip
```

- `Ljubljana` ([**Mitrovic et al.,
  2013**](https://ieeexplore.ieee.org/abstract/document/6507588))
  provides paired 2D/3D digital subtraction angiography (DSA) images.
  The data were collected from 10 patients undergoing endovascular
  image-guided interventions at the University of Ljubljana. Ground
  truth camera poses were estimated by registering surface fiducial
  markers.

``` zsh
mkdir -p data/
wget --no-check-certificate -O data/ljubljana.zip "https://drive.google.com/uc?export=download&confirm=yes&id=1x585pGLI8QGk21qZ2oGwwQ9LMJ09Tqrx"
unzip -o data/ljubljana.zip -d data
rm data/ljubljana.zip
```

<!-- - `2D-3D-GS` ([**Tomaževič et al., 2004**](https://pubmed.ncbi.nlm.nih.gov/16192053/)) ...
&#10;- `VerSe` ([**Sekuboyina et al., 2020**](https://pubs.rsna.org/doi/10.1148/ryai.2020190074)) ... -->

## Experiments

To run the experiments in `DiffPose`, run the following scripts (ensure
you’ve downloaded the data first):

``` zsh
# DeepFluoro dataset
cd experiments/deepfluoro
srun python train.py     # Pretrain pose regression CNN on synthetic X-rays
srun python register.py  # Run test-time optimization with the best network per subject
```

``` zsh
# Ljubljana dataset
cd experiments/ljubljana
srun python train.py
srun python register.py
```

The training and test-time optimization scripts use SLURM to run on all
subjects in parallel:

- `experiments/deepfluoro/train.py` is configured to run across six
  A6000 GPUs
- `experiments/deepfluoro/register.py` is configured to run across six
  2080 Ti GPUs
- `experiments/ljubljana/train.py` is configured to run across twenty
  2080 Ti GPUs
- `experiments/ljubljana/register.py` is configured to run on twenty
  2080 Ti GPUs

The GPU configurations can be changed at the end of each script using
[`submitit`](https://github.com/facebookincubator/submitit).

## Development

`DiffPose` package, docs, and CI are all built using
[`nbdev`](https://nbdev.fast.ai/). To get set up with`nbdev`, install
the following

``` zsh
conda install jupyterlab nbdev -c fastai -c conda-forge 
nbdev_install_quarto      # To build docs
nbdev_install_hooks       # Make notebooks git-friendly
pip install -e  ".[dev]"  # Install the development verison of DiffPose
```

Running `nbdev_help` will give you the full list of options. The most
important ones are

``` zsh
nbdev_preview  # Render docs locally and inspect in browser
nbdev_clean    # NECESSARY BEFORE PUSHING
nbdev_test     # tests notebooks
nbdev_export   # builds package and builds docs
nbdev_readme   # Render the readme
```

For more details, follow this [in-depth
tutorial](https://nbdev.fast.ai/tutorials/tutorial.html).

## Citing `DiffPose`

If you find `DiffPose` or
[`DiffDRR`](https://github.com/eigenvivek/DiffDRR) useful in your work,
please cite the appropriate papers:

    @inproceedings{gopalakrishnanDiffDRR2022,
        author    = {Gopalakrishnan, Vivek and Golland, Polina},
        title     = {Fast Auto-Differentiable Digitally Reconstructed Radiographs for Solving Inverse Problems in Intraoperative Imaging},
        year      = {2022},
        booktitle = {Clinical Image-based Procedures: 11th International Workshop, CLIP 2022, Held in Conjunction with MICCAI 2022, Singapore, Proceedings},
        series    = {Lecture Notes in Computer Science},
        publisher = {Springer},
        doi       = {https://doi.org/10.1007/978-3-031-23179-7_1},
    }
