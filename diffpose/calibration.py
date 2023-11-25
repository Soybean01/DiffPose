# AUTOGENERATED! DO NOT EDIT! File to edit: ../notebooks/api/02_calibration.ipynb.

# %% auto 0
__all__ = ['RigidTransform', 'perspective_projection']

# %% ../notebooks/api/02_calibration.ipynb 4
import torch

# %% ../notebooks/api/02_calibration.ipynb 6
from typing import Optional

from beartype import beartype
from diffdrr.utils import convert
from jaxtyping import Float, jaxtyped
from pytorch3d.transforms import Transform3d


@beartype
class RigidTransform(Transform3d):
    @jaxtyped
    def __init__(
        self,
        R: Float[torch.Tensor, "..."],
        t: Float[torch.Tensor, "... 3"],
        parameterization: str = "matrix",
        convention: Optional[str] = None,
        device=None,
        dtype=torch.float32,
    ):
        if device is None and (R.device == t.device):
            device = R.device

        R = convert(R, parameterization, "matrix", convention)
        if R.dim() == 2 and t.dim() == 1:
            R = R.unsqueeze(0)
            t = t.unsqueeze(0)
        assert (batch_size := len(R)) == len(t)

        matrix = torch.zeros(batch_size, 4, 4, device=device, dtype=dtype)
        matrix[..., :3, :3] = R.transpose(-1, -2)
        matrix[..., 3, :3] = t
        matrix[..., 3, 3] = 1

        super().__init__(matrix=matrix, device=device, dtype=dtype)

    def get_rotation(self, parameterization=None, convention=None):
        R = self.get_matrix()[..., :3, :3].transpose(-1, -2)
        if parameterization is not None:
            R = convert(R, "matrix", parameterization, None, convention)
        return R

    def get_translation(self):
        return self.get_matrix()[..., 3, :3]

    def inverse(self):
        """Closed-form inverse for rigid transforms."""
        R = self.get_rotation().transpose(-1, -2)
        t = self.get_translation()
        t = -torch.einsum("bij,bj->bi", R, t)
        return RigidTransform(R, t, device=self.device, dtype=self.dtype)

    def compose(self, other):
        T = super().compose(other)
        R = T.get_matrix()[..., :3, :3].transpose(-1, -2)
        t = T.get_matrix()[..., 3, :3]
        return RigidTransform(R, t, device=self.device, dtype=self.dtype)

    def clone(self):
        R = self.get_matrix()[..., :3, :3].transpose(-1, -2).clone()
        t = self.get_matrix()[..., 3, :3].clone()
        return RigidTransform(R, t, device=self.device, dtype=self.dtype)

# %% ../notebooks/api/02_calibration.ipynb 8
@beartype
@jaxtyped
def perspective_projection(
    extrinsic: RigidTransform,  # Extrinsic camera matrix (world to camera)
    intrinsic: Float[torch.Tensor, "3 3"],  # Intrinsic camera matrix (camera to image)
    x: Float[torch.Tensor, "b n 3"],  # World coordinates
) -> Float[torch.Tensor, "b n 2"]:
    x = extrinsic.transform_points(x)
    x = torch.einsum("ij, bnj -> bni", intrinsic, x)
    z = x[..., -1].unsqueeze(-1).clone()
    x = x / z
    return x[..., :2]
