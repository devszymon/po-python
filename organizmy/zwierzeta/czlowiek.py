from organizmy.bazowe import Zwierze
from umiejetnosci.samopalenie import Calopalenie


class Czlowiek(Zwierze):
    def __init__(self, swiat):
        super().__init__(5, 4, swiat)
        self._kierunek_ruchu = None
        self._umiejetnosc = Calopalenie(self)

    @property
    def kierunek_ruchu(self):
        return self._kierunek_ruchu

    @kierunek_ruchu.setter
    def kierunek_ruchu(self, wartosc):
        self._kierunek_ruchu = wartosc

    def znak(self):
        return "H"

    def aktywuj_umiejetnosc(self):
        if self._umiejetnosc.aktywuj():
            self.swiat.dodaj_log("Człowiek aktywował Całopalenie!")
        else:
            self.swiat.dodaj_log("Umiejętność ładuje się lub już trwa!")

    def akcja(self):
        if self.kierunek_ruchu:
            nx = self.polozenie[0] + self.kierunek_ruchu[0]
            ny = self.polozenie[1] + self.kierunek_ruchu[1]
            nowe_pole = (nx, ny)

            if self.swiat.czy_pole_na_planszy(nowe_pole):
                self.przemiesc_sie_lub_walcz(nowe_pole)

            self.kierunek_ruchu = None

        self._umiejetnosc.dzialanie(self.swiat)
        self._umiejetnosc.aktualizuj_stan()

    def stan_dodatkowy(self) -> dict:
        return {
            "kierunek_ruchu": list(self.kierunek_ruchu) if self.kierunek_ruchu else None,
            "umiejetnosc": self._umiejetnosc.stan(),
        }

    def wczytaj_stan_dodatkowy(self, dane: dict):
        kierunek = dane.get("kierunek_ruchu")
        self.kierunek_ruchu = tuple(kierunek) if kierunek else None
        self._umiejetnosc.wczytaj_stan(dane.get("umiejetnosc", {}))
