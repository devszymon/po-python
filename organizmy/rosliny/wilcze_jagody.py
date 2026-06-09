from organizmy.bazowe import Roslina


class WilczeJagody(Roslina):
    def __init__(self, swiat):
        super().__init__(99, swiat)

    def znak(self):
        return "j"

    def wplyw_na_atakujacego(self, atakujacy):
        self.swiat.usun_organizm(atakujacy)
        self.swiat.dodaj_log(f"{atakujacy.nazwa()} ginie od Wilczych Jagód!")

