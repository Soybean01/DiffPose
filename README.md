DiffPose
================

<!-- WARNING: THIS FILE WAS AUTOGENERATED! DO NOT EDIT! -->

> Patient-specific intraoperative 2D/3D registration via differentiable
> rendering

[![CI](https://github.com/eigenvivek/DiffPose/actions/workflows/test.yaml/badge.svg)](https://github.com/eigenvivek/DiffPose/actions/workflows/test.yaml)
[![License:
MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Docs](https://github.com/eigenvivek/DiffPose/actions/workflows/deploy.yaml/badge.svg)](https://vivekg.dev/DiffPose)
[![Code style:
black](https://img.shields.io/badge/Code%20style-black-black.svg)](https://github.com/psf/black)

<img src="https://github.com/eigenvivek/DiffPose/blob/main/notebooks/test_time_optimization.gif"/>

## Install

``` zsh
pip install DiffPose
```

This will install the dependencies listed under `requirements` in
[`settings.ini`](https://github.com/eigenvivek/DiffPose/blob/9a522b04a739334b9ddb89f3a606ab78d80bc6f6/settings.ini#L42).

## Datasets

We evaluate `DiffPose` networks on the following datasets.

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

- `VerSe` ([**Sekuboyina et al., 2020**](https://pubs.rsna.org/doi/10.1148/ryai.2020190074)) ... -->

## Development (optional)

`DiffPose` package, docs, and CI are all built using
[`nbdev`](https://nbdev.fast.ai/). To get set up with`nbdev`, install
the following

``` zsh
conda install jupyterlab nbdev -c fastai -c conda-forge 
nbdev_install_quarto  # To build docs
nbdev_install_hooks  # Make notebooks git-friendly
pip install -e  ".[dev]"  # Install the development verison of DiffPose
```

Running `nbdev_help` will give you the full list of options. The most
important ones are

``` zsh
nbdev_preview  # Render docs locally and inspect in browser
nbdev_prepare  # NECESSARY BEFORE PUSHING: builds package, tests notebooks, and builds docs in one step
```

For more details, follow this [in-depth
tutorial](https://nbdev.fast.ai/tutorials/tutorial.html).
