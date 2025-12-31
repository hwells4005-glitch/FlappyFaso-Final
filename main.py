import random
import math
import struct
import wave
import os
from kivy.config import Config
from kivy.storage.jsonstore import JsonStore
from kivy.animation import Animation

# Optimisation
Config.set('graphics', 'resizable', '0')
Config.set('kivy', 'exit_on_escape', '1')

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import NumericProperty, ListProperty, BooleanProperty, ObjectProperty, StringProperty, ListProperty
from kivy.metrics import dp
from kivy.graphics.texture import Texture
from kivy.core.audio import SoundLoader

# --- GÉNÉRATEUR DE SONS (Sauf flap.wav) ---
def create_sounds():
    if not os.path.exists('score.wav'):
        with wave.open('score.wav', 'w') as f:
            f.setparams((1, 2, 44100, 0, 'NONE', 'not compressed'))
            data = []
            for i in range(int(44100 * 0.1)):
                vol = 0.5 * (1 - (i / (44100 * 0.1)))
                v = math.sin(2 * math.pi * 1500 * (i / 44100.0)) * vol
                data.append(struct.pack('h', int(v * 32767)))
            f.writeframes(b''.join(data))

    if not os.path.exists('crash.wav'):
        with wave.open('crash.wav', 'w') as f:
            f.setparams((1, 2, 44100, 0, 'NONE', 'not compressed'))
            data = []
            for i in range(int(44100 * 0.3)):
                vol = 0.8 * (1 - (i / (44100 * 0.3)))
                noise = (random.random() * 2 - 1) * vol
                data.append(struct.pack('h', int(noise * 32767)))
            f.writeframes(b''.join(data))

    if not os.path.exists('music.wav'):
        with wave.open('music.wav', 'w') as f:
            f.setparams((1, 2, 44100, 0, 'NONE', 'not compressed'))
            data = []
            tempo = 44100 * 0.5 
            total_len = int(44100 * 2.0)
            for i in range(total_len):
                val = 0
                if (i % int(tempo)) < 2000:
                    val = 0.3 * math.sin(2 * math.pi * 100 * (i/44100.0))
                data.append(struct.pack('h', int(val * 32767)))
            f.writeframes(b''.join(data))

kv = '''
#:import dp kivy.metrics.dp

<FasoStar>:
    canvas:
        Color:
            rgba: 0.988, 0.82, 0.086, 0.9
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
    size: dp(70), dp(70)
    canvas.before:
        PushMatrix
        Rotate:
            angle: self.angle
            origin: self.center
    canvas:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size
            source: 'bird.png' 
    canvas.after:
        PopMatrix

<Flash>:
    size_hint: 1, 1
    opacity: 0
    canvas:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size

<FlappyGame>:
    pipe_layer: pipe_layer
    bird: bird
    flash_layer: flash_layer
    
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size
            texture: self.bg_texture
    
    FasoStar:
        id: bg_star
        size_hint: None, None
        size: dp(250), dp(250)
        center_y: root.height / 2
        opacity: 0.8 if not root.started else 0.4

    Widget:
        id: pipe_layer

    Bird:
        id: bird
        pos: dp(100), root.height / 2
        opacity: 1 if root.started else 0

    Flash:
        id: flash_layer

    # --- ACCUEIL ---
    BoxLayout:
        orientation: 'vertical'
        size_hint: 1, 1
        visible: not root.started and not root.game_over
        opacity: 1 if (not root.started and not root.game_over) else 0
        
        Label:
            text: "FLAPPY FASO"
            font_size: '50sp'
            bold: True
            color: 1, 1, 1, 1
            outline_width: 3
            outline_color: 0,0,0,1
            size_hint_y: 0.4
        
        # RANG (MODIFIÉ: PLUS DE TOURISTE !)
        Label:
            text: root.rank_title
            font_size: '28sp'
            color: 0, 1, 0, 1
            bold: True
            size_hint_y: 0.1
            outline_width: 1
            outline_color: 0,0,0,1
        
        Label:
            text: "XP TOTAL: " + str(int(root.display_xp))
            font_size: '22sp'
            color: 1, 1, 1, 0.9
            size_hint_y: 0.1
            bold: True

        Label:
            text: "Taper pour jouer"
            font_size: '25sp'
            bold: True
            size_hint_y: 0.4
            outline_width: 1
            outline_color: 0,0,0,1

    # --- GAME OVER ---
    BoxLayout:
        orientation: 'vertical'
        size_hint: 0.8, 0.5
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        visible: root.game_over
        opacity: 1 if root.game_over else 0
        canvas.before:
            Color:
                rgba: 0, 0, 0, 0.9
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [20,]
        
        Label:
            text: "GAME OVER"
            font_size: '40sp'
            bold: True
            color: 1, 0, 0, 1
            size_hint_y: 0.2
            
        # MEDAILLE (CORRIGÉE: TEXTE COLORÉ AU LIEU D'IMAGE)
        Label:
            text: root.medal_text
            font_size: '35sp'
            bold: True
            color: root.medal_color # La couleur change selon la médaille
            size_hint_y: 0.3
            outline_width: 2
            outline_color: 0,0,0,1

        Label:
            text: "Score: " + str(root.score)
            font_size: '30sp'
            size_hint_y: 0.15
            
        Label:
            text: "Meilleur: " + str(root.high_score)
            font_size: '20sp'
            color: 1, 1, 0, 1
            size_hint_y: 0.15
            
        Button:
            text: "REJOUER"
            font_size: '25sp'
            background_color: 0, 0.6, 0, 1
            on_release: root.reset()
            size_hint_y: 0.2

    # SCORE JEU
    Label:
        text: str(root.score)
        font_size: '60sp'
        pos_hint: {"center_x": 0.5, "top": 0.96}
        bold: True
        color: 1, 1, 1, 1
        outline_width: 2
        outline_color: 0,0,0,1
        opacity: 1 if root.started and not root.game_over else 0
'''

