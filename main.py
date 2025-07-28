import pygame

pygame.init()

# setup the screen
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 650
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("JOUST")
# set up the clock
clock = pygame.time.Clock()

# Constants
GRAVITY = 0.5
# set initial variables

running = True
moving_left = False
moving_right = False

BG = (0, 0, 0)  # Background color (black)


def load_sliced_sprites(w, h, filename):  # function to load and slice sprites
    # returns a list of image frames sliced from file
    images = []
    master_image = pygame.image.load(filename)
    master_image = master_image.convert_alpha()
    master_width, master_height = master_image.get_size()
    for i in range(int(master_width / w)):
        images.append(master_image.subsurface((i * w, 0, w, h)))
    return images


def loadPlatforms():
    platformimages = []
    platformimages.append(pygame.image.load("img/plat1.png").convert_alpha())
    platformimages.append(pygame.image.load("img/plat2.png").convert_alpha())
    platformimages.append(pygame.image.load("img/plat3.png").convert_alpha())
    platformimages.append(pygame.image.load("img/plat4.png").convert_alpha())
    platformimages.append(pygame.image.load("img/plat5.png").convert_alpha())
    platformimages.append(pygame.image.load("img/plat6.png").convert_alpha())
    platformimages.append(pygame.image.load("img/plat7.png").convert_alpha())
    platformimages.append(pygame.image.load("img/plat8.png").convert_alpha())
    return platformimages


class platformClass(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.topleft = (x, y)
        self.right = self.rect.right
        self.top = self.rect.top


class Player(
    pygame.sprite.Sprite
):  # Player class to handle player actions and animations
    def __init__(self, images, x, y):
        super().__init__()
        self.alive = True
        self.direction = 1
        self.frame = 3
        self.flip = False
        self.flying = False
        self.flap_count = 0
        self.images = images
        self.image = self.images[self.frame]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.update_time = pygame.time.get_ticks()
        self.vel_y = 0

    def move(
        self, moving_left, moving_right
    ):  # function to handle player movement and flight
        dx = 0
        dy = 0

        if moving_left:
            dx -= 5
            self.direction = -1
            self.flip = True
        if moving_right:
            dx += 5
            self.direction = 1
            self.flip = False

        if self.rect.left + dx < 0:
            self.rect.left = SCREEN_WIDTH - 60 + dx
        elif self.rect.right + dx > SCREEN_WIDTH:
            self.rect.right = 60 + dx

        if self.rect.top <= 20:
            dy = 20 - self.rect.top
            self.flying = False

        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
            self.flap_count -= 1
        dy += self.vel_y

        if self.rect.bottom + dy > 550:
            dy = 550 - self.rect.bottom
            self.flying = False
            self.flap_count = 0
            self.vel_y = 0

        self.rect.x += dx
        self.rect.y += dy

    def walk(self):  # function to handle player walking animation
        ANIMATION_COOLDOWN = 50
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame += 1
        if self.frame > 2:
            self.frame = 0

        self.image = self.images[self.frame]

    def fly(self):  # function to handle player flying animation
        ANIMATION_COOLDOWN = 100
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame += 1
        if self.frame > 6:
            self.frame = 5
        self.image = self.images[self.frame]

    def idle(self):  # function to handle player idle animation
        self.frame = 3
        self.image = self.images[self.frame]

    def update_animation(self):
        pass

    def draw(self):  # function to draw the player on the screen
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


# Load images for player, enemies, and other sprites
playerimages = load_sliced_sprites(60, 60, "img/playerMounted.png")
enemyimages = load_sliced_sprites(60, 58, "img/enemies2.png")
spawnimages = load_sliced_sprites(60, 60, "img/spawn1.png")
enemyunmountedimages = load_sliced_sprites(60, 60, "img/unmounted.png")
playerunmountedimages = load_sliced_sprites(60, 60, "img/playerUnmounted.png")
eggimages = load_sliced_sprites(40, 33, "img/egg.png")
# Load platform images
platforms = pygame.sprite.Group()  # Group to hold platform sprites
platformImages = loadPlatforms()
plat1 = platformClass(platformImages[0], 200, 550)
plat2 = platformClass(platformImages[1], 350, 395)
plat3 = platformClass(platformImages[2], 350, 130)
plat4 = platformClass(platformImages[3], 0, 100)
plat5 = platformClass(platformImages[4], 759, 100)
plat6 = platformClass(platformImages[5], 0, 310)
plat7 = platformClass(platformImages[6], 759, 310)
plat8 = platformClass(platformImages[7], 600, 290)
platforms.add(plat1, plat2, plat3, plat4, plat5, plat6, plat7, plat8)


player = Player(playerimages, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Main game loop
while running:
    screen.fill(BG)  # Fill the screen with the background color
    lavaRect = [0, 600, 900, 50]
    pygame.draw.rect(screen, (255, 0, 0), lavaRect)
    lavaRect2 = [0, 620, 900, 30]
    pygame.draw.rect(screen, (255, 0, 0), lavaRect)

    for platform in platforms:  # Draw all platforms
        screen.blit(platform.image, platform.rect)

    player.update_animation()  # Update player animation
    player.draw()

    if player.alive:  # call the appropriate player animation based on state
        if player.flying or player.vel_y != 0:
            player.fly()
        elif moving_left or moving_right:
            player.walk()
        else:
            player.idle()
        player.move(moving_left, moving_right)

    for event in pygame.event.get():  # Handle events
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:  # Handle key presses
            if event.key == pygame.K_LEFT:
                moving_left = True
            if event.key == pygame.K_RIGHT:
                moving_right = True
            if event.key == pygame.K_ESCAPE:
                running = False
            if (
                event.key == pygame.K_SPACE and player.flap_count < 4
            ):  # Limit the number of flaps
                player.flying = True
                player.flap_count += 1
                player.vel_y = -10
                player.frame = 5  # Set to flying frame

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                moving_left = False
            if event.key == pygame.K_RIGHT:
                moving_right = False

    pygame.display.update()  # Update the display
    clock.tick(60)  # Limit to 60 frames per second
pygame.quit()
