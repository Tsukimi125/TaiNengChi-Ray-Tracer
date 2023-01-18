from taichi.math import *
import taichi as ti
from object import HitRecord
from material import *


@ti.data_oriented
class Scene:
    def __init__(self):
        self.shapes = []

    def add_shape(self, shape):
        self.shapes.append(shape)

    @ti.func
    def hit(self, r, t_min: float, t_max: float):
        hit_something = False
        hit_record_closet = HitRecord()
        hit_material_id = 0.5
        hit_material_info = Material_Info(
            albedo=vec3(0.0)
        )

        closest_so_far = t_max  # 目前为止最近的碰撞点

        for index in ti.static(range(len(self.shapes))):
            is_hit, hit_record = self.shapes[index].hit(r, t_min, closest_so_far)
            if is_hit:
                hit_something = True
                closest_so_far = hit_record.t
                hit_record_closet = hit_record
                hit_material_id = self.shapes[index].material_id
                hit_material_info = self.shapes[index].material_info

        return hit_something, hit_record_closet, hit_material_id, hit_material_info
