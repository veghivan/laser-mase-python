import os

IRANYOK = ["Észak", "Kelet", "Dél", "Nyugat"]
NEHEZSEGEK = {
    "Könnyű":  120,
    "Közepes": 240,
    "Nehéz": 360,
    "Géniusz": 600
}
#ezek nem random globális listák 	(◔_◔)


#Profil
class Profil:
    """
    A Profil osztály egy játékos profilját reprezentálja, beleértve a gamertag-et, a teljesített pályákat,
    az összpontszámot és az összesen eltöltött időt. Ez az osztály kezeli a profil adatainak mentését és betöltését.

    :ivar gamertag: A játékos egyedi felhasználóneve.
    :ivar teljesitett_palyak: A teljesített pályák listája.
    :ivar osszpontszam: A játékos összpontszáma.
    :ivar osszido: A játékban eltöltött összes idő másodpercben.
    """
    
    def __init__(self, gamertag: str) -> None:
        self.gamertag = gamertag
        self.teljesitett_palyak = []
        self.osszpontszam = 0
        self.osszido = 0


    def __str__(self) -> str:
        profil_info = f"Gamertag: {self.gamertag}\n"
        profil_info += f"Összpontszám: {self.osszpontszam}\n"
        profil_info += f"Összesen eltöltött idő: {self.osszido} másodperc\n\n"
        profil_info += "Teljesített pályák:\n"
        for palya in self.teljesitett_palyak:
            profil_info += f"  - Pálya ID: {palya.id}, Nehézség: {palya.nehezseg}, Idő: {palya.ido} másodperc, Pontok: {NEHEZSEGEK[palya.nehezseg]}\n"
        
        return profil_info


    def frissit_palya_eredmenyt(self, palya_id: int, palya_nehezseg: str, uj_ido: int) -> bool:
        """
        Frissíti a megadott pálya eredményét a profilban. Hozzáadja a pályát, ha még nem szerepel,
        vagy frissíti az időt, ha javulás történt.

        :param palya_id: A pálya azonosítója.
        :param palya_nehezseg: A pálya nehézségi szintje.
        :param uj_ido: Az új idő, amit a játékos elérte a pályán.
        :return: Igaz, ha frissítés történt, hamis, ha nem.
        :rtype: bool
        """
        meglevo_palya = next((palya for palya in self.teljesitett_palyak if palya.id == palya_id), None)
        if meglevo_palya:
            if uj_ido < meglevo_palya.ido:
                meglevo_palya.ido = uj_ido

                return True  # Jelzi, hogy már volt ilyen pálya és frissítettük az időt
        else:
            uj_palya = TeljesitettPalya(palya_id, palya_nehezseg, uj_ido)
            self.teljesitett_palyak.append(uj_palya)

            return False  # Jelzi, hogy új pálya került hozzáadásra
        
        return False  # Ha nem történt frissítés

    
    def frissit_osszertekeket(self) -> None:
        """
        Frissíti a profil összértékeit, beleértve az összpontszámot és az összesen eltöltött időt. 
        Összegzi a teljesített pályákhoz tartozó időket és pontszámokat, majd frissíti a profil összidejét és összpontszámát.

        :return: Nincs visszatérési érték.
        :rtype: None
        """
        self.osszido = sum(palya.ido for palya in self.teljesitett_palyak)
        self.osszpontszam = sum(NEHEZSEGEK[palya.nehezseg] for palya in self.teljesitett_palyak)


    def mentes_frissites(self) -> None:
        """
        Mentésre frissíti a profil adatait egy fájlba. A profil információit tartalmazó fájlt
        a profil gamertagje alapján hozza létre vagy frissíti a 'profilok' könyvtárban.

        :return: Nincs visszatérési érték.
        :rtype: None
        """
        with open(f'profilok/{self.gamertag}.txt', 'w') as f:
            f.write(str(self))


    @classmethod
    def profilok_listazasa(cls) -> list:
        """
        Listázza az összes elérhető profilnevet a 'profilok' mappából. Keresi az összes .txt fájlt a könyvtárban,
        és visszaadja a fájlok neveit profilnevekként (kiterjesztés nélkül).

        :return: A meglévő profilnevek listája.
        :rtype: list
        """
        profil_fajlok = [f for f in os.listdir('profilok') if f.endswith('.txt')]
        return [f.replace('.txt', '') for f in profil_fajlok]

    @classmethod
    def betoltes_fajlnev_alapjan(cls, fajlnev: str) -> "Profil":
        """
        Betölti a megadott fájlnév alapján a profil adatait. Olvassa a fájlt és létrehoz egy Profil példányt
        a fájlban található adatok alapján.

        :param fajlnev: A betöltendő profil fájlneve.
        :return: A betöltött profil példánya, vagy None, ha a fájl nem található.
        :rtype: Profil or None
        """
        try:
            with open(f'profilok/{fajlnev}', 'r') as file:
                profil_adatok = file.read().splitlines()
                gamertag = profil_adatok[0].split(": ")[1]
                osszpontszam = int(profil_adatok[1].split(": ")[1])
                osszido = int(profil_adatok[2].split(": ")[1].split()[0])
                teljesitett_palyak_adatok = profil_adatok[4:]
                teljesitett_palyak = []
                for sor in teljesitett_palyak_adatok:
                    if sor.startswith("  - Pálya ID:"):
                        palya_adatok = sor.split(", ")
                        palya_id = palya_adatok[0].split(": ")[1]
                        palya_nehezseg = palya_adatok[1].split(": ")[1]
                        palya_ido = int(palya_adatok[2].split(": ")[1].split()[0])
                        teljesitett_palyak.append(TeljesitettPalya(palya_id, palya_nehezseg, palya_ido))
                profil = cls(gamertag)
                profil.osszpontszam = osszpontszam
                profil.osszido = osszido
                profil.teljesitett_palyak = teljesitett_palyak

                return profil
        except FileNotFoundError:
            print(f"A(z) {fajlnev} profil nem található.")

            return None
    

    @classmethod
    def menus_betoltes(cls) -> "Profil":
        """
        Interaktív menü a profilok közötti választáshoz. Lehetővé teszi a játékosnak, hogy kiválassza
        a betölteni kívánt profilt a meglévők közül. A felhasználó a profilok listájából választhat.

        :return: A kiválasztott profil példánya, vagy None, ha nincs kiválasztott profil.
        :rtype: Profil or None
        """
        profilok = cls.profilok_listazasa()
        if not profilok:
            print("\nNincsenek mentett profilok.")

            return None
        
        print("\nElérhető profilok:")
        while True:

            for index, profil_nev in enumerate(profilok):
                print(f"{index + 1}. {profil_nev}")

            try:
                valasztas = int(input("\nVálassz egy profilt a számával (pl. 1, 2, ...): ")) - 1
                if 0 <= valasztas < len(profilok):
                    kivalasztott_fajlnev = profilok[valasztas] + ".txt"

                    return cls.betoltes_fajlnev_alapjan(kivalasztott_fajlnev)
                
                else:
                    print("Érvénytelen választás. Kérlek, adj meg egy létező profil sorszámát.")
            except ValueError:
                print("Kérlek, adj meg egy érvényes számot.")