class Flash(Widget):
    pass

class FasoStar(Widget):
    vertices = ListProperty([])
    indices = ListProperty([])
    angle = NumericProperty(0)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self.calculate_points, size=self.calculate_points)
        Clock.schedule_once(self.calculate_points, 0)
        Clock.schedule_interval(self.rotate, 1.0/60.0)
    def rotate(self, dt): self.angle += 0.5
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
    gap = NumericProperty(dp(180))
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
    high_score = NumericProperty(0)
    total_xp = NumericProperty(0)
    display_xp = NumericProperty(0)
    
    rank_title = StringProperty("NOVICE") # On remplace Touriste
    
    # NOUVEAU SYSTEME DE MEDAILLE (Texte + Couleur)
    medal_text = StringProperty("")
    medal_color = ListProperty([1, 1, 1, 1])
    
    started = BooleanProperty(False)
    game_over = BooleanProperty(False)
    velocity = NumericProperty(0)
    gravity = NumericProperty(dp(1300))
    game_speed = NumericProperty(dp(200))
    
    pipes = ListProperty([])
    bird = ObjectProperty(None)
    pipe_layer = ObjectProperty(None)
    flash_layer = ObjectProperty(None)
    bg_texture = ObjectProperty(None)
    pipe_tex_red = ObjectProperty(None)
    pipe_tex_green = ObjectProperty(None)
    bg_star = ObjectProperty(None)
    
    sound_score = ObjectProperty(None)
    sound_flap = ObjectProperty(None)
    sound_crash = ObjectProperty(None)
    music = ObjectProperty(None)
    
    store = None
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.generate_flag_bg()
        self.pipe_tex_red = self.gen_pipe_tex((239, 43, 45))
        self.pipe_tex_green = self.gen_pipe_tex((0, 158, 73))
        
        create_sounds()
        try:
            self.sound_score = SoundLoader.load('score.wav')
            self.sound_flap = SoundLoader.load('flap.wav') 
            self.sound_crash = SoundLoader.load('crash.wav')
            self.music = SoundLoader.load('music.wav')
            if self.music: 
                self.music.loop = True
                self.music.volume = 0.5
                self.music.play() 
        except: 
            print("Erreur sons")

        self.store = JsonStore('game_data.json')
        if self.store.exists('stats'):
            data = self.store.get('stats')
            self.high_score = data.get('best', 0)
            self.total_xp = data.get('xp', 0)
        self.update_rank()
        self.animate_xp()

        Clock.schedule_interval(self.update, 1.0/60.0)
        self.spawn_timer = 0
        Clock.schedule_once(self.init_star, 0.1)

    def init_star(self, dt):
        if self.bg_star: self.bg_star.center_x = self.width / 2

    def animate_xp(self):
        self.display_xp = 0
        anim = Animation(display_xp=self.total_xp, duration=1.5, t='out_expo')
        anim.start(self)

    def update_rank(self):
        # ICI ON CHANGE LES NOMS DES RANGS
        if self.total_xp < 50: self.rank_title = "NOVICE" # Fini "Touriste"
        elif self.total_xp < 200: self.rank_title = "APPRENTI"
        elif self.total_xp < 500: self.rank_title = "CITOYEN"
        elif self.total_xp < 1000: self.rank_title = "PATRIOTE"
        elif self.total_xp < 5000: self.rank_title = "ÉTALON"
        else: self.rank_title = "LÉGENDE DU FASO 👑"

    def save_data(self):
        if self.score > self.high_score:
            self.high_score = self.score
        
        self.total_xp += self.score
        self.update_rank()
        self.store.put('stats', best=self.high_score, xp=self.total_xp)

    def trigger_game_over(self):
        if not self.game_over:
            self.game_over = True
            if self.sound_crash: self.sound_crash.play()
            
            # ATTRIBUTION MEDAILLE (TEXTE + COULEUR)
            # Plus de problème d'image buggée !
            if self.score >= 50: 
                self.medal_text = "MEDAILLE D'OR"
                self.medal_color = [1, 0.84, 0, 1] # Jaune Or
            elif self.score >= 20: 
                self.medal_text = "MEDAILLE D'ARGENT"
                self.medal_color = [0.75, 0.75, 0.75, 1] # Gris Argent
            elif self.score >= 10: 
                self.medal_text = "MEDAILLE DE BRONZE"
                self.medal_color = [0.8, 0.5, 0.2, 1] # Marron Bronze
            else: 
                self.medal_text = "COURAGE !"
                self.medal_color = [1, 1, 1, 1] # Blanc
            
            self.save_data()

    def do_flash(self):
        anim = Animation(opacity=0.6, duration=0.05) + Animation(opacity=0, duration=0.15)
        anim.start(self.flash_layer)

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
             return super().on_touch_down(touch)
             
        if self.sound_flap:
            if self.sound_flap.state == 'play': self.sound_flap.stop()
            self.sound_flap.play()

        if not self.started:
            self.started = True
            self.velocity = dp(400)
        else:
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
        self.game_speed = dp(200)
        if self.bg_star: self.bg_star.center_x = self.width / 2
        self.animate_xp()

    def spawn_pipe(self):
        p = Pipe(tex_top=self.pipe_tex_red, tex_bot=self.pipe_tex_green)
        p.set_height(self.height)
        p.x = self.width
        self.pipe_layer.add_widget(p)
        self.pipes.append(p)

    def update(self, dt):
        target_speed = dp(200) + (self.score * dp(5))
        if target_speed > dp(450): target_speed = dp(450)
        self.game_speed = target_speed

        if self.bg_star and self.started and not self.game_over:
            self.bg_star.x -= (self.game_speed * 0.3) * dt
            if self.bg_star.right < 0:
                self.bg_star.x = self.width

        if not self.started or self.game_over: return
        
        self.velocity -= self.gravity * dt
        self.bird.y += self.velocity * dt
        self.bird.angle = max(min(self.velocity * 0.15, 30), -60)
        
        self.spawn_timer += dt
        required_time = 1.8 * (dp(200) / self.game_speed) 
        if self.spawn_timer > required_time:
            self.spawn_pipe()
            self.spawn_timer = 0
            
        for p in self.pipes[:]:
            p.x -= self.game_speed * dt
            
            if p.right < self.bird.x and not p.scored:
                self.score += 1
                p.scored = True
                self.do_flash()
                if self.sound_score:
                    if self.sound_score.state == 'play': self.sound_score.stop()
                    self.sound_score.play()
            
            if p.right < 0:
                self.pipe_layer.remove_widget(p)
                self.pipes.remove(p)
                
            if (self.bird.right > p.x and self.bird.x < p.right):
                if (self.bird.y < p.bottom_h) or (self.bird.top > p.top_y):
                    self.trigger_game_over()
                    
        if self.bird.y < 0 or self.bird.top > self.height:
            self.trigger_game_over()

class FlappyApp(App):
    def build(self):
        Builder.load_string(kv)
        return FlappyGame()

if __name__ == '__main__':
    FlappyApp().run()
        
