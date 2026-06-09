# umiejetnosci/calopalenie.py
class Calopalenie:
    def __init__(self, wlasciciel):
        self.wlasciciel = wlasciciel
        self.czy_aktywna = False
        self.czas_trwania = 0
        self.cooldown = 0

    def aktywuj(self) -> bool:
        if self.cooldown == 0 and not self.czy_aktywna:
            self.czy_aktywna = True
            self.czas_trwania = 5
            return True
        return False

    def aktualizuj_stan(self):
        if self.czy_aktywna:
            self.czas_trwania -= 1
            if self.czas_trwania == 0:
                self.czy_aktywna = False
                self.cooldown = 5
        elif self.cooldown > 0:
            self.cooldown -= 1

    def dzialanie(self, swiat):
        if not self.czy_aktywna:
            return
            
        sasiednie_pola = swiat.pobierz_sasiednie_pola(self.wlasciciel.polozenie)
        for pole in sasiednie_pola:
            org = swiat.pobierz_organizm(pole)
            if org:
                swiat.dodaj_log(f"Całopalenie niszczy {org.nazwa()} na polu {pole}!")
                swiat.usun_organizm(org)