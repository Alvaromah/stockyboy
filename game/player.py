import math

class Player():
    def __init__(self, x, y, images):
        super().__init__()
        self.images = images
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.anim_speed = 4
        self.anim_counter = 0
        self.movement = 0
        self.movement_frames = 0
        self.jumping = False
        self.original_x = x
        self.original_y = y
        self.gravity = 1
        self.jump_velocity = 16
        self.crashing = False

    def move(self, direction, length, duration):
        if self.crashing:
            return
        if self.rect.x + direction < 106 or self.rect.x + direction > 406:
            return
        if self.movement_frames == 0:
            self.movement = (direction * length) / duration
            self.movement_frames = duration

    def jump(self):
        if not self.jumping:
            self.jumping = True
            self.velocity_y = -self.jump_velocity
            if self.image_index < 6:
                self.image_index = 3
            else:
                self.image_index = 10
            self.image = self.images[self.image_index]

    def update(self, speed):
        self.anim_speed = 10 - speed

        if self.crashing:
            self.rect.x += self.velocity_x
            self.rect.y += self.velocity_y
            self.velocity_y += self.gravity
            if self.rect.x >= 2400:
                self.rect.x = self.original_x
                self.rect.y = self.original_y
                self.crashing = False

        elif self.jumping:
            self.rect.y += self.velocity_y
            self.velocity_y += self.gravity

            if self.image_index < 6:
                self.image_index = 3
            else:
                self.image_index = 10
            self.image = self.images[self.image_index]

            if self.rect.y >= self.original_y:
                self.jumping = False
                self.rect.y = self.original_y  # Reset the y position after the jump

        else:
            self.anim_counter += 1

        if not self.crashing:
            self.anim_counter += 1

            if self.anim_counter >= self.anim_speed:
                self.anim_counter = 0
                self.image_index = (self.image_index + 1) % len(self.images)
                self.image = self.images[self.image_index]

            if self.movement_frames > 0:
                self.rect.x += self.movement
                self.movement_frames -= 1
                if self.movement_frames == 0:
                    print(self.rect.x)

    def collide(self, rects):
        if not self.jumping and not self.crashing:
            bounds = self.rect.inflate(-80, -100)
            bounds.y += 50
            for rect in rects:
                rect = rect.inflate(-80, -60)
                if bounds.colliderect(rect):
                    self.crash()
                    return True
        return False

    def collide_box(self, rects):
        if not self.crashing:
            bounds = self.rect.inflate(-25, -100)
            bounds.y += 50
            for rect in rects:
                rect = rect.inflate(-0, -60)
                rect.y += 30
                if bounds.colliderect(rect):
                    self.crash()
                    return True
        return False

    def crash(self):
        self.crashing = True
        self.crash_velocity = 20
        self.crash_angle = math.radians(60)
        self.velocity_x = self.crash_velocity * math.cos(self.crash_angle)
        self.velocity_y = -self.crash_velocity * math.sin(self.crash_angle)
        self.movement = 0
        self.movement_frames = 0

    def draw(self, screen):
        screen.blit(self.image, self.rect)

