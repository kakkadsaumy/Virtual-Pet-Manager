import pygame
import sys
import math
import random

# Constants 
WIDTH = 800
HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
LIGHT_GRAY = (200, 200, 200)
BLUE = (0, 100, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
MAX_STAT = 100
GAME_NAME = "Python Digital Assignment 1 - Saumy Kakkad and Reejashiwin Subramanian"

# Helper Functions

def lerp(a, b, t):
    return a + (b - a) * t


def clamp(value, min_val, max_val):
    return max(min_val, min(max_val, value))


def draw_quadratic_bezier(surface, start_point, control_point, end_point, width):
    points = []
    steps = 20
    for i in range(steps + 1):
        t = i / steps
        x = (1 - t) ** 2 * start_point[0] + 2 * (1 - t) * t * control_point[0] + t ** 2 * end_point[0]
        y = (1 - t) ** 2 * start_point[1] + 2 * (1 - t) * t * control_point[1] + t ** 2 * end_point[1]
        points.append((int(x), int(y)))

    if len(points) > 1:
        pygame.draw.lines(surface, BLACK, False, points, width)

# Pet Drawing Function

def draw_pet(surf, pet, center, size, time_now):
    species = pet.species
    base_happiness = pet.happiness / MAX_STAT

    # Coloring: happy => warm yellow/orange; unhappy => blueish
    r = int(lerp(120, 245, base_happiness))
    g = int(lerp(120, 225, base_happiness))
    b = int(lerp(200, 155, 1.0 - (1 - base_happiness) * 0.5))
    face_color = (clamp(r, 40, 255), clamp(g, 40, 255), clamp(b, 40, 255))

    small_font = pygame.font.SysFont("Arial", 12, bold=True)

    eye_size = 8
    left_eye_center = right_eye_center = (center[0], center[1])
    mouth_y = center[1]
    mouth_width = int(size * 0.4)

    if species == "dog":
        body_color = (218, 165, 32) 
        ear_color = (200, 140, 20)
        eye_color = BLACK

        pygame.draw.ellipse(surf, body_color, (center[0] - size, center[1] - size / 3, size * 2, size * 1.2))

        # Dog head
        head_radius = int(size * 0.8)
        head_center = (center[0], center[1] - int(size * 0.8))
        pygame.draw.circle(surf, body_color, head_center, head_radius)

        # Floppy ears
        ear_width = int(size * 0.6)
        ear_height = int(size * 0.8)
        # Left ear
        pygame.draw.ellipse(surf, ear_color,
                            (head_center[0] - head_radius - ear_width // 3,
                             head_center[1] - head_radius // 2,
                             ear_width, ear_height))
        # Right ear
        pygame.draw.ellipse(surf, ear_color,
                            (head_center[0] + head_radius - ear_width * 2 // 3,
                             head_center[1] - head_radius // 2,
                             ear_width, ear_height))

        # Muzzle
        muzzle_color = (240, 200, 160)
        muzzle_rect = (center[0] - size // 2, center[1] - int(size * 0.5), size, size // 2)
        pygame.draw.ellipse(surf, muzzle_color, muzzle_rect)

        # Black nose
        nose_size = int(size * 0.15)
        nose_center = (center[0], center[1] - int(size * 0.3))
        pygame.draw.circle(surf, (20, 20, 20), nose_center, nose_size)

        eye_offset_x = int(size * 0.25)
        eye_offset_y = int(size * -0.65)
        left_eye_center = (center[0] - eye_offset_x, center[1] + eye_offset_y)
        right_eye_center = (center[0] + eye_offset_x, center[1] + eye_offset_y)

        # Eyes
        pygame.draw.circle(surf, WHITE, left_eye_center, eye_size + 2)
        pygame.draw.circle(surf, eye_color, left_eye_center, eye_size)
        pygame.draw.circle(surf, WHITE, right_eye_center, eye_size + 2)
        pygame.draw.circle(surf, eye_color, right_eye_center, eye_size)

        # Smile
        mouth_y = center[1] - int(size * 0.2)
        mouth_width = int(size * 0.4)

        start_point = (center[0] - mouth_width // 2, mouth_y)
        end_point = (center[0] + mouth_width // 2, mouth_y)

        # Smile height varies with happiness
        smile_height = int(size * 0.2 * base_happiness)
        control_point = (center[0], mouth_y + smile_height)

        draw_quadratic_bezier(surf, start_point, control_point, end_point, 2)

        # Wagging tail
        tail_length = int(size * 0.8)
        wag = math.sin(time_now * 8) * (0.3 + base_happiness)
        tail_start = (center[0] + int(size * 0.9), center[1] + int(size * 0.1))
        tail_end = (tail_start[0] + int(tail_length * 0.4),
                    tail_start[1] + int(tail_length * 0.6) + int(wag * 20))
        pygame.draw.line(surf, body_color, tail_start, tail_end, 10)


    elif species == "cat":
        # Colors
        body_color = (170, 170, 170)
        ear_color = (130, 130, 130)
        inner_ear_color = (255, 200, 200)
        eye_color = (40, 40, 40)
        nose_color = (255, 150, 150)
        whisker_color = (20, 20, 20) 

        # Head
        head_r = int(size * 0.70)
        head_center = (center[0], center[1] - int(size * 0.4))
        pygame.draw.circle(surf, body_color, head_center, head_r)

        # Ears
        ear_base_width = head_r * 0.6
        ear_height = head_r * 1.0

        # Left Ear
        left_ear = [
            (head_center[0] - head_r * 0.8, head_center[1] - head_r * 0.4),
            (head_center[0] - head_r * 0.4, head_center[1] - head_r * 1.3),
            (head_center[0] - head_r * 0.1, head_center[1] - head_r * 0.4),
        ]
        pygame.draw.polygon(surf, ear_color, left_ear)

        # Left Inner Ear
        left_inner = [
            (head_center[0] - head_r * 0.7, head_center[1] - head_r * 0.5),
            (head_center[0] - head_r * 0.4, head_center[1] - head_r * 1.05),
            (head_center[0] - head_r * 0.2, head_center[1] - head_r * 0.5),
        ]
        pygame.draw.polygon(surf, inner_ear_color, left_inner)

        # Right Ear (mirrored)
        right_ear = [
            (head_center[0] + head_r * 0.8, head_center[1] - head_r * 0.4),
            (head_center[0] + head_r * 0.4, head_center[1] - head_r * 1.3),
            (head_center[0] + head_r * 0.1, head_center[1] - head_r * 0.4),
        ]
        pygame.draw.polygon(surf, ear_color, right_ear)

        # Right Inner Ear
        right_inner = [
            (head_center[0] + head_r * 0.7, head_center[1] - head_r * 0.5),
            (head_center[0] + head_r * 0.4, head_center[1] - head_r * 1.05),
            (head_center[0] + head_r * 0.2, head_center[1] - head_r * 0.5),
        ]
        pygame.draw.polygon(surf, inner_ear_color, right_inner)

        # Eyes
        eye_r = int(size * 0.1)  
        eye_offset_x = head_r * 0.35
        eye_offset_y = head_r * 0.1

        left_eye_center = (head_center[0] - eye_offset_x, head_center[1] - eye_offset_y)
        right_eye_center = (head_center[0] + eye_offset_x, head_center[1] - eye_offset_y)

        # White of the eye 
        eye_width_slanted = int(size * 0.3)
        eye_height_slanted = int(size * 0.15)

        # Left eye white
        left_eye_rect = pygame.Rect(0, 0, eye_width_slanted, eye_height_slanted)
        left_eye_rect.center = left_eye_center
        pygame.draw.ellipse(surf, WHITE, left_eye_rect)

        # Right eye white
        right_eye_rect = pygame.Rect(0, 0, eye_width_slanted, eye_height_slanted)
        right_eye_rect.center = right_eye_center
        pygame.draw.ellipse(surf, WHITE, right_eye_rect)

        # Pupils 
        pupil_width = int(eye_r * 0.3)
        pupil_height = int(eye_r * 1.5)
        pygame.draw.rect(surf, eye_color,
                         (left_eye_center[0] - pupil_width // 2,
                          left_eye_center[1] - pupil_height // 2,
                          pupil_width, pupil_height))
        pygame.draw.rect(surf, eye_color,
                         (right_eye_center[0] - pupil_width // 2,
                          right_eye_center[1] - pupil_height // 2,
                          pupil_width, pupil_height))

        # Nose
        nose_y = head_center[1] + size * 0.12
        nose_size = size * 0.1
        nose = [
            (head_center[0] - nose_size * 0.5, nose_y - nose_size * 0.5),
            (head_center[0] + nose_size * 0.5, nose_y - nose_size * 0.5),
            (head_center[0], nose_y),
        ]
        pygame.draw.polygon(surf, nose_color, nose)

        # Mouth
        mouth_y_start = nose_y
        mouth_line_len = size * 0.1

        pygame.draw.line(surf, eye_color, (head_center[0], mouth_y_start),
                         (head_center[0], mouth_y_start + mouth_line_len), 2)

        # Whiskers
        whisker_length = int(size * 0.6)
        whisker_y_start = nose_y - size * 0.05
        whisker_gap = int(size * 0.1)

        for i in range(3):
            # Left Whiskers
            y_offset = (i - 1) * whisker_gap
            pygame.draw.line(surf, whisker_color,
                             (head_center[0] - 5, whisker_y_start + y_offset),
                             (head_center[0] - whisker_length, whisker_y_start + y_offset + (i - 1) * 5), 1)

            # Right Whiskers
            pygame.draw.line(surf, whisker_color,
                             (head_center[0] + 5, whisker_y_start + y_offset),
                             (head_center[0] + whisker_length, whisker_y_start + y_offset + (i - 1) * 5), 1)

        # Body
        body_width = int(size * 1.6)
        body_height = int(size * 1.0)
        body_top_left = (center[0] - body_width // 2, center[1] - body_height // 2 + int(size * 0.2))
        pygame.draw.ellipse(surf, body_color, (body_top_left[0], body_top_left[1], body_width, body_height))

        # Paws
        paw_r = int(size * 0.20)
        paw_y = center[1] + size * 0.6
        pygame.draw.circle(surf, body_color, (center[0] - size * 0.35, paw_y), paw_r)
        pygame.draw.circle(surf, body_color, (center[0] + size * 0.35, paw_y), paw_r)

        # Tail
        tail_start = (center[0] + size * 0.6, center[1] + size * 0.3)
        tail_mid = (tail_start[0] + size * 0.6, tail_start[1] - size * 0.2)
        tail_end = (tail_start[0] + size * 0.9, tail_start[1] + size * 0.3)
        pygame.draw.lines(surf, body_color, False, [tail_start, tail_mid, tail_end], 10)

    elif species == "turtle":
        # Colors 
        shell_base_color = (60, 120, 60)       
        shell_pattern_color = (80, 140, 80)    
        skin_color = (100, 180, 100)           
        eye_pupil_color = BLACK
        mouth_color = BLACK

        # Body
        shell_rect_width = int(size * 1.8)
        shell_rect_height = int(size * 1.0)
        shell_rect = (center[0] - shell_rect_width // 2, center[1] - shell_rect_height // 2, shell_rect_width, shell_rect_height)
        pygame.draw.ellipse(surf, shell_base_color, shell_rect)

        # Shell Pattern 
        draw_quadratic_bezier(surf, (center[0], shell_rect[1]),
                              (center[0], center[1]),
                              (center[0], shell_rect[1] + shell_rect_height), 2)

        draw_quadratic_bezier(surf, (shell_rect[0] + shell_rect_width * 0.1, shell_rect[1] + shell_rect_height * 0.25),
                              (center[0], shell_rect[1] + shell_rect_height * 0.15),
                              (shell_rect[0] + shell_rect_width * 0.9, shell_rect[1] + shell_rect_height * 0.25), 2)
        draw_quadratic_bezier(surf, (shell_rect[0] + shell_rect_width * 0.1, shell_rect[1] + shell_rect_height * 0.5),
                              (center[0], shell_rect[1] + shell_rect_height * 0.4),
                              (shell_rect[0] + shell_rect_width * 0.9, shell_rect[1] + shell_rect_height * 0.5), 2)

        draw_quadratic_bezier(surf, (shell_rect[0] + shell_rect_width * 0.1, shell_rect[1] + shell_rect_height * 0.75),
                              (center[0], shell_rect[1] + shell_rect_height * 0.85),
                              (shell_rect[0] + shell_rect_width * 0.9, shell_rect[1] + shell_rect_height * 0.75), 2)

        pygame.draw.circle(surf, shell_pattern_color, (center[0], center[1] - int(shell_rect_height * 0.2)), int(size * 0.2))
        pygame.draw.circle(surf, shell_pattern_color, (center[0], center[1] + int(shell_rect_height * 0.2)), int(size * 0.2))
        pygame.draw.circle(surf, shell_pattern_color, (center[0] - int(shell_rect_width * 0.25), center[1]), int(size * 0.2))
        pygame.draw.circle(surf, shell_pattern_color, (center[0] + int(shell_rect_width * 0.25), center[1]), int(size * 0.2))


        # Neck
        neck_width = int(size * 0.4)
        neck_height = int(size * 0.3)
        neck_top_left = (center[0] - neck_width // 2, center[1] - shell_rect_height // 2 - neck_height * 0.8)
        neck_rect = pygame.Rect(neck_top_left[0], neck_top_left[1], neck_width, neck_height)
        pygame.draw.ellipse(surf, skin_color, neck_rect)


        # Head
        head_radius = int(size * 0.4)
        head_center_y = center[1] - shell_rect_height // 2 - neck_height * 0.8 - head_radius * 0.7
        head_center = (center[0], head_center_y)
        pygame.draw.ellipse(surf, skin_color, (head_center[0] - head_radius * 0.8, head_center_y - head_radius, head_radius * 1.6, head_radius * 1.5))

        # Eyes
        eye_offset_x = int(head_radius * 0.4)
        eye_offset_y = int(head_radius * 0.2)
        left_eye_center = (head_center[0] - eye_offset_x, head_center_y - eye_offset_y)
        right_eye_center = (head_center[0] + eye_offset_x, head_center_y - eye_offset_y)
        eye_size = int(lerp(3, 7, (pet.happiness + pet.energy) / (2 * MAX_STAT))) # Dynamic eye size

        # Whites of the eyes 
        pygame.draw.circle(surf, WHITE, left_eye_center, eye_size + 2)
        pygame.draw.circle(surf, WHITE, right_eye_center, eye_size + 2)

        # Pupils
        pygame.draw.circle(surf, eye_pupil_color, left_eye_center, eye_size)
        pygame.draw.circle(surf, eye_pupil_color, right_eye_center, eye_size)

        # Mouth
        mouth_start = (head_center[0] - int(head_radius * 0.3), head_center_y + int(head_radius * 0.5))
        mouth_end = (head_center[0] + int(head_radius * 0.3), head_center_y + int(head_radius * 0.5))
        pygame.draw.line(surf, mouth_color, mouth_start, mouth_end, 2)


        # Limbs
        limb_width = int(size * 0.6)
        limb_height = int(size * 0.3)

        # Front-left leg
        pygame.draw.ellipse(surf, skin_color,
                            (center[0] - shell_rect_width // 2 - limb_width * 0.6, # X
                             center[1] - shell_rect_height // 2 + limb_height * 0.8, # Y
                             limb_width, limb_height))

        # Front-right leg
        pygame.draw.ellipse(surf, skin_color,
                            (center[0] + shell_rect_width // 2 - limb_width * 0.4, # X
                             center[1] - shell_rect_height // 2 + limb_height * 0.8, # Y
                             limb_width, limb_height))

        # Back-left leg
        pygame.draw.ellipse(surf, skin_color,
                            (center[0] - shell_rect_width // 2 - limb_width * 0.3,
                             center[1] + shell_rect_height // 2 - limb_height * 1.2,
                             limb_width, limb_height))
        # Back-right leg
        pygame.draw.ellipse(surf, skin_color,
                            (center[0] + shell_rect_width // 2 - limb_width * 0.7,
                             center[1] + shell_rect_height // 2 - limb_height * 1.2,
                             limb_width, limb_height))


        # Tail
        tail_width = int(size * 0.2)
        tail_height = int(size * 0.2)
        tail_point_x = center[0]
        tail_point_y = center[1] + shell_rect_height // 2 + tail_height * 0.8

        tail_left = (tail_point_x - tail_width // 2, tail_point_y - tail_height)
        tail_right = (tail_point_x + tail_width // 2, tail_point_y - tail_height)
        tail_tip = (tail_point_x, tail_point_y)
        pygame.draw.polygon(surf, skin_color, [tail_left, tail_right, tail_tip])

        left_eye_center = left_eye_center
        right_eye_center = right_eye_center

# Class Definitions

class Pet:
    def __init__(self, name, species):
        self.name = name
        self.species = species
        self.happiness = 80 # Higher is better
        self.energy = 70  # Higher is better
        self.hunger = 20  # Lower is better
        self.size = 30  
        self.game_size = 100
        self.mood_decay_rate = 0.05  # Stat decay per update

    def update(self, dt):
        # Time-based decay of stats
        self.happiness = clamp(self.happiness - self.mood_decay_rate * dt * 5, 0, MAX_STAT)
        self.energy = clamp(self.energy - self.mood_decay_rate * dt * 3, 0, MAX_STAT)
        self.hunger = clamp(self.hunger + self.mood_decay_rate * dt * 2, 0, MAX_STAT)

        # Extreme Hunger/Fatigue impacts happiness
        if self.hunger > 80 or self.energy < 20:
            self.happiness = clamp(self.happiness - self.mood_decay_rate * dt * 10, 0, MAX_STAT)

    def feed(self):
        self.hunger = clamp(self.hunger - 30, 0, MAX_STAT)
        self.happiness = clamp(self.happiness + 15, 0, MAX_STAT)
        self.energy = clamp(self.energy + 5, 0, MAX_STAT)

    def play(self):
        self.energy = clamp(self.energy - 20, 0, MAX_STAT)
        self.happiness = clamp(self.happiness + 30, 0, MAX_STAT)
        self.hunger = clamp(self.hunger + 10, 0, MAX_STAT)

    def rest(self):
        self.energy = clamp(self.energy + 50, 0, MAX_STAT)
        self.happiness = clamp(self.happiness + 5, 0, MAX_STAT)
        self.hunger = clamp(self.hunger - 15, 0, MAX_STAT)

# Input Box 

class InputBox:
    def __init__(self, x, y, w, h, font):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = LIGHT_GRAY
        self.text = 'Enter a name!'
        self.font = font
        self.active = False
        self.text_surface = self.font.render(self.text, True, BLACK)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
                self.color = WHITE
                if self.text == "Enter a name!":
                    self.text = ''
                self.text_surface = self.font.render(self.text, True, BLACK)
            else:
                self.active = False
                self.color = LIGHT_GRAY
                if self.text == '':
                    self.text = "Enter a name for your pet"
                self.text_surface = self.font.render(self.text, True, BLACK)

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    text_to_return = self.text
                    self.active = False
                    self.color = LIGHT_GRAY
                    return text_to_return
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

                self.text_surface = self.font.render(self.text, True, BLACK)

                if self.text_surface.get_width() > self.rect.width - 10:
                    self.text = self.text[:-1]
                    self.text_surface = self.font.render(self.text, True, BLACK)

        return None

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.text_surface, (self.rect.x + 5, self.rect.y + 5))
        if self.active:
            pygame.draw.rect(screen, BLUE, self.rect, 2)

# Button Class
class Button:
    def __init__(self, x, y, w, h, text, font, color=GRAY, action=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = font
        self.color = color
        self.base_color = color
        self.text_surface = self.font.render(self.text, True, BLACK)
        self.action = action

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            current_color = tuple(min(255, c + 30) for c in self.base_color)
        else:
            current_color = self.base_color

        pygame.draw.rect(screen, current_color, self.rect, border_radius=8)
        text_rect = self.text_surface.get_rect(center=self.rect.center)
        screen.blit(self.text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            if self.action:
                self.action()
            return True
        return False

# GameManager Class 
class GameManager:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(GAME_NAME)
        self.clock = pygame.time.Clock()
        self.running = True
        self.time_now = 0.0

        self.font_large = pygame.font.SysFont("phosphate", 55)
        self.font_medium = pygame.font.SysFont("futura", 20)
        self.font_small = pygame.font.SysFont("futura", 16)

        self.game_state = "PET_CREATION"
        self.day_counter = 1
        self.pet = None
        self.pet_options = ["dog", "cat", "turtle"]
        self.selected_species = "dog"

        # Sparkle effect variables
        self.sparkle_timer = 0.0  
        self.sparkle_duration = 0.5  
        self.sparkle_position = (0, 0)
        self.particles = []

        self.input_box = None
        self.setup_ui()

    def setup_ui(self):
        self.input_box = InputBox(WIDTH // 2 - 150, HEIGHT // 2 - 100, 300, 40, self.font_medium)

        # Pet Creation Buttons 
        button_width = 90
        button_gap = 100  
        x_start = WIDTH // 2 - (len(self.pet_options) * button_gap) // 2 + (button_gap - button_width) // 2

        self.species_buttons = []
        for i, species in enumerate(self.pet_options):
            btn = Button(x_start + i * button_gap, HEIGHT // 2 - 40, button_width, 40, species.capitalize(),
                         self.font_small,
                         action=lambda s=species: self.select_species(s))
            self.species_buttons.append(btn)

        self.start_button = Button(WIDTH // 2 - 75, HEIGHT // 2 + 150, 150, 50, "Start Game", self.font_medium,
                                   action=self.create_pet_and_start)

        # UI for GAME state
        button_y = HEIGHT - 60
        self.action_buttons = [
            Button(50, button_y, 100, 40, "Feed", self.font_medium, color=GREEN, action=lambda: self.pet.feed()),
            Button(170, button_y, 100, 40, "Play", self.font_medium, color=BLUE, action=lambda: self.pet.play()),
            Button(290, button_y, 100, 40, "Rest", self.font_medium, color=LIGHT_GRAY, action=lambda: self.pet.rest()),
        ]

        utility_y = 20
        self.utility_buttons = [
            Button(WIDTH - 250, utility_y, 100, 40, "End Day", self.font_medium, color=ORANGE, action=self.end_day),
            Button(WIDTH - 130, utility_y, 100, 40, "Quit", self.font_medium, color=RED, action=self.quit_game),
        ]

    def select_species(self, species):
        self.selected_species = species

    def create_pet_and_start(self):
        name = self.input_box.text.strip()
        species = self.selected_species

        if name and name != "Enter a name":
            self.pet = Pet(name, species)
            self.pet.size = self.pet.game_size
            self.game_state = "GAME"
        else:
            print("Please enter a name for your pet.")
            self.input_box.text = "Enter a name for your pet!"
            self.input_box.text_surface = self.font_medium.render(self.input_box.text, True, RED)

    def end_day(self):
        # Advances the game time, increasing stat decay significantly and starting the sparkle effect.
        print(f"Day {self.day_counter} ended.")

        decay_multiplier = 50

        self.pet.happiness = clamp(self.pet.happiness - self.pet.mood_decay_rate * decay_multiplier * 5, 0, MAX_STAT)
        self.pet.energy = clamp(self.pet.energy - self.pet.mood_decay_rate * decay_multiplier * 3, 0, MAX_STAT)
        self.pet.hunger = clamp(self.pet.hunger + self.pet.mood_decay_rate * decay_multiplier * 2, 0, MAX_STAT)

        self.day_counter += 1

        # Start the sparkle effect
        self.sparkle_timer = self.sparkle_duration
        self.sparkle_position = (WIDTH // 2, HEIGHT // 2 + 50)
        self.particles = []

        # Generate initial burst of particles
        for _ in range(30):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 6)
            life = random.uniform(0.1, self.sparkle_duration)
            self.particles.append([
                self.sparkle_position[0] + random.randint(-self.pet.size, self.pet.size),
                self.sparkle_position[1] + random.randint(-self.pet.size, self.pet.size),
                math.cos(angle) * speed,
                math.sin(angle) * speed,
                life
            ])

    def quit_game(self):
        self.running = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if self.game_state == "PET_CREATION":
                result = self.input_box.handle_event(event)
                if result:
                    self.create_pet_and_start()  # Handle name submission via Enter key

                for btn in self.species_buttons:
                    btn.handle_event(event)
                self.start_button.handle_event(event)

            elif self.game_state == "GAME":
                for btn in self.action_buttons:
                    btn.handle_event(event)
                for btn in self.utility_buttons:
                    btn.handle_event(event)

    def update(self):
        dt = self.clock.tick(FPS) / 1000.0
        self.time_now = pygame.time.get_ticks() / 1000.0

        if self.game_state == "GAME" and self.pet:
            self.pet.update(dt)

            if self.pet.happiness <= 5 or self.pet.hunger >= 95 or self.pet.energy <= 5:
                if self.day_counter >= 3:
                    self.game_state = "GAME_OVER"

            if self.sparkle_timer > 0:
                self.sparkle_timer -= dt

                new_particles = []
                for p in self.particles:
                    p[0] += p[2] * dt * 60  
                    p[1] += p[3] * dt * 60  
                    p[4] -= dt 

                    if p[4] > 0:
                        new_particles.append(p)
                self.particles = new_particles

                # Add a few fading particles over time
                if random.random() < 0.3:
                    angle = random.uniform(0, 2 * math.pi)
                    speed = random.uniform(1, 4)
                    life = random.uniform(0.1, self.sparkle_timer)
                    if life > 0:
                        self.particles.append([
                            self.sparkle_position[0] + random.randint(-self.pet.size // 2, self.pet.size // 2),
                            self.sparkle_position[1] + random.randint(-self.pet.size // 2, self.pet.size // 2),
                            math.cos(angle) * speed,
                            math.sin(angle) * speed,
                            life
                        ])
            else:
                self.particles = []

    def draw_sparkles(self):
        if self.sparkle_timer > 0:
            for p in self.particles:
                # Calculate size based on particle life
                life_ratio = p[4] / self.sparkle_duration
                radius = int(lerp(1, 4, life_ratio))

                # Draw the particle 
                try:
                    pygame.draw.circle(self.screen, YELLOW, (int(p[0]), int(p[1])), radius)
                except ValueError:
                    pass

    def draw_ui_background(self):
        self.screen.fill((230, 240, 250))

    def draw_pet_creation(self):
        self.draw_ui_background()
        
        # Title
        title_text = self.font_large.render("Create Your Pet", True, BLACK)
        self.screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 70))

        # Name input 
        name_label = self.font_medium.render("Pet Name:", True, BLACK)
        self.screen.blit(name_label, (WIDTH // 2 - name_label.get_width() // 2, HEIGHT // 2 - 165))

        self.input_box.rect.centerx = WIDTH // 2
        self.input_box.rect.y = HEIGHT // 2 - 140
        self.input_box.draw(self.screen)

        # Species selection 
        species_label = self.font_medium.render("Choose Species:", True, BLACK)
        self.screen.blit(species_label, (WIDTH // 2 - species_label.get_width() // 2, HEIGHT // 2 - 75))

        # Pet preview 
        preview_size = 45
        preview_center = (WIDTH // 2, HEIGHT // 2 + 25)  
        temp_pet = Pet("Preview", self.selected_species)
        draw_pet(self.screen, temp_pet, preview_center, preview_size, self.time_now)

        # Species buttons 
        button_width = 90
        button_gap = 100
        x_start = WIDTH // 2 - (len(self.pet_options) * button_gap) // 2 + (button_gap - button_width) // 2
        y_position = HEIGHT // 2 + 80

        for i, btn in enumerate(self.species_buttons):
            btn.rect.x = x_start + i * button_gap
            btn.rect.y = y_position
            if btn.text.lower() == self.selected_species:
                btn.base_color = ORANGE
            else:
                btn.base_color = (255, 0, 255)
            btn.draw(self.screen)

        # Start button 
        self.start_button.rect.centerx = WIDTH // 2
        self.start_button.rect.y = HEIGHT // 2 + 148
        self.start_button.draw(self.screen)

    def draw_game(self):
        self.screen.fill((180, 220, 255))

        # Draw Pet 
        # The pet's center position = (WIDTH//2, HEIGHT//2 + 50)
        draw_pet(self.screen, self.pet, (WIDTH // 2, HEIGHT // 2 + 50), self.pet.size, self.time_now)

        # Draw Sparkles on the pet
        self.draw_sparkles()

        # Draw Stats

        # Day Counter 
        day_text = self.font_medium.render(f"Day: {self.day_counter}", True, BLACK)
        self.screen.blit(day_text, (20, 20))

        # Pet Name 
      
        name_text = self.font_large.render(self.pet.name, True, BLACK)
        self.screen.blit(name_text, (20, 55)) 

        stats_y = 120  

        stat_gap = 30  

        self.draw_stat_bar("Happiness", self.pet.happiness, (20, stats_y), (255, 200, 0))
        self.draw_stat_bar("Energy", self.pet.energy, (20, stats_y + stat_gap), (0, 255, 0))
        self.draw_stat_bar("Hunger", MAX_STAT - self.pet.hunger, (20, stats_y + stat_gap * 2), (165, 42, 42))

        for btn in self.action_buttons:
            btn.draw(self.screen)
        for btn in self.utility_buttons:
            btn.draw(self.screen)

    def draw_stat_bar(self, label, value, position, color):
        x, y = position
        bar_width = 150
        bar_height = 15

        text = self.font_small.render(f"{label}: {int(value)}%", True, BLACK)
        self.screen.blit(text, (x, y))

        bar_x_start = x + 160

        pygame.draw.rect(self.screen, GRAY, (bar_x_start, y + 2, bar_width, bar_height))
        fill_width = (value / MAX_STAT) * bar_width
        pygame.draw.rect(self.screen, color, (bar_x_start, y + 2, fill_width, bar_height))
        pygame.draw.rect(self.screen, BLACK, (bar_x_start, y + 2, bar_width, bar_height), 1)

    def draw_game_over(self):
        self.screen.fill(BLACK)
        game_over_text = self.font_large.render(f"{self.pet.name} passed away...", True, RED)
        self.screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))

        info_text = self.font_medium.render(
            f"You managed to keep them alive for {self.day_counter} days. Reload to play again.", True, WHITE)
        self.screen.blit(info_text, (WIDTH // 2 - info_text.get_width() // 2, HEIGHT // 2 + 20))

    def draw(self):
        if self.game_state == "PET_CREATION":
            self.draw_pet_creation()
        elif self.game_state == "GAME" and self.pet:
            self.draw_game()
        elif self.game_state == "GAME_OVER":
            self.draw_game_over()

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()

        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    game = GameManager()
    game.run()