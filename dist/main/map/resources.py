import pyglet
import random
pyglet.resource.path = ['resources',
                        'resources/forest',
                        'resources/grass',
                        'resources/water',
                        'resources/mountain',
                        'resources/hills',
                        'resources/desert',
                        'resources/flatland']
pyglet.resource.reindex()


def center_anchor(img):
    img.anchor_x = img.width/2
    img.anchor_y = img.height/2

"""
IMAGES
"""

#DESERT#
desert_images = [
    pyglet.resource.image('desert.png'),
    pyglet.resource.image('desert2.png'),
    pyglet.resource.image('desert3.png'),
    pyglet.resource.image('desert4.png'),
    pyglet.resource.image('desert5.png'),
    pyglet.resource.image('desert6.png'),
    pyglet.resource.image('desert7.png'),
    pyglet.resource.image('desert8.png')
]

desert_border_images = [
    pyglet.resource.image('desert-nw.png'),
    pyglet.resource.image('desert-n.png'),
    pyglet.resource.image('desert-ne.png'),
    pyglet.resource.image('desert-sw.png'),
    pyglet.resource.image('desert-s.png'),
    pyglet.resource.image('desert-se.png')
]

for img in desert_images + desert_border_images:
    center_anchor(img)

def random_desert():
    return random.choice(desert_images)
    
def desert_border(hexdir):
    return desert_border_images[hexdir]
    
desert_hill_images = [
    pyglet.resource.image('desert_hill.png'),
    pyglet.resource.image('desert_hill2.png'),
    pyglet.resource.image('desert_hill3.png')
]

desert_hill_border_images = [
    pyglet.resource.image('desert_hill-nw.png'),
    pyglet.resource.image('desert_hill-n.png'),
    pyglet.resource.image('desert_hill-ne.png'),
    pyglet.resource.image('desert_hill-sw.png'),
    pyglet.resource.image('desert_hill-s.png'),
    pyglet.resource.image('desert_hill-se.png')
]

for img in desert_hill_images + desert_hill_border_images:
    center_anchor(img)

def random_desert_hill():
    return random.choice(desert_hill_images)
    
def desert_hill_border(hexdir):
    return desert_hill_border_images[hexdir]

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

semidry_grass_images = [
    pyglet.resource.image('semi-dry.png'),
    pyglet.resource.image('semi-dry2.png'),
    pyglet.resource.image('semi-dry3.png'),
    pyglet.resource.image('semi-dry4.png'),
    pyglet.resource.image('semi-dry5.png'),
    pyglet.resource.image('semi-dry6.png')
]

dry_grass_images = [
    pyglet.resource.image('dry_grass.png'),
    pyglet.resource.image('dry_grass2.png'),
    pyglet.resource.image('dry_grass3.png'),
    pyglet.resource.image('dry_grass4.png'),
    pyglet.resource.image('dry_grass5.png'),
    pyglet.resource.image('dry_grass6.png')
]

grass_border_images = [
    pyglet.resource.image('green-nw.png'),
    pyglet.resource.image('green-n.png'),
    pyglet.resource.image('green-ne.png'),
    pyglet.resource.image('green-sw.png'),
    pyglet.resource.image('green-s.png'),
    pyglet.resource.image('green-se.png')
]

abrupt_grass_border_images = [
    pyglet.resource.image('green-abrupt-nw.png'),
    pyglet.resource.image('green-abrupt-n.png'),
    pyglet.resource.image('green-abrupt-ne.png'),
    pyglet.resource.image('green-abrupt-sw.png'),
    pyglet.resource.image('green-abrupt-s.png'),
    pyglet.resource.image('green-abrupt-se.png')
]

semidry_grass_border_images = [
    pyglet.resource.image('semi-dry-nw.png'),
    pyglet.resource.image('semi-dry-n.png'),
    pyglet.resource.image('semi-dry-ne.png'),
    pyglet.resource.image('semi-dry-sw.png'),
    pyglet.resource.image('semi-dry-s.png'),
    pyglet.resource.image('semi-dry-se.png')
]

abrupt_semidry_grass_border_images = [
    pyglet.resource.image('semi-dry-abrupt-nw.png'),
    pyglet.resource.image('semi-dry-abrupt-n.png'),
    pyglet.resource.image('semi-dry-abrupt-ne.png'),
    pyglet.resource.image('semi-dry-abrupt-sw.png'),
    pyglet.resource.image('semi-dry-abrupt-s.png'),
    pyglet.resource.image('semi-dry-abrupt-se.png')
]

