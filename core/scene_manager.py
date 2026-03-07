class SceneManager:
    def __init__(self, first_scene):
        self.scene = first_scene

    def set_scene(self, new_scene):
        self.scene = new_scene

    def handle_events(self, events):
        self.scene.handle_events(events)

    def update(self):
        self.scene.update()

    def draw(self):
        self.scene.draw()