from taichi.math import *
import taichi as ti
from ray import Ray
from object import Shape, Sphere, HitRecord
from scene import Scene
from camera import Camera
from material import *
from sampler import *
from rtmath import *

ti.init(arch=ti.gpu)


# 图像显示设置

image_resolution = (800, 800)  # 图像分辨率
aspect_ratio = image_resolution[0] / image_resolution[1]
image_pixels = ti.Vector.field(3, float, image_resolution)  # 图像的像素场

# 场景设置
scene = Scene()


lambert_green = Material_Info(
    albedo=vec3(0.0, 0.6, 0.0)
)

lambert_red = Material_Info(
    albedo=vec3(0.6, 0.0, 0.0)
)

lambert_info = Material_Info(
    albedo=vec3(0.8, 0.8, 0.8)
)

light_5x = Material_Info(
    albedo=vec3(5.0)
)

light_10x = Material_Info(
    albedo=vec3(10.0)
)

metal_info = Material_Info(
    albedo=vec3(0.8, 0.6, 0.2),
    roughness=0.1
)
scene.add_shape(Sphere(vec3(-0.2, -0.4, 0), 0.1, 1, metal_info))
scene.add_shape(Sphere(vec3(0.2, -0.4, 0), 0.1, 0, lambert_info))

scene.add_shape(Sphere(vec3(0, 5.4925, 0), 5.0, -1, light_10x))


scene.add_shape(Sphere(vec3(0, 0, 100.5), 100, 0, lambert_info))

scene.add_shape(Sphere(vec3(100.5, 0, 0), 100, 0, lambert_red))
scene.add_shape(Sphere(vec3(-100.5, 0, 0), 100, 0, lambert_green))

scene.add_shape(Sphere(vec3(0, -100.5, 0), 100, 0, lambert_info))
scene.add_shape(Sphere(vec3(0, 100.5, 0), 100, 0, lambert_info))


# scene.add_shape(Sphere(vec3(0, 100.5, -1), 100, lambert_mat))
# scene.add_shape(Sphere(vec3(-100.5, 0, -1), 100, lambert_mat))
# scene.add_shape(Sphere(vec3(100.5, 0, -1), 100, lambert_mat))

# 光线追踪相关设置

SAMPLES_PER_PIXEL = 256  # 每个像素的采样数

p_RR = 0.8  # 路径追踪的概率
MAX_TRACE_TIME = 100  # 最大追踪次数


# 计算光线颜色
@ti.func
def ray_color(r):
    color = vec3(0.0)
    brightness = vec3(1.0)
    ray = r

    for _ in range(MAX_TRACE_TIME):
        # 路径追踪概率
        if ti.random() > p_RR:
            break

        is_hit, hit_record, hit_material_id, hit_material_info = scene.hit(ray, 0.001, 1000000.0)
        if is_hit:
            # target = hit_record.position + hit_record.normal + random_in_unit_sphere()
            # target = hit_record.position + hit_record.normal + random_unit_vector()
            # target = hit_record.position + random_in_hemisphere(hit_record.normal)
            # ray = Ray(hit_record.position, normalize(target - hit_record.position))
            # ray, color_attenuation, brightness_attenuation = BSDF(hit_material_id, mat_info, ray, hit_record)
            ray, color, brightness_attenuation = BSDF(ray, hit_record, hit_material_id, hit_material_info)
            brightness *= brightness_attenuation
            if hit_material_id <= -1:
                break

            is_hit = False

            # ray, color, brightness_attenuation = mat.BRDF

        else:
            # unit_dir = normalize(r.direction)

            # 设定天空颜色
            # t = 0.5 * unit_dir.y + 0.5
            # color = (1.0 - t) * vec3(1.0) + t * vec3(0.5, 0.7, 1.0)
            color = vec3(0.0, 0.0, 0.0)
            break

    return color * brightness


@ti.kernel
def render():   # 渲染函数
    lower_left_corner = vec3(-2.0, -1.0, -1.0)
    horizontal = vec3(4.0, 0.0, 0.0)
    vertical = vec3(0.0, 2.0, 0.0)
    origin = vec3(0.0, 0.0, 0.0)

    camera = Camera(
        lookfrom=vec3(0.0, 0.0, -2.5),
        lookat=vec3(0.0, 0.0, 0.0),
        vup=vec3(0.0, 1.0, 0.0),
        aspect=aspect_ratio,
        vfov=30.0,
        aperture=0.01,
        focus=2.5
    )
    for i, j in image_pixels:   # 并行遍历像素场
        color = vec3(0.0)
        for _ in range(SAMPLES_PER_PIXEL):
            u = (i + ti.random()) / image_resolution[0]  # 计算归一化的 u 坐标
            v = (j + ti.random()) / image_resolution[1]  # 计算归一化的 v 坐标
            ray = camera.get_ray(vec2(u, v))  # 生成光线
            color += ray_color(ray)
        color /= SAMPLES_PER_PIXEL
        color = vec3(sqrt(color.x), sqrt(color.y), sqrt(color.z))  # gamma 矫正
        image_pixels[i, j] = color  # 设置像素颜色


window = ti.ui.Window("TaiNengChi Renderer", image_resolution)  # 创建窗口
canvas = window.get_canvas()    # 获取画布

while window.running:
    render()    # 调用渲染函数
    canvas.set_image(image_pixels)  # 为画布设置图像
    window.show()   # 显示窗口
