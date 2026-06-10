from abc import ABC, abstractmethod
import random

class Organizm(ABC):
    def __init__(self, sila: int, inicjatywa: int, swiat):
        self._sila = sila
        self.inicjatywa = inicjatywa
        self.swiat = swiat
        self.polozenie = (0, 0)
        self.wiek = 0
        self.zyje = True

    @property
    def sila(self): return self._sila

    @sila.setter
    def sila(self, wartosc): self._sila = wartosc

    @abstractmethod
    def akcja(self): pass

    @abstractmethod
    def kolizja(self, atakujacy): pass

    @abstractmethod
    def znak(self) -> str: pass

    def nazwa(self) -> str:
        return self.__class__.__name__

    def czy_odbija_atak(self, atakujacy) -> bool: return False
    def czy_ucieka(self) -> bool: return False
    def czy_odporny_na_barszcz(self) -> bool: return False
    def wplyw_na_atakujacego(self, atakujacy): pass
    def stan_dodatkowy(self) -> dict: return {}
    def wczytaj_stan_dodatkowy(self, dane: dict): pass


class Zwierze(Organizm):
    def akcja(self):
        nowe_pole = self.losuj_pole_ruchu()
        if nowe_pole != self.polozenie:
            self.przemiesc_sie_lub_walcz(nowe_pole)

    def losuj_pole_ruchu(self, zasieg: int = 1):
        sasiednie = self.swiat.pobierz_sasiednie_pola(self.polozenie, zasieg)
        return random.choice(sasiednie) if sasiednie else self.polozenie

    def przemiesc_sie_lub_walcz(self, nowe_pole: tuple):
        obronca = self.swiat.pobierz_organizm(nowe_pole)
        if obronca is None:
            self.swiat.przesun_organizm(self, nowe_pole)
        else:
            obronca.kolizja(self)

    def kolizja(self, atakujacy):
        if type(self) == type(atakujacy):
            wolne = self.swiat.znajdz_wolne_sasiednie(self.polozenie)
            if wolne:
                nowy = self.__class__(self.swiat)
                self.swiat.dodaj_organizm(nowy, wolne)
                self.swiat.dodaj_log(f"Rozmnażanie: Powstał nowy {self.nazwa()}")
            return

        if self.czy_odbija_atak(atakujacy):
            self.swiat.dodaj_log(f"{self.nazwa()} odbija atak {atakujacy.nazwa()}!")
            return

        if self.czy_ucieka():
            wolne = self.swiat.znajdz_wolne_sasiednie(self.polozenie)
            if wolne:
                self.swiat.dodaj_log(f"{self.nazwa()} ucieka przed {atakujacy.nazwa()}!")
                poprzednie_pole_obroncy = self.polozenie
                self.swiat.przesun_organizm(self, wolne)
                self.swiat.przesun_organizm(atakujacy, poprzednie_pole_obroncy)
                return

        if atakujacy.sila >= self.sila:
            self.swiat.dodaj_log(f"{atakujacy.nazwa()} zabija {self.nazwa()}")
            self.swiat.usun_organizm(self)
            self.swiat.przesun_organizm(atakujacy, self.polozenie)
        else:
            self.swiat.dodaj_log(f"{self.nazwa()} broni się i zabija {atakujacy.nazwa()}")
            self.swiat.usun_organizm(atakujacy)


class Roslina(Organizm):
    def __init__(self, sila: int, swiat):
        super().__init__(sila=sila, inicjatywa=0, swiat=swiat)

    def akcja(self):
        szansa_na_zasianie = 0.05
        if random.random() < szansa_na_zasianie:
            wolne = self.swiat.znajdz_wolne_sasiednie(self.polozenie)
            if wolne:
                nowa = self.__class__(self.swiat)
                self.swiat.dodaj_organizm(nowa, wolne)
                self.swiat.dodaj_log(f"{self.nazwa()} rozsiewa się.")

    def kolizja(self, atakujacy):
        self.swiat.dodaj_log(f"{atakujacy.nazwa()} zjada {self.nazwa()}")
        self.wplyw_na_atakujacego(atakujacy)

        self.swiat.usun_organizm(self)

        if atakujacy.zyje:
            self.swiat.przesun_organizm(atakujacy, self.polozenie)