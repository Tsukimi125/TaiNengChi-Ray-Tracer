from taichi.math import *
import taichi as ti

from rtmath import *


@ti.data_oriented
class Sampler:
    pass


@ti.func
def random_in_unit_sphere():
    p = 2.0 * rand3() - vec3(1.0)
    while p.norm() >= 1.0:
        p = 2.0 * rand3() - vec3(1.0)
    return normalize(p)


@ti.func
def random_unit_vector():
    a = randf_min_max(0, 2*pi)
    z = randf_min_max(-1, 1)
    r = sqrt(1 - z*z)
    return normalize(vec3(r*cos(a), r*sin(a), z))


@ti.func
def random_in_hemisphere(normal):
    in_unit_sphere = random_in_unit_sphere()
    return ti.select(dot(in_unit_sphere, normal) > 0.0, in_unit_sphere, -in_unit_sphere)

# vec3 random_in_hemisphere(const vec3 & normal) {
#     vec3 in_unit_sphere = random_in_unit_sphere()
#     if (dot(in_unit_sphere, normal) > 0.0) // In the same hemisphere as the normal
#     return in_unit_sphere
#     else
#     return -in_unit_sphere
# }