#Bábuk
class Babu:
    """
    A Babu osztály egy általános bábut reprezentál a játékban. Tartalmazza a bábu típusát, pozícióját és tájolását.
    Alapvető műveleteket biztosít, mint például a bábu forgatása és mozgatása.

    :ivar tipus: A bábu típusa.
    :ivar pozicio: A bábu pozíciója a táblán (x, y koordináták).
    :ivar tajolas: A bábu tájolása (0: Észak, 1: Kelet, 2: Dél, 3: Nyugat).
    """
    
    def __init__(self, tipus, pozicio = None, tajolas = 0):

        self.tipus = tipus
        self.pozicio = pozicio #ez egy tuple(x, y)!!!!!!!!!!!
        self.tajolas = tajolas 


    def __str__(self) -> str:
        """
        Szöveges reprezentációt ad vissza a báburól, tartalmazza a típusát, pozícióját és tájolását.

        :return: A bábu szöveges reprezentációja.
        :rtype: str
        """
        tajolas_szoveg =  IRANYOK[self.tajolas]
        pozicio_szoveg = "Nincs" if self.pozicio is None else str(self.pozicio)

        return f"{self.tipus:>15} | Pozició: {pozicio_szoveg:>8} | Tájolás: {tajolas_szoveg:>7}"


    def forgatas(self, merre: str) -> None:
        """
        Forgatja a bábut a megadott irányba.

        :param merre: A forgatás iránya ('j' a jobbra, 'b' a balra forgatáshoz).
        :type merre: str
        """
        if merre == "j":
            self.tajolas = (self.tajolas + 1) % 4
        if merre == "b":
            self.tajolas = (self.tajolas - 1) % 4


    def mozgatas(self, uj_pozicio: tuple):
        """
        Mozgatja a bábut az új pozícióba.

        :param uj_pozicio: Az új pozíció, ahová a bábut mozgatni kell.
        :type uj_pozicio: tuple
        """
        self.pozicio = uj_pozicio


