import pygame

class Sokoban:
  def __init__(self):
    pygame.init()

    self.load_images()
    self.new_game()

    self.height = len(self.map)
    self.width = len(self.map[0])
    self.scale = self.images[0].get_width()

    window_height = self.height * self.scale + self.scale
    window_width = self.width * self.scale
    self.window = pygame.display.set_mode((window_width, window_height))

    pygame.display.set_caption("Sokoban")

    self.font = pygame.font.SysFont("Arial", 24)

    self.main_loop()


  def load_images(self):
    self.images = []
    for image in ["floor","wall","target","box","robot","done","target_robot"]:
      self.images.append(pygame.image.load(image + ".png"))

  def new_game(self):
    self.map = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                  [1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1],
                  [1, 2, 3, 0, 0, 0, 1, 0, 0, 1, 2, 3, 0, 0, 0, 0, 1],
                  [1, 0, 0, 1, 2, 3, 0, 2, 3, 0, 0, 0, 1, 0, 0, 0, 1],
                  [1, 0, 4, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1],
                  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

    self.moves = 0

  def game_solved(self):
    for y in range(self.height):
      for x in range(self.width):
        if self.map[y][x] in [2,6]:
          return False
    return True

  def check_events(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        exit()

      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
          self.move(0,-1)
        if event.key == pygame.K_RIGHT:
          self.move(0,1)
        if event.key == pygame.K_UP:
          self.move(-1,0)
        if event.key == pygame.K_DOWN:
          self.move(1,0)
        if event.key == pygame.K_SPACE:
          self.new_game()
        if event.key == pygame.K_ESCAPE:
          exit()

  def find_robot(self):
    for y in range(self.height):
      for x in range(self.width):
        if self.map[y][x] in [4,6]:
          return y, x

  def move(self, move_y, move_x):
    if self.game_solved():
      return

    old_robot_y, old_robot_x = self.find_robot()
    new_robot_y = old_robot_y + move_y
    new_robot_x = old_robot_x + move_x

    if self.map[new_robot_y][new_robot_x] == 1:
      return

    if self.map[new_robot_y][new_robot_x] in [3,5]:
      new_box_y = new_robot_y + move_y
      new_box_x = new_robot_x + move_x

      if self.map[new_box_y][new_box_x] in [1,3,5]:
        return

      self.map[new_box_y][new_box_x] += 3
      self.map[new_robot_y][new_robot_x] -= 3

    self.map[old_robot_y][old_robot_x] -= 4
    self.map[new_robot_y][new_robot_x] += 4
    self.moves += 1

  def draw_window(self):

    self.window.fill((0,0,0))

    for y in range(self.height):
      for x in range(self.width):
        image = self.images[self.map[y][x]]
        self.window.blit(image, (x * self.scale, y * self.scale))

    game_text = self.font.render(f"Moves: {self.moves}", True, (255,0,0))
    self.window.blit(game_text, (25, self.height * self.scale + 10))

    game_text = self.font.render("Esc = exit", True, (255,0,0))
    self.window.blit(game_text, (200, self.height * self.scale + 10))

    game_text = self.font.render("Space = restart", True, (255,0,0))
    self.window.blit(game_text, (400, self.height * self.scale + 10))

    if self.game_solved():
      game_text = self.font.render("Game solved!", True, (255,0,0))
      x = (self.width * self.scale - game_text.get_width()) / 2
      y = (self.height * self.scale - game_text.get_height()) / 2
      pygame.draw.rect(self.window, (0,0,0), (x, y, game_text.get_width(), game_text.get_height()))
      self.window.blit(game_text, (x,y))

    pygame.display.flip()

  def main_loop(self):
    while True:
      self.check_events()
      self.draw_window()


if __name__ == "__main__":
  Sokoban()
