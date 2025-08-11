import pygame
import math
import random
import sys

# --- Constants ---
# Screen dimensions
WIDTH, HEIGHT = 1200, 900
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE_ROBOT = (50, 50, 255)
GRAY = (40, 40, 40)
BLUE_LINE = (0, 150, 255)
GOAL_COLOR = (255, 215, 0) # Gold for the goal
FPS = 60
COMMAND_DELAY = 0.1
TURN_SPEED = 90

# --- Maze Generator ---
class Maze:
    """
    Generates a perfect maze using Randomized Depth-First Search.
    A perfect maze has exactly one path between any two cells.
    """
    def __init__(self, grid_w, grid_h, cell_size):
        self.grid_w = grid_w
        self.grid_h = grid_h
        self.cell_size = cell_size
        # Grid stores wall info: [top, right, bottom, left]
        self.grid = [[{'T': True, 'R': True, 'B': True, 'L': True} for _ in range(grid_w)] for _ in range(grid_h)]
        self.solution_path = []
        self.walls = []
        self.generate()

    def generate(self):
        stack = [(0, 0)]
        visited = set([(0, 0)])
        path_to_goal = []

        while stack:
            cx, cy = stack[-1]
            path_to_goal.append((cx, cy))

            if (cx, cy) == (self.grid_w - 1, self.grid_h - 1):
                self.solution_path = list(path_to_goal) # Found a path

            neighbors = []
            # Check neighbors: Top, Right, Bottom, Left
            if cy > 0 and (cx, cy - 1) not in visited: neighbors.append(('T', cx, cy - 1))
            if cx < self.grid_w - 1 and (cx + 1, cy) not in visited: neighbors.append(('R', cx + 1, cy))
            if cy < self.grid_h - 1 and (cx, cy + 1) not in visited: neighbors.append(('B', cx, cy + 1))
            if cx > 0 and (cx - 1, cy) not in visited: neighbors.append(('L', cx - 1, cy))

            if neighbors:
                direction, nx, ny = random.choice(neighbors)
                # Knock down walls between current and next cell
                if direction == 'T':
                    self.grid[cy][cx]['T'] = False
                    self.grid[ny][nx]['B'] = False
                elif direction == 'R':
                    self.grid[cy][cx]['R'] = False
                    self.grid[ny][nx]['L'] = False
                elif direction == 'B':
                    self.grid[cy][cx]['B'] = False
                    self.grid[ny][nx]['T'] = False
                elif direction == 'L':
                    self.grid[cy][cx]['L'] = False
                    self.grid[ny][nx]['R'] = False
                
                visited.add((nx, ny))
                stack.append((nx, ny))
            else:
                stack.pop()
                path_to_goal.pop()
        
        # Create wall rects for drawing
        for y in range(self.grid_h):
            for x in range(self.grid_w):
                if self.grid[y][x]['T']: self.walls.append(pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, 2))
                if self.grid[y][x]['R']: self.walls.append(pygame.Rect((x + 1) * self.cell_size, y * self.cell_size, 2, self.cell_size))
                if self.grid[y][x]['B']: self.walls.append(pygame.Rect(x * self.cell_size, (y + 1) * self.cell_size, self.cell_size, 2))
                if self.grid[y][x]['L']: self.walls.append(pygame.Rect(x * self.cell_size, y * self.cell_size, 2, self.cell_size))