class Ures(Babu):
    """
    Az Ures osztály egy speciális típusú bábut reprezentál a játékban, amely üres mezőt jelképez.
    Nincs különleges tulajdonsága vagy viselkedése; alapvetően egy placeholder a táblán.

    :ivar pozicio: A bábu pozíciója a táblán (x, y koordináták).
    """
    
    def __init__(self, pozicio):

        super().__init__("Üres", pozicio, None)


class SpaceRock(Babu):
    """
    A SpaceRock osztály egy akadályt jelentő bábut reprezentál. Ez a bábu blokkolja a lézer útját,
    és nem mozgatható vagy forgatható a játék során.

    :ivar tipus: A bábu típusa, ebben az esetben "SpaceRock".
    :ivar pozicio: A bábu pozíciója a táblán (x, y koordináták).
    :ivar tajolas: A bábu tájolása, ami ebben az esetben nem releváns, mivel a SpaceRock nem forgatható.
    """

    def __init__(self, tipus, pozicio=None, tajolas=0):
        super().__init__("SpaceRock", pozicio, tajolas)



class Tukor(Babu):
    """
    A Tukor osztály egy tükröt jelent, amely megváltoztatja a lézer irányát.
    A tükör tájolásától függően a lézer iránya változik meg érkezésekor.

    :ivar tipus: A bábu típusa, ebben az esetben "Tükör".
    :ivar pozicio: A tükör pozíciója a táblán.
    :ivar tajolas: A tükör tájolása.
    """

    def __init__(self, tipus, pozicio, tajolas=0):

        super().__init__("Tükör", pozicio, tajolas)


    def tukrozes(self, beerkezo_irany):
        """
        Kiszámítja a lézer új irányát a tükörre érkezéskor, attól függően, hogy milyen tájolású a tükör.

        :param beerkezo_irany: A lézer érkezési iránya.
        :return: A lézer új iránya a tükörrel való interakció után.
        """

        if self.tajolas % 2 == 0:

            if beerkezo_irany % 2 == 0:
                
                return  (beerkezo_irany - 1) % 4    

            else:

                return (beerkezo_irany + 1) % 4  

        else:    
            if beerkezo_irany % 2 != 0:
                
                return  (beerkezo_irany - 1) % 4    

            else:

                return (beerkezo_irany + 1) % 4 
       

class AteresztoTukor(Babu):
    """
    Az AteresztoTukor osztály egy speciális típusú tükröt reprezentál, amely képes a lézert átereszteni és
    egyidejűleg tükrözni is. Ezáltal két különböző irányba is továbbítja a lézert.

    :ivar tipus: A bábu típusa, ebben az esetben "ÁteresztőTükör".
    :ivar pozicio: Az ÁteresztőTükör pozíciója a táblán.
    :ivar tajolas: Az ÁteresztőTükör tájolása.
    """

    def __init__(self, tipus, pozicio=None, tajolas=0):
        super().__init__("ÁteresztőTükör", pozicio, tajolas)

    
    def tukrozes_ateresztes(self, beerkezo_irany):
        """
        Kiszámítja a lézer új irányát, és meghatározza az áteresztett lézer irányát is.

        :param beerkezo_irany: A lézer érkezési iránya.
        :return: A lézer új iránya és az áteresztett lézer iránya.
        """

        if self.tajolas % 2 == 0:

            if beerkezo_irany % 2 == 0:
                
                return  (beerkezo_irany - 1) % 4, beerkezo_irany    

            else:

                return (beerkezo_irany + 1) % 4, beerkezo_irany

        else:    
            if beerkezo_irany % 2 != 0:
                
                return  (beerkezo_irany - 1) % 4, beerkezo_irany    

            else:

                return (beerkezo_irany + 1) % 4, beerkezo_irany


