from organizmy.bazowe import Zwierze


class CyberOwca(Zwierze):
    def __init__(self, swiat):
        super().__init__(10, 4, swiat)

    def znak(self):
        return "C"

    def czy_odporny_na_barszcz(self):
        return True

    def akcja(self):
        from organizmy.rosliny import BarszczSosnowskiego

        barszcze = [
            organizm for organizm in self.swiat.pobierz_organizmy()
            if isinstance(organizm, BarszczSosnowskiego) and organizm.zyje
        ]

        if not barszcze:
            super().akcja()
            return

        cel = min(
            barszcze,
            key=lambda barszcz: abs(barszcz.polozenie[0] - self.polozenie[0]) + abs(
                barszcz.polozenie[1] - self.polozenie[1]
            ),
        )

        dx = max(-1, min(1, cel.polozenie[0] - self.polozenie[0]))
        dy = max(-1, min(1, cel.polozenie[1] - self.polozenie[1]))
        nowe_pole = (self.polozenie[0] + dx, self.polozenie[1] + dy)

        if nowe_pole != self.polozenie:
            self.przemiesc_sie_lub_walcz(nowe_pole)

