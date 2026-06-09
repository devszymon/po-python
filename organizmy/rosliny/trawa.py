from organizmy.bazowe import Roslina


class Trawa(Roslina):
    def __init__(self, swiat):
        super().__init__(0, swiat)

    def znak(self):
        return "t"