class Raketa(Babu):
    """
    A Raketa osztály egy célbábut reprezentál, amelyet a lézerrel kell aktiválni a játék során.
    A rakéta aktiválása a játék egyik fő célja.

    :ivar tipus: A bábu típusa, ebben az esetben "Rakéta".
    :ivar pozicio: A Rakéta pozíciója a táblán.
    :ivar tajolas: A Rakéta tájolása.
    :ivar aktivalva: Jelzi, hogy a rakéta aktiválva van-e.
    """

    def __init__(self, tipus, pozicio=None, tajolas=0):
        super().__init__("Rakéta", pozicio, tajolas)
        self.aktivalva = False


class Tabla:
    """
    A Tabla osztály a játéktáblát reprezentálja, amely egy 5x5-ös mátrixot tartalmaz. Kezeli a bábuk elhelyezését,
    mozgatását és eltávolítását a tábláról, valamint a bábuk lekérdezését a tábláról.

    :ivar matrix: A tábla mátrixa, amely a bábukat tartalmazza.
    :type matrix: list[list[Babu]]
    """

    def __init__(self) -> None:

        self.matrix = [[Ures((x, y)) for y in range(5)] for x in range(5)]


    def babu_elhelyez(self, babu: "Babu", pozicio: tuple) -> None:
        """
        Elhelyez egy bábut a megadott pozícióban a táblán.

        :param babu: Az elhelyezendő bábu.
        :param pozicio: A bábu pozíciója a táblán (x, y koordináták).
        :type babu: Babu
        :type pozicio: tuple
        """
        x, y = pozicio
        self.matrix[x][y] = babu


    def babu_mozgatas(self, honnan: tuple, hova: tuple) -> None:
        """
        Mozgat egy bábut egyik pozícióból a másikba a táblán.

        :param honnan: A bábu jelenlegi pozíciója.
        :param hova: A cél pozíció, ahová a bábut mozgatni kell.
        :type honnan: tuple
        :type hova: tuple
        """
        jatekbabu = self.melyik_babu(honnan)

        if jatekbabu is not None and isinstance(jatekbabu, Babu):
            self.babu_elhelyez(jatekbabu, hova)
            self.babu_torol(honnan)
            jatekbabu.mozgatas(hova)


    def babu_torol(self, pozicio: tuple) -> None:
        """
        Eltávolít egy bábut a megadott pozícióból a táblán, helyére üres bábut helyez.

        :param pozicio: A bábu pozíciója, amit eltávolítani kell.
        :type pozicio: tuple
        """
        x, y = pozicio
        self.matrix[x][y] = Ures((x, y))


    def melyik_babu(self, pozicio: tuple) -> "Babu":
        """
        Lekérdezi, hogy milyen bábu található a megadott pozícióban a táblán.

        :param pozicio: A lekérdezni kívánt pozíció a táblán.
        :type pozicio: tuple
        :return: A pozícióban található bábu.
        :rtype: Babu
        """
        x, y = pozicio
        
        return self.matrix[x][y]


class TeljesitettPalya:
    """
    A TeljesitettPalya osztály egy teljesített pálya adatait tárolja, beleértve a pálya azonosítóját, nehézségi szintjét,
    és az eltelt időt. Ez az osztály a játékos profiljában kerül felhasználásra a teljesített pályák nyilvántartásához.

    :ivar id: A pálya azonosítója.
    :ivar nehezseg: A pálya nehézségi szintje.
    :ivar ido: A pálya teljesítéséhez szükséges idő másodpercben.
    :type id: int
    :type nehezseg: str
    :type ido: int
    """

    def __init__(self, id, nehezseg, eltelt_ido) -> None:

        self.id = id
        self.nehezseg = nehezseg
        self.ido = eltelt_ido



#innen jönnek a függvények

def irany_inverter(lezer_irany: int) -> int:
    """
    Megfordítja a megadott lézer irányát.

    :param lezer_irany: A lézer iránya (0, 1, 2 vagy 3).
    :type lezer_irany: int
    :return: Az irány megfordítva (0, 1, 2 vagy 3).
    :rtype: int
    """
    return (lezer_irany + 2) % 4


