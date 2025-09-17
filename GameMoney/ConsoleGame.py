"""
Pygame port of Spend Within Reason

Controls:
- S: spend (enter amount via number keys, Enter to confirm, Backspace to edit)
- E: earn (enter amount via number keys, Enter to confirm)
- N: next level
- Q or ESC: quit

If pygame is not available, this script falls back to running the console `Game.py`.
"""
import sys
import random
import os

try:
    import pygame
except Exception as e:
    print("Pygame not available or failed to initialize:", e)
    print("Falling back to console mode using Game.py")
    # Fall back to running the original Game.py console game
    import runpy
    runpy.run_path('Game.py', run_name='__main__')
    sys.exit(0)

# Optional PIL import for GIF frame extraction (best animation)
try:
    from PIL import Image as PILImage
    PIL_AVAILABLE = True
except Exception:
    PIL_AVAILABLE = False

pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 480
FPS = 30
FONT_NAME = pygame.font.get_default_font()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Spend Within Reason')
clock = pygame.time.Clock()
font = pygame.font.Font(FONT_NAME, 20)
big_font = pygame.font.Font(FONT_NAME, 32)


class GIFPlayer:
    """
    Loads an animated GIF (if PIL available) into a list of pygame surfaces and durations.
    Falls back to loading the first frame with pygame.image.load() if PIL not available.
    """
    def __init__(self, path, max_height=200):
        self.path = path
        self.frames = []          # list of (surface, duration_ms)
        self.index = 0
        self.acc = 0              # ms accumulator
        self.max_height = max_height
        self.loaded = False

        if not os.path.isfile(path):
            # file not found, nothing to do
            self.loaded = False
            return

        if PIL_AVAILABLE:
            try:
                img = PILImage.open(path)
                # iterate frames
                for frame_idx in range(0, getattr(img, "n_frames", 1)):
                    img.seek(frame_idx)
                    duration = img.info.get('duration', 100)  # ms
                    # convert to RGBA and to a mode pygame likes
                    frame = img.convert('RGBA')
                    # convert to string buffer then pygame image
                    mode = frame.mode
                    size = frame.size
                    data = frame.tobytes()
                    surf = pygame.image.fromstring(data, size, mode).convert_alpha()
                    # scale down if taller than max_height
                    if surf.get_height() > self.max_height:
                        scale = self.max_height / surf.get_height()
                        new_w = int(surf.get_width() * scale)
                        new_h = int(self.max_height)
                        surf = pygame.transform.smoothscale(surf, (new_w, new_h))
                    self.frames.append((surf, int(duration)))
                if not self.frames:
                    # no frames loaded, try fallback
                    raise RuntimeError("PIL loaded but no frames found")
                self.loaded = True
            except Exception:
                # fallback to single-frame load via pygame
                self.frames = []
                self.loaded = False

        if (not PIL_AVAILABLE) or (not self.loaded):
            # fallback: try pygame.image.load to get a single surface
            try:
                surf = pygame.image.load(path).convert_alpha()
                if surf.get_height() > self.max_height:
                    scale = self.max_height / surf.get_height()
                    new_w = int(surf.get_width() * scale)
                    new_h = int(self.max_height)
                    surf = pygame.transform.smoothscale(surf, (new_w, new_h))
                # give it a default duration so animation code won't fail
                self.frames = [(surf, 1000)]
                self.loaded = True
            except Exception:
                # couldn't load the image at all
                self.frames = []
                self.loaded = False

    def update(self, dt_ms):
        if not self.loaded or not self.frames:
            return
        if len(self.frames) == 1:
            return  # static image, nothing to advance
        self.acc += dt_ms
        _, duration = self.frames[self.index]
        while self.acc >= duration:
            self.acc -= duration
            self.index = (self.index + 1) % len(self.frames)
            _, duration = self.frames[self.index]

    def draw(self, surf, x, y):
        if not self.loaded or not self.frames:
            return
        current_surf, _ = self.frames[self.index]
        surf.blit(current_surf, (x, y))

    def get_size(self):
        if not self.loaded or not self.frames:
            return (0, 0)
        s, _ = self.frames[0]
        return s.get_size()


