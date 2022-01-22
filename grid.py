import pygame
from bird import *
from particle import *

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.birds = []

    def get_birds(self):
        return self.birds.copy()

    def flush_birds(self):
        birds = self.get_birds()
        self.clear_birds()
        return birds

    def flush_movable(self):
        keep = []
        discard = []
        for bird in self.birds:
            if bird.movable:
                discard.append(bird)
            else:
                keep.append(bird)
        self.birds = keep
        return discard

    def clear_birds(self):
        self.birds = []

    def add_bird(self, bird):
        self.birds.append(bird)

    def total_bird_value(self):
        return sum([bird.bird_count for bird in self.birds])

    def update(self, dt, events):
        for bird in self.birds:
            bird.update(dt, events)


class Grid:
    def __init__(self, width, height, level):
        self.level = level
        self.width = width
        self.height = height
        self.cells = [[Cell(x, y) for x in range(width)] for y in range(height)]
        self.max_birds_in_line = 2
        self.draw_offset = (0, 0)
        self.particles = []

        self.grid_surf = pygame.Surface(c.TILE_SIZE)
        self.grid_surf.fill((0, 0, 0))
        self.grid_surf.set_colorkey((0, 0, 0))
        pygame.draw.rect(self.grid_surf, (255, 255, 255), (4, 4, c.TILE_WIDTH-8, c.TILE_HEIGHT-8))
        self.grid_surf.set_alpha(50)

    def get_birds_at(self, x, y):
        return self.cells[y][x].get_birds()

    def can_place_at(self, x, y, bird):
        return not self.get_birds_at(x, y)

    def add_bird(self, x, y, bird):
        self.cells[y][x].add_bird(bird)
        for i in range(30):
            px = x*c.TILE_WIDTH - (c.TILE_WIDTH * self.width)//2 + c.TILE_WIDTH//2
            py = y*c.TILE_HEIGHT - (c.TILE_HEIGHT * self.height)//2 + c.TILE_HEIGHT//2
            self.particles.append(PigeonPlaceParticle((px, py)))

    def flush_birds_at(self, x, y):
        """ Gets the birds in a cell and clears them. """
        return self.cells[y][x].flush_birds()

    def update(self, dt, events):
        x, y = self.mouse_position_to_grid_position(pygame.mouse.get_pos())
        for particle in self.particles[:]:
            particle.update(dt, events)
            if particle.destroyed:
                self.particles.remove(particle)
        for cell in self.enumerate_cells():
            cell.update(dt, events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    possible_bird = Bird(self.level.game)
                    if self.is_valid_xy(x, y):
                        if self.can_place_at(x, y, possible_bird):
                            self.add_bird(x, y, possible_bird)
                        else:
                            self.cells[y][x].flush_movable()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    bad_cells = self.check_collisions()
                    if bad_cells:
                        for cell in bad_cells:
                            for bird in cell.get_birds():
                                bird.flash_red()
                    else:
                        self.level.complete()


    def enumerate_cells(self):
        for row in self.cells:
            for cell in row:
                yield cell

    def enumerate_populated_cells(self):
        for cell in self.enumerate_cells():
            if cell.birds:
                yield cell

    def draw(self, surface, offset=(0, 0)):
        width_px = self.width * c.TILE_WIDTH
        height_px = self.height * c.TILE_HEIGHT
        x0 = offset[0] - width_px//2 + self.draw_offset[0]
        y0 = offset[1] - height_px//2 + self.draw_offset[1]
        for y_idx, row in enumerate(self.cells):
            y_draw = y0 + y_idx * c.TILE_HEIGHT + c.TILE_HEIGHT//2
            for x_idx, cell in enumerate(row):
                x_draw = x0 + x_idx * c.TILE_WIDTH + c.TILE_WIDTH//2

                # draw grid
                x_offset = x_draw - c.TILE_WIDTH//2
                y_offset = y_draw - c.TILE_HEIGHT//2
                surface.blit(self.grid_surf, (x_offset, y_offset))

        for particle in self.particles:
            particle.draw(surface, offset=offset)

        for y_idx, row in enumerate(self.cells):
            y_draw = y0 + y_idx * c.TILE_HEIGHT + c.TILE_HEIGHT // 2
            for x_idx, cell in enumerate(row):
                x_draw = x0 + x_idx * c.TILE_WIDTH + c.TILE_WIDTH // 2

                for bird in cell.get_birds():
                    bird.draw(surface, (x_draw, y_draw))

    def mouse_position_to_grid_position(self, mpos):
        x, y = mpos
        x -= c.LEVEL_RECTANGLE_CENTER[0] - (self.width * c.TILE_WIDTH)//2
        y -= c.LEVEL_RECTANGLE_CENTER[1] - (self.height * c.TILE_HEIGHT)//2
        x /= c.TILE_WIDTH
        y /= c.TILE_HEIGHT
        return (int(x), int(y))

    def is_valid_xy(self, x, y):
        return x < self.width and y < self.height and x >= 0 and y >= 0

    def check_collisions(self):
        """ Determines whether there are more than max_birds_in_line birds in a line.

            Returns a list of all cells in the line if a line is found.
        """

        # dict containing a tuple (MN, MD, BN, BD) where M is slope, split into numerator and denominator, and B is y
        # intercept of lines. Vertical and horizontal lines are ignored and checked separately. Values are hash sets
        # of cell objects in the line.
        lines = {}
        three_or_more_lines = set()
        cells_by_x = {}
        three_or_more_xs = set()


        for cell_1 in self.enumerate_populated_cells():
            for cell_2 in self.enumerate_populated_cells():
                if cell_1.x > cell_2.x:
                    # We'll hit this case later on in the loop with cell_1 and cell_2 swapped
                    continue
                if cell_1 is cell_2:
                    continue
                if cell_1.x == cell_2.x:
                    if cell_1.x not in cells_by_x:
                        cells_by_x[cell_1.x] = set()
                    else:
                        three_or_more_xs.add(cell_1.x)
                    cells_by_x[cell_1.x].add(cell_1)
                    cells_by_x[cell_1.x].add(cell_2)
                    continue
                m_num = int(cell_2.y - cell_1.y)
                m_den = int(cell_2.x - cell_1.x)
                m_gcd = math.gcd(m_num, m_den)
                m_num /= m_gcd
                m_den /= m_gcd
                b_num = int(cell_1.y * m_den - m_num * cell_1.x)
                b_den = int(m_den)
                b_gcd = math.gcd(b_num, b_den)
                b_num /= b_gcd
                b_den /= b_gcd
                line_tuple = (m_num, m_den, b_num, b_den)
                if line_tuple not in lines:
                    lines[line_tuple] = set()
                else:
                    three_or_more_lines.add(line_tuple)
                lines[line_tuple].add(cell_1)
                lines[line_tuple].add(cell_2)

        for x in three_or_more_xs:
            cells = cells_by_x[x]
            value = sum([cell.total_bird_value() for cell in cells])
            if value > self.max_birds_in_line:
                return list(cells)

        for line_tuple in three_or_more_lines:
            cells = lines[line_tuple]
            value = sum([cell.total_bird_value() for cell in cells])
            if value > self.max_birds_in_line:
                return list(cells)

        return []
