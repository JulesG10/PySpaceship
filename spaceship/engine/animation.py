

class AnimationItem:

    def __init__(self, images, duration, loop=1, frame_index=0, start_time = 0, stop = False):
        self.is_stop = stop
        self.images = images
        self.duration = duration
        self.index = frame_index
        self.time = start_time
        self.loop = loop


class Animation:

    def __init__(self, renderer):
        self.renderer = renderer
        self.animations: list[AnimationItem] = []

    def create(self, item: AnimationItem):
        self.animations.append(item)
        return len(self.animations)-1

    def reset(self, id, start_index=1, loop=1):
        self.animations[id] = AnimationItem([], 0, 1, 0, 0, False)

    def draw(self, id, position, deltatime, size=(-1, -1), ratotation=0, scale=1):
        if id >= len(self.animations):
            return

        animation = self.animations[id]
        if not animation.is_stop:
            animation.time += deltatime * 100

            if animation.time > animation.duration:
                animation.time = 0
                animation.index += 1

                if animation.index > len(animation.images) - 1:
                    animation.index = 0

                    if animation.loop != -1:
                        animation.loop -= 1

                        if animation.loop <= 0:
                            animation.is_stop = True

            image = animation.images[animation.index]
            self.renderer.effect(image, position, size, ratotation, scale)
