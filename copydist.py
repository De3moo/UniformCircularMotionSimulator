import pygame
import math
from tabulate import tabulate
from table import run

pygame.init()
WIDTH, HEIGHT = 1024, 768  
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)  
pygame.display.set_caption("Uniform Circular Motion Simulation")  

# Colors
WHITE = (255, 255, 255)  
BLACK = (0, 0, 0)  
RED = (255, 0, 0) 
BLUE = (0, 0, 255)  
GRAY = (200, 200, 200) 
DARK_GRAY = (100, 100, 100)  
GREEN = (0, 255, 0)  

font = pygame.font.SysFont(None, 24)
clock = pygame.time.Clock()  
radius = 1.0  
angle = 0.0  # Changed to float for trigonometric functions
angular_velocity = 0.1  
mass = 1.0 
tangential_velocity = 1.0
centripetal_acceleration = tangential_velocity**2/radius
centripetal_force = mass * centripetal_acceleration  
period = 2 * math.pi / angular_velocity  
frequency = 1 / period 

data_sim = []
simulation_running = True  

input_boxes = {
    "tangential_velocity": pygame.Rect(10, 150, 140, 30),
    "radius": pygame.Rect(10, 190, 140, 30),
    "mass": pygame.Rect(10, 230, 140, 30),
    "scaling_factor": pygame.Rect(10, 270, 140, 30)  
}


input_texts = {key: "" for key in input_boxes.keys()}
active_box = None  
simulation = 0
scale = 100  

def render_text(text, x, y):
    label = font.render(text, True, BLUE)
    screen.blit(label, (x, y))

def draw_button(text, x, y, w, h, active):
    color = RED if active else GREEN
    pygame.draw.rect(screen, color, (x, y, w, h))
    pygame.draw.rect(screen, BLACK, (x, y, w, h), 2)  
    label = font.render(text, True, BLACK)
    screen.blit(label, (x + w // 2 - label.get_width() // 2, y + h // 2 - label.get_height() // 2))

def draw_tablebutton(text, x, y, w, h, active):
    color = GRAY if active else GRAY
    pygame.draw.rect(screen, color, (x, y, w, h))
    pygame.draw.rect(screen, BLACK, (x, y, w, h), 2)  
    label = font.render(text, True, BLACK)
    screen.blit(label, (x + w // 2 - label.get_width() // 2, y + h // 2 - label.get_height() // 2))

def display_simulation(sim_center_x, sim_center_y):
    global angle
    pygame.draw.circle(screen, BLACK, (sim_center_x, sim_center_y), int(radius * scale), 1)
    pygame.draw.circle(screen, GREEN, (sim_center_x, sim_center_y), 5) 
    object_x = sim_center_x + radius * scale * math.cos(angle)
    object_y = sim_center_y + radius * scale * math.sin(angle)
    pygame.draw.line(screen, BLACK, (sim_center_x, sim_center_y), (int(object_x), int(object_y)), 2)  
    pygame.draw.circle(screen, RED, (int(object_x), int(object_y)), 10)  
    angle += tangential_velocity / 60  
    if angle >= 2 * math.pi:  
        angle -= 2 * math.pi

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos

            if 10 <= mouse_x <= 150 and 10 <= mouse_y <= 50:
                simulation_running = not simulation_running
               
            if 10 <= mouse_x <= 150 and 70 <= mouse_y <= 100:
                simulation+=1
                data_sim.append([simulation, radius, angle, angular_velocity, mass, tangential_velocity, centripetal_acceleration ,centripetal_force, period,frequency ])
                
            if 10 <= mouse_x <= 150 and 600 <= mouse_y <= 630:
                run(data_sim)
                pygame.quit()  # Added parentheses to actually quit pygame

            for key, box in input_boxes.items():
                if box.collidepoint(mouse_x, mouse_y):
                    active_box = key
                    break
            else:
                active_box = None
        if event.type == pygame.KEYDOWN and active_box is not None:
            if event.key == pygame.K_BACKSPACE:
                input_texts[active_box] = input_texts[active_box][:-1]
            elif event.key == pygame.K_RETURN:  
                try:
                    value = float(input_texts[active_box])
                    if active_box == "tangential_velocity":
                        tangential_velocity = max(0.01, value)
                    elif active_box == "radius":
                        radius = max(0.1, value)
                    elif active_box == "mass":
                        mass = max(0.1, value)
                    elif active_box == "centripetal_force":
                        centripetal_force = max(0.1, value)
                        centripetal_acceleration = centripetal_force / mass
                        tangential_velocity = math.sqrt(centripetal_acceleration / radius)
                    elif active_box == "scaling_factor":
                        scale = max(1, value)  
                  
                    period = 2 * math.pi / angular_velocity
                    frequency = 1 / period
                    angular_velocity = tangential_velocity / radius
                except ValueError:
                    pass
                input_texts[active_box] = ""  
            else:
                input_texts[active_box] += event.unicode
        if event.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = event.w, event.h
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    if active_box != "centripetal_force":
        centripetal_acceleration = tangential_velocity**2/radius
        centripetal_force = mass * centripetal_acceleration
        period = 2*(math.pi)*radius/tangential_velocity
        frequency = 1 / period
    screen.fill(WHITE)  

    draw_button("Stop" if simulation_running else "Start", 10, 10, 140, 40, True)
    draw_tablebutton("Add Sim", 10, 70, 140, 40, False )
    draw_tablebutton("Results", 10, 600, 140, 40, False )

    for key, box in input_boxes.items():
        pygame.draw.rect(screen, GRAY, box)  # Draw input box
        pygame.draw.rect(screen, BLACK, box, 2)  # Border
        label = font.render(input_texts[key], True, BLACK)
        screen.blit(label, (box.x + 5, box.y + 5))
    render_text("Tangential Velocity:", 160, 150)
    render_text("Radius (meters):", 160, 190)
    render_text("Mass (kg):", 160, 230)
    render_text("Scaling Factor:", 160, 270)  
    sim_center_x = WIDTH - 300
    sim_center_y = HEIGHT - 300

    if simulation_running:
        display_simulation(sim_center_x, sim_center_y)

    render_text(f"Total Simulations {len(data_sim)} ", 160, 80)
    render_text(f"Angular Velocity: {angular_velocity:.2f} rad/s", 10, 350)
    render_text(f"Radius: {radius:.2f} m", 10, 380)
    render_text(f"Mass: {mass:.1f} kg", 10, 410)
    render_text(f"Tangential Velocity: {tangential_velocity:.2f} m/s", 10, 440)
    render_text(f"Centripetal Acceleration: {centripetal_acceleration:.2f} m/s^2", 10, 470)
    render_text(f"Centripetal Force: {centripetal_force:.2f} N", 10, 500)
    render_text(f"Period: {period:.2f} s", 10, 530)
    render_text(f"Frequency: {frequency:.2f} Hz", 10, 560)
    render_text(f"Scaling 1 meter = : {scale:.2f} Pixels", 500, 100)  

    pygame.display.flip()   
    clock.tick(60)  

pygame.quit()