class Player:
    def __init__(self, balance=500):
        self.balance = balance
        self.level = 1

    def spend_money(self, amount):
        self.balance -= amount

    def earn_money(self, amount):
        self.balance += amount

    def check_bankruptcy(self):
        return self.balance < 0

    def next_level(self):
        if self.balance >= 0:
            self.level += 1
            return True
        return False

    def get_mode(self):
        if self.balance > 10000:
            return "Billionaire"
        if self.balance > 5000:
            return "Sugar Daddy"
        elif self.balance > 2500:
            return "Rich Kid"
        elif self.balance > 250:
            return "Average Joe"
        else:
            return "Poor"


class RandomEvent:
    @staticmethod
    def trigger_event(player):
        events = [
            ("Found a $50 bill on the street!", 50),
            ("Lost your wallet! You lose $100.", -100),
            ("Won a small lottery! You gain $200.", 200),
            ("Car broke down! Pay $150 for repairs.", -150),
            ("Received a birthday gift of $75.", 75),
            ("Medical emergency! Hospital bill costs $300.", -300),
            ("Your friend repaid a debt: +$120.", 120),
            ("You got fined for speeding: -$90.", -90),
            ("Unexpected tax refund: +$180.", 180),
        ]

        # 1% chance of jail event
        if random.random() < 0.01:
            return ("Go to jail: -$1000", -1000)

        return random.choice(events)


class SpendingEvent:
    SAMPLE = [
        # Items
        ("Your daughter wants a new phone for her birthday", 'Items'),
        ("Your laptop broke down, need replacement", 'Items'),
        ("You saw a limited edition watch on sale", 'Items'),
        ("A surprise sale: new headphones you can't resist", 'Items'),
        ("Kids want new school shoes", 'Items'),

        # Family
        ("You were invited to a family wedding and want to contribute", 'Family'),
        ("Parents need financial help with groceries", 'Family'),
        ("Your cousin’s baby shower gift", 'Family'),
        ("Help sibling with a down payment", 'Family'),
        ("Family reunion travel costs", 'Family'),

        # Health
        ("You need a routine medical checkup", 'Health'),
        ("Dental treatment required this month", 'Health'),
        ("Your gym membership renewal is due", 'Health'),
        ("Prescription refill costs", 'Health'),
        ("Therapy session—you prioritized mental health", 'Health'),

        # Education
        ("A short course can boost your skills", 'Education'),
        ("Your child’s school tuition fees", 'Education'),
        ("You buy books for professional growth", 'Education'),
        ("Online certification is on offer this month", 'Education'),
        ("Workshop fee for a career boost", 'Education'),

        # Entertainment
        ("A weekend trip with friends is planned", 'Entertainment'),
        ("Concert tickets for your favorite band", 'Entertainment'),
        ("Subscription renewal for streaming services", 'Entertainment'),
        ("New video game release you're excited for", 'Entertainment'),
        ("Dining out with friends (special occasion)", 'Entertainment'),

        # Home
        ("House maintenance is required", 'Home'),
        ("Plumbing issue needs fixing", 'Home'),
        ("New furniture for living room", 'Home'),
        ("Replace broken window", 'Home'),
        ("Garden landscaping project", 'Home'),

        # Transport
        ("Car needs servicing this month", 'Transport'),
        ("Fuel prices increased this week", 'Transport'),
        ("Need to replace car tires", 'Transport'),
        ("Public transport pass renewal", 'Transport'),
        ("Rideshare surge pricing hit this week", 'Transport'),
    ]

    BASE_COST = {
        'Items': 200,
        'Family': 150,
        'Health': 120,
        'Education': 180,
        'Entertainment': 80,
        'Home': 220,
        'Transport': 100,
    }

    @staticmethod
    def generate(level, count=None, cooldowns=None):
        """Generate 2–4 events for the given level (randomly 2,3 or 4)."""
        if count is None:
            count = random.choice([2, 3, 4])
        events = []
        attempts = 0
        while len(events) < count and attempts < 100:
            attempts += 1
            text, cat = random.choice(SpendingEvent.SAMPLE)
            # skip if on cooldown
            if cooldowns and text in cooldowns and level < cooldowns[text]:
                continue
            base = SpendingEvent.BASE_COST.get(cat, 100)
            mean = base * (1 + 0.1 * (level - 1))
            cost = max(10, int(random.gauss(mean, mean * 0.2)))
            # avoid duplicates in this batch
            if any(ev['text'] == text for ev in events):
                continue
            events.append({'text': text, 'category': cat, 'cost': cost})
        return events


class NewsEvent:
    SAMPLES = [
        'Stock market sees minor gains; small investors cheer.',
        'Local startup secures funding, promises new jobs.',
        'Banks announce a promotion on savings accounts.',
        'Crypto prices wobble amid regulatory news.',
        'New fintech app launches cashback campaign.',
        'Government discusses tax relief measures for households.',
    ]

    @staticmethod
    def random_news():
        return random.choice(NewsEvent.SAMPLES)


def draw_text(surf, text, size, x, y, color=(255, 255, 255)):
    if size >= 30:
        f = big_font
    else:
        f = font
    img = f.render(str(text), True, color)
    surf.blit(img, (x, y))


def modal_spending_loop(player, ev, event_cooldowns, gif_player=None):
    """Show a modal of a single spending event; returns when Y/N chosen or quit."""
    pushing = True
    while pushing:
        dt = clock.tick(FPS)
        for ge in pygame.event.get():
            if ge.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ge.type == pygame.KEYDOWN:
                if ge.key == pygame.K_y:
                    player.spend_money(ev['cost'])
                    return ('paid', ev)
                elif ge.key == pygame.K_n:
                    return ('skipped', ev)
                elif ge.key == pygame.K_q or ge.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        # draw modal, include gif if present
        screen.fill((18, 24, 32))
        draw_text(screen, f'Level: {player.level}', 28, 20, 20)
        draw_text(screen, f'Balance: ${player.balance}', 24, 20, 60)
        draw_text(screen, 'Spending Opportunity:', 28, 20, 110)
        draw_text(screen, ev['text'], 20, 20, 150)
        draw_text(screen, f"Category: {ev['category']}  Cost: ${ev['cost']}", 20, 20, 190)
        draw_text(screen, 'Press Y to pay, N to skip', 20, 20, 230)
        # update & draw gif
        if gif_player and gif_player.loaded:
            gif_player.update(dt)
            gw, gh = gif_player.get_size()
            gif_x = WIDTH - gw - 20
            gif_y = 20
            gif_player.draw(screen, gif_x, gif_y)
        pygame.display.flip()


