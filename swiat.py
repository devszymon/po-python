import json
import random

class Swiat:
    def __init__(self, szerokosc: int, wysokosc: int):
        self._szerokosc = szerokosc
        self._wysokosc = wysokosc
        self._tura = 0
        self._organizmy = []
        self._plansza = {}
        self._logi = []

    @property
    def szerokosc(self): return self._szerokosc
    
    @property
    def wysokosc(self): return self._wysokosc

    @property
    def tura(self): return self._tura

    def dodaj_log(self, komunikat: str):
        self._logi.append(komunikat)

    def pobierz_logi_i_wyczysc(self):
        logi = self._logi[:]
        self._logi.clear()
        return logi

    def czy_pole_na_planszy(self, pole: tuple) -> bool:
        x, y = pole
        return 0 <= x < self._szerokosc and 0 <= y < self._wysokosc

    def pobierz_organizm(self, pole: tuple):
        return self._plansza.get(pole)

    def pobierz_organizmy(self):
        return self._organizmy[:]

    def dodaj_organizm(self, organizm, pole: tuple):
        if self.czy_pole_na_planszy(pole) and pole not in self._plansza:
            self._organizmy.append(organizm)
            self._plansza[pole] = organizm
            organizm.polozenie = pole

    def usun_organizm(self, organizm):
        if organizm in self._organizmy:
            organizm.zyje = False
            self._organizmy.remove(organizm)
            if self._plansza.get(organizm.polozenie) == organizm:
                del self._plansza[organizm.polozenie]

    def przesun_organizm(self, organizm, nowe_pole: tuple):
        stare_pole = organizm.polozenie
        if self._plansza.get(stare_pole) == organizm:
            del self._plansza[stare_pole]
        self._plansza[nowe_pole] = organizm
        organizm.polozenie = nowe_pole

    def pobierz_sasiednie_pola(self, pole: tuple, zasieg: int = 1):
        x, y = pole
        pola = []
        for dx in range(-zasieg, zasieg + 1):
            for dy in range(-zasieg, zasieg + 1):
                if dx == 0 and dy == 0:
                    continue
                nowe = (x + dx, y + dy)
                if self.czy_pole_na_planszy(nowe):
                    pola.append(nowe)
        return pola

    def znajdz_wolne_sasiednie(self, pole: tuple, zasieg: int = 1):
        sasiednie = self.pobierz_sasiednie_pola(pole, zasieg)
        wolne = [p for p in sasiednie if p not in self._plansza]
        return random.choice(wolne) if wolne else None

    def wykonaj_ture(self):
        self._tura += 1
        self._organizmy.sort(key=lambda o: (o.inicjatywa, o.wiek), reverse=True)

        for org in self._organizmy[:]:
            if org.zyje:
                org.akcja()
            org.wiek += 1

    def zapisz_stan(self, sciezka: str):
        dane = {
            "szerokosc": self._szerokosc,
            "wysokosc": self._wysokosc,
            "tura": self._tura,
            "organizmy": []
        }

        for org in self._organizmy:
            if not org.zyje:
                continue
            dane["organizmy"].append({
                "typ": org.__class__.__name__,
                "x": org.polozenie[0],
                "y": org.polozenie[1],
                "sila": org.sila,
                "wiek": org.wiek,
                "dodatkowy_stan": org.stan_dodatkowy()
            })

        with open(sciezka, "w", encoding="utf-8") as plik:
            json.dump(dane, plik, ensure_ascii=False, indent=2)

        self.dodaj_log(f"Zapisano stan świata do pliku: {sciezka}")

    def wczytaj_stan(self, sciezka: str):
        from organizmy.zwierzeta import Wilk, Owca, Lis, Zolw, Antylopa, CyberOwca, Czlowiek
        from organizmy.rosliny import Trawa, Mlecz, Guarana, WilczeJagody, BarszczSosnowskiego

        klasy = {
            "Wilk": Wilk,
            "Owca": Owca,
            "Lis": Lis,
            "Zolw": Zolw,
            "Antylopa": Antylopa,
            "CyberOwca": CyberOwca,
            "Czlowiek": Czlowiek,
            "Trawa": Trawa,
            "Mlecz": Mlecz,
            "Guarana": Guarana,
            "WilczeJagody": WilczeJagody,
            "BarszczSosnowskiego": BarszczSosnowskiego,
        }

        with open(sciezka, "r", encoding="utf-8") as plik:
            dane = json.load(plik)

        self._szerokosc = dane["szerokosc"]
        self._wysokosc = dane["wysokosc"]
        self._tura = dane["tura"]
        self._organizmy.clear()
        self._plansza.clear()
        self._logi.clear()

        for wpis in dane["organizmy"]:
            klasa = klasy.get(wpis["typ"])
            if not klasa:
                continue
            organizm = klasa(self)
            organizm.sila = wpis["sila"]
            organizm.wiek = wpis["wiek"]
            organizm.wczytaj_stan_dodatkowy(wpis.get("dodatkowy_stan", {}))
            self.dodaj_organizm(organizm, (wpis["x"], wpis["y"]))

        self.dodaj_log(f"Wczytano stan świata z pliku: {sciezka}")

    def rysuj_swiat(self):
        print(f"--- Tura {self._tura} ---")
        for y in range(self._wysokosc):
            wiersz = ""
            for x in range(self._szerokosc):
                org = self._plansza.get((x, y))
                wiersz += org.znak() if org else "."
            print(wiersz)
        print("-------------")