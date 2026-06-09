import random

from organizmy.bazowe import Zwierze


class Antylopa(Zwierze):
    def __init__(self, swiat):
        super().__init__(4, 4, swiat)

    def znak(self):
        return "A"

    def akcja(self):
        nowe_pole = self.losuj_pole_ruchu(zasieg=2)
        if nowe_pole != self.polozenie:
            self.przemiesc_sie_lub_walcz(nowe_pole)

    def czy_ucieka(self):
        return random.random() < 0.5

