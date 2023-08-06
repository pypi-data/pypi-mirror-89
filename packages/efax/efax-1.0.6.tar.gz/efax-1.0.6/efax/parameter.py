from __future__ import annotations

from typing import TYPE_CHECKING, Any, Union

from tjax import field, field_names_values_metadata, fields

__all__ = ['parameter_names_values_axes', 'parameter_names_axes']


def distribution_parameter(axes: int) -> Any:
    return field(metadata={'axes': axes})


def parameter_names_values_axes(x: Parametrization) -> Iterable[str, Array, int]:
    for name, value, metadata in field_names_values_metadata(x, static=False):
        n_axes = metadata['axes']
        if not isinstance(n_axes, int):
            raise TypeError
        yield name, value, n_axes


def parameter_names_axes(x: Union[Type[Parametrization], Parametrization]) -> Iterable[str, int]:
    for field in fields(x, static=False):
        n_axes = field.metadata['axes']
        if not isinstance(n_axes, int):
            raise TypeError
        yield field.name, n_axes


if TYPE_CHECKING:
    from .exponential_family import Parametrization
