import random
import math
from kivy.config import Config

# Optimisation graphique
Config.set('graphics', 'resizable', '0')
Config.set('kivy', 'exit_on_escape', '1')

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import NumericProperty, ListProperty, BooleanProperty, ObjectProperty
from kivy.metrics import dp
from kivy.graphics.texture import Texture

kv = '''
#:import dp kivy.metrics.dp

<FasoStar>:
    canvas:
        Color:
            rgba: 0.988, 0.82, 0.086, 0.8
        Mesh:
            mode: 'triangle_fan'
            vertices: self.vertices
            indices: self.indices

<Pipe>:
    size_hint: None, None
    canvas:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            pos: self.x, self.top_y
            size: self.width, self.top_h
            texture: self.tex_top
        Rectangle:
            pos: self.x, self.y
            size: self.width, self.bottom_h
            texture: self.tex_bot
        Color:
            rgba: 0, 0, 0, 1
        Line:
            rectangle: (self.x, self.top_y, self.width, self.top_h)
            width: 1.5
        Line:
            rectangle: (self.x, self.y, self.width, self.bottom_h)
            width: 1.5

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
            rgba: 0.988, 0.82, 0.086, 1
        Ellipse:
            pos: self.pos
            size: self.size
        Color:
            rgba: 1, 1, 0.8, 0.6
        Ellipse:
            pos: self.x + self.width*0.1, self.y + self.height*0.25
            size: self.width*0.6, self.height*0.5
        Color:
            rgba: 0,0,0,1
        Line:
            circle: (self.center_x, self.center_y, self.width/2)
            width: 1.2
    canvas.after:
        PopMatrix

<FlappyGame>:
    pipe_layer: pipe_layer
    bird: bird
    
    # FOND DRAPEAU
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size
            texture: self.bg_texture
    
    # ETOILE CENTRALE
    FasoStar:
        id: bg_star
        size_hint: None, None
        size: dp(200), dp(200)
        center: self.parent.center if self.parent else (0,0)

    Widget:
        id: pipe_layer

    Bird:
        id: bird
        pos: dp(100), root.height / 2

    # SCORE
    Label:
        text: str(root.score)
        font_size: '60sp'
        pos_hint: {"center_x": 0.5, "top": 0.96}
        bold: True
        color: 1, 1, 1, 1
        outline_width: 2
        outline_color: 0,0,0,1

    Label:
        text: "TAP TO START" if not root.started else ""
        font_size: '30sp'
        bold: True
        color: 1, 1, 1, 1
        outline_width: 2
        outline_color: 0,0,0,1
        center: root.center
'''

class FasoStar(Widget):
    vertices = ListProperty([])
    indices = ListProperty([])
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self.calculate_points, size=self.calculate_points)
        Clock.schedule_once(self.calculate_points, 0)
    
    def calculate_points(self, *args):
        cx, cy = self.center_x, self.center_y
        outer = self.width / 2
        inner = outer * 0.4
        points = [cx, cy, 0.5, 0.5]
        angle_step = math.pi / 5
        angle = -math.pi / 2
        for i in range(11):
            r = outer if i % 2 == 0 else inner
            points.extend([cx + math.cos(angle)*r, cy + math.sin(angle)*r, 0, 0])
            angle += angle_step
        self.vertices = points
        self.indices = list(range(12))

class Pipe(Widget):
    gap = NumericProperty(dp(160))
    top_y = NumericProperty(0)
    top_h = NumericProperty(0)
    bottom_h = NumericProperty(0)
    tex_top = ObjectProperty(None)
    tex_bot = ObjectProperty(None)
    
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
    bg_texture = ObjectProperty(None)
    pipe_tex_red = ObjectProperty(None)
    pipe_tex_green = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.generate_flag_bg()
        self.pipe_tex_red = self.gen_pipe_tex((239, 43, 45))
        self.pipe_tex_green = self.gen_pipe_tex((0, 158, 73))
        
        Clock.schedule_interval(self.update, 1.0/60.0)
        self.spawn_timer = 0

    def gen_pipe_tex(self, color):
        tex = Texture.create(size=(32, 1), colorfmt='rgb')
        buf = []
        r, g, b = color
        for i in range(32):
            factor = 1.0
            if i < 5: factor = 0.6 + (i*0.08)
            elif i > 25: factor = 1.0 - ((i-25)*0.1)
            buf.extend([int(r*factor), int(g*factor), int(b*factor)])
        tex.blit_buffer(bytes(buf), colorfmt='rgb', bufferfmt='ubyte')
        return tex

    def generate_flag_bg(self):
        tex = Texture.create(size=(1, 64), colorfmt='rgb')
        buf = []
        for i in range(64):
            if i < 32: buf.extend([0, 158, 73])
            else: buf.extend([239, 43, 45])
        tex.blit_buffer(bytes(buf), colorfmt='rgb', bufferfmt='ubyte')
        tex.mag_filter = 'nearest'
        self.bg_texture = tex

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
        p = Pipe(tex_top=self.pipe_tex_red, tex_bot=self.pipe_tex_green)
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
            
            if p.right < self.bird.x and not p.scored:
                self.score += 1
                p.scored = True
                # PLUS DE SON = PLUS DE CRASH !
            
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
    