def main():
    # Game starts immediately with default balance
    player = Player(balance=500)

    # Attempt to load the gif player for "whatever.gif"
    gif_player = GIFPlayer('man-402_256.gif', max_height=200)
    if not gif_player.loaded:
        # if not loaded, gif_player will be harmless (no drawing)
        pass

    # Game state
    input_mode = None  # 'spend' or 'earn' or None
    input_buffer = ''
    status_messages = []  # list of last messages to display
    random_event_cooldown = 0
    event_cooldowns = {}
    news_shown_for_level = player.level

    def push(msg):
        status_messages.insert(0, msg)
        if len(status_messages) > 6:
            status_messages.pop()

    push('Game started. Good luck!')
    start_message_shown_at = pygame.time.get_ticks()
    start_message_duration_ms = 2000
    initial_events_shown = False

    running = True
    while running:
        dt = clock.tick(FPS)  # ms since last tick, used for gif timing
        # Check start message timer and show initial spending events once after it expires
        if (not initial_events_shown) and (pygame.time.get_ticks() - start_message_shown_at >= start_message_duration_ms):
            events = SpendingEvent.generate(player.level, cooldowns=event_cooldowns)
            for ev in events:
                result = modal_spending_loop(player, ev, event_cooldowns, gif_player=gif_player)
                if result and result[0] == 'paid':
                    push(f'Paid ${result[1]["cost"]} for: {result[1]["text"]}.')
                    event_cooldowns[result[1]['text']] = player.level + 30
                else:
                    push('Skipped expense.')
            initial_events_shown = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if input_mode is None:
                    if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_n:
                        if player.next_level():
                            push(f'Advanced to level {player.level}.')
                            events = SpendingEvent.generate(player.level, cooldowns=event_cooldowns)
                            for ev in events:
                                result = modal_spending_loop(player, ev, event_cooldowns, gif_player=gif_player)
                                if result and result[0] == 'paid':
                                    push(f'Paid ${result[1]["cost"]} for: {result[1]["text"]}.')
                                    event_cooldowns[result[1]['text']] = player.level + 30
                                else:
                                    push('Skipped expense.')
                            news_shown_for_level = -1
                        else:
                            push('Cannot advance while bankrupt.')
                    elif event.key == pygame.K_s:
                        input_mode = 'spend'
                        input_buffer = ''
                    elif event.key == pygame.K_e:
                        input_mode = 'earn'
                        input_buffer = ''
                else:
                    if event.key == pygame.K_RETURN:
                        try:
                            amt = int(input_buffer) if input_buffer != '' else 0
                        except ValueError:
                            amt = 0
                        if input_mode == 'spend':
                            if amt > player.balance:
                                push('Cannot spend more than current balance!')
                            else:
                                player.spend_money(amt)
                                push(f'Spent ${amt}. New balance ${player.balance}.')
                        elif input_mode == 'earn':
                            player.earn_money(amt)
                            push(f'Earned ${amt}. New balance ${player.balance}.')
                        input_mode = None
                        input_buffer = ''
                    elif event.key == pygame.K_BACKSPACE:
                        input_buffer = input_buffer[:-1]
                    else:
                        if event.unicode.isdigit():
                            input_buffer += event.unicode

        # Random money-affecting events
        if random_event_cooldown <= 0:
            if random.random() < 0.03:
                ev = RandomEvent.trigger_event(player)
                push(ev[0])
                if ev[1] > 0:
                    player.earn_money(ev[1])
                    push(f'Gained ${ev[1]}. Balance ${player.balance}.')
                else:
                    player.spend_money(-ev[1])
                    push(f'Lost ${-ev[1]}. Balance ${player.balance}.')
                random_event_cooldown = 5 * FPS
        else:
            random_event_cooldown -= 1

        # News event
        if news_shown_for_level != player.level:
            if random.random() < 0.02:
                news = NewsEvent.random_news()
                push(f'NEWS: {news}')
                news_shown_for_level = player.level

        # Bankruptcy check
        if player.check_bankruptcy():
            push('You are bankrupt! Balance below 0.')

        # Update GIF animation
        if gif_player and gif_player.loaded:
            gif_player.update(dt)

        # Draw
        screen.fill((18, 24, 32))
        draw_text(screen, f'Level: {player.level}', 24, 20, 20)
        draw_text(screen, f'Balance: ${player.balance}', 24, 220, 20)
        draw_text(screen, f'Mode: {player.get_mode()}', 20, 20, 60)
        draw_text(screen, 'Controls: S spend, E earn, N next level, Q quit', 18, 20, 100)

        # draw gif on the right if available
        if gif_player and gif_player.loaded:
            gw, gh = gif_player.get_size()
            gif_x = WIDTH - gw - 20
            gif_y = 20
            gif_player.draw(screen, gif_x, gif_y)

        if input_mode is not None:
            draw_text(screen, f'{input_mode.upper()} AMOUNT: {input_buffer}', 28, 20, 140, (255, 220, 180))
            draw_text(screen, 'Press Enter to confirm, Backspace to edit', 18, 20, 180, (200, 200, 200))

        y = 220
        for i, m in enumerate(status_messages):
            draw_text(screen, m, 18, 20, y + i * 26, (200, 200 - i * 20, 200))

        if player.check_bankruptcy():
            draw_text(screen, 'BANKRUPT - Press E to earn money or Q to quit', 24, 20, HEIGHT - 80, (240, 80, 80))

        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()

