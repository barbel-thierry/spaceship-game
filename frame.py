import math
import random

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Rectangle
from kivy.uix.label import CoreLabel, Label
from kivy.uix.widget import Widget

from entities.block import Block
from entities.player import Player


class Screen(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._blocks = set()
        self._pressed_keys = set()

        self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down)
        self._keyboard.bind(on_key_up=self._on_key_up)

        self._score = 0
        self._score_label = CoreLabel(text='Score: ' + str(self._score), font_size=20)
        self._score_label.refresh()

        with self.canvas:
            self._player = Player()
            self._score_instruction = Rectangle(
                texture=self._score_label.texture,
                pos=(0, Window.height - 30),
                size=self._score_label.texture.size
            )

        self._frame = Clock.schedule_interval(self._on_frame, 0)
        self._move = Clock.schedule_interval(self._move_blocks, 1 / 45)
        self._spawn = Clock.schedule_interval(self._spawn_blocks, 2)

    def _on_frame(self, dt):
        step = 500 * dt

        x, y = self._player.pos
        if 'left' in self._pressed_keys:
            x -= step
        if 'right' in self._pressed_keys:
            x += step
        if (x + self._player.size[0]) > Window.width:
            x = Window.width - self._player.size[0]
        if x < 0:
            x = 0
        self._player.pos = (x, y)

        # if screen size changes
        self._score_instruction.pos = (0, Window.height - 30)

    def _move_blocks(self, dt):
        disapeared = []

        for block in self._blocks:
            block.pos = (block.pos[0], block.pos[1] - 10)
            self._check_for_collision(block)

            if block.pos[1] + block.size[1] <= 0:
                disapeared.append(block)
                self.score = self._score + 1

        for hidden_block in disapeared:
            self._blocks.remove(hidden_block)

    def _spawn_blocks(self, dt):
        player_width = self._player.size[0]
        pathways_number = random.randint(1, 3)
        fake_paths_number = random.randint(2, 5)

        # total of paths and blocks must be odd
        if (pathways_number + fake_paths_number) % 2 == 0:
            fake_paths_number += 1

        free_space = self.width - ((pathways_number * (player_width + 20)) + (fake_paths_number * (player_width - 20)))
        interval_size = int(math.ceil(free_space / (pathways_number + fake_paths_number + 1)))

        holes = []
        for path in range(pathways_number):
            holes.append(player_width + 20)
        for fake_path in range(fake_paths_number):
            holes.append(player_width - 20)

        line = [interval_size]
        for i in range(pathways_number + fake_paths_number):
            index = random.randint(1, len(holes))
            line.append(holes[index - 1])
            line.append(interval_size)
            del holes[index - 1]

        pos_x = 0
        plain = True
        for x in line:
            if (pos_x + x) > Window.width:
                x = Window.width - pos_x
            if plain:
                with self.canvas:
                    block = Block((pos_x, Window.height - 50), (x, 30))
                    self._blocks.add(block)
            pos_x += x
            plain = not plain

    def _check_for_collision(self, block):
        same_height_or_under = block.pos[1] <= (int(self._player.pos[1]) + self._player.size[1])
        block_left = block.pos[0]
        block_right = block.pos[0] + block.size[0]
        player_left_in_block = block_left < int(self._player.pos[0]) < block_right
        player_right_in_block = block_left < (int(self._player.pos[0]) + self._player.size[0]) < block_right

        if same_height_or_under and (player_left_in_block or player_right_in_block):
            self._blocks = set()
            self._lost()

    def _lost(self):
        self._frame.cancel()
        self._move.cancel()
        self._spawn.cancel()
        self.canvas.clear()

        with self.canvas:
            text = "Your spaceship crashed...\n"
            if self._score > 0:
                text += "But you managed to score " + str(self._score) + " points!!\n\n"
            else:
                text += "You will do better next time!!\n\n"
            text += "Press `y` if you want to play again."

            Label(
                pos=((Window.width - 100) / 2, Window.height / 2),
                size=(100, 30),
                text=text
            )

            self._restart = Clock.schedule_interval(self._on_endgame, 0)

    def _on_endgame(self, dt):
        if 'y' in self._pressed_keys:
            self._restart.cancel()
            self.canvas.clear()
            self.__init__()

    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard.unbind(on_key_up=self._on_key_up)
        self._keyboard = None

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        self._pressed_keys.add(keycode[1])

    def _on_key_up(self, keyboard, keycode):
        if keycode[1] in self._pressed_keys:
            self._pressed_keys.remove(keycode[1])

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        self._score = value
        self._score_label.text = "Score: " + str(value)
        self._score_label.refresh()
        self._score_instruction.texture = self._score_label.texture
        self._score_instruction.size = self._score_label.texture.size
