import random

from organizmy.bazowe import Zwierze


class Lis(Zwierze):
    def __init__(self, swiat):
        super().__init__(3, 7, swiat)

    def znak(self):
        return "L"

    def losuj_pole_ruchu(self, zasieg=1):
        sasiednie = self.swiat.pobierz_sasiednie_pola(self.polozenie, zasieg)
        bezpieczne = []
        for pole in sasiednie:
            organizm = self.swiat.pobierz_organizm(pole)
            if organizm is None or organizm.sila <= self.sila:
                bezpieczne.append(pole)
        return random.choice(bezpieczne) if bezpieczne else self.polozenie

