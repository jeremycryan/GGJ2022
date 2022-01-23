from bird import *
import constants as c
import time, math
from button import Button

class Card:

    def __init__(self, level, bird_key):
        self.age = 0
        self.level = level
        self.bird_key = bird_key
        bird_class = bird_from_key(bird_key)
        self.bird = bird_class(self.level.game, animation=False)

        self.surf = pygame.image.load(c.image_path("card.png")).convert()
        self.surf.set_colorkey(self.surf.get_at((0, 0)))
        self.selected_surf = pygame.image.load(c.image_path("card_selected.png")).convert()
        self.selected_surf.set_colorkey(self.surf.get_at((0, 0)))
        white = pygame.Surface((self.surf.get_width(), self.surf.get_height()))
        white.fill((200, 128, 255))
        self.hover_surf = self.surf.copy()
        white.set_alpha(45)
        self.hover_surf.blit(white, (0, 0))
        self.hover_surf.set_colorkey(self.hover_surf.get_at((0, 0)))
        self.selected = False
        self.hovered = False

    def select(self, selected=True):
        self.selected = selected

    def update(self, dt, events):
        self.bird.update(dt, events)
        self.age += dt

    def draw(self, surface, offset=(0, 0)):
        x = offset[0] - c.CARD_WIDTH//2
        y = offset[1] - c.CARD_HEIGHT//2
        if self.selected:
            surface.blit(self.selected_surf, (x, y))
        elif self.hovered:
            surface.blit(self.hover_surf, (x, y))
        else:
            surface.blit(self.surf, (x, y))

        bx = offset[0]
        by = offset[1] - 20
        self.bird.draw(surface, (bx, by))

        name = self.level.inventory.bird_names[self.bird_key]
        x = offset[0] - name.get_width()//2
        y = offset[1] - name.get_height()//2 + 30
        surface.blit(name, (x, y))

        amount = self.level.inventory.bird_amounts[self.bird_key]
        x = offset[0] - amount.get_width()//2
        y = offset[1] - amount.get_height()//2 + 65
        surface.blit(amount, (x, y))