# --- Robot Class ---
class Robot:
    def __init__(self, x, y, size):
        self.pos = pygame.Vector2(x, y)
        self.angle = -90
        self.size = size
        self.vel = pygame.Vector2(0, 0)
        self.angular_vel = 0
        self.wheel_forces = [0, 0, 0, 0]
        self.force_to_vel_factor = 0.5
        self.force_to_rot_factor = 5
        self.rect = pygame.Rect(0, 0, size, size)
        self.rect.center = self.pos
        self.pid_error_sum = 0
        self.pid_last_error = 0
        self.wall_sensors = {}
        self.floor_sensors = {}
        self.wall_sensor_points_relative = self._create_wall_sensor_layout()
        self.floor_sensor_points_relative = self._create_floor_sensor_layout()
        self.sensor_points_world = {}


    def _create_wall_sensor_layout(self):
        points = {'front': [], 'left': [], 'right': [],'back':[]}
        half = self.size / 2
        for i in range(4):
            spacing = (i - 1.5) * (self.size / 4)
            points['front'].append(pygame.Vector2(spacing, half))
            points['right'].append(pygame.Vector2(half, spacing))
            points['left'].append(pygame.Vector2(-half, spacing))
            points['back'].append(pygame.Vector2(-spacing, -half))
        return points

    def _create_floor_sensor_layout(self):
        # 16 sensors in a line under the robot to detect the floor line
        points = {'front': [], 'left': [], 'right': [],'back':[]}
        half = self.size / 2
        for i in range(4):
            spacing = (i - 1.5) * (self.size / 4)
            points['front'].append(pygame.Vector2(spacing, half))
            points['right'].append(pygame.Vector2(half, spacing))
            points['left'].append(pygame.Vector2(-half, spacing))
            points['back'].append(pygame.Vector2(-spacing, -half))
        return points
    
    def update_physics(self, dt,walls):
        original_pos = pygame.Vector2(self.pos)

        f_fl, f_fr, f_rl, f_rr = self.wheel_forces
        force_y = (f_fl + f_fr + f_rl + f_rr)
        force_x = (-f_fl + f_fr + f_rl - f_rr)
        torque = (-f_fl + f_fr - f_rl + f_rr)

        local_vel = pygame.Vector2(force_x, force_y) * self.force_to_vel_factor
        world_vel = local_vel.rotate(-self.angle)
        self.vel = world_vel
        self.angular_vel = torque * self.force_to_rot_factor

        new_pos = self.pos + self.vel * dt
        new_angle = (self.angle + self.angular_vel * dt) % 360

        trial_rect = pygame.Rect(0, 0, self.size, self.size)
        trial_rect.center = new_pos
        collision = any(trial_rect.colliderect(w) for w in walls)

        if not collision:
            self.pos = new_pos
            self.angle = new_angle
        else:
            # Try X movement only
            temp_pos_x = pygame.Vector2(self.pos.x + self.vel.x * dt, self.pos.y)
            trial_rect.center = temp_pos_x
            if not any(trial_rect.colliderect(w) for w in walls):
                self.pos.x += self.vel.x * dt
            # Try Y movement only
            temp_pos_y = pygame.Vector2(self.pos.x, self.pos.y + self.vel.y * dt)
            trial_rect.center = temp_pos_y
            if not any(trial_rect.colliderect(w) for w in walls):
                self.pos.y += self.vel.y * dt
            self.vel = pygame.Vector2(0, 0)
            self.angular_vel = 0

        self.rect.center = self.pos


    def update_sensors(self, walls, line_path_segments):
        self.sensor_points_world = {'wall': {'front': [], 'left': [], 'right': [],'back':[]}, 'floor': {'front': [], 'left': [], 'right': [],'back':[]}}
        self.wall_sensors = {'front': [1]*4, 'left': [1]*4, 'right': [1]*4,'back': [1]*4}
        self.floor_sensors = {'front': [1]*4, 'left': [1]*4, 'right': [1]*4,'back': [1]*4}
        
        # Update Wall Sensors
        for side, points in self.wall_sensor_points_relative.items():
            for i, p_rel in enumerate(points):
                p_rot = p_rel.rotate(-self.angle)
                p_start = self.pos + p_rot
                p_end = p_start + p_rot.normalize() * 15
                self.sensor_points_world['wall'][side].append((p_start, p_end))
                for wall in walls:
                    if wall.clipline(p_start, p_end):
                        self.wall_sensors[side][i] = 0; break

        # Update Floor Sensors
        for side, points in self.floor_sensor_points_relative.items():
            for i, p_rel in enumerate(points):
               p_rot = p_rel.rotate(-self.angle)
               p_world = self.pos + p_rot
               self.sensor_points_world['floor'][side].append(p_world)
        
               for seg_start, seg_end in line_path_segments:
                   a = pygame.Vector2(seg_start)
                   b = pygame.Vector2(seg_end)
                   if (b - a).length() == 0:
                      continue
                   t = max(0, min(1, (p_world - a).dot(b - a) / (b - a).length_squared()))
                   closest_point = a + t * (b - a)
                   if p_world.distance_to(closest_point) < 4:
                      self.floor_sensors[side][i] = 0
                      break


        
    def draw(self, screen):
        # Draw Robot
        robot_surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        robot_surface.fill(BLUE_ROBOT)
        pygame.draw.rect(robot_surface, GREEN, (self.size/2 - 5, self.size - 10, 10, 10))
        rotated_surface = pygame.transform.rotate(robot_surface, self.angle)
        new_rect = rotated_surface.get_rect(center=self.pos)
        screen.blit(rotated_surface, new_rect.topleft)

        # Draw Sensors
        for side in self.sensor_points_world['wall']:
            for i, (start, end) in enumerate(self.sensor_points_world['wall'][side]):
                color = RED if self.wall_sensors[side][i] == 0 else GREEN
                pygame.draw.line(screen, color, start, end, 1)
        for side in self.sensor_points_world['floor']:
            for i, p in enumerate(self.sensor_points_world['floor'][side]):
                color = RED if self.floor_sensors[side][i] == 0 else GREEN
                pygame.draw.circle(screen, color, (int(p.x), int(p.y)), 3)


    def manual_control(self, keys):
        p = 100
        self.wheel_forces = [0,0,0,0]
        if keys[pygame.K_UP]: self.wheel_forces = [p, p, p, p]
        elif keys[pygame.K_DOWN]: self.wheel_forces = [-p, -p, -p, -p]
        elif keys[pygame.K_LEFT]: self.wheel_forces = [p, -p, -p, p]
        elif keys[pygame.K_RIGHT]: self.wheel_forces = [-p, p, p, -p]
        elif keys[pygame.K_a]: self.wheel_forces = [p, -p, p, -p]
        elif keys[pygame.K_d]: self.wheel_forces = [-p, p, -p, p]
        if keys[pygame.K_LEFT]:
            self.angle -= TURN_SPEED * dt
        if keys[pygame.K_RIGHT]:
            self.angle += TURN_SPEED * dt
            
    def auto_wall_follow(self):
        self.angle += TURN_SPEED * dt
        p, tp = 80, 100
        front = self.wall_sensors.get('front', [1]*4)
        left = self.wall_sensors.get('left', [1]*4)
        if 0 in front: self.wheel_forces = [-tp, tp, -tp, tp]
        elif all(s == 1 for s in left): self.wheel_forces = [tp, -tp, tp, -tp]
        else: self.wheel_forces = [p, p, p, p]

    def auto_line_follow(self):

        # PID Constants
        Kp = 0.4  # Proportional gain
        Ki = 0.01 # Integral gain
        Kd = 0.2  # Derivative gain
        
        # Weighted error calculation from 5 floor sensors
        # [-2, -1, 0, 1, 2] weights for sensors
        # A value of 0 means perfectly centered
        sensors = self.floor_sensors['front']
        error = (sensors[0] * -2 + sensors[1] * -1 + sensors[2] * 1 + sensors[3] * 2)


        # If all sensors are off the line, the error is ambiguous.
        # We use the last known error to try and find the line again.
        if all(s == 1 for s in self.floor_sensors):
            error = self.pid_last_error * 1.5 # Turn harder to find the line
        
        self.pid_error_sum += error
        derivative = error - self.pid_last_error
        self.pid_last_error = error

        # PID output
        turn = Kp * error + Ki * self.pid_error_sum + Kd * derivative
        
        base_speed = 60
        self.wheel_forces = [base_speed - turn, base_speed + turn, base_speed - turn, base_speed + turn]
        self.angle += TURN_SPEED * dt

