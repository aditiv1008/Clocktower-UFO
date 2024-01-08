from utils import *
from ray import *
from cli import render
from PIL import Image

brick = np.array(Image.open("texture/brick.png"))
brick = brick[:,:,:3]
square = np.array(Image.open("texture/dot.png"))
square = square[:,:,:3]

blue = Material(vec([173/255, 216/255, 230/255]), k_m=0.1)
tan = Material(vec([0.7, 0.7, 0.4]), 0.6)
gray = Material(vec([0.2, 0.2, 0.2]))
white = Material(vec([1, 0.95, 0.95]))
green = Material(vec([50/255, 205/255, 50/255]),0.6)

# Read the triangle mesh for a 2x2x2 cube, and scale it down to 1x1x1 to fit the scene.
vs_list, uv_list, normal_list = read_obj_triangles(open("tower.obj"))
vs_list = vs_list *0.9

vs_list_top, uv_list_top, normal_list_top = read_obj_triangles(open("tower_top.obj"))
vs_list_top = vs_list_top * 0.9

vs_list_clock,uv_list_clock,normal_list_clock = read_obj_triangles(open("clock.obj"))
vs_list_clock = vs_list_clock * 0.9

vs_list_cube,uv_list_cube,normal_list_cube = read_obj_triangles(open("cube.obj"))
vs_list_cube = vs_list_cube * 0.5


clock = [Triangle(vs1, white) for vs1 in vs_list_clock]
cube = [Triangle(vs1, white) for vs1 in vs_list_cube]
tower = [Triangle(vs, tan, uv, normal[0], brick) for vs,uv,normal in zip(vs_list,uv_list,normal_list)]
csg_union = CSGNode(clock, tower, operation='union')




ufo_material = Material(k_d=vec([0.5, 0.5, 0.5]), k_s=0.5, p=30.0, k_m=0.1)
ufo_material_inner = Material(k_d=vec([0.5, 0.5, 0.5]), k_s=0.5, p=30.0, k_m=0.1, k_a=vec([0.0, 0.8, 0.0]))
ufo_material_inner.k_e = vec([1.0, 1.0, 1.0])

# Create UFO saucer using intersection of spheres
ufo_saucer_outer = Sphere(vec([0, 1.0, -3]), 1.4, ufo_material)
ufo_saucer_inner = Sphere(vec([0, -0.8, -3]), 1.4, ufo_material)

ufo_saucer = CSGNode(ufo_saucer_outer, ufo_saucer_inner, operation='intersection')

# Create UFO top using spheres
ufo_top_outer = Sphere(vec([0, 0.5, -3]), 0.6, ufo_material_inner)
ufo_top_inner = Sphere(vec([0, -0.4, -3]), 0.4, ufo_material_inner)

# Combine UFO saucer and top using union operations
ufo = CSGNode(ufo_saucer, ufo_top_outer, operation='union')
ufo = CSGNode(ufo, ufo_top_inner, operation='union')



scene = Scene(
  [
    # Make a big sphere for the floor
    Sphere(vec([0,-43,0]), 39.5, green),
  ] + 
  tower + 
  [
    # Make triangle objects from the vertex coordinates
    Triangle(vs, blue, uv, normal[0], square) for vs,uv,normal in zip(vs_list_top,uv_list_top,normal_list_top)
  ] + [csg_union]+
  [ufo] 
    ,bg_color=vec([135/255,206/255,250/255]))

lights = [
    PointLight(vec([12,10,2]), vec([300,300,300])),
    PointLight(vec([0, -0.3, -3]), vec([1000, 1000, 1000])),
    AmbientLight(0.1),
]

camera = Camera(vec([7,7,7]), target=vec([0,0,0]), vfov=25, aspect=16/9)
# camera = Camera(vec([1,1,1]), target=vec([0,0,0]), vfov=25, aspect=16/9)

render(camera, scene, lights)