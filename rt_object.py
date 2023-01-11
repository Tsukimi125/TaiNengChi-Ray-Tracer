from taichi.math import *
import taichi as ti


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
    def __init__(self, center: vec3, radius: float):
        self.center = center
        self.radius = radius

    @ti.func
    def hit(self, r, t_min: float, t_max: float):
        oc = r.origin - self.center
        a = r.direction.dot(r.direction)
        b = 2.0 * oc.dot(r.direction)
        c = oc.dot(oc) - self.radius * self.radius
        discriminant = b * b - 4 * a * c

        is_hit = False
        hit_record = HitRecord()

        if discriminant > 0:
            discriminant_sqrt = sqrt(discriminant)
            temp = (-b - discriminant_sqrt) / (2 * a)
            if temp < t_max and temp > t_min:
                is_hit = True
                p = r.at(temp)
                n = normalize(p - self.center)
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
                temp = (-b + discriminant_sqrt) / (2 * a)
                if temp < t_max and temp > t_min:
                    is_hit = True
                    p = r.at(temp)
                    n = normalize(p - self.center)
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


'''
@ti.data_oriented
class Sphere(Shape):
    def __init__(self, center: vec3, radius: float):
        self.center = center
        self.radius = radius

    @ti.func
    def hit(self, r, t_min: float, t_max: float):
        oc = r.origin - self.center
        a = dot(r.direction, r.direction)
        b = 2 * dot(oc, r.direction)
        c = dot(oc, oc) - self.radius * self.radius
        discriminant = b * b - 4 * a * c

        is_hit = False
        hit_record = HitRecord()

        if discriminant > 0:
            root = sqrt(discriminant)
            temp = 0.5 * (-b - root) / a
            if temp < t_max and temp > t_min:
                is_hit = True
                p = r.at(temp)
                n = normalize(p - self.center)
                front_face = dot(n, r.direction) < 0.0
                # n = n if front_face else -n
                # f = 1 if front_face else 0
                hit_record = HitRecord(
                    position=p,
                    normal=n,
                    t=temp,
                    front_face=front_face
                )

            temp = 0.5 * (-b + root) / a
            if temp < t_max and temp > t_min:
                is_hit = True
                p = r.at(temp)
                # n = (p - self.center) / self.radius
                n = normalize(p - self.center)
                front_face = dot(n, r.direction) < 0.0
                # n = n if front_face else -n
                # f = 1 if front_face else 0
                hit_record = HitRecord(
                    position=p,
                    normal=n,
                    t=temp,
                    front_face=front_face
                )

        return is_hit, hit_record
'''
