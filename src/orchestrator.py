from typing import TypeVar, Type

from view import GridView

Grid_Model = TypeVar(name="Grid_Model", covariant=True)


class GridOrchestrator:
    registry: dict[tuple, Grid_Model] = {}

    @classmethod
    def get_grid_view_with_parameters(
        cls, grid_size: int, location_probability: float, model_type: Type
    ) -> GridView:
        grid = cls._get_grid(grid_size, location_probability, model_type)
        return GridView(grid)

    @classmethod
    def _get_grid(
        cls, grid_size: int, location_probability: float, model_type: Type
    ) -> Grid_Model:
        key = (grid_size, location_probability)
        if key in cls.registry:
            return cls.registry[key]
        else:
            grid = model_type(size=grid_size, location_probability=location_probability)
            cls.registry[key] = grid
        return grid