def lezer_kovetkezo_szamitas(pozicio: tuple, irany: int) -> tuple:
    """
    Kiszámítja a következő pozíciót a táblán a megadott lézer irány alapján.

    :param pozicio: A kiinduló pozíció (x, y koordináták).
    :param irany: A lézer iránya (0, 1, 2 vagy 3).
    :type pozicio: tuple
    :type irany: int
    :return: Az új pozíció (x, y koordináták).
    :rtype: tuple
    """
    x, y = pozicio

    if irany == 0:

        return (x - 1, y)
    
    elif irany == 1:

        return (x, y + 1)
    
    elif irany == 2:

        return (x + 1, y)
    
    elif irany == 3:

        return (x, y - 1)


def lezer_irany_kiszamitas(jelenlegi_pozicio: tuple, elozo_pozicio: tuple) -> int or None:
    """
    Kiszámítja a lézer irányát két adott pozíció alapján a táblán.

    :param jelenlegi_pozicio: A jelenlegi pozíció (x, y koordináták).
    :param elozo_pozicio: Az előző pozíció (x, y koordináták).
    :type jelenlegi_pozicio: tuple
    :type elozo_pozicio: tuple
    :return: A lézer iránya (0, 1, 2 vagy 3) vagy None, ha az irány nem határozható meg.
    :rtype: int or None
    """
    jelenlegi_x, jelenlegi_y = jelenlegi_pozicio
    elozo_x, elozo_y = elozo_pozicio

    if jelenlegi_x > elozo_x:
        return 2  # Dél
    
    elif jelenlegi_x < elozo_x:
        return 0  # Észak
    
    elif jelenlegi_y > elozo_y:
        return 1  # Kelet
    
    elif jelenlegi_y < elozo_y:
        return 3  # Nyugat
    
    return None



def lezer_utvonal(tabla: "Tabla", kezdo_pozicio = (1, 0), kezdo_irany = 1) -> dict:
    """
    Kiszámítja a lézer útvonalát a táblán a kezdő pozíció és irány alapján.

    :param tabla: A tábla objektum.
    :param kezdo_pozicio: A kezdő pozíció (x, y koordináták) (alapértelmezett: (1, 0)).
    :param kezdo_irany: A kezdő lézer iránya (0, 1, 2 vagy 3) (alapértelmezett: 1).
    :type tabla: Tabla
    :type kezdo_pozicio: tuple
    :type kezdo_irany: int
    :return: Az útvonalak (fo_utvonal és ateresztett_utvonal) a pozíciók listájaként.
    :rtype: dict
    """
    x, y = kezdo_pozicio
    lezer_irany = kezdo_irany
    utvonalak = {"fo_utvonal": [], "ateresztett_utvonal": []}

    while 0 <= x < 5 and 0 <= y < 5:
        utvonalak["fo_utvonal"].append((x, y))
        jatekbabu = tabla.melyik_babu((x, y))

        if isinstance(jatekbabu, SpaceRock):
            utvonalak["fo_utvonal"].append((x, y))
            break

        if isinstance(jatekbabu, Raketa):
            utvonalak["fo_utvonal"].append((x, y))
            if irany_inverter(lezer_irany) == jatekbabu.tajolas:
                jatekbabu.aktivalva = True
            break

        if isinstance(jatekbabu, Tukor):
            lezer_irany = jatekbabu.tukrozes(irany_inverter(lezer_irany))

        elif isinstance(jatekbabu, AteresztoTukor):
            tukrozott_irany, ateresztett_irany = jatekbabu.tukrozes_ateresztes(irany_inverter(lezer_irany))

            # Az áteresztett lézer útvonalának kiszámítása
            ateresztett_x, ateresztett_y = x, y
            while 0 <= ateresztett_x < 5 and 0 <= ateresztett_y < 5:
                ateresztett_jatekbabu = tabla.melyik_babu((ateresztett_x, ateresztett_y))

                if isinstance(ateresztett_jatekbabu, SpaceRock):
                    utvonalak["ateresztett_utvonal"].append((ateresztett_x, ateresztett_y))
                    break

                if isinstance(ateresztett_jatekbabu, Raketa):
                    utvonalak["ateresztett_utvonal"].append((ateresztett_x, ateresztett_y))
                    if ateresztett_irany == ateresztett_jatekbabu.tajolas:
                        ateresztett_jatekbabu.aktivalva = True
                    break

                if isinstance(ateresztett_jatekbabu, Tukor):
                    ateresztett_irany = ateresztett_jatekbabu.tukrozes(irany_inverter(ateresztett_irany))

                utvonalak["ateresztett_utvonal"].append((ateresztett_x, ateresztett_y))
                ateresztett_x, ateresztett_y = lezer_kovetkezo_szamitas((ateresztett_x, ateresztett_y), irany_inverter(ateresztett_irany))

            lezer_irany = tukrozott_irany

        x, y = lezer_kovetkezo_szamitas((x, y), lezer_irany)

    return utvonalak


