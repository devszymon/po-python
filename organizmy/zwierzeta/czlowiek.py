from organizmy.bazowe import Zwierze
from umiejetnosci.samopalenie import Calopalenie


class Czlowiek(Zwierze):
    def __init__(self, swiat):
        super().__init__(5, 4, swiat)
        self.kierunek_ruchu = None
        self.umiejetnosc = Calopalenie(self)

    def znak(self):
        return "H"

    def aktywuj_umiejetnosc(self):
        if self.umiejetnosc.aktywuj():
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

        self.umiejetnosc.dzialanie(self.swiat)
        self.umiejetnosc.aktualizuj_stan()

    def stan_dodatkowy(self) -> dict:
        return {
            "kierunek_ruchu": list(self.kierunek_ruchu) if self.kierunek_ruchu else None,
            "umiejetnosc": self.umiejetnosc.stan(),
        }

    def wczytaj_stan_dodatkowy(self, dane: dict):
        kierunek = dane.get("kierunek_ruchu")
        self.kierunek_ruchu = tuple(kierunek) if kierunek else None
        self.umiejetnosc.wczytaj_stan(dane.get("umiejetnosc", {}))

