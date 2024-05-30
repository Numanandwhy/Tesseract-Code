import pygame
import math
import numpy as np
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Trippy Tesseract Visualization')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Tesseract vertices and edges
vertices = [
    np.array([x, y, z, w])
    for x in [-1, 1]
    for y in [-1, 1]
    for z in [-1, 1]
    for w in [-1, 1]
]

edges = [
    (i, j) for i in range(len(vertices)) for j in range(i + 1, len(vertices))
    if np.sum(np.abs(vertices[i] - vertices[j])) == 2
]

# Projection functions
def rotate_4d(vertices, angle_xy, angle_zw, angle_xz, angle_yw):
    rotation_xy = np.array([
        [math.cos(angle_xy), -math.sin(angle_xy), 0, 0],
        [math.sin(angle_xy), math.cos(angle_xy), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])
    rotation_zw = np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, math.cos(angle_zw), -math.sin(angle_zw)],
        [0, 0, math.sin(angle_zw), math.cos(angle_zw)]
    ])
    rotation_xz = np.array([
        [math.cos(angle_xz), 0, -math.sin(angle_xz), 0],
        [0, 1, 0, 0],
        [math.sin(angle_xz), 0, math.cos(angle_xz), 0],
        [0, 0, 0, 1]
    ])
    rotation_yw = np.array([
        [1, 0, 0, 0],
        [0, math.cos(angle_yw), 0, -math.sin(angle_yw)],
        [0, 0, 1, 0],
        [0, math.sin(angle_yw), 0, math.cos(angle_yw)]
    ])
    rotated_vertices = [np.dot(np.dot(np.dot(np.dot(v, rotation_xy), rotation_zw), rotation_xz), rotation_yw) for v in vertices]
    return rotated_vertices

def project_3d_to_2d(v):
    distance = 10
    factor = distance / (distance - v[2])
    x = v[0] * factor * 100 + width // 2
    y = v[1] * factor * 100 + height // 2
    return np.array([x, y])

def bend_effect(v, time):
    # Apply a sinusoidal bending effect to the vertices
    bend_factor = 0.5
    new_v = v.copy()
    new_v[0] += bend_factor * math.sin(new_v[1] + time)
    new_v[1] += bend_factor * math.sin(new_v[2] + time)
    new_v[2] += bend_factor * math.sin(new_v[0] + time)
    return new_v

def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def gradient_color(start_color, end_color, factor):
    return tuple(
        int(start_color[i] + factor * (end_color[i] - start_color[i])) for i in range(3)
    )

# Main loop
running = True
angle_xy = 100
angle_zw = 100
angle_xz = 100
angle_yw = 100
time = 0

clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)

    # Rotate and project vertices
    rotated_vertices = rotate_4d(vertices, angle_xy, angle_zw, angle_xz, angle_yw)
    bent_vertices = [bend_effect(v, time) for v in rotated_vertices]
    projected_vertices = [project_3d_to_2d(v[:3]) for v in bent_vertices]
    YELLOW = (255, 255, 0)
    # Draw edges of the tesseract
    for edge in edges:
        points = [projected_vertices[edge[0]], projected_vertices[edge[1]]]
        pygame.draw.line(screen, YELLOW, points[0], points[1], 1)

    for vertex in projected_vertices:
        for i in range(4):  # Draw 8 lines from each vertex
            angle = i * (180 * math.pi / 1) + time
            end_x = vertex[0] + 1000 * math.cos(angle)
            end_y = vertex[1] + 1000 * math.sin(angle)
            color_factor = (math.sin(time + i) + 1) / 2
            color = gradient_color((255, 0, 0), (0, 0, 255), color_factor)
         #   pygame.draw.line(screen, color, vertex, (end_x, end_y), 1)

    pygame.display.flip()
    
    clock.tick(16)
    angle_xy += 0.01
    angle_zw += 0.013
    angle_xz += 0.015
    angle_yw += 0.017
    time += 0.005

pygame.quit()