#Rakéta függvény kiegészítés

def get_raketak(tabla: Tabla) -> Raketa:
    """
    Visszaadja az összes rakétát a tábláról egy listában.

    :param tabla: A tábla objektum.
    :type tabla: Tabla
    :return: A rakéták listája.
    :rtype: list[Raketa]
    """
    raketak = []
    for x in range(5):
        for y in range(5):
            piece = tabla.melyik_babu((x, y))
            if isinstance(piece, Raketa):
                raketak.append(piece)
    return raketak


def raketa_aktivalas_deaktivallas(tabla, lezer_utvonalak) -> Tabla:
    """
    Frissíti az összes rakéta aktiválási állapotát a táblán a lézer útvonalak alapján.

    :param tabla: A tábla objektum.
    :param lezer_utvonalak: A lézer útvonalak eredménye.
    :type tabla: Tabla
    :type lezer_utvonalak: dict
    :return: A frissített tábla objektum.
    :rtype: Tabla
    """
    # Minden rakéta aktiválási állapotának frissítése.
    for raketa in get_raketak(tabla):
        raketa_aktivalva = False  # Alapértelmezetten feltételezzük, hogy a rakéta nem aktiválódik.

        # Ellenőrizzük, hogy a rakéta benne van-e a fő útvonalban.
        if raketa.pozicio in lezer_utvonalak['fo_utvonal']:
            index = lezer_utvonalak['fo_utvonal'].index(raketa.pozicio)
            if index > 0:
                elozo_pozicio = lezer_utvonalak['fo_utvonal'][index - 1]
                lezer_irany = lezer_irany_kiszamitas(raketa.pozicio, elozo_pozicio)
                if irany_inverter(lezer_irany) == raketa.tajolas:
                    raketa_aktivalva = True

        # Hasonló logika az áteresztett útvonal esetén, ha van ilyen.
        if 'ateresztett_utvonal' in lezer_utvonalak:
            if raketa.pozicio in lezer_utvonalak['ateresztett_utvonal']:
                index = lezer_utvonalak['ateresztett_utvonal'].index(raketa.pozicio)
                if index > 0:
                    elozo_pozicio = lezer_utvonalak['ateresztett_utvonal'][index - 1]
                    lezer_irany = lezer_irany_kiszamitas(raketa.pozicio, elozo_pozicio)
                    if irany_inverter(lezer_irany) == raketa.tajolas:
                        raketa_aktivalva = True

        # Frissítjük a rakéta aktiválási állapotát.
        raketa.aktivalva = raketa_aktivalva

    return tabla


#Babus függvények

def minden_babu_felhasznalva(tabla: Tabla, felhasznalhato_babuk: list) -> bool:
    """
    Ellenőrzi, hogy minden felhasználható bábu el lett-e helyezve a táblán.

    :param tabla: A tábla objektum.
    :param felhasznalhato_babuk: A felhasználható bábuk listája.
    :type tabla: Tabla
    :type felhasznalhato_babuk: list
    :return: True, ha minden bábu el van helyezve, különben False.
    :rtype: bool
    """
    for babu in felhasznalhato_babuk:
        if babu.pozicio == (None, None):
            return False
    return True


