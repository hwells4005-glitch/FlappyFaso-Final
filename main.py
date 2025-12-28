import random
import math
import struct
import wave
import os
try:
    from kivy.config import Config
    Config.set('graphics', 'resizable', '0')
    Config.set('graphics', 'width', '400')
    Config.set('graphics', 'height', '700')
except: pass

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import NumericProperty, ListProperty, BooleanProperty, ObjectProperty
from kivy.metrics import dp
from kivy.core.audio import SoundLoader
from kivy.storage.jsonstore import JsonStore
from kivy.graphics import Color, Ellipse, Rectangle, Line, Mesh
from kivy.graphics.texture import Texture
from kivy.core.window import Window 

# --- SONS AUTOMATIQUES (Pas besoin de fichiers mp3) ---
def generate_audio_files():
    if not os.path.exists('score.wav'):
        sample_rate = 44100
        with wave.open('score.wav', 'w') as f:
            f.setnchannels(1); f.setsampwidth(2); f.setframerate(sample_rate)
            data = []
            for i in range(int(sample_rate * 0.1)):
                t = i / sample_rate
                val = math.sin(2 * math.pi * 880.0 * t) * 0.3 
                data.append(struct.pack('<h', int(val * 32767)))
            f.writeframes(b''.join(data))

# --- DESIGN ---
kv = """
#:import dp kivy.metrics.dp

<Pipe>:
    canvas:
        Color:
            rgba: 0.93, 0.11, 0.14, 1
        Rectangle:
            pos: self.x, self.top_y
            size: self.width, self.top_h
        Color:
            rgba: 0, 0.6, 0.3, 1
        Rectangle:
            pos: self.x, self.y
            size: self.width, self.bottom_h
        Color:
            rgba: 0,0,0,1
        Line:
            rectangle: (self.x, self.top_y, self.width, self.top_h)
            width: 2
        Line:
            rectangle: (self.x, self.y, self.width, self.bottom_h)
            width: 2

<Bird>:
    size_hint: None, None
    size: dp(45), dp(45)
    canvas.before:
        PushMatrix
        Rotate:
            angle: self.angle
            origin: self.center
    canvas:
        Color:
            rgba: 1, 0.85, 0, 1
        Ellipse:
            pos: self.pos
            size: self.size
        Color:
            rgba: 0,0,0,1
        Line:
            circle: (self.center_x, self.center_y, self.width/2)
            width: 1.5
    canvas.after:
        PopMatrix

<FlappyGame>:
    pipe_layer: pipe_layer
    bird: bird
    
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size
    
    Widget:
        id: pipe_layer
    Bird:
        id: bird
        pos: dp(100), root.height / 2
        
    Label:
        text: str(root.score)
        font_size: '60sp'
        pos_hint: {"center_x": 0.5, "top": 0.95}
        color: 0,0,0,1
        bold: True

    Label:
        text: "TAP TO START" if not root.started else ""
        font_size: '30sp'
        color: 0,0,0,0.5
        bold: True
        center: root.center
"""

class Pipe(Widget):
    gap = NumericProperty(dp(160))
    top_y = NumericProperty(0)
    top_h = NumericProperty(0)
    bottom_h = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.width = dp(75)
        self.scored = False

    def set_height(self, h):
        floor = dp(50)
        avail = h - self.gap - (floor*2)
        if avail < 50: avail = 50
        rand = random.randint(0, int(avail))
        self.bottom_h = floor + rand
        self.top_y = self.bottom_h + self.gap
        self.top_h = h - self.top_y

class Bird(Widget):
    angle = NumericProperty(0)

class FlappyGame(FloatLayout):
    score = NumericProperty(0)
    started = BooleanProperty(False)
    game_over = BooleanProperty(False)
    velocity = NumericProperty(0)
    gravity = NumericProperty(dp(1300))
    pipes = ListProperty([])
    bird = ObjectProperty(None)
    pipe_layer = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        generate_audio_files()
        self.sound_score = SoundLoader.load('score.wav')
        Clock.schedule_interval(self.update, 1.0/60.0)
        self.spawn_timer = 0

    def on_touch_down(self, touch):
        if self.game_over:
            self.reset()
        else:
            self.started = True
            self.velocity = dp(400)

    def reset(self):
        self.pipe_layer.clear_widgets()
        self.pipes = []
        self.bird.pos = (dp(100), self.height/2)
        self.bird.angle = 0
        self.velocity = 0
        self.score = 0
        self.game_over = False
        self.started = False

    def spawn_pipe(self):
        p = Pipe()
        p.set_height(self.height)
        p.x = self.width
        self.pipe_layer.add_widget(p)
        self.pipes.append(p)

    def update(self, dt):
        if not self.started or self.game_over: return
        self.velocity -= self.gravity * dt
        self.bird.y += self.velocity * dt
        self.bird.angle = max(min(self.velocity * 0.15, 30), -60)
        
        self.spawn_timer += dt
        if self.spawn_timer > 1.8:
            self.spawn_pipe()
            self.spawn_timer = 0
            
        for p in self.pipes[:]:
            p.x -= dp(200) * dt
            # SCORE INSTANTANÉ (V16)
            if p.right < self.bird.x and not p.scored:
                self.score += 1
                p.scored = True
                if self.sound_score: self.sound_score.play()
            
            if p.right < 0:
                self.pipe_layer.remove_widget(p)
                self.pipes.remove(p)
            if (self.bird.right > p.x and self.bird.x < p.right):
                if (self.bird.y < p.bottom_h) or (self.bird.top > p.top_y):
                    self.game_over = True
        if self.bird.y < 0 or self.bird.top > self.height:
            self.game_over = True

class FlappyApp(App):
    def build(self):
        Builder.load_string(kv)
        return FlappyGame()

if __name__ == '__main__':
    FlappyApp().run()
