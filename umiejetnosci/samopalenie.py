class Calopalenie:
    def __init__(self, wlasciciel):
        self.__wlasciciel = wlasciciel
        self.__czy_aktywna = False
        self.__czas_trwania = 0
        self.__cooldown = 0

    def aktywuj(self) -> bool:
        if self.__cooldown == 0 and not self.__czy_aktywna:
            self.__czy_aktywna = True
            self.__czas_trwania = 5
            return True
        return False

    def aktualizuj_stan(self):
        if self.__czy_aktywna:
            self.__czas_trwania -= 1
            if self.__czas_trwania == 0:
                self.__czy_aktywna = False
                self.__cooldown = 5
        elif self.__cooldown > 0:
            self.__cooldown -= 1

    def stan(self) -> dict:
        return {
            "czy_aktywna": self.__czy_aktywna,
            "czas_trwania": self.__czas_trwania,
            "cooldown": self.__cooldown,
        }

    def wczytaj_stan(self, dane: dict):
        self.__czy_aktywna = bool(dane.get("czy_aktywna", False))
        self.__czas_trwania = int(dane.get("czas_trwania", 0))
        self.__cooldown = int(dane.get("cooldown", 0))

    def dzialanie(self, swiat):
        if not self.__czy_aktywna:
            return
            
        sasiednie_pola = swiat.pobierz_sasiednie_pola(self.__wlasciciel.polozenie)
        for pole in sasiednie_pola:
            org = swiat.pobierz_organizm(pole)
            if org:
                swiat.dodaj_log(f"Całopalenie niszczy {org.nazwa()} na polu {pole}!")
                swiat.usun_organizm(org)