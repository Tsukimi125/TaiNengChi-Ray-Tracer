from taichi.math import *
import taichi as ti


@ti.dataclass
class Ray:
    origin: vec3
    direction: vec3

    @ti.func
    def at(r, t: float) -> vec3:
        return r.origin + t * r.direction
        
