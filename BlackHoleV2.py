import pygame
import math
import random
import sys

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
FPS = 60
BLACK_HOLE_RADIUS = 50
EVENT_HORIZON_RADIUS = 120
ACCELERATION = 0.05
MAX_PARTICLES = 1000
PARTICLE_SIZE = 3
STARS_COUNT = 300
BACKGROUND_COLOR = (0, 0, 0)
LIGHT_BEND_STRENGTH = 30

# Colors
WHITE = (255, 255, 255)
GREY = (169, 169, 169)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (25, 25, 50)
BLACK = (0, 0, 0)

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Black Hole Visualization")
clock = pygame.time.Clock()

# Particle class to simulate the accretion disk
class Particle:
    def __init__(self, x, y, angle, speed, color):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.color = color
        self.size = PARTICLE_SIZE

    def update(self, center_x, center_y):
        # Rotate particles around the black hole
        self.angle += self.speed
        self.x = center_x + 150 * math.cos(self.angle)
        self.y = center_y + 150 * math.sin(self.angle)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)

# Star class to simulate background stars
class Star:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT)
        self.size = random.randint(1, 3)
        self.speed = random.uniform(0.1, 0.5)

    def update(self):
        self.x += self.speed
        if self.x > SCREEN_WIDTH:
            self.x = 0
        self.y += self.speed
        if self.y > SCREEN_HEIGHT:
            self.y = 0

    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.size)

# Background class to handle starfield and warping effect
class Starfield:
    def __init__(self, star_count):
        self.stars = [Star() for _ in range(star_count)]

    def update(self):
        for star in self.stars:
            star.update()

    def draw(self, screen):
        for star in self.stars:
            star.draw(screen)

# Function to draw the black hole event horizon
def draw_black_hole(screen, center_x, center_y):
    pygame.draw.circle(screen, BLACK, (center_x, center_y), BLACK_HOLE_RADIUS)
    pygame.draw.circle(screen, GREY, (center_x, center_y), EVENT_HORIZON_RADIUS, 5)

# Function to simulate gravitational lensing (distortion of light around black hole)
def gravitational_lensing(screen, stars, center_x, center_y):
    for star in stars:
        dx = star.x - center_x
        dy = star.y - center_y
        distance = math.hypot(dx, dy)
        
        if distance < EVENT_HORIZON_RADIUS + LIGHT_BEND_STRENGTH:
            # Apply light bending effect based on proximity
            lensing_factor = (EVENT_HORIZON_RADIUS + LIGHT_BEND_STRENGTH - distance) / LIGHT_BEND_STRENGTH
            warped_x = center_x + dx * lensing_factor
            warped_y = center_y + dy * lensing_factor
            star.x = warped_x
            star.y = warped_y

# Function to draw the accretion disk with varying particle sizes
def draw_accretion_disk(screen, particles, center_x, center_y):
    for particle in particles:
        particle.update(center_x, center_y)
        particle.draw(screen)

# Function to simulate a pulsar effect from the black hole
def pulsar_effect(screen, center_x, center_y, frame):
    pulse_intensity = (math.sin(frame / 10) + 1) * 0.5  # Sinusoidal intensity
    pygame.draw.circle(screen, (255, int(pulse_intensity * 255), 0), (center_x, center_y), BLACK_HOLE_RADIUS + int(pulse_intensity * 30))

# Function to handle camera movement and zoom
def move_camera(screen, x_offset, y_offset, zoom_factor):
    return pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA), x_offset, y_offset, zoom_factor

def main():
    running = True
    center_x = SCREEN_WIDTH // 2
    center_y = SCREEN_HEIGHT // 2
    particles = []
    stars = []

    # Initialize particles for the accretion disk
    for _ in range(MAX_PARTICLES):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(0.02, 0.05)
        color = random.choice([RED, YELLOW])
        particles.append(Particle(center_x, center_y, angle, speed, color))

    # Initialize starfield
    starfield = Starfield(STARS_COUNT)

    # Frame counter for pulsar effect
    frame = 0

    # Main game loop
    while running:
        screen.fill(BACKGROUND_COLOR)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update the starfield and gravitational lensing
        starfield.update()
        gravitational_lensing(screen, starfield.stars, center_x, center_y)

        # Draw the background stars
        starfield.draw(screen)

        # Draw the black hole (event horizon and center)
        draw_black_hole(screen, center_x, center_y)

        # Draw the accretion disk (particles rotating around the black hole)
        draw_accretion_disk(screen, particles, center_x, center_y)

        # Add pulsar effect
        pulsar_effect(screen, center_x, center_y, frame)

        # Update the display
        pygame.display.flip()

        # Increment frame counter for pulsar effect
        frame += 1

        # Control frame rate
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