dry_grass_border_images = [
    pyglet.resource.image('dry-nw.png'),
    pyglet.resource.image('dry-n.png'),
    pyglet.resource.image('dry-ne.png'),
    pyglet.resource.image('dry-sw.png'),
    pyglet.resource.image('dry-s.png'),
    pyglet.resource.image('dry-se.png')
]

abrupt_dry_grass_border_images = [
    pyglet.resource.image('dry-abrupt-nw.png'),
    pyglet.resource.image('dry-abrupt-n.png'),
    pyglet.resource.image('dry-abrupt-ne.png'),
    pyglet.resource.image('dry-abrupt-sw.png'),
    pyglet.resource.image('dry-abrupt-s.png'),
    pyglet.resource.image('dry-abrupt-se.png')
]

for img in (grass_images + dry_grass_images + semidry_grass_images
    + grass_border_images + semidry_grass_border_images + dry_grass_border_images
    + abrupt_grass_border_images + abrupt_semidry_grass_border_images
    + abrupt_dry_grass_border_images):
    
    center_anchor(img)

def random_grass():
    return random.choice(grass_images)
    
def random_semidry_grass():
    return random.choice(semidry_grass_images)
    
def random_dry_grass():
    return random.choice(dry_grass_images)
    
def grass_border(hexdir):
    return grass_border_images[hexdir]
    
def abrupt_grass_border(hexdir):
    return abrupt_grass_border_images[hexdir]
    
def semidry_grass_border(hexdir):
    return semidry_grass_border_images[hexdir]
    
def abrupt_semidry_grass_border(hexdir):
    return abrupt_semidry_grass_border_images[hexdir]
    
def dry_grass_border(hexdir):
    return dry_grass_border_images[hexdir]
    
def abrupt_dry_grass_border(hexdir):
    return abrupt_dry_grass_border_images[hexdir]

#SNOW#
snow_images = [
    pyglet.resource.image('snow.png'),
    pyglet.resource.image('snow2.png'),
    pyglet.resource.image('snow3.png')
]

snow_hill_images = [
    pyglet.resource.image('snow_hill.png'),
    pyglet.resource.image('snow_hill2.png'),
    pyglet.resource.image('snow_hill3.png')
]

snow_mountain_images = [
    pyglet.resource.image('snow_mtn.png'),
    pyglet.resource.image('snow_mtn2.png'),
    pyglet.resource.image('snow_mtn3.png')
]

snow_border_images = [
    pyglet.resource.image('snow-nw.png'),
    pyglet.resource.image('snow-n.png'),
    pyglet.resource.image('snow-ne.png'),
    pyglet.resource.image('snow-sw.png'),
    pyglet.resource.image('snow-s.png'),
    pyglet.resource.image('snow-se.png')
]

snow_hill_border_images = [
    pyglet.resource.image('snow_hill-nw.png'),
    pyglet.resource.image('snow_hill-n.png'),
    pyglet.resource.image('snow_hill-ne.png'),
    pyglet.resource.image('snow_hill-sw.png'),
    pyglet.resource.image('snow_hill-s.png'),
    pyglet.resource.image('snow_hill-se.png')
]

snow_water_border_images = [
    pyglet.resource.image('snow-to-water-nw.png'),
    pyglet.resource.image('snow-to-water-n.png'),
    pyglet.resource.image('snow-to-water-ne.png'),
    pyglet.resource.image('snow-to-water-sw.png'),
    pyglet.resource.image('snow-to-water-s.png'),
    pyglet.resource.image('snow-to-water-se.png')
]
    
for img in (snow_images + snow_hill_images + 
    snow_mountain_images + snow_border_images +
    snow_hill_border_images + snow_water_border_images):
    center_anchor(img)
    
def random_snow():
    return random.choice(snow_images)
    
def random_snow_hills():
    return random.choice(snow_hill_images)
    
def random_snow_mountains():
    return random.choice(snow_mountain_images)
    
def snow_border(hexdir):
    return snow_border_images[hexdir]
    
def snow_hill_border(hexdir):
    return snow_hill_border_images[hexdir]
    
def snow_water_border(hexdir):
    return snow_water_border_images[hexdir]
    
#FOREST#
forest_images = [
    pyglet.resource.image('deciduous-summer1.png'),
    pyglet.resource.image('deciduous-summer2.png'),
    pyglet.resource.image('deciduous-summer3.png'),
    pyglet.resource.image('deciduous-summer4.png')
]

pine_images = [
    pyglet.resource.image('pine.png'),
    pyglet.resource.image('pine2.png'),
    pyglet.resource.image('pine3.png'),
    pyglet.resource.image('pine4.png')
]

