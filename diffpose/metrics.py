# AUTOGENERATED! DO NOT EDIT! File to edit: ../notebooks/api/04_metrics.ipynb.

# %% auto 0
__all__ = ['NormalizedCrossCorrelation', 'MultiscaleNormalizedCrossCorrelation', 'GradientNormalizedCrossCorrelation',
           'GeodesicSO3', 'GeodesicTranslation', 'GeodesicSE3', 'DoubleGeodesic']

# %% ../notebooks/api/04_metrics.ipynb 3
from diffdrr.metrics import (
    GradientNormalizedCrossCorrelation2d,
    MultiscaleNormalizedCrossCorrelation2d,
    NormalizedCrossCorrelation2d,
)
from torchmetrics import Metric

# %% ../notebooks/api/04_metrics.ipynb 5
class CustomMetric(Metric):
    is_differentiable: True

    def __init__(self, LossClass, **kwargs):
        super().__init__()
        self.lossfn = LossClass(**kwargs)
        self.add_state("loss", default=torch.tensor(0.0), dist_reduce_fx="sum")
        self.add_state("count", default=torch.tensor(0), dist_reduce_fx="sum")

    def update(self, preds, target):
        self.loss += self.lossfn(preds, target).sum()
        self.count += len(preds)

    def compute(self):
        return self.loss.float() / self.count

# %% ../notebooks/api/04_metrics.ipynb 7
class NormalizedCrossCorrelation(CustomMetric):
    """`torchmetric` wrapper for NCC."""

    higher_is_better: True

    def __init__(self, patch_size=None):
        super().__init__(NormalizedCrossCorrelation2d, patch_size=patch_size)


class MultiscaleNormalizedCrossCorrelation(CustomMetric):
    """`torchmetric` wrapper for Multiscale NCC."""

    higher_is_better: True

    def __init__(self, patch_sizes, patch_weights):
        super().__init__(
            MultiscaleNormalizedCrossCorrelation2d,
            patch_sizes=patch_sizes,
            patch_weights=patch_weights,
        )


class GradientNormalizedCrossCorrelation(CustomMetric):
    """`torchmetric` wrapper for GradNCC."""

    higher_is_better: True

    def __init__(self, patch_size=None):
        super().__init__(GradientNormalizedCrossCorrelation2d, patch_size=patch_size)

# %% ../notebooks/api/04_metrics.ipynb 9
import torch
from beartype import beartype
from diffdrr.utils import convert
from jaxtyping import Float, jaxtyped
from pytorch3d.transforms import (
    so3_log_map,
    so3_relative_angle,
    so3_rotation_angle,
    standardize_quaternion,
)

from .calibration import RigidTransform

# %% ../notebooks/api/04_metrics.ipynb 10
class GeodesicSO3(torch.nn.Module):
    """Calculate the angular distance between two rotations in SO(3)."""

    def __init__(self):
        super().__init__()

    @jaxtyped(typechecker=beartype)
    def forward(
        self,
        pose_1: RigidTransform,
        pose_2: RigidTransform,
    ) -> Float[torch.Tensor, "b"]:
        r1 = pose_1.get_rotation()
        r2 = pose_2.get_rotation()
        rdiff = r1 @ r2.transpose(-1, -2)
        return so3_log_map(rdiff).norm(dim=-1)


class GeodesicTranslation(torch.nn.Module):
    """Calculate the angular distance between two rotations in SO(3)."""

    def __init__(self):
        super().__init__()

    @jaxtyped(typechecker=beartype)
    def forward(
        self,
        pose_1: RigidTransform,
        pose_2: RigidTransform,
    ) -> Float[torch.Tensor, "b"]:
        t1 = pose_1.get_translation()
        t2 = pose_2.get_translation()
        return (t1 - t2).norm(dim=1)

# %% ../notebooks/api/04_metrics.ipynb 11
class GeodesicSE3(torch.nn.Module):
    """Calculate the distance between transforms in the log-space of SE(3)."""

    def __init__(self):
        super().__init__()

    @jaxtyped(typechecker=beartype)
    def forward(
        self,
        pose_1: RigidTransform,
        pose_2: RigidTransform,
    ) -> Float[torch.Tensor, "b"]:
        return pose_2.compose(pose_1.inverse()).get_se3_log().norm(dim=1)

# %% ../notebooks/api/04_metrics.ipynb 12
@beartype
class DoubleGeodesic(torch.nn.Module):
    """Calculate the angular and translational geodesics between two SE(3) transformation matrices."""

    def __init__(
        self,
        sdr: float,  # Source-to-detector radius
        eps: float = 1e-4,  # Avoid overflows in sqrt
    ):
        super().__init__()
        self.sdr = sdr
        self.eps = eps

        self.rotation = GeodesicSO3()
        self.translation = GeodesicTranslation()

    @jaxtyped(typechecker=beartype)
    def forward(self, pose_1: RigidTransform, pose_2: RigidTransform):
        angular_geodesic = self.sdr * self.rotation(pose_1, pose_2)
        translation_geodesic = self.translation(pose_1, pose_2)
        double_geodesic = (
            (angular_geodesic).square() + translation_geodesic.square() + self.eps
        ).sqrt()
        return angular_geodesic, translation_geodesic, double_geodesic
