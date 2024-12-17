from ursina import *
from ursina.shaders import lit_with_shadows_shader
from ursina.prefabs.first_person_controller import FirstPersonController
from perlin_noise import PerlinNoise
import random

noise = PerlinNoise(octaves=3, seed=random.randint(0, 1000))

# init app
app = Ursina()
shader = lit_with_shadows_shader

# game variables
selected_block = "dirt"

# textures
block_textures = {
    "dirt": load_texture("assets/textures/dirt.png"),
    "cobblestone": load_texture("assets/textures/cobblestone.png"),
    "bedrock": load_texture("assets/textures/bedrock.png"),
}


# game objects
class Block(Entity):
    def __init__(self, position, block_type):
        super().__init__(
            model="cube",
            texture=block_textures[block_type],
            scale=1,
            origin_y=0.5,
            position=position,
            collider="box",
            shader=shader,
        )
        self.block_type = block_type


hand = Entity(
    parent=camera,
    model="cube",
    texture=block_textures[selected_block],
    scale=0.2,
    position=(0.35, -0.25, 0.5),
    rotation=(-15, -30, -5),
)


# terrain generation
def genTerrain(size=20):
    min_height = -5
    for x in range(size):
        for y in range(size):
            z = math.floor(noise([x * 0.02, y * 0.02]) * 7.5)
            for z in range(z, min_height - 1, -1):
                Block(position=(x, z + min_height, y), block_type="dirt")


def input(key):
    global selected_block
    if key == "right mouse down":
        hit_info = raycast(camera.world_position, camera.forward, distance=5)
        if hit_info.hit:
            block = Block(hit_info.entity.position + hit_info.normal, selected_block)
            Audio("assets/sfx/sand3.ogg", loop=False, autoplay=True)
    if key == "left mouse down" and mouse.hovered_entity:
        if not mouse.hovered_entity.block_type == "bedrock":
            destroy(mouse.hovered_entity)
            Audio("assets/sfx/sand2.ogg", loop=False, autoplay=True)

    if key == "1":
        selected_block = "dirt"
    if key == "2":
        selected_block = "cobblestone"
    if key == "3":
        selected_block = "bedrock"


genTerrain()

player = FirstPersonController(
    mouse_sensitivity=Vec2(100, 100),
    position=(0, 5, 0),
    height=1,
)


def update():
    # update player
    if player.y < -50:
        player.position = (0, 5, 0)

    # update hand
    hand.texture = block_textures[selected_block]


scene.fog_density = 0.05
sky = Sky()
window.fullscreen = True
app.run()
