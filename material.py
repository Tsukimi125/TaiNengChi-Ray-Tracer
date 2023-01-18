from taichi.math import *
import taichi as ti
from sampler import *
from rtmath import *
from ray import *


@ti.dataclass
class Material_Info:
    albedo: vec3
    roughness: float


@ti.func
def BSDF(ray_in, hit_record, material_id, material_info):
    ray_out = Ray(vec3(0.0), vec3(0.0))
    color = vec3(1.0)
    brightness_attenuation = vec3(1.0)
    if material_id == 0:
        ray_out, color, brightness_attenuation = BSDF_Lambert(ray_in, hit_record, material_info)
    elif material_id == 1:
        ray_out, color, brightness_attenuation = BSDF_Metal(ray_in, hit_record, material_info)
    elif material_id == -1:
        brightness_attenuation = material_info.albedo\

    return ray_out, color, brightness_attenuation


@ti.func
def BSDF_Lambert(ray_in, hit_record, material_info):
    p = hit_record.position
    # o = normalize(hit_record.normal + random_unit_vector())
    o = normalize(random_in_hemisphere(hit_record.normal))
    # o = reflect(ray_in.direction, n)
    ray_out = Ray(p, o)
    color = vec3(1.0)
    brightness_attenuation = material_info.albedo
    return ray_out, color, brightness_attenuation


@ti.func
def BSDF_Metal(ray_in, hit_record, material_info):
    p = hit_record.position
    n = hit_record.normal
    i = ray_in.direction
    o = reflect(i, n + material_info.roughness * random_unit_vector())
    ray_out = Ray(p, o)
    color = vec3(1.0)
    brightness_attenuation = material_info.albedo
    return ray_out, color, brightness_attenuation


@ti.func
def Diffuse_Light(self, material_info):
    return material_info.albedo


# Lambert = ti.types.struct(albedo=vec3, __struct_methods={'BSDF': BSDF_Lambert})
# Metal = ti.types.struct(albedo=vec3, __struct_methods={'BSDF': BSDF_Metal})
# Light_Source = ti.types.struct(__struct_methods={'BSDF': BSDF_Light_Source})


# @ti.data_oriented
# class Material:

#     @ti.func
#     def BSDF(self, ray_in, hit_record):
#         pass


# @ti.data_oriented
# class Lambert:
#     def __init__(self, albedo: vec3):
#         self.albedo = albedo

#     @ti.func
#     def BSDF(self, ray_in, hit_record):
#         p = hit_record.position
#         n = normalize(random_in_hemisphere(hit_record.normal))
#         o = reflect(ray_in.direction, n)

#         ray_out = Ray(p, o)

#         color = self.albedo
#         brightness_attenuation = 1
#         return ray_out, color, brightness_attenuation
