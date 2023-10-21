from flask import Flask, render_template
import pygame
import os

app = Flask(__name__)

@app.route('/')
def index():
    # Инициализация Pygame
    import pygame
    import os.path
    import random

    def load_image(name, color_key=None):
        fullname = os.path.join(name)
        try:
            image = pygame.image.load(fullname).convert()
        except pygame.error as message:
            print('Cannot load image:', name)
            raise SystemExit(message)

        if color_key is not None:
            if color_key == -1:
                color_key = image.get_at((0, 0))
            image.set_colorkey(color_key)
        else:
            image = image.convert_alpha()
        return image

    def load_level(filename):
        filename = filename
        # читаем уровень, убирая символы перевода строки
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]

        # и подсчитываем максимальную длину
        max_width = max(map(len, level_map))

        # дополняем каждую строку пустыми клетками ('.')
        return list(map(lambda x: x.ljust(max_width, '.'), level_map))

    class Tile(pygame.sprite.Sprite):
        def __init__(self, tile_type, pos_x, pos_y):
            super().__init__(tiles_group, all_sprites)
            self.image = tile_images[tile_type]
            self.rect = self.image.get_rect().move(
                tile_width * pos_x, tile_height * pos_y)

    class Player(pygame.sprite.Sprite):
        def __init__(self, pos_x, pos_y):
            super().__init__(player_group, all_sprites)
            self.image = player_image
            self.x = pos_x;
            self.y = pos_y
            self.rect = self.image.get_rect().move(
                tile_width * pos_x, tile_height * pos_y)

    def generate_level(level):
        new_player, x, y = None, None, None
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == '.':
                    Tile('empty', x, y)
                elif level[y][x] == '#':
                    Tile('wall', x, y)
                elif level[y][x] == '@':
                    Tile('empty', x, y)
                    new_player = Player(x, y)
        # вернем игрока, а также размер поля в клетках
        return new_player, x, y

    if __name__ == '__main__':
        pygame.init()
        size = width, height = 550, 550
        screen = pygame.display.set_mode(size)

        tile_images = {
            'wall': pygame.transform.scale(load_image('box.png'), (50, 50)),
            'empty': pygame.transform.scale(load_image('grass.png'), (50, 50))
        }
        player_image = load_image('img.png')
        player_image = pygame.transform.scale(player_image, (50, 50))
        player_image.set_colorkey((0, 0, 0))

        tile_width = tile_height = 50

        player = None

        all_sprites = pygame.sprite.Group()
        tiles_group = pygame.sprite.Group()
        player_group = pygame.sprite.Group()

        game = load_level('map.txt')

        running = 1
        fps = 60
        clock = pygame.time.Clock()
        i = 0
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and player.y > 0:
                        i = 1
                        if game[player.y - 1][player.x] != '#':
                            L = list(game[player.y - 1])
                            L[player.x] = '@'
                            game[player.y - 1] = L
                            L = list(game[player.y])
                            L[player.x] = '.'
                            game[player.y] = L
                            break
                    if event.key == pygame.K_LEFT and player.x > 0:
                        i = 2
                        if game[player.y][player.x - 1] != '#':
                            L = list(game[player.y])
                            L[player.x - 1] = '@'
                            L[player.x] = '.'
                            game[player.y] = L
                            break
                    if event.key == pygame.K_DOWN and player.y < len(game) - 1:
                        i = 3
                        if game[player.y + 1][player.x] != '#':
                            L = list(game[player.y + 1])
                            L[player.x] = '@'
                            game[player.y + 1] = L
                            L = list(game[player.y])
                            L[player.x] = '.'
                            game[player.y] = L
                            break
                    if event.key == pygame.K_RIGHT and player.x < len(game[0]) - 1:
                        i = 4
                        if game[player.y][player.x + 1] != '#':
                            L = list(game[player.y])
                            L[player.x + 1] = '@'
                            L[player.x] = '.'
                            game[player.y] = L
                            break
                    if event.key == pygame.K_SPACE and i:
                        if i == 1:
                            if player.y > 0:
                                L = list(game[player.y - 1])
                                L[player.x] = '.'
                                game[player.y - 1] = L
                        if i == 2:
                            if player.x > 0:
                                L = list(game[player.y])
                                L[player.x - 1] = '.'
                                game[player.y] = L
                        if i == 3:
                            if player.y < len(game) - 1:
                                L = list(game[player.y + 1])
                                L[player.x] = '.'
                                game[player.y + 1] = L
                        if i == 4:
                            if player.x < len(game[0]) - 1:
                                L = list(game[player.y])
                                L[player.x + 1] = '.'
                                game[player.y] = L

            player, level_x, level_y = generate_level(game)

            all_sprites.draw(screen)

            pygame.display.flip()
            clock.tick(fps)

        pygame.quit()

    return render_template('index.html', debug=app.debug)

if __name__ == '__main__':
    app.run(debug=True)