class Inventory:
    def __init__(self, level):
        self.level = level
        self.starting_birds = {}
        self.bird_names = {}
        self.reset_birds()

        self.sidebar_surface = pygame.Surface((c.SIDEBAR_WIDTH, c.SIDEBAR_HEIGHT))
        self.sidebar_surface.fill((140, 32, 180))

        self.cards = [Card(self.level, bird_key) for bird_key in self.starting_birds]
        self.selected_card = None

        self.gradient = pygame.image.load(c.image_path("gradient.png"))
        self.gradient = pygame.transform.scale(self.gradient, (32, c.WINDOW_HEIGHT))

        self.bird_name_font = pygame.font.Font(c.font_path("marediv.ttf"), 20)
        self.bird_amount_font = pygame.font.Font(c.font_path("a_goblin_appears.ttf"), 28)

        submit_button_surf = pygame.image.load(c.image_path("submit_button.png"))
        submit_button_surf.set_colorkey((255, 255, 0))
        submit_button_hover_surf = pygame.image.load(c.image_path("submit_button_hover.png"))
        submit_button_hover_surf.set_colorkey((255, 255, 0))
        self.submit_button = Button(
            submit_button_surf,
            (c.SIDEBAR_WIDTH//2, c.WINDOW_HEIGHT - 70),
            click_surf=submit_button_hover_surf,
            grow_percent=5,
            on_click=self.submit,
        )
        self.submit_button.scale = 0

    def submit(self):
        self.level.grid.check_for_level_complete()
        pass

    def select_card(self, card):
        if self.selected_card is not None:
            self.cards[self.selected_card].select(False)
        self.selected_card = card
        self.cards[self.selected_card].select(True)

    def hover_card(self, card):
        card.hovered = True

    def set_starting_birds(self, birds):
        self.starting_birds = birds
        self.reset_birds()
        self.cards = [Card(self.level, bird_key) for bird_key in self.starting_birds]
        if self.cards:
            self.select_card(0)
        else:
            self.selected_card = None

        self.bird_name_color = (0, 0, 0)
        self.bird_names = {name: self.bird_name_font.render(bird_from_key(name).name, False, self.bird_name_color) for name in birds}
        self.bird_amounts = {name: self.bird_amount_font.render(f"{self.birds[name]}", False, self.bird_name_color) for name in birds}

    def pop_selected_bird(self):
        if not self.cards:
            return None
        if self.selected_card is None:
            return None
        selected_bird_key = self.cards[self.selected_card].bird_key
        if not self.has_birds_of_type(selected_bird_key):
            return None
        return self.pop_bird_of_type(selected_bird_key)

    def peek_selected_bird(self):
        if not self.cards:
            return None
        if self.selected_card is None:
            return None
        selected_bird_key = self.cards[self.selected_card].bird_key
        if not self.has_birds_of_type(selected_bird_key):
            return None
        return self.peek_bird_of_type(selected_bird_key)

    def reset_birds(self):
        self.birds = self.starting_birds.copy()

    def has_birds_of_type(self, key):
        if key not in self.birds:
            return False
        if self.birds[key] < 1:
            return False
        return True

    def pop_bird_of_type(self, key):
        if not self.has_birds_of_type(key):
            return None
        for bird in BIRD_TYPES:
            if bird.key == key:
                self.birds[key] -= 1
                self.bird_amounts[key] = self.bird_amount_font.render(f"{self.birds[key]}", True, self.bird_name_color)
                return bird(self.level.game)
        return None

    def peek_bird_of_type(self, key):
        if not self.has_birds_of_type(key):
            return None
        for bird in BIRD_TYPES:
            if bird.key == key:
                return bird(self.level.game)
        return None

    def update(self, dt, events):
        if not self.empty():
            self.submit_button.disable()
        else:
            self.submit_button.enable()
        self.submit_button.update(dt, events)
        for card in self.cards:
            card.hovered = False
        mpos = pygame.mouse.get_pos()
        hovered_card = self.get_hovered_card(mpos)
        if hovered_card is not None:
            hovered_card.hovered = True
        for card in self.cards:
            card.update(dt, events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if hovered_card is not None:
                        self.select_card(self.cards.index(hovered_card))

    def get_hovered_card(self, mpos):
        x = mpos[0] - c.SIDEBAR_RECT[0]
        y = mpos[1] - c.SIDEBAR_RECT[1]
        padding = (c.SIDEBAR_WIDTH - c.CARD_WIDTH * 2)//3
        col_1_x = padding + c.CARD_WIDTH//2
        col_2_x = 2*padding + (c.CARD_WIDTH * 3)//2
        xs = col_1_x, col_2_x
        for i, card in enumerate(self.cards):
            xc = xs[i % len(xs)]
            yc = i//2 * c.CARD_HEIGHT + padding + c.CARD_HEIGHT//2
            if abs(x - xc) < c.CARD_WIDTH//2 and abs(y - yc) < c.CARD_HEIGHT//2:
                return card

    def draw(self, surface, offset=(0, 0)):
        self.draw_sidebar(surface, offset)
        self.draw_cards(surface, offset)
        self.draw_shadow(surface, offset)
        self.submit_button.draw(surface)

    def draw_sidebar(self, surface, offset=(0, 0)):
        x = offset[0] + c.SIDEBAR_RECT[0]
        y = c.SIDEBAR_RECT[1]
        surface.blit(self.sidebar_surface, (x, y))

    def draw_cards(self, surface, offset=(0, 0)):
        padding = (c.SIDEBAR_WIDTH - c.CARD_WIDTH * 2)//3
        col_1_x = padding + c.CARD_WIDTH//2 + offset[0]
        col_2_x = 2*padding + (c.CARD_WIDTH * 3)//2 + offset[0]
        xs = col_1_x, col_2_x
        for i, card in enumerate(self.cards):
            x = xs[i % len(xs)]
            y = i//2 * (c.CARD_HEIGHT + padding) + padding + c.CARD_HEIGHT//2

            x += 2 * math.cos(time.time() * math.pi * 1 + i * math.pi * 0.8)
            y += 2 * math.sin(time.time() * math.pi * 1.1 + i * math.pi * 0.8)

            card.draw(surface, offset=(x, y))

    def draw_shadow(self, surface, offset=(0, 0)):
        x = offset[0] + c.SIDEBAR_WIDTH
        y = offset[1]
        surface.blit(self.gradient, (x, y), special_flags=pygame.BLEND_MULT)

    def empty(self):
        total = 0
        for bird in self.birds:
            total += self.birds[bird]
        return total==0

    def add_birds(self, birds):
        # Add birds flushed from a tile
        for bird in birds:
            key = bird.key
            if key in self.birds:
                self.birds[key] += 1
                self.bird_amounts[key] = self.bird_amount_font.render(f"{self.birds[key]}", True, self.bird_name_color)