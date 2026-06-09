from organizmy.bazowe import Roslina


class Mlecz(Roslina):
    def __init__(self, swiat):
        super().__init__(0, swiat)

    def znak(self):
        return "m"

    def akcja(self):
        for _ in range(3):
            super().akcja()

