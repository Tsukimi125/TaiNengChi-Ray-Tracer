from taichi.math import *
import taichi as ti
from rt_ray import Ray
from rt_object import Shape, Sphere, HitRecord
from rt_scene import Scene

ti.init(arch=ti.gpu)    # 初始化 Taichi ，GPU 加速

image_resolution = (1600, 800)  # 图像分辨率
aspect_ratio = image_resolution[0] / image_resolution[1]
image_pixels = ti.Vector.field(3, float, image_resolution)  # 图像的像素场

scene = Scene()

scene.add_shape(Sphere(vec3(0, 0, -1), 0.5))
scene.add_shape(Sphere(vec3(0, -100.5, -1), 100))


@ti.func
def hit_sphere(center: vec3, radius: float, r):
    pass


# 计算光线颜色
@ti.func
def ray_color(r):
    color = vec3(0.0)
    is_hit, hit_record = scene.hit(r, 0.0, 1000000.0)
    if is_hit:
        N = hit_record.normal

        N = 0.5*vec3(N.x+1, N.y+1, N.z+1)
        #NL = vec3(dot(N, normalize(vec3(0.5, 0.5, 0.5))))
        color = N
    else:
        unit_dir = normalize(r.direction)

        # 设定天空颜色
        t = 0.5 * unit_dir.y + 0.5
        color = (1.0 - t) * vec3(1.0) + t * vec3(0.5, 0.7, 1.0)
    return color


@ti.kernel
def render():   # 渲染函数
    lower_left_corner = vec3(-2.0, -1.0, -1.0)
    horizontal = vec3(4.0, 0.0, 0.0)
    vertical = vec3(0.0, 2.0, 0.0)
    origin = vec3(0.0, 0.0, 0.0)

    for i, j in image_pixels:   # 并行遍历像素场
        u = i / image_resolution[0]  # 计算归一化的 u 坐标
        v = j / image_resolution[1]  # 计算归一化的 v 坐标
        ray = Ray(origin, lower_left_corner + u * horizontal + v * vertical)
        color = ray_color(ray)
        image_pixels[i, j] = color  # 设置像素颜色


window = ti.ui.Window("TaiNengChi Renderer", image_resolution)  # 创建窗口
canvas = window.get_canvas()    # 获取画布

while window.running:
    render()    # 调用渲染函数
    canvas.set_image(image_pixels)  # 为画布设置图像
    window.show()   # 显示窗口
