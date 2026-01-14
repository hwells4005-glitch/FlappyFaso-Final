## **4. Code principal optimisé (`main.py`)**

```python
"""
Flappy Faso - Jeu mobile addictif avec thème patriotique
Version optimisée et professionnelle
"""

import random
import math
import json
import os
from datetime import datetime
from pathlib import Path

from kivy.config import Config
from kivy.storage.jsonstore import JsonStore
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import (
    NumericProperty, ListProperty, BooleanProperty,
    ObjectProperty, StringProperty, DictProperty
)
from kivy.metrics import dp, sp
from kivy.graphics.texture import Texture
from kivy.core.audio import SoundLoader
from kivy.core.image import Image as CoreImage
from kivy.graphics import (
    Color, Rectangle, Line, Mesh, RoundedRectangle,
    Ellipse, Rotate, PushMatrix, PopMatrix
)

# === CONFIGURATION GLOBALE ===
Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')
Config.set('kivy', 'exit_on_escape', '1')
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

# Configuration AdMob (IDs de test)
ADMOB_APP_ID = "ca-app-pub-3940256099942544~3347511713"
ADMOB_BANNER_ID = "ca-app-pub-3940256099942544/6300978111"
ADMOB_INTERSTITIAL_ID = "ca-app-pub-3940256099942544/1033173712"
USE_ADMOB = True

# Vérification KivMob
kivmob_available = False
try:
    from kivmob import KivMob, TestIds
    kivmob_available = True
except ImportError:
    print("KivMob non disponible - Publicités désactivées")

# === CONSTANTES DU JEU ===
class GameConfig:
    # Physique
    GRAVITY = dp(1300)
    JUMP_FORCE = dp(400)
    MIN_GAME_SPEED = dp(240)
    MAX_GAME_SPEED = dp(500)
    SPEED_INCREMENT = dp(8)
    
    # Tuyaux
    PIPE_WIDTH = dp(75)
    PIPE_GAP = dp(180)
    PIPE_MIN_HEIGHT = dp(100)
    PIPE_SPAWN_TIME = 1.3  # secondes
    PIPE_VARIATION = dp(120)
    
    # Oiseau
    BIRD_SIZE = dp(50)
    BIRD_ROTATION_FACTOR = 0.15
    BIRD_MAX_ROTATION = 30
    BIRD_MIN_ROTATION = -60
    HIT_MARGIN = dp(10)
    
    # XP et Niveaux
    XP_PER_SCORE = 1
    LEVELS = [
        {"name": "NOVICE", "xp": 0, "color": [0.5, 0.5, 0.5, 1]},
        {"name": "APPRENTI", "xp": 50, "color": [0, 0.8, 0, 1]},
        {"name": "CITOYEN", "xp": 200, "color": [0, 0.5, 1, 1]},
        {"name": "PATRIOTE", "xp": 500, "color": [1, 0.5, 0, 1]},
        {"name": "ÉTALON", "xp": 1000, "color": [1, 0, 0, 1]},
        {"name": "LÉGENDE", "xp": 5000, "color": [1, 0.84, 0, 1]},
    ]
    
    # Médailles
    MEDALS = [
        {"score": 0, "name": "COURAGE !", "color": [0.7, 0.7, 0.7, 1]},
        {"score": 10, "name": "BRONZE", "color": [0.8, 0.5, 0.2, 1]},
        {"score": 20, "name": "ARGENT", "color": [0.75, 0.75, 0.75, 1]},
        {"score": 50, "name": "OR", "color": [1, 0.84, 0, 1]},
        {"score": 100, "name": "PLATINE", "color": [0.6, 0.8, 1, 1]},
    ]
    
    # Couleurs
    COLORS = {
        "green": [0, 158/255, 73/255, 1],
        "red": [239/255, 43/255, 45/255, 1],
        "yellow": [1, 0.84, 0, 1],
        "white": [1, 1, 1, 1],
        "black": [0, 0, 0, 1],
        "dark_bg": [0.1, 0.1, 0.1, 0.95],
    }

# === GESTIONNAIRE DE SONS ===
class SoundManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_sounds()
        return cls._instance
    
    def _init_sounds(self):
        self.sounds = {}
        self.muted = False
        
        # Chargement des sons
        sound_files = {
            'jump': 'assets/sounds/jump.wav',
            'score': 'assets/sounds/score.wav',
            'hit': 'assets/sounds/hit.wav',
            'game_over': 'assets/sounds/game_over.wav',
        }
        
        for name, path in sound_files.items():
            if os.path.exists(path):
                self.sounds[name] = SoundLoader.load(path)
                if self.sounds[name]:
                    self.sounds[name].volume = 0.5
            else:
                print(f"Son non trouvé: {path}")
                self.sounds[name] = None
    
    def play(self, sound_name):
        if not self.muted and sound_name in self.sounds and self.sounds[sound_name]:
            try:
                self.sounds[sound_name].play()
            except:
                pass
    
    def toggle_mute(self):
        self.muted = not self.muted
        return self.muted

# === COMPOSANTS GRAPHIQUES ===
class ParticleSystem(Widget):
    particles = ListProperty([])
    
    def emit(self, pos, count=10, color=[1, 1, 1, 1], speed_range=(100, 300)):
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(*speed_range)
            velocity = [math.cos(angle) * speed, math.sin(angle) * speed]
            lifetime = random.uniform(0.5, 1.5)
            
            self.particles.append({
                'pos': list(pos),
                'velocity': velocity,
                'lifetime': lifetime,
                'max_lifetime': lifetime,
                'color': color,
                'size': random.uniform(dp(5), dp(15))
            })
    
    def update(self, dt):
        to_remove = []
        for i, p in enumerate(self.particles):
            p['pos'][0] += p['velocity'][0] * dt
            p['pos'][1] += p['velocity'][1] * dt
            p['lifetime'] -= dt
            
            if p['lifetime'] <= 0:
                to_remove.append(i)
        
        for i in reversed(to_remove):
            self.particles.pop(i)
        
        self.canvas.clear()
        with self.canvas:
            for p in self.particles:
                alpha = p['lifetime'] / p['max_lifetime']
                Color(*p['color'][:3], p['color'][3] * alpha)
                Ellipse(
                    pos=(p['pos'][0] - p['size']/2, p['pos'][1] - p['size']/2),
                    size=(p['size'], p['size'])
                )

class FasoStar(Widget):
    vertices = ListProperty([])
    indices = ListProperty([])
    angle = NumericProperty(0)
    pulse_scale = NumericProperty(1)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self._update_vertices, size=self._update_vertices)
        Clock.schedule_once(self._update_vertices, 0)
        
        # Animation de pulsation
        anim = Animation(pulse_scale=1.1, duration=2) + Animation(pulse_scale=1, duration=2)
        anim.repeat = True
        anim.start(self)
        
        Clock.schedule_interval(self._rotate, 1/60)
    
    def _rotate(self, dt):
        self.angle += 0.5
    
    def _update_vertices(self, *args):
        cx, cy = self.center_x, self.center_y
        scale = self.pulse_scale
        outer = (self.width / 2) * scale
        inner = outer * 0.4
        
        points = [cx, cy, 0.5, 0.5]
        angle_step = math.pi / 5
        angle = -math.pi / 2
        
        for i in range(11):
            r = outer if i % 2 == 0 else inner
            points.extend([
                cx + math.cos(angle) * r,
                cy + math.sin(angle) * r,
                0, 0
            ])
            angle += angle_step
        
        self.vertices = points
        self.indices = list(range(12))

class Pipe(Widget):
    gap = NumericProperty(GameConfig.PIPE_GAP)
    top_y = NumericProperty(0)
    top_h = NumericProperty(0)
    bottom_h = NumericProperty(0)
    tex_top = ObjectProperty(None)
    tex_bot = ObjectProperty(None)
    scored = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.width = GameConfig.PIPE_WIDTH
        self._create_textures()
    
    def _create_textures(self):
        """Crée des textures avec effet 3D pour les tuyaux"""
        if not self.tex_top:
            self.tex_top = self._generate_pipe_texture(GameConfig.COLORS["red"])
        if not self.tex_bot:
            self.tex_bot = self._generate_pipe_texture(GameConfig.COLORS["green"])
    
    def _generate_pipe_texture(self, color):
        tex = Texture.create(size=(32, 1), colorfmt='rgb')
        buf = bytearray()
        r, g, b = [int(c * 255) for c in color[:3]]
        
        for i in range(32):
            rel_x = i / 32.0
            # Effet d'éclairage
            light = 0.6 + 0.4 * math.sin(rel_x * math.pi)
            if 6 <= i <= 9:
                light += 0.3  # Highlight au centre
            light = min(light, 1.0)
            
            buf.extend([
                int(r * light),
                int(g * light),
                int(b * light)
            ])
        
        tex.blit_buffer(bytes(buf), colorfmt='rgb', bufferfmt='ubyte')
        tex.mag_filter = 'linear'
        return tex
    
    def set_height(self, screen_height, last_y=None):
        """Définit la hauteur du tuyau inférieur"""
        floor = GameConfig.PIPE_MIN_HEIGHT
        max_h = screen_height - floor - self.gap
        
        if last_y is None:
            # Premier tuyau
            self.bottom_h = screen_height / 2 - (self.gap / 2)
        else:
            # Variation contrôlée
            variation = random.randint(
                int(-GameConfig.PIPE_VARIATION),
                int(GameConfig.PIPE_VARIATION)
            )
            new_h = last_y + variation
            new_h = max(floor + dp(20), min(new_h, max_h - dp(20)))
            self.bottom_h = new_h
        
        self.top_y = self.bottom_h + self.gap
        self.top_h = screen_height - self.top_y

class Bird(Widget):
    angle = NumericProperty(0)
    flap_animation = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (GameConfig.BIRD_SIZE, GameConfig.BIRD_SIZE)
        
        # Animation de battement d'ailes
        self._start_flap_animation()
    
    def _start_flap_animation(self):
        anim = Animation(flap_animation=1, duration=0.2) + \
               Animation(flap_animation=0, duration=0.2)
        anim.repeat = True
        anim.start(self)
    
    def jump(self):
        SoundManager().play('jump')
        anim = Animation(flap_animation=1, duration=0.1) + \
               Animation(flap_animation=0, duration=0.1)
        anim.start(self)

class FlashEffect(Widget):
    opacity = NumericProperty(0)
    
    def flash(self, color=[1, 1, 1, 1]):
        self.canvas.clear()
        with self.canvas:
            Color(*color)
            Rectangle(pos=self.pos, size=self.size)
        
        anim = Animation(opacity=0.7, duration=0.05) + \
               Animation(opacity=0, duration=0.15)
        anim.start(self)

# === ÉCRANS D'INTERFACE ===
class IntroScreen(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self._animate_intro, 0.5)
    
    def _animate_intro(self, dt):
        logo = self.ids.logo_lbl
        anim = (
            Animation(opacity=1, duration=1.5) +
            Animation(opacity=1, duration=1.0) +
            Animation(opacity=0, duration=0.5)
        )
        anim.start(logo)

class StatsPopup(FloatLayout):
    def __init__(self, game, **kwargs):
        super().__init__(**kwargs)
        self.game = game
        self._update_stats()
    
    def _update_stats(self):
        stats = self.game.get_stats()
        self.ids.rank_label.text = f"RANG: {stats['rank']}"
        self.ids.xp_label.text = f"XP: {stats['xp']}"
        self.ids.best_label.text = f"MEILLEUR: {stats['best']}"
        self.ids.games_label.text = f"PARTIES: {stats['games']}"
        self.ids.next_rank_label.text = stats['next_rank']

# === JEU PRINCIPAL ===
class FlappyGame(FloatLayout):
    # Propriétés du jeu
    score = NumericProperty(0)
    high_score = NumericProperty(0)
    total_xp = NumericProperty(0)
    games_played = NumericProperty(0)
    
    # États
    show_stats = BooleanProperty(False)
    in_intro = BooleanProperty(True)
    started = BooleanProperty(False)
    game_over = BooleanProperty(False)
    paused = BooleanProperty(False)
    
    # Propriétés UI
    rank_title = StringProperty("NOVICE")
    next_rank_text = StringProperty("")
    medal_text = StringProperty("")
    medal_color = ListProperty([1, 1, 1, 1])
    
    # Physique
    velocity = NumericProperty(0)
    gravity = NumericProperty(GameConfig.GRAVITY)
    game_speed = NumericProperty(GameConfig.MIN_GAME_SPEED)
    
    # Références
    pipes = ListProperty([])
    bird = ObjectProperty(None)
    pipe_layer = ObjectProperty(None)
    flash_layer = ObjectProperty(None)
    intro_layer = ObjectProperty(None)
    particle_layer = ObjectProperty(None)
    bg_texture = ObjectProperty(None)
    bg_star = ObjectProperty(None)
    
    # Données
    store = None
    last_pipe_y = NumericProperty(0)
    spawn_timer = NumericProperty(0)
    
    # Publicités
    ads = None
    ad_counter = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._init_game()
    
    def _init_game(self):
        """Initialisation complète du jeu"""
        # Configuration initiale
        self._init_storage()
        self._init_graphics()
        self._init_audio()
        self._init_ads()
        
        # Planification des mises à jour
        Clock.schedule_interval(self.update, 1.0 / 60.0)
        Clock.schedule_once(self._init_star, 0.1)
        
        # Démarrer l'intro
        Clock.schedule_once(self.start_intro, 0.5)
    
    def _init_storage(self):
        """Initialise le système de sauvegarde"""
        self.store = JsonStore('data/game_data.json')
        if self.store.exists('stats'):
            data = self.store.get('stats')
            self.high_score = data.get('best', 0)
            self.total_xp = data.get('xp', 0)
            self.games_played = data.get('games', 0)
        else:
            self._create_default_save()
        
        self.update_rank()
    
    def _create_default_save(self):
        """Crée un fichier de sauvegarde par défaut"""
        self.store.put('stats',
            best=0,
            xp=0,
            games=0,
            achievements=[],
            last_played=datetime.now().isoformat()
        )
    
    def _init_graphics(self):
        """Initialise les éléments graphiques"""
        self._generate_background()
        self.pipe_tex_red = self._generate_pipe_texture(GameConfig.COLORS["red"])
        self.pipe_tex_green = self._generate_pipe_texture(GameConfig.COLORS["green"])
    
    def _init_audio(self):
        """Initialise le gestionnaire audio"""
        self.sound_manager = SoundManager()
    
    def _init_ads(self):
        """Initialise les publicités"""
        if kivmob_available and USE_ADMOB:
            try:
                self.ads = KivMob(ADMOB_APP_ID)
                self.ads.new_banner(ADMOB_BANNER_ID, top_pos=False)
                self.ads.request_banner()
                self.ads.show_banner()
                
                # Interstitiel
                self.ads.new_interstitial(ADMOB_INTERSTITIAL_ID)
                self.ads.request_interstitial()
            except Exception as e:
                print(f"Erreur initialisation pubs: {e}")
    
    def _generate_background(self):
        """Génère le fond drapeau"""
        tex = Texture.create(size=(1, 64), colorfmt='rgb')
        buf = bytearray()
        
        for i in range(64):
            if i < 32:  # Vert
                buf.extend([0, 158, 73])
            else:       # Rouge
                buf.extend([239, 43, 45])
        
        tex.blit_buffer(bytes(buf), colorfmt='rgb', bufferfmt='ubyte')
        tex.mag_filter = 'linear'
        self.bg_texture = tex
    
    def _generate_pipe_texture(self, color):
        """Génère une texture pour les tuyaux"""
        return Pipe()._generate_pipe_texture(color)
    
    def _init_star(self, dt):
        """Positionne l'étoile de fond"""
        if self.bg_star:
            self.bg_star.center_x = self.width / 2
    
    # === GESTION DES ÉTATS ===
    def start_intro(self, dt):
        """Démarre l'animation d'introduction"""
        if self.intro_layer:
            logo = self.intro_layer.ids.logo_lbl
            anim = (
                Animation(opacity=1, duration=1.5) +
                Animation(opacity=1, duration=1.0) +
                Animation(opacity=0, duration=0.5)
            )
            anim.bind(on_complete=self._end_intro)
            anim.start(logo)
    
    def _end_intro(self, *args):
        """Termine l'intro"""
        self.in_intro = False
    
    def toggle_stats(self):
        """Affiche/masque les statistiques"""
        self.show_stats = not self.show_stats
    
    def toggle_pause(self):
        """Met le jeu en pause/reprise"""
        self.paused = not self.paused
    
    # === SYSTÈME DE PROGRESSION ===
    def update_rank(self):
        """Met à jour le rang du joueur"""
        for i, level in enumerate(GameConfig.LEVELS):
            if self.total_xp >= level["xp"]:
                self.rank_title = level["name"]
                
                # Prochain niveau
                if i + 1 < len(GameConfig.LEVELS):
                    next_level = GameConfig.LEVELS[i + 1]
                    needed = next_level["xp"] - self.total_xp
                    self.next_rank_text = f"Plus que {needed} XP pour {next_level['name']}!"
                else:
                    self.next_rank_text = "Niveau maximum atteint !"
    
    def get_stats(self):
        """Retourne les statistiques du joueur"""
        return {
            'rank': self.rank_title,
            'xp': int(self.total_xp),
            'best': self.high_score,
            'games': self.games_played,
            'next_rank': self.next_rank_text
        }
    
    def save_data(self):
        """Sauvegarde les données du jeu"""
        if self.score > self.high_score:
            self.high_score = self.score
        
        self.total_xp += self.score * GameConfig.XP_PER_SCORE
        self.games_played += 1
        
        self.store.put('stats',
            best=self.high_score,
            xp=self.total_xp,
            games=self.games_played,
            last_played=datetime.now().isoformat()
        )
        
        self.update_rank()
    
    def get_medal(self, score):
        """Détermine la médaille selon le score"""
        medal = GameConfig.MEDALS[0]
        for m in GameConfig.MEDALS:
            if score >= m["score"]:
                medal = m
        return medal
    
    # === GESTION DU JEU ===
    def start_game(self):
        """Démarre une nouvelle partie"""
        if not self.started and not self.game_over:
            self.started = True
            self.velocity = GameConfig.JUMP_FORCE
            self.bird.jump()
    
    def trigger_game_over(self):
        """Déclenche la fin de partie"""
        if not self.game_over:
            self.game_over = True
            self.sound_manager.play('hit')
            
            # Médaille
            medal = self.get_medal(self.score)
            self.medal_text = medal["name"]
            self.medal_color = medal["color"]
            
            # Particules
            if self.particle_layer:
                self.particle_layer.emit(
                    self.bird.center,
                    count=30,
                    color=[1, 0.84, 0, 1],
                    speed_range=(100, 400)
                )
            
            # Sauvegarde
            self.save_data()
            
            # Publicité interstitielle (toutes les 3 parties)
            self.ad_counter += 1
            if self.ad_counter >= 3 and self.ads:
                self.ads.show_interstitial()
                self.ad_counter = 0
                self.ads.request_interstitial()
    
    def reset(self):
        """Réinitialise le jeu pour une nouvelle partie"""
        # Nettoyage
        self.pipe_layer.clear_widgets()
        self.pipes = []
        
        # Réinitialisation des propriétés
        self.bird.pos = (dp(100), self.height / 2)
        self.bird.angle = 0
        self.velocity = 0
        self.score = 0
        self.game_over = False
        self.started = False
        self.game_speed = GameConfig.MIN_GAME_SPEED
        self.last_pipe_y = 0
        self.spawn_timer = 0
        
        # Réinitialisation de l'étoile
        if self.bg_star:
            self.bg_star.center_x = self.width / 2
    
    def do_flash(self):
        """Effet flash lors du passage d'un tuyau"""
        self.flash_layer.flash([1, 1, 1, 1])
        self.sound_manager.play('score')
    
    # === GÉNÉRATION DES TUYAUX ===
    def spawn_pipe(self):
        """Génère un nouveau tuyau"""
        p = Pipe(tex_top=self.pipe_tex_red, tex_bot=self.pipe_tex_green)
        
        if len(self.pipes) > 0:
            p.set_height(self.height, last_y=self.last_pipe_y)
        else:
            p.set_height(self.height)
        
        self.last_pipe_y = p.bottom_h
        p.x = self.width
        self.pipe_layer.add_widget(p)
        self.pipes.append(p)
    
    # === BOUCLE DE JEU ===
    def update(self, dt):
        """Boucle principale de mise à jour"""
        if self.paused or not self.started or self.game_over:
            return
        
        # Mise à jour de la vitesse
        target_speed = (
            GameConfig.MIN_GAME_SPEED + 
            (self.score * GameConfig.SPEED_INCREMENT)
        )
        self.game_speed = min(target_speed, GameConfig.MAX_GAME_SPEED)
        
        # Animation du fond
        if self.bg_star:
            self.bg_star.x -= (self.game_speed * 0.3) * dt
            if self.bg_star.right < 0:
                self.bg_star.x = self.width
        
        # Physique de l'oiseau
        self.velocity -= self.gravity * dt
        self.bird.y += self.velocity * dt
        
        # Rotation de l'oiseau
        rotation = self.velocity * GameConfig.BIRD_ROTATION_FACTOR
        self.bird.angle = max(
            min(rotation, GameConfig.BIRD_MAX_ROTATION),
            GameConfig.BIRD_MIN_ROTATION
        )
        
        # Génération des tuyaux
        self.spawn_timer += dt
        required_time = GameConfig.PIPE_SPAWN_TIME * (
            GameConfig.MIN_GAME_SPEED / self.game_speed
        )
        
        if self.spawn_timer > required_time:
            self.spawn_pipe()
            self.spawn_timer = 0
        
        # Gestion des tuyaux
        for p in self.pipes[:]:
            # Déplacement
            p.x -= self.game_speed * dt
            
            # Score
            if p.right < self.bird.x and not p.scored:
                self.score += 1
                p.scored = True
                self.do_flash()
            
            # Suppression
            if p.right < 0:
                self.pipe_layer.remove_widget(p)
                self.pipes.remove(p)
            
            # Collisions
            if self._check_collision(p):
                self.trigger_game_over()
                break
        
        # Collisions avec les bords
        if self.bird.y < 0 or self.bird.top > self.height:
            self.trigger_game_over()
    
    def _check_collision(self, pipe):
        """Vérifie la collision avec un tuyau"""
        margin = GameConfig.HIT_MARGIN
        
        # Vérifie si l'oiseau est dans la zone horizontale du tuyau
        in_horizontal_zone = (
            self.bird.right - margin > pipe.x and
            self.bird.x + margin < pipe.right
        )
        
        if in_horizontal_zone:
            # Vérifie les collisions verticales
            hit_top = self.bird.top - margin > pipe.top_y
            hit_bottom = self.bird.y + margin < pipe.bottom_h
            
            if hit_top or hit_bottom:
                return True
        
        return False
    
    # === GESTION DES TOUCHES ===
    def on_touch_down(self, touch):
        """Gère les touches de l'écran"""
        if self.show_stats or self.in_intro:
            return super().on_touch_down(touch)
        
        if self.game_over:
            return super().on_touch_down(touch)
        
        if not self.started:
            if touch.y < self.height * 0.7:
                self.start_game()
        else:
            self.velocity = GameConfig.JUMP_FORCE
            self.bird.jump()
        
        return True

# === APPLICATION PRINCIPALE ===
class FlappyFasoApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Flappy Faso"
        self.icon = "assets/icon.png" if os.path.exists("assets/icon.png") else None
    
    def build(self):
        """Construit l'interface du jeu"""
        # Chargement du fichier KV
        kv_file = Path(__file__).parent / "game.kv"
        if kv_file.exists():
            Builder.load_file(str(kv_file))
        else:
            # Fallback au KV intégré
            Builder.load_string(KV_STRING)
        
        return FlappyGame()
    
    def on_pause(self):
        """Gère la mise en pause de l'app"""
        return True
    
    def on_resume(self):
        """Gère la reprise de l'app"""
        pass

# === FICHIER KV (game.kv) ===
KV_STRING = '''
#:import dp kivy.metrics.dp
#:import sp kivy.metrics.sp

<FasoStar>:
    canvas:
        Color:
            rgba: 1, 0.84, 0, 1
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

<Bird>:
    size_hint: None, None
    size: dp(50), dp(50)
    canvas.before:
        PushMatrix
        Rotate:
            angle: self.angle
            origin: self.center
    canvas:
        # Corps
        Color:
            rgba: 1, 0.84, 0, 1
        Ellipse:
            pos: self.pos
            size: self.size
        
        # Œil
        Color:
            rgba: 0, 0, 0, 1
        Ellipse:
            pos: self.x + dp(35), self.y + dp(30)
            size: dp(8), dp(8)
        
        # Bec
        Color:
            rgba: 1, 0.5, 0, 1
        Triangle:
            points:
                [self.x + dp(50), self.y + dp(25),
                self.x + dp(60), self.y + dp(25),
                self.x + dp(55), self.y + dp(15)]
        
        # Aile (animation)
        Color:
            rgba: 1, 0.7, 0, 1
        Ellipse:
            pos: self.x + dp(10), self.y + dp(10 + self.flap_animation * 10)
            size: dp(25), dp(15)
    canvas.after:
        PopMatrix

<FlashEffect>:
    size_hint: 1, 1
    opacity: 0

<ParticleSystem>:
    size_hint: 1, 1

<IntroScreen>:
    size_hint: 1, 1
    canvas.before:
        Color:
            rgba: 0, 0, 0, 0.9
        Rectangle:
            pos: self.pos
            size: self.size
    
    BoxLayout:
        orientation: 'vertical'
        padding: dp(50)
        spacing: dp(20)
        
        Label:
            id: logo_lbl
            text: "FLAPPY FASO"
            font_size: '48sp'
            bold: True
            color: 0, 1, 0, 1
            outline_width: 3
            outline_color: 0, 0, 0, 1
            opacity: 0
        
        Label:
            text: "Préparez-vous à voler !"
            font_size: '24sp'
            color: 1, 1, 1, 1
            opacity: 0.8

<StatsPopup>:
    size_hint: 0.9, 0.8
    pos_hint: {'center_x': 0.5, 'center_y': 0.5}
    
    canvas.before:
        Color:
            rgba: 0.1, 0.1, 0.1, 0.95
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(20),]
        
        Color:
            rgba: 1, 0.84, 0, 1
        Line:
            rounded_rectangle: [self.x, self.y, self.width, self.height, dp(20)]
            width: dp(2)
    
    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(10)
        
        Label:
            id: title_label
            text: "PROFIL JOUEUR"
            font_size: '32sp'
            bold: True
            color: 1, 0.84, 0, 1
            size_hint_y: 0.15
        
        Label:
            id: rank_label
            text: "RANG: NOVICE"
            font_size: '24sp'
            bold: True
            color: 0, 1, 0, 1
            size_hint_y: 0.12
        
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: 0.12
            
            Label:
                text: "XP:"
                font_size: '20sp'
            
            ProgressBar:
                max: 100
                value: 50
        
        Label:
            id: xp_label
            text: "XP TOTAL: 0"
            font_size: '20sp'
            size_hint_y: 0.1
        
        Label:
            id: best_label
            text: "MEILLEUR SCORE: 0"
            font_size: '20sp'
            color: 0.5, 0.8, 1, 1
            size_hint_y: 0.1
        
        Label:
            id: games_label
            text: "PARTIES JOUÉES: 0"
            font_size: '18sp'
            size_hint_y: 0.1
        
        Label:
            id: next_rank_label
            text: ""
            font_size: '16sp'
            color: 0.7, 0.7, 0.7, 1
            size_hint_y: 0.15
        
        Button:
            text: "FERMER"
            size_hint_y: 0.15
            background_color: 1, 0, 0, 1
            font_size: '22sp'
            on_release: root.game.toggle_stats()

<FlappyGame>:
    pipe_layer: pipe_layer
    bird: bird
    flash_layer: flash_layer
    intro_layer: intro_layer
    particle_layer: particle_layer
    bg_star: bg_star
    
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size
            texture: root.bg_texture
    
    FasoStar:
        id: bg_star
        size_hint: None, None
        size: dp(250), dp(250)
        center_y: root.height * 0.5
        opacity: 0.9 if not root.started else 0.5
    
    Widget:
        id: pipe_layer
    
    Bird:
        id: bird
        pos: dp(100), root.height * 0.5
        opacity: 1 if root.started else 0
    
    FlashEffect:
        id: flash_layer
    
    ParticleSystem:
        id: particle_layer
    
    # === MENU PRINCIPAL ===
    BoxLayout:
        orientation: 'vertical'
        size_hint: 1, 1
        visible: not root.started and not root.game_over and not root.show_stats and not root.in_intro
        opacity: 1 if self.visible else 0
        padding: dp(30)
        spacing: dp(15)
        
        Label:
            text: "FLAPPY FASO"
            font_size: '56sp'
            bold: True
            color: 1, 1, 1, 1
            outline_width: 4
            outline_color: 0, 0, 0, 1
            size_hint_y: 0.3
        
        Button:
            text: "JOUER"
            size_hint_y: 0.15
            background_color: 0, 0.6, 0, 1
            font_size: '24sp'
            bold: True
            on_release: root.start_game()
        
        Button:
            text: "STATISTIQUES"
            size_hint_y: 0.15
            background_color: 0, 0.5, 1, 1
            font_size: '22sp'
            bold: True
            on_release: root.toggle_stats()
        
        Button:
            text: "SON: ON"
            size_hint_y: 0.12
            background_color: 0.5, 0.5, 0.5, 1
            font_size: '18sp'
            on_release: 
                self.text = "SON: OFF" if root.sound_manager.toggle_mute() else "SON: ON"
        
        Label:
            text: "Touchez l'écran pour sauter !"
            font_size: '20sp'
            color: 1, 1, 1, 1
            outline_width: 2
            outline_color: 0, 0, 0, 1
            size_hint_y: 0.28
    
    # === STATISTIQUES ===
    StatsPopup:
        game: root
        visible: root.show_stats
        opacity: 1 if root.show_stats else 0
    
    # === GAME OVER ===
    BoxLayout:
        orientation: 'vertical'
        size_hint: 0.85, 0.6
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        visible: root.game_over
        opacity: 1 if root.game_over else 0
        
        canvas.before:
            Color:
                rgba: 0, 0, 0, 0.95
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [dp(25),]
            
            Color:
                rgba: 1, 0.84, 0, 1
            Line:
                rounded_rectangle: [self.x, self.y, self.width, self.height, dp(25)]
                width: dp(3)
        
        Label:
            text: "GAME OVER"
            font_size: '42sp'
            bold: True
            color: 1, 0, 0, 1
            outline_width: 3
            outline_color: 0, 0, 0, 1
            size_hint_y: 0.2
        
        Label:
            text: root.medal_text
            font_size: '36sp'
            bold: True
            color: root.medal_color
            outline_width: 2
            outline_color: 0, 0, 0, 1
            size_hint_y: 0.25
        
        Label:
            text: "Score: {}".format(root.score)
            font_size: '32sp'
            color: 1, 1, 1, 1
            size_hint_y: 0.15
        
        Label:
            text: "Meilleur: {}".format(root.high_score)
            font_size: '24sp'
            color: 1, 1, 0, 1
            size_hint_y: 0.1
        
        Button:
            text: "REJOUER"
            font_size: '28sp'
            bold: True
            background_color: 0, 0.7, 0, 1
            on_release: root.reset()
            size_hint_y: 0.2
    
    # === SCORE EN JEU ===
    Label:
        text: str(root.score)
        font_size: '64sp'
        pos_hint: {'center_x': 0.5, 'top': 0.96}
        bold: True
        color: 1, 1, 1, 1
        outline_width: 3
        outline_color: 0, 0, 0, 1
        opacity: 1 if root.started and not root.game_over else 0
    
    # === PAUSE ===
    Button:
        text: "II"
        size_hint: None, None
        size: dp(50), dp(50)
        pos_hint: {'right': 0.98, 'top': 0.98}
        background_color: 0.5, 0.5, 0.5, 0.7
        font_size: '24sp'
        bold: True
        opacity: 1 if root.started and not root.game_over else 0
        on_release: root.toggle_pause()
    
    # === ÉCRAN DE PAUSE ===
    BoxLayout:
        orientation: 'vertical'
        size_hint: 0.8, 0.5
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        visible: root.paused
        opacity: 1 if root.paused else 0
        
        canvas.before:
            Color:
                rgba: 0, 0, 0, 0.9
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [dp(20),]
        
        Label:
            text: "PAUSE"
            font_size: '40sp'
            bold: True
            color: 1, 0.84, 0, 1
            size_hint_y: 0.3
        
        Button:
            text: "REPRENDRE"
            font_size: '24sp'
            background_color: 0, 0.6, 0, 1
            on_release: root.toggle_pause()
            size_hint_y: 0.25
        
        Button:
            text: "MENU"
            font_size: '24sp'
            background_color: 0.8, 0.3, 0, 1
            on_release: 
                root.toggle_pause()
                root.reset()
            size_hint_y: 0.25
    
    # === INTRODUCTION ===
    IntroScreen:
        id: intro_layer
        opacity: 1 if root.in_intro else 0
        visible: root.in_intro
'''

# === POINT D'ENTRÉE ===
if __name__ == '__main__':
    # Création des répertoires nécessaires
    os.makedirs('assets/sounds', exist_ok=True)
    os.makedirs('assets/fonts', exist_ok=True)
    os.makedirs('data', exist_ok=True)
    
    # Lancement de l'application
    FlappyFasoApp().run()