def interakcio_a_babukkal(tabla: Tabla, felhasznalhato_babuk: list) -> Tabla:
    """
    Kezeli a játékos interakcióját a felhasználható bábukkal a táblán.

    :param tabla: A tábla objektum.
    :param felhasznalhato_babuk: A felhasználható bábuk listája.
    :type tabla: Tabla
    :type felhasznalhato_babuk: list
    :return: A frissített tábla objektum.
    :rtype: Tabla
    """
    # Bábu kiválasztása
    while True:
        try:
            valasztas = int(input("Add meg a bábu sorszámát: ")) - 1
            if valasztas < 0 or valasztas >= len(felhasznalhato_babuk):
                raise ValueError("Érvénytelen bábu sorszám.")
            break
        except ValueError as e:
            print(f"Hiba: {e}")

    kivalasztott_babu = felhasznalhato_babuk[valasztas]

    # Elhelyezés, ha a bábu még nincs a táblán
    if kivalasztott_babu.pozicio == (None, None):
        while True:
            try:
                uj_x, uj_y = map(int, input("Add meg a bábu új koordinátáit sor;oszlop formátumban: ").split(";"))
                uj_pozicio = (uj_x, uj_y)
                if isinstance(tabla.melyik_babu(uj_pozicio), Ures):
                    kivalasztott_babu.mozgatas(uj_pozicio)
                    break
                else:
                    print("Ez a pozíció már foglalt!")
            except ValueError:
                print("Hibás koordináta. Kérlek, add meg újra a koordinátákat.")

        while True:
            tajolas_input = input("Add meg a bábu tájolását: ").strip().lower()
            tajolas = None
            for irany in IRANYOK:
                if irany.lower() == tajolas_input:
                    tajolas = irany
                    break

            if tajolas is not None:
                kivalasztott_babu.tajolas = IRANYOK.index(tajolas)
                break
            else:
                print("Érvénytelen tájolás.")

        tabla.babu_elhelyez(kivalasztott_babu, uj_pozicio)
    else:
        # Mozgatás vagy forgatás, ha a bábu már a táblán van
        while True:
            akcio = input("Válassz egy műveletet (mozgat/forgat): ").lower()
            if akcio in ["mozgat", "forgat"]:
                break
            else:
                print("Érvénytelen művelet. Kérlek, válassz 'mozgat' vagy 'forgat' közül.")

        if akcio == "mozgat":
            while True:
                try:
                    uj_x, uj_y = map(int, input("Add meg a bábu új koordinátáit sor;oszlop formátumban: ").split(";"))
                    uj_pozicio = (uj_x, uj_y)
                    if isinstance(tabla.melyik_babu(uj_pozicio), Ures):
                        tabla.babu_mozgatas(kivalasztott_babu.pozicio, uj_pozicio)
                        break
                    else:
                        print("Ez a pozíció már foglalt!")
                except ValueError:
                    print("Hibás koordináta. Kérlek, add meg újra a koordinátákat.")
                    
        elif akcio == "forgat":
            while True:
                merre = input("Add meg a forgatás irányát (j/b): ").lower()
                if merre in ["j", "b"]:
                    kivalasztott_babu.forgatas(merre)
                    break
                else:
                    print("Érvénytelen irány. Kérlek, válassz 'j' (jobbra) vagy 'b' (balra) közül.")

    return tabla


#Profil függvények

def kovetkezo_palya(profil: Profil) -> None or str:
    """
    Kiválasztja a következő játszandó pályát a játékos profilja alapján.

    :param profil: A játékos profilja.
    :type profil: Profil
    :return: A következő pálya elérési útvonala vagy None, ha minden pálya már teljesítve van.
    :rtype: str or None
    """
    if not profil.teljesitett_palyak:

        return "palyak/palya1.txt"
    
    utolso_teljesitett_palya_id = max(int(palya.id) for palya in profil.teljesitett_palyak)
    if utolso_teljesitett_palya_id < 20:
        kovetkezo_palya_szam = utolso_teljesitett_palya_id + 1

        return f"palyak/palya{kovetkezo_palya_szam}.txt"
    
    return None  # Minden pálya teljesítve


def korabbi_palyak_kivalasztasa(profil: Profil) -> None or str:
    """
    Lehetővé teszi a játékos számára, hogy korábban már teljesített pályákat válasszon újrajátszásra.

    :param profil: A játékos profilja.
    :type profil: Profil
    :return: A kiválasztott pálya elérési útvonala vagy None, ha nincsenek teljesített pályák.
    :rtype: str or None
    """
    if not profil.teljesitett_palyak:
        print("Még nincs teljesített pálya.")
        return None

    print("\n\nTeljesített pályák:")
    for index, palya in enumerate(profil.teljesitett_palyak, start=1):
        print(f"{index}. Pálya: {palya.id}, Eltelt idő: {palya.ido}mp")

    valasztas = int(input("\nVálassz egy pályát a javításhoz (0 a visszalépéshez): "))
    if valasztas == 0 or valasztas > len(profil.teljesitett_palyak):

        return None

    kivalasztott_palya = profil.teljesitett_palyak[valasztas - 1]

    return f"palyak/palya{kivalasztott_palya.id}.txt"