# --- Main Simulation ---
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Advanced Micromouse & Line Follower Simulator")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)

    # --- Setup ---
    cell_size = 60
    # THIS IS THE CORRECTED LINE:
    maze = Maze(WIDTH // cell_size, HEIGHT // cell_size, cell_size)
    robot = Robot(cell_size / 2, cell_size / 2, cell_size * 0.6)
    goal_rect = pygame.Rect((maze.grid_w - 1) * cell_size, (maze.grid_h - 1) * cell_size, cell_size, cell_size)
    
    # Convert solution path from grid coords to pixel coords for drawing
    line_path_pixels = [(x * cell_size + cell_size/2, y * cell_size + cell_size/2) for x, y in maze.solution_path]
    line_path_segments = []
    if len(line_path_pixels) > 1:
        for i in range(len(line_path_pixels) - 1):
            line_path_segments.append((line_path_pixels[i], line_path_pixels[i+1]))

    # --- State ---
    global dt
    running = True
    autopilot_mode = "MANUAL" # MANUAL, WALL, LINE
    win_message = ""
    dt = 0
    command_timer=0

    while running:
        dt=clock.tick(FPS)/1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: main() # Restart simulation
                if event.key == pygame.K_m:
                    modes = ["MANUAL", "WALL", "LINE"]
                    current_index = modes.index(autopilot_mode)
                    autopilot_mode = modes[(current_index + 1) % len(modes)]

        if not win_message:
            command_timer += dt
            if command_timer >= COMMAND_DELAY:
                if autopilot_mode == "MANUAL":
                    robot.manual_control(pygame.key.get_pressed())
                elif autopilot_mode == "WALL":
                    robot.auto_wall_follow()
                elif autopilot_mode == "LINE":
                    robot.auto_line_follow()

        robot.update_physics(dt,maze.walls)
        robot.update_sensors(maze.walls, line_path_segments)

        if goal_rect.collidepoint(robot.pos) and not win_message:
            win_message = "GOAL REACHED!"

        # --- Drawing ---
        screen.fill(GRAY)
        pygame.draw.rect(screen, GOAL_COLOR, goal_rect)
        if len(line_path_pixels) > 1:
            pygame.draw.lines(screen, BLUE_LINE, False, line_path_pixels, 6)
        for wall in maze.walls: pygame.draw.rect(screen, BLACK, wall)
        robot.draw(screen)

        # --- UI ---
        mode_text = font.render(f"Mode: {autopilot_mode} (Press M to change)", True, WHITE)
        controls_text = font.render("Controls: ARROWS (Move), A/D (Rotate), R (New Maze)", True, WHITE)
        screen.blit(mode_text, (20, 20))
        screen.blit(controls_text, (20, 45))
        if win_message:
            win_font = pygame.font.Font(None, 74)
            win_surface = win_font.render(win_message, True, GOAL_COLOR)
            screen.blit(win_surface, win_surface.get_rect(center=(WIDTH/2, HEIGHT/2)))

        pygame.display.flip()
        dt = clock.tick(60) / 1000.0

    pygame.quit()

if __name__ == "__main__":
    main()