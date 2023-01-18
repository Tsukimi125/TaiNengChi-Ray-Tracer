from taichi.math import *
import taichi as ti
from material import *


@ti.dataclass
class HitRecord:
    position: vec3    # 碰撞位置
    normal: vec3      # 法线
    t: float          # 光线到碰撞位置的欧几里得距离
    front_face: ti.i32  # 碰撞是否为正面，即光线是否从表面外部射入


@ti.data_oriented
class Shape:

    @ti.func
    def hit(self, r, t_min: float, t_max: float):
        pass


@ti.data_oriented
class Sphere(Shape):
    def __init__(self, center: vec3, radius: float, material_id: ti.int64, material_info: Material_Info):
        self.center = center
        self.radius = radius
        self.material_id = material_id
        self.material_info = material_info

    @ti.func
    def hit(self, r, t_min: float, t_max: float):
        oc = r.origin - self.center
        a = r.direction.dot(r.direction)
        half_b = oc.dot(r.direction)
        c = oc.dot(oc) - self.radius * self.radius
        discriminant = half_b * half_b - a * c

        is_hit = False
        hit_record = HitRecord()

        if discriminant > 0:
            discriminant_sqrt = sqrt(discriminant)
            temp = (-half_b - discriminant_sqrt) / a
            if temp < t_max and temp > t_min:
                is_hit = True
                p = r.at(temp)
                n = normalize(p - self.center)

                # 判定是否为正面
                front_face = dot(n, r.direction) < 0.0
                n = ti.select(front_face, n, -n)
                front_face = ti.select(front_face, 1, 0)
                hit_record = HitRecord(
                    position=p,
                    normal=n,
                    t=temp,
                    front_face=front_face
                )

            if is_hit == False:
                temp = (-half_b + discriminant_sqrt) / a
                if temp < t_max and temp > t_min:
                    is_hit = True
                    p = r.at(temp)
                    n = normalize(p - self.center)

                    # 判定是否为正面
                    front_face = dot(n, r.direction) < 0.0
                    n = ti.select(front_face, n, -n)
                    front_face = ti.select(front_face, 1, 0)
                    hit_record = HitRecord(
                        position=p,
                        normal=n,
                        t=temp,
                        front_face=front_face
                    )

        return is_hit, hit_record


@ti.data_oriented
class Plane(Shape):
    def __init__(self, center: vec3, normal: float, scale: vec2, material_id: ti.int32, material_info: Material_Info):
        self.center = center
        self.normal = normal
        self.scale = scale
        self.material_id = material_id
        self.material_info = material_info

    @ti.func
    def hit(self, r, t_min: float, t_max: float):
        plane_p = self.center
        plane_n = self.normal
        point_p = r.origin
        point_d = r.direction

        is_hit = False
        hit_record = HitRecord()

        return is_hit, hit_record
