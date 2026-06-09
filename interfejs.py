import os
import tkinter as tk

from organizmy.rosliny import Trawa, Mlecz, Guarana, WilczeJagody, BarszczSosnowskiego
from organizmy.zwierzeta import Wilk, Owca, Lis, Zolw, Antylopa, CyberOwca, Czlowiek
from swiat import Swiat


class AplikacjaSwiata:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Wirtualny Świat")
        self.rozmiar_pola = 2
        self.sciezka_zapisu = os.path.join(os.path.dirname(__file__), "zapis_swiata.json")

        self.swiat = Swiat(20, 20)
        self.gracz = Czlowiek(self.swiat)
        self.swiat.dodaj_organizm(self.gracz, (10, 10))

        self.klasy_startowe = [
            Wilk, Owca, Lis, Zolw, Antylopa, CyberOwca,
            Trawa, Mlecz, Guarana, WilczeJagody, BarszczSosnowskiego,
        ]
        self.klasy_do_dodawania = {
            "Wilk": Wilk,
            "Owca": Owca,
            "Lis": Lis,
            "Żółw": Zolw,
            "Antylopa": Antylopa,
            "CyberOwca": CyberOwca,
            "Trawa": Trawa,
            "Mlecz": Mlecz,
            "Guarana": Guarana,
            "Wilcze Jagody": WilczeJagody,
            "Barszcz Sosnowskiego": BarszczSosnowskiego,
        }
        self.kolory_organizmow = {
            Wilk: ("#b0bec5", "#000000"),
            Owca: ("#ffffff", "#000000"),
            Lis: ("#ffb74d", "#000000"),
            Zolw: ("#a5d6a7", "#000000"),
            Antylopa: ("#ffcc80", "#000000"),
            CyberOwca: ("#90a4ae", "#ffffff"),
            Czlowiek: ("#64b5f6", "#000000"),
            Trawa: ("#81c784", "#000000"),
            Mlecz: ("#fff176", "#000000"),
            Guarana: ("#ef9a9a", "#000000"),
            WilczeJagody: ("#8e24aa", "#ffffff"),
            BarszczSosnowskiego: ("#2e7d32", "#ffffff"),
        }
        self.kolor_pustego_pola = ("#f5f5f5", "#616161")
        self.wybrany_typ = tk.StringVar(value="Wilk")

        self._zainicjalizuj_swiat()
        self._zbuduj_interfejs()
        self._podlacz_klawisze()
        self.odswiez_widok()

    def _zainicjalizuj_swiat(self):
        for klasa in self.klasy_startowe:
            for _ in range(3):
                wolne = self.swiat.znajdz_wolne_sasiednie((10, 10), zasieg=10)
                if wolne:
                    self.swiat.dodaj_organizm(klasa(self.swiat), wolne)

    def _zbuduj_interfejs(self):
        kontener = tk.Frame(self.root)
        kontener.pack(padx=10, pady=10)

        self.ramka_planszy = tk.Frame(kontener, bd=1, relief=tk.SOLID)
        self.ramka_planszy.grid(row=0, column=0, padx=(0, 10))

        panel = tk.Frame(kontener)
        panel.grid(row=0, column=1, sticky="n")

        self.etykieta_tury = tk.Label(panel, text="Tura: 0")
        self.etykieta_tury.pack(anchor="w")
        self.etykieta_autora = tk.Label(panel, text="Autor: Szymon Jankowski | Indeks: 208489")
        self.etykieta_autora.pack(anchor="w", pady=(0, 8))

        tk.Button(panel, text="Następna tura", command=self.wykonaj_ture).pack(fill="x")
        tk.Button(panel, text="Aktywuj umiejętność", command=self.aktywuj_umiejetnosc).pack(fill="x", pady=(4, 0))
        tk.Button(panel, text="Zapisz", command=self.zapisz_stan).pack(fill="x", pady=(4, 0))
        tk.Button(panel, text="Wczytaj", command=self.wczytaj_stan).pack(fill="x", pady=(4, 0))

        tk.Label(panel, text="Dodaj na kliknięte pole:").pack(anchor="w", pady=(8, 0))
        tk.OptionMenu(panel, self.wybrany_typ, *self.klasy_do_dodawania.keys()).pack(fill="x")

        tk.Label(panel, text="Log zdarzeń:").pack(anchor="w", pady=(8, 0))
        self.pole_logow = tk.Text(panel, width=48, height=20, state=tk.DISABLED)
        self.pole_logow.pack()

        self.pola = []
        for y in range(self.swiat.wysokosc):
            wiersz = []
            for x in range(self.swiat.szerokosc):
                pole = tk.Label(
                    self.ramka_planszy,
                    text=".",
                    width=self.rozmiar_pola,
                    height=1,
                    relief=tk.RIDGE,
                    borderwidth=1,
                    font=("Consolas", 11),
                )
                pole.grid(row=y, column=x)
                pole.bind("<Button-1>", lambda _e, px=x, py=y: self.dodaj_organizm_na_pole(px, py))
                wiersz.append(pole)
            self.pola.append(wiersz)

    def _podlacz_klawisze(self):
        self.root.bind("<Up>", lambda _e: self.ruch_gracza((0, -1)))
        self.root.bind("<Down>", lambda _e: self.ruch_gracza((0, 1)))
        self.root.bind("<Left>", lambda _e: self.ruch_gracza((-1, 0)))
        self.root.bind("<Right>", lambda _e: self.ruch_gracza((1, 0)))
        self.root.bind("<space>", lambda _e: self.wykonaj_ture())
        self.root.bind("p", lambda _e: self.aktywuj_umiejetnosc())
        self.root.bind("k", lambda _e: self.zapisz_stan())
        self.root.bind("l", lambda _e: self.wczytaj_stan())

    def dodaj_organizm_na_pole(self, x: int, y: int):
        if self.swiat.pobierz_organizm((x, y)) is not None:
            self.swiat.dodaj_log(f"Pole {(x, y)} jest zajęte.")
            self.odswiez_widok()
            return

        klasa = self.klasy_do_dodawania[self.wybrany_typ.get()]
        self.swiat.dodaj_organizm(klasa(self.swiat), (x, y))
        self.swiat.dodaj_log(f"Dodano {self.wybrany_typ.get()} na pole {(x, y)}.")
        self.odswiez_widok()

    def ruch_gracza(self, kierunek: tuple[int, int]):
        if self.gracz.zyje:
            self.gracz.kierunek_ruchu = kierunek
        self.wykonaj_ture()

    def wykonaj_ture(self):
        self.swiat.wykonaj_ture()
        self.odswiez_widok()

    def aktywuj_umiejetnosc(self):
        if self.gracz.zyje:
            self.gracz.aktywuj_umiejetnosc()
        self.odswiez_widok()

    def zapisz_stan(self):
        self.swiat.zapisz_stan(self.sciezka_zapisu)
        self.odswiez_widok()

    def wczytaj_stan(self):
        try:
            self.swiat.wczytaj_stan(self.sciezka_zapisu)
            znaleziony = next((o for o in self.swiat.pobierz_organizmy() if isinstance(o, Czlowiek)), None)
            if znaleziony:
                self.gracz = znaleziony
            else:
                self.swiat.dodaj_log("Brak Człowieka po wczytaniu stanu.")
        except FileNotFoundError:
            self.swiat.dodaj_log(f"Brak pliku zapisu: {self.sciezka_zapisu}")
        self.odswiez_widok()

    def odswiez_widok(self):
        self.etykieta_tury.config(text=f"Tura: {self.swiat.tura}")

        for y in range(self.swiat.wysokosc):
            for x in range(self.swiat.szerokosc):
                org = self.swiat.pobierz_organizm((x, y))
                if org:
                    tlo, tekst = self.kolory_organizmow.get(type(org), ("#cfd8dc", "#000000"))
                    self.pola[y][x].config(text=org.znak(), bg=tlo, fg=tekst)
                else:
                    tlo, tekst = self.kolor_pustego_pola
                    self.pola[y][x].config(text=".", bg=tlo, fg=tekst)

        logi = self.swiat.pobierz_logi_i_wyczysc()
        if logi:
            self.pole_logow.config(state=tk.NORMAL)
            for wpis in logi:
                self.pole_logow.insert(tk.END, f"{wpis}\n")
            self.pole_logow.see(tk.END)
            self.pole_logow.config(state=tk.DISABLED)


def uruchom_aplikacje():
    root = tk.Tk()
    AplikacjaSwiata(root)
    root.mainloop()
