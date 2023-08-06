from dataclasses import dataclass
from math import sqrt


@dataclass
class Dimension:
    min: float
    max: float

    def to_base(self, value: float) -> float:
        return (value - self.min) / (self.max - self.min)

    def from_base(self, value: float) -> float:
        return value * (self.max - self.min) + self.min


@dataclass
class PitchDimensions:
    x_dim: Dimension
    y_dim: Dimension
    x_per_meter: float = None
    y_per_meter: float = None

    @property
    def length(self) -> float:
        return (
            (self.x_dim.max - self.x_dim.min) / self.x_per_meter
            if self.x_per_meter
            else None
        )

    @property
    def width(self) -> float:
        return (
            (self.y_dim.max - self.y_dim.min) / self.y_per_meter
            if self.y_per_meter
            else None
        )


@dataclass(frozen=True)
class Point:
    x: float
    y: float

    def distance_to(self, other: "Point") -> float:
        # returns the euclidean distance between the point and another provided point
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
