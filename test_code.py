import pygame as pg
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import random

pg.init()
pg.mixer.init()
pg.mixer.music.load('andromeda-space-adventure-403080.mp3')
pg.mixer.music.play(-1)

display = (1200, 800)
pg.display.set_mode(display, pg.DOUBLEBUF | pg.OPENGL)

gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
glTranslatef(0.0, 0.0, -20.0)
glEnable(GL_DEPTH_TEST)

SUN_COLOR = (1.0, 0.80, 0.20)
SUN_CENTER_COLOR = (1.0, 0.95, 0.30)
SUN_EDGE_COLOR = (0.8, 0.40, 0.10)
MERCURY_COLOR = (0.75, 0.62, 0.45)
VENUS_COLOR = (0.95, 0.80, 0.70)
EARTH_COLOR = (0.2, 0.6, 0.7)
MARS_COLOR = (0.90, 0.30, 0.22)
JUPITER_COLOR = (0.90, 0.75, 0.55)
SATURN_COLOR = (0.98, 0.93, 0.60)
URANUS_COLOR = (0.55, 0.85, 0.98)
NEPTUNE_COLOR = (0.25, 0.45, 0.85)

STAR_COUNT = 500
stars = []
for _ in range(STAR_COUNT):
    x = random.uniform(-50, 50)
    y = random.uniform(-50, 50)
    z = random.uniform(-50, 50)
    speed = random.uniform(0.01, 0.05)
    stars.append([x, y, z, speed])


def draw_sphere(radius, slices, stacks, color, rotation, angle=0, distance=0):
    glPushMatrix()
    glRotatef(rotation, 0, 1, 0)
    if color == SUN_COLOR:
        for i in range(slices):
            theta1 = i * math.pi * 2 / slices
            theta2 = (i + 1) * math.pi * 2 / slices
            glBegin(GL_QUAD_STRIP)
            for j in range(stacks + 1):
                phi = j * math.pi / stacks
                x1 = radius * math.cos(theta1) * math.sin(phi)
                y1 = radius * math.sin(theta1) * math.sin(phi)
                z1 = radius * math.cos(phi)
                x2 = radius * math.cos(theta2) * math.sin(phi)
                y2 = radius * math.sin(theta2) * math.sin(phi)
                z2 = radius * math.cos(phi)
                y_normalized = (y1 + radius) / (2 * radius)
                shade = 0.3 + y_normalized * 0.7
                glColor3f(1.0, shade, 0.0)
                glVertex3f(x1, y1, z1)
                glVertex3f(x2, y2, z2)
            glEnd()
    else:
        for i in range(slices):
            theta1 = i * math.pi * 2 / slices
            theta2 = (i + 1) * math.pi * 2 / slices
            glBegin(GL_QUAD_STRIP)
            for j in range(stacks + 1):
                phi = j * math.pi / stacks
                x1 = radius * math.cos(theta1) * math.sin(phi)
                y1 = radius * math.sin(theta1) * math.sin(phi)
                z1 = radius * math.cos(phi)
                x2 = radius * math.cos(theta2) * math.sin(phi)
                y2 = radius * math.sin(theta2) * math.sin(phi)
                z2 = radius * math.cos(phi)
                planet_x = distance * math.cos(math.radians(angle - camera_angle))
                planet_z = distance * math.sin(math.radians(angle - camera_angle))
                if planet_z > 0:
                    dark_color = (color[0] * 0.3, color[1] * 0.3, color[2] * 0.3)
                    glColor3fv(dark_color)
                else:
                    glColor3fv(color)
                glVertex3f(x1, y1, z1)
                glVertex3f(x2, y2, z2)
            glEnd()
    glPopMatrix()


def draw_ring(inner_radius, outer_radius, segments):
    glBegin(GL_QUAD_STRIP)
    for i in range(segments + 1):
        angle = i * 2 * math.pi / segments
        x = math.cos(angle)
        z = math.sin(angle)
        glColor3f(0.8, 0.8, 0.8)
        glVertex3f(x * inner_radius, 0, z * inner_radius)
        glVertex3f(x * outer_radius, 0, z * outer_radius)
    glEnd()


def draw_orbit(radius):
    glBegin(GL_LINE_LOOP)
    glColor3f(0.3, 0.3, 0.3)
    for i in range(0, 360, 5):
        angle = math.radians(i)
        x = math.cos(angle) * radius
        z = math.sin(angle) * radius
        glVertex3f(x, 0, z)
    glEnd()


