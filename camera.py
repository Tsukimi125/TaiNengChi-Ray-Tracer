from taichi.math import *
import taichi as ti
from ray import Ray


@ti.func
def random_in_unit_disk():  # 单位圆内随机取一点
    x = ti.random()
    a = ti.random() * 2 * pi
    return sqrt(x) * vec2(sin(a), cos(a))


@ti.dataclass
class Camera:  # 摄像机类
    lookfrom: vec3  # 视点位置
    lookat: vec3  # 目标位置
    vup: vec3  # 向上的方向
    vfov: float  # 纵向视野
    aspect: float  # 传感器长宽比
    aperture: float  # 光圈大小
    focus: float  # 对焦距离

    @ti.func
    def get_ray(self, uv: vec2) -> Ray:
        # 根据 vfov 和画布长宽比计算出半高和半宽
        theta = radians(self.vfov)  # 角度转弧度
        half_height = tan(theta * 0.5)
        half_width = self.aspect * half_height

        # 以目标位置到摄像机位置为 Z 轴正方向
        z = normalize(self.lookfrom - self.lookat)
        # 计算出摄像机传感器的 XY 轴正方向
        x = normalize(cross(self.vup, z))
        y = cross(z, x)

        # 计算出画布左下角
        lower_left_corner = self.lookfrom - half_width * self.focus*x \
            - half_height * self.focus*y \
            - self.focus*z

        horizontal = 2.0 * half_width * self.focus * x
        vertical = 2.0 * half_height * self.focus * y

        # 模拟光进入镜头光圈
        lens_radius = self.aperture * 0.5
        rud = lens_radius * random_in_unit_disk()
        offset = x * rud.x + y * rud.y

        # 计算光线起点和方向
        ro = self.lookfrom + offset
        rp = lower_left_corner + uv.x*horizontal \
            + uv.y*vertical
        rd = normalize(rp - ro)

        return Ray(ro, rd)

# @ti.dataclass
# class Camera:
#     origin: vec3
#     lower_left_corner: vec3
#     horizontal: vec3
#     vertical: vec3

#     @ti.func
#     def get_ray(self, u: float, v: float) -> Ray:
#         return Ray(
#             origin=self.origin,
#             direction=self.lower_left_corner + u * self.horizontal + v * self.vertical - self.origin
#         )
