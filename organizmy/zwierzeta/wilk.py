from organizmy.bazowe import Zwierze


class Wilk(Zwierze):
    def __init__(self, swiat):
        super().__init__(9, 5, swiat)

    def znak(self):
        return "W"

