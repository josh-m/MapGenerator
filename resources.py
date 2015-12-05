import pyglet
import random
pyglet.resource.path = ['resources',
                        'resources/forest',
                        'resources/grass',
                        'resources/water',
                        'resources/mountain']
pyglet.resource.reindex()


def center_anchor(img):
    img.anchor_x = img.width/2
    img.anchor_y = img.height/2

"""
IMAGES
"""
#GRASS#
grass_images = [
    pyglet.resource.image('green1.png'),
    pyglet.resource.image('green2.png'),
    pyglet.resource.image('green3.png'),
    pyglet.resource.image('green4.png'),
    pyglet.resource.image('green5.png'),
    pyglet.resource.image('green6.png'),
    pyglet.resource.image('green7.png'),
    pyglet.resource.image('green8.png')
]

for img in grass_images:
    center_anchor(img)

def random_grass():
    return random.choice(grass_images)

#FOREST#
forest_images = [
    pyglet.resource.image('deciduous-summer1.png'),
    pyglet.resource.image('deciduous-summer2.png'),
    pyglet.resource.image('deciduous-summer3.png'),
    pyglet.resource.image('deciduous-summer4.png')
]

for img in forest_images:
    center_anchor(img)

def random_forest():
    img = random.choice(forest_images)
    return img

#MOUNTAIN#    
mountain_images = [
    pyglet.resource.image('basic.png'),
    pyglet.resource.image('basic2.png'),
    pyglet.resource.image('basic3.png')
]
for img in mountain_images:
    center_anchor(img)

def random_mountain():
    img = random.choice(mountain_images)
    return img

#TOWN#
town_image = pyglet.resource.image('human-house.png')
center_anchor(town_image)

"""
UNITS
"""

#SETTLER#
settler_image = pyglet.resource.image('caravan.png')
center_anchor(settler_image)

#WOLF#
wolf_image = pyglet.resource.image('wolf.png')
center_anchor(wolf_image)

"""
UI
"""
selection_image = pyglet.resource.image('selection-overlay.png')
center_anchor(selection_image)

"""
ANIMATIONS

"""
ocean_images = [
    pyglet.resource.image('ocean-A01.png'),
    pyglet.resource.image('ocean-A02.png'),
    pyglet.resource.image('ocean-A03.png'),
    pyglet.resource.image('ocean-A04.png'),
    pyglet.resource.image('ocean-A05.png'),
    pyglet.resource.image('ocean-A06.png'),
    pyglet.resource.image('ocean-A07.png'),
    pyglet.resource.image('ocean-A08.png'),
    pyglet.resource.image('ocean-A09.png'),
    pyglet.resource.image('ocean-A10.png'),
    pyglet.resource.image('ocean-A11.png'),
    pyglet.resource.image('ocean-A12.png'),
    pyglet.resource.image('ocean-A13.png'),
    pyglet.resource.image('ocean-A14.png'),
    pyglet.resource.image('ocean-A15.png')
]
for img in ocean_images:
    center_anchor(img)


ocean_anim = pyglet.image.Animation.from_image_sequence(
        ocean_images, 0.1)
