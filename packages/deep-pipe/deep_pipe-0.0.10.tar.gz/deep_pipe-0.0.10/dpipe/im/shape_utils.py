import numpy as np

from dpipe.itertools import extract
from ..checks import check_len
from .axes import broadcast_to_axes, fill_by_indices, AxesLike


def compute_shape_from_spatial(complete_shape, spatial_shape, spatial_dims):
    check_len(spatial_shape, spatial_dims)
    shape = np.array(complete_shape)
    shape[list(spatial_dims)] = spatial_shape
    return tuple(shape)


def broadcastable(first_shape, second_shape):
    return all((m == n) or (m == 1) or (n == 1) for m, n in zip(first_shape[::-1], second_shape[::-1]))


def broadcast_shape_nd(shape, n):
    if len(shape) > n:
        raise ValueError(f'len({shape}) > {n}')
    return (1,) * (n - len(shape)) + tuple(shape)


def broadcast_shape(x_shape, y_shape):
    if not broadcastable(x_shape, y_shape):
        raise ValueError(f'Shapes are not broadcastable: {x_shape} {y_shape}')

    max_n = max(len(x_shape), len(y_shape))
    x_shape = broadcast_shape_nd(x_shape, max_n)
    y_shape = broadcast_shape_nd(y_shape, max_n)
    return tuple(map(max, x_shape, y_shape))


def extract_dims(array, ndim=1):
    """Decrease the dimensionality of ``array`` by extracting ``ndim`` leading singleton dimensions."""
    for _ in range(ndim):
        assert len(array) == 1, len(array)
        array = array[0]
    return array


def prepend_dims(array, ndim=1):
    """Increase the dimensionality of ``array`` by adding ``ndim`` leading singleton dimensions."""
    idx = (None,) * ndim
    return np.asarray(array)[idx]


def append_dims(array, ndim=1):
    """Increase the dimensionality of ``array`` by adding ``ndim`` singleton dimensions to the end of its shape."""
    idx = (...,) + (None,) * ndim
    return np.asarray(array)[idx]


def shape_after_convolution(shape: AxesLike, kernel_size: AxesLike, stride: AxesLike = 1, padding: AxesLike = 0,
                            dilation: AxesLike = 1, valid: bool = True) -> tuple:
    """Get the shape of a tensor after applying a convolution with corresponding parameters."""
    padding, shape, dilation, kernel_size = map(np.asarray, [padding, shape, dilation, kernel_size])

    result = (shape + 2 * padding - dilation * (kernel_size - 1) - 1) / stride + 1
    to_int = np.floor if valid else np.ceil

    result = to_int(result).astype(int)
    new_shape = tuple(result)
    if (result <= 0).any():
        raise ValueError(f'Such a convolution is not possible. Output shape: {new_shape}.')
    return new_shape


def shape_after_full_convolution(shape: AxesLike, kernel_size: AxesLike, axes: AxesLike = None, stride: AxesLike = 1,
                                 padding: AxesLike = 0, dilation: AxesLike = 1, valid: bool = True) -> tuple:
    """
    Get the shape of a tensor after applying a convolution with corresponding parameters along the given axes.
    The dimensions along the remaining axes will become singleton.
    """
    axes, *params = broadcast_to_axes(axes, kernel_size, stride, padding, dilation)

    return fill_by_indices(
        np.ones_like(shape),
        shape_after_convolution(extract(shape, axes), *params, valid), axes
    )
