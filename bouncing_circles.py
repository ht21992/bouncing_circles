import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Constants
WIDTH, HEIGHT = 600, 600
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
FPS = 60

# Function to draw a circle
def draw_circle(surface, color, center, radius, width=0):
    pygame.draw.circle(surface, color, center, radius, width)

# Function to draw a line
def draw_line(surface, color, start_pos, end_pos, width=1):
    pygame.draw.line(surface, color, start_pos, end_pos, width)

# Function to calculate distance between two points
def distance(p1, p2):
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

# Function to calculate reflection vector
def reflect_vector(vector, normal):
    dot = vector[0] * normal[0] + vector[1] * normal[1]
    return (vector[0] - 2 * dot * normal[0], vector[1] - 2 * dot * normal[1])

# Function to create a particle effect
def create_particles(position, color, num_particles=10):
    particles = []
    for _ in range(num_particles):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(1, 5)
        particles.append({
            'position': position,
            'velocity': (speed * math.cos(angle), speed * math.sin(angle)),
            'color': color,
            'ttl': random.randint(10, 30)
        })
    return particles

# Main function
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Bouncing Circles")

    clock = pygame.time.Clock()

    # Circle properties
    circle_radius = 200
    inner_circle_radius = 20

    # Blue circle properties
    blue_circle_pos = [random.randint(circle_radius + inner_circle_radius, WIDTH - circle_radius - inner_circle_radius),
                       random.randint(circle_radius + inner_circle_radius, HEIGHT - circle_radius - inner_circle_radius)]
    blue_circle_speed = [random.randint(-5, 5), random.randint(-5, 5)]
    blue_circle_color = BLUE

    # Green circle properties
    green_circle_pos = [random.randint(circle_radius + inner_circle_radius, WIDTH - circle_radius - inner_circle_radius),
                        random.randint(circle_radius + inner_circle_radius, HEIGHT - circle_radius - inner_circle_radius)]
    green_circle_speed = [random.randint(-5, 5), random.randint(-5, 5)]
    green_circle_color = GREEN

    collision_points_blue = []  # List to store collision points for blue circle
    collision_points_green = []  # List to store collision points for green circle

    # Checkbox properties
    checkbox_rect = pygame.Rect(50, 50, 20, 20)
    checkbox_checked = False

    # Font setup
    font = pygame.font.Font(None, 24)

    # Particle effects
    blue_particles = []
    green_particles = []

    # Sound effects
    collision_sound = pygame.mixer.Sound('collision.mp3')

    running = True
    while running:
        screen.fill((0, 0, 0))

        # Draw outer circle
        draw_circle(screen, RED, (WIDTH // 2, HEIGHT // 2), circle_radius, 2)

        # Draw fancy checkbox
        pygame.draw.rect(screen, WHITE, checkbox_rect, 2)
        if checkbox_checked:
            pygame.draw.rect(screen, GREEN, (checkbox_rect.x + 3, checkbox_rect.y + 3, 14, 14))

        # Draw text next to checkbox
        text_surface = font.render("Activate/Deactivate Collision", True, WHITE)
        screen.blit(text_surface, (checkbox_rect.right + 10, checkbox_rect.centery - text_surface.get_height() // 2))

        # Draw help text for changing colors
        help_text_surface_b = font.render("Press 'B' to change blue circle color", True, BLUE)
        screen.blit(help_text_surface_b, (20, HEIGHT - 60))
        help_text_surface_g = font.render("Press 'G' to change green circle color", True, GREEN)
        screen.blit(help_text_surface_g, (20, HEIGHT - 30))

        # Update blue circle position
        blue_circle_pos[0] += blue_circle_speed[0]
        blue_circle_pos[1] += blue_circle_speed[1]

        # Update green circle position
        green_circle_pos[0] += green_circle_speed[0]
        green_circle_pos[1] += green_circle_speed[1]

        # Check for collision with boundaries for blue circle
        if blue_circle_pos[0] - inner_circle_radius < 0 or blue_circle_pos[0] + inner_circle_radius > WIDTH:
            blue_circle_speed[0] *= -1
        if blue_circle_pos[1] - inner_circle_radius < 0 or blue_circle_pos[1] + inner_circle_radius > HEIGHT:
            blue_circle_speed[1] *= -1

        # Check for collision with boundaries for green circle
        if green_circle_pos[0] - inner_circle_radius < 0 or green_circle_pos[0] + inner_circle_radius > WIDTH:
            green_circle_speed[0] *= -1
        if green_circle_pos[1] - inner_circle_radius < 0 or green_circle_pos[1] + inner_circle_radius > HEIGHT:
            green_circle_speed[1] *= -1

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                if checkbox_rect.collidepoint(mouse_pos):
                    checkbox_checked = not checkbox_checked
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:  # Change blue circle color
                    blue_circle_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                elif event.key == pygame.K_g:  # Change green circle color
                    green_circle_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        # Check for collision between blue and red circle
        distance_to_center_blue = distance((WIDTH // 2, HEIGHT // 2), blue_circle_pos)
        if distance_to_center_blue + inner_circle_radius >= circle_radius:
            normal_blue = ((blue_circle_pos[0] - WIDTH // 2) / distance_to_center_blue,
                          (blue_circle_pos[1] - HEIGHT // 2) / distance_to_center_blue)
            blue_circle_speed = reflect_vector(blue_circle_speed, normal_blue)
            intersection_point_blue = (int(blue_circle_pos[0] - blue_circle_speed[0]),
                                       int(blue_circle_pos[1] - blue_circle_speed[1]))
            collision_points_blue.append(intersection_point_blue)
            blue_particles += create_particles(intersection_point_blue, blue_circle_color)

        # Check for collision between green and red circle
        distance_to_center_green = distance((WIDTH // 2, HEIGHT // 2), green_circle_pos)
        if distance_to_center_green + inner_circle_radius >= circle_radius:
            normal_green = ((green_circle_pos[0] - WIDTH // 2) / distance_to_center_green,
                            (green_circle_pos[1] - HEIGHT // 2) / distance_to_center_green)
            green_circle_speed = reflect_vector(green_circle_speed, normal_green)
            intersection_point_green = (int(green_circle_pos[0] - green_circle_speed[0]),
                                        int(green_circle_pos[1] - green_circle_speed[1]))
            collision_points_green.append(intersection_point_green)
            green_particles += create_particles(intersection_point_green, green_circle_color)

        # Check for collision between blue and green circles if checkbox is checked
        if checkbox_checked:
            distance_blue_green = distance(blue_circle_pos, green_circle_pos)
            if distance_blue_green <= inner_circle_radius * 2:
                normal_blue_green = [(green_circle_pos[0] - blue_circle_pos[0]) / distance_blue_green,
                                     (green_circle_pos[1] - blue_circle_pos[1]) / distance_blue_green]
                blue_circle_speed = reflect_vector(blue_circle_speed, normal_blue_green)
                green_circle_speed = reflect_vector(green_circle_speed, normal_blue_green)
                collision_sound.play()

        # Draw lines between collision points for blue circle with blue color
        for i in range(len(collision_points_blue) - 1):
            draw_line(screen, blue_circle_color, collision_points_blue[i], collision_points_blue[i + 1])

        # Draw lines between collision points for green circle with green color
        for i in range(len(collision_points_green) - 1):
            draw_line(screen, green_circle_color, collision_points_green[i], collision_points_green[i + 1])

        # Draw blue circle
        draw_circle(screen, blue_circle_color, (int(blue_circle_pos[0]), int(blue_circle_pos[1])), inner_circle_radius)

        # Draw green circle
        draw_circle(screen, green_circle_color, (int(green_circle_pos[0]), int(green_circle_pos[1])), inner_circle_radius)

        # Update and draw particles
        for particle in blue_particles[:]:
            particle['position'] = (particle['position'][0] + particle['velocity'][0],
                                    particle['position'][1] + particle['velocity'][1])
            particle['ttl'] -= 1
            if particle['ttl'] <= 0:
                blue_particles.remove(particle)
            else:
                draw_circle(screen, particle['color'], (int(particle['position'][0]), int(particle['position'][1])), 2)

        for particle in green_particles[:]:
            particle['position'] = (particle['position'][0] + particle['velocity'][0],
                                    particle['position'][1] + particle['velocity'][1])
            particle['ttl'] -= 1
            if particle['ttl'] <= 0:
                green_particles.remove(particle)
            else:
                draw_circle(screen, particle['color'], (int(particle['position'][0]), int(particle['position'][1])), 2)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
