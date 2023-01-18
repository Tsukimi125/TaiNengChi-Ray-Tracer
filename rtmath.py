from taichi.math import *
import taichi as ti

infinity = 114514
PI = 3.1415926535897932385


@ti.func
def degrees_to_radians(degrees) -> float:
    return degrees * PI / 180


@ti.func
def randf_min_max(min, max) -> float:
    return min + (max - min) * ti.random()


@ti.func
def rand3() -> vec3:
    return vec3(ti.random(), ti.random(), ti.random())  # 不能只写一个ti.random()，否则方向都是一样的


@ti.func
def rand3_min_max(min, max) -> vec3:
    return vec3(randf_min_max(min, max), randf_min_max(min, max), randf_min_max(min, max))


@ti.func
def clamp(x, min, max) -> float:
    return min(max(x, min), max)
