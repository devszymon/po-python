from organizmy.bazowe import Zwierze


class Owca(Zwierze):
    def __init__(self, swiat):
        super().__init__(4, 4, swiat)

    def znak(self):
        return "O"

