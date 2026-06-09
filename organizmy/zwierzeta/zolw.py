import random

from organizmy.bazowe import Zwierze


class Zolw(Zwierze):
    def __init__(self, swiat):
        super().__init__(2, 1, swiat)

    def znak(self):
        return "Z"

    def akcja(self):
        if random.random() > 0.75:
            super().akcja()

    def czy_odbija_atak(self, atakujacy):
        return atakujacy.sila < 5