def draw_stars():
    glBegin(GL_POINTS)
    glColor3f(1, 1, 1)
    for star in stars:
        glVertex3f(star[0], star[1], star[2])
        star[2] -= star[3]
        if star[2] < -50:
            star[2] = 50
            star[0] = random.uniform(-50, 50)
            star[1] = random.uniform(-50, 50)
    glEnd()


def update_planet(planet):
    planet['angle'] += planet['speed']
    planet['rotation'] += planet['rotation_speed']
    if planet['angle'] >= 360:
        planet['angle'] -= 360
    if planet['rotation'] >= 360:
        planet['rotation'] -= 360
    return planet


def draw_planet(planet):
    glPushMatrix()
    glRotatef(planet['angle'], 0, 1, 0)
    glTranslatef(planet['distance'], 0, 0)
    draw_sphere(planet['radius'], 16, 16, planet['color'], planet['rotation'], planet['angle'], planet['distance'])
    glPopMatrix()


def draw_ringed_planet(planet):
    draw_planet(planet)
    glPushMatrix()
    glRotatef(planet['angle'], 0, 1, 0)
    glTranslatef(planet['distance'], 0, 0)
    draw_ring(planet['ring_radius'], planet['ring_radius'] + 0.2, 32)
    glPopMatrix()


planets = [
    {'radius': 0.4, 'distance': 4, 'color': MERCURY_COLOR, 'speed': 0.5, 'rotation_speed': 0.5, 'angle': random.uniform(0, 360), 'rotation': 0},
    {'radius': 0.6, 'distance': 5, 'color': VENUS_COLOR, 'speed': 0.4, 'rotation_speed': 0.4, 'angle': random.uniform(0, 360), 'rotation': 0},
    {'radius': 0.7, 'distance': 6, 'color': EARTH_COLOR, 'speed': 0.3, 'rotation_speed': 0.3, 'angle': random.uniform(0, 360), 'rotation': 0},
    {'radius': 0.5, 'distance': 7, 'color': MARS_COLOR, 'speed': 0.25, 'rotation_speed': 0.25, 'angle': random.uniform(0, 360), 'rotation': 0},
    {'radius': 1.2, 'distance': 9, 'color': JUPITER_COLOR, 'speed': 0.2, 'rotation_speed': 0.2, 'angle': random.uniform(0, 360), 'rotation': 0},
    {'radius': 1.0, 'distance': 11, 'color': SATURN_COLOR, 'speed': 0.15, 'rotation_speed': 0.15, 'angle': random.uniform(0, 360), 'rotation': 0, 'ring_radius': 1.5},
    {'radius': 0.8, 'distance': 13, 'color': URANUS_COLOR, 'speed': 0.1, 'rotation_speed': 0.1, 'angle': random.uniform(0, 360), 'rotation': 0},
    {'radius': 0.8, 'distance': 15, 'color': NEPTUNE_COLOR, 'speed': 0.08, 'rotation_speed': 0.08, 'angle': random.uniform(0, 360), 'rotation': 0}
]

camera_angle = 0
camera_distance = 30
clock = pg.time.Clock()

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                camera_angle += 5
            elif event.key == pg.K_RIGHT:
                camera_angle -= 5
            elif event.key == pg.K_UP:
                camera_distance = max(10, camera_distance - 1)
            elif event.key == pg.K_DOWN:
                camera_distance = min(30, camera_distance + 1)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glLoadIdentity()

    gluPerspective(45, (display[0] / display[1]), 0.1, 100.0)
    camera_x = math.sin(math.radians(camera_angle)) * camera_distance
    camera_z = math.cos(math.radians(camera_angle)) * camera_distance
    camera_height = 5 + (camera_distance * 0.1)
    gluLookAt(camera_x, camera_height, camera_z, 0, 0, 0, 0, 1, 0)

    draw_stars()
    draw_sphere(2.0, 16, 16, SUN_COLOR, 0)

    for planet in planets:
        draw_orbit(planet['distance'])
        planet = update_planet(planet)
        if 'ring_radius' in planet:
            draw_ringed_planet(planet)
        else:
            draw_planet(planet)

    pg.display.flip()
    clock.tick(60)