rainforest_images = [
    pyglet.resource.image('rainforest.png'),
    pyglet.resource.image('rainforest2.png'),
    pyglet.resource.image('rainforest3.png'),
    pyglet.resource.image('rainforest4.png'),
    pyglet.resource.image('rainforest5.png'),
    pyglet.resource.image('rainforest6.png'),
    pyglet.resource.image('rainforest7.png'),
    pyglet.resource.image('rainforest8.png'),
    pyglet.resource.image('rainforest9.png')
]

savanna_forest_images = [
    pyglet.resource.image('savanna.png'),
    pyglet.resource.image('savanna2.png'),
    pyglet.resource.image('savanna3.png'),
    pyglet.resource.image('savanna4.png'),
    pyglet.resource.image('savanna5.png'),
    pyglet.resource.image('savanna6.png'),
    pyglet.resource.image('savanna7.png'),
    pyglet.resource.image('savanna8.png'),
    pyglet.resource.image('savanna9.png'),
    pyglet.resource.image('savanna10.png'),
    pyglet.resource.image('savanna11.png'),
    pyglet.resource.image('savanna12.png')
]

jungle_images = [
    pyglet.resource.image('jungle.png'),
    pyglet.resource.image('jungle2.png'),
    pyglet.resource.image('jungle3.png'),
    pyglet.resource.image('jungle4.png'),
    pyglet.resource.image('jungle5.png'),
    pyglet.resource.image('jungle6.png'),
    pyglet.resource.image('jungle7.png'),
    pyglet.resource.image('jungle8.png')
]

palm_images = [
    pyglet.resource.image('palm-desert.png'),
    pyglet.resource.image('palm-desert2.png'),
    pyglet.resource.image('palm-desert3.png'),
    pyglet.resource.image('palm-desert4.png'),
    pyglet.resource.image('palm-desert5.png'),
    pyglet.resource.image('palm-desert6.png')
]


for img in (
    forest_images + pine_images + rainforest_images + savanna_forest_images +
    jungle_images + palm_images):
    center_anchor(img)

def random_forest():
    img = random.choice(forest_images)
    return img

def random_pine():
    img = random.choice(pine_images)
    return img
    
def random_rainforest():
    img = random.choice(rainforest_images)
    return img
    
def random_savanna():
    img = random.choice(savanna_forest_images)
    return img
    
def random_jungle():
    img = random.choice(jungle_images)
    return img
    
def random_palm():
    img = random.choice(palm_images)
    return img

#HILLS#
hill_images = [
    pyglet.resource.image('regular.png'),
    pyglet.resource.image('regular2.png'),
    pyglet.resource.image('regular3.png')
]

dry_hill_images = [
    pyglet.resource.image('dry_hill.png'),
    pyglet.resource.image('dry_hill2.png'),
    pyglet.resource.image('dry_hill3.png')
]


for img in hill_images + dry_hill_images:
    center_anchor(img)
    
def random_hills():
    return random.choice(hill_images)
    
def random_dry_hills():
    return random.choice(dry_hill_images)
    
    
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

dry_mountain_images = [
    pyglet.resource.image('dry.png'),
    pyglet.resource.image('dry2.png'),
    pyglet.resource.image('dry3.png')
]

for img in dry_mountain_images:
    center_anchor(img)

def random_dry_mountain():
    img = random.choice(dry_mountain_images)
    return img
    
#ICE#
ice_images = [
    pyglet.resource.image('ice.png'),
    pyglet.resource.image('ice2.png'),
    pyglet.resource.image('ice3.png'),
    pyglet.resource.image('ice4.png'),
    pyglet.resource.image('ice5.png'),
    pyglet.resource.image('ice6.png')
]

ice_border_images = [
    pyglet.resource.image('ice-nw.png'),
    pyglet.resource.image('ice-n.png'),
    pyglet.resource.image('ice-ne.png'),
    pyglet.resource.image('ice-sw.png'),
    pyglet.resource.image('ice-s.png'),
    pyglet.resource.image('ice-se.png')
]

#indeces correspond to HexDir enum
ice_water_border_images = [
    pyglet.resource.image('ice-to-water-nw.png'),
    pyglet.resource.image('ice-to-water-n.png'),
    pyglet.resource.image('ice-to-water-ne.png'),
    pyglet.resource.image('ice-to-water-sw.png'),
    pyglet.resource.image('ice-to-water-s.png'),
    pyglet.resource.image('ice-to-water-se.png')
]

for img in ice_images + ice_border_images + ice_water_border_images:
    center_anchor(img)

def random_ice():
    img = random.choice(ice_images)
    return img
    
def ice_border(hexdir):
    return ice_border_images[hexdir]
    
def ice_water_border(hexdir):
    return ice_water_border_images[hexdir]
    
    
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
