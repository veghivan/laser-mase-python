import pyconio as con
import time
import logika
import fajlkezeles


def print_fejlec(profil: logika.Profil = None, palya_id: int = None, palya_nehezseg: str = None) -> None:
    """
    Megjelen?ti a j?t?k fejl?c?t, bele?rtve a verzi?sz?mot, a j?t?kos gamertagj?t ?s a p?lyainform?ci?kat,
    ha azok rendelkez?sre ?llnak. A fejl?c megjelen?t?se minden f?bb funkci? el?tt t?rt?nik.

    :param logika.Profil profil: A j?t?kos profilja, amely tartalmazza a gamertag-et. Alap?rtelmez?sben None.
    :param int palya_id: A p?lya azonos?t?ja. Alap?rtelmez?sben None.
    :param str palya_nehezseg: A p?lya neh?zs?gi szintje. Alap?rtelmez?sben None.
    :return: Nincs visszat?r?si ?rt?k.
    :rtype: None
    """
 
    con.clrscr()
    con.textcolor(con.Gray)
    con.gotoxy(0, 0)

    fejlec_szoveg = "Laser Maze V1.0 by PT9860"
    if profil is not None:
        fejlec_szoveg += f"\tProfil: {profil.gamertag}"

    if palya_id is not None:
        fejlec_szoveg += f"\tP?lya: {palya_id} | Neh?zs?g: {palya_nehezseg}"      

    print(fejlec_szoveg)
    con.textcolor(con.White)


def print_tabla_lezzerrel(tabla: logika.Tabla, laser_utvonalak) -> None:
    """
    Megjelen?ti a j?t?kt?bl?t a k?perny?n, bele?rtve a b?bukat ?s a l?zer ?tvonalait.
    A b?buk sz?nez?se azok ?llapot?t?l f?gg (pl. aktiv?lt rak?t?k z?lden jelennek meg).
    A t?bla bal oldali ?s fels? r?sz?n indexek seg?tik a t?j?koz?d?st.

    :param logika.Tabla tabla: A j?t?kt?bla objektuma.
    :param laser_utvonalak: A l?zer ?tvonalainak list?ja vagy egy?b reprezent?ci?ja.
    :return: Nincs visszat?r?si ?rt?k.
    :rtype: None
    """

    con.textcolor(con.White)

    # Fels? indexek (oszlopok)
    print("   ", end="")
    for oszlop in range(5):
        print(f" {oszlop} ", end="")
    print()

    # Fels? szeg?ly
    print("  +" + "---" * 5 + "+")

    for x in range(5):
        # Oldals? indexek (sorok)
        print(f"{x} |", end="")

        for y in range(5):
            piece = tabla.melyik_babu((x, y))
            con.textcolor(con.White)  # Alap?rtelmezett sz?n be?ll?t?sa

            if isinstance(piece, logika.SpaceRock):
                con.textcolor(con.White)
                print(" S ", end="")
            elif isinstance(piece, logika.Tukor):
                con.textcolor(con.Magenta)
                print(" T ", end="")
            elif isinstance(piece, logika.AteresztoTukor):
                con.textcolor(con.Green)
                print(" A ", end="")
            elif isinstance(piece, logika.Raketa):
                if piece.aktivalva:  
                    con.textcolor(con.LightGreen)
                else:
                    con.textcolor(con.Yellow)
                print(" R ", end="")
            elif any((x, y) in ut for ut in laser_utvonalak.values()):
                con.textcolor(con.Red)
                print(" L ", end="")
            else:
                con.textcolor(con.White)
                print(" * ", end="")

        # Jobb oldali szeg?ly
        con.textcolor(con.White)
        print("|")

    # Als? szeg?ly
    con.textcolor(con.White)
    print("  +" + "---" * 5 + "+")


def print_dicsoseglista() -> None:
    """
    A dics?s?glist?t jelen?ti meg, amely rangsorolja a j?t?kosokat a teljes?tm?ny?k alapj?n.
    Az els? h?rom helyezett kiemelt sz?nnel jelenik meg. Ha a lista nem tal?lhat?, hiba?zenet jelenik meg.

    :return: Nincs visszat?r?si ?rt?k.
    :rtype: None
    """

    try:
        with open('dicsoseglista.txt', 'r') as f:
            dicsoseglista = f.readlines()

        print("\nDics?s?glista:\n")
        for index, sor in enumerate(dicsoseglista, start=1):
            if index <= 3:  # Top 3 helyez?s kiemel?se
                con.textcolor(con.Yellow)
            else:
                con.textcolor(con.White)

            print(f"{index}. Helyezet:  {sor.strip()}")

        con.textcolor(con.White)  # Vissza?ll?tjuk az alap?rtelmezett sz?nt
    except FileNotFoundError:
        print("A dics?s?glista m?g nem l?tezik, vagy nem tal?lhat?.")


def print_raketak_info(raketak: list) -> None:
    """
    Megjelen?ti az ?sszes rak?ta inform?ci?it a j?t?k sor?n, bele?rtve azok poz?ci?j?t, t?jol?s?t ?s aktiv?l?si ?llapot?t.
    Ez seg?t a j?t?kosnak a strat?giai d?nt?sek meghozatal?ban.

    :param list raketak: A j?t?kban l?v? rak?t?k list?ja.
    :return: Nincs visszat?r?si ?rt?k.
    :rtype: None
    """

    print("\n")
    for index, raketa in enumerate(raketak, 1):
        aktivalva_szoveg = "Igen" if raketa.aktivalva else "Nem"
        print(f"Rak?ta_{index} Poz?ci?ja: {raketa.pozicio} | T?jol?s: {logika.IRANYOK[raketa.tajolas]:>7} | Aktiv?lva: {aktivalva_szoveg:>5}")
    print("\n")


def print_felhasznalhato_babuk(felhasznalhato_babuk: list) -> None:
    """
    A felhaszn?lhat? b?buk list?j?t jelen?ti meg, bele?rtve azok t?pus?t, poz?ci?j?t ?s t?jol?s?t.
    Ez seg?t a j?t?kosnak a t?bla megtervez?s?ben ?s a j?t?kstrat?gia kialak?t?s?ban.

    :param list felhasznalhato_babuk: A j?t?kban haszn?lhat? b?buk list?ja.
    :return: Nincs visszat?r?si ?rt?k.
    :rtype: None
    """

    print("Felhaszn?lhat? B?buk:")
    for index, tipus in enumerate(felhasznalhato_babuk):
        print(f"{index + 1:>5}) {tipus}")
    print("\n")


def jatek_futtatas(profil: logika.Profil, palya_fajlnev: str):
    """
    Egy j?t?kmenetet futtat megadott profil ?s p?lyaf?jl alapj?n. Bet?lti a p?ly?t, kezeli a j?t?kos interakci?it,
    ?s ellen?rzi a j?t?k v?g?llapot?t. Friss?ti a profil statisztik?it ?s a dics?s?glist?t sikeres teljes?t?s eset?n.
    A j?t?k addig tart, am?g a j?t?kos teljes?ti a p?ly?t vagy kil?p.

    :param logika.Profil profil: A j?t?kos profilja.
    :param str palya_fajlnev: A p?lyaf?jl neve.
    :return: Nincs visszat?r?si ?rt?k.
    :rtype: None
    """

    tabla, felhasznalhato_babuk, (palya_id, palya_nehezseg) = fajlkezeles.beolvas_palyat(palya_fajlnev)
    raketak = logika.get_raketak(tabla)
    kezdesi_ido = time.time()

    while True:
        jelenlegi_ido = time.time()
        print_fejlec(profil, palya_id, palya_nehezseg)

        lezer_ut = logika.lezer_utvonal(tabla)
        tabla = logika.raketa_aktivalas_deaktivallas(tabla, lezer_ut)
        
        print_tabla_lezzerrel(tabla, lezer_ut)
        print_raketak_info(raketak)
        print_felhasznalhato_babuk(felhasznalhato_babuk)

        if all(raketa.aktivalva for raketa in raketak):
            if logika.minden_babu_felhasznalva(tabla, felhasznalhato_babuk):
                eltelt_ido = int(jelenlegi_ido - kezdesi_ido)
                szerzett_pontszam = logika.NEHEZSEGEK[palya_nehezseg]

                # Friss?tj?k a teljes?tett p?lya adatait a profilban
                van_mar_ilyen_palya = profil.frissit_palya_eredmenyt(palya_id, palya_nehezseg, eltelt_ido)

                profil.frissit_osszertekeket()
                profil.mentes_frissites()
                fajlkezeles.dicsoseglista_keszitese_frissites()

                con.textcolor(con.Green)
                uzenet = "Sikeresen jav?tottad az id?det!" if van_mar_ilyen_palya else "Sikeresen teljes?tetted a p?ly?t!"
                print(f"\nGratul?lok! {uzenet} \nP?lya: {palya_id} \nEltelt id?: {eltelt_ido}mp\nSzerzett pontsz?m: {szerzett_pontszam}")

                con.textcolor(con.White)
                time.sleep(5)
                break
            else:
                con.textcolor(con.Red)
                print("Minden b?but fel kell haszn?lni a p?lya teljes?t?s?hez!")
                con.textcolor(con.White)
                time.sleep(5)
                continue

        tabla = logika.interakcio_a_babukkal(tabla, felhasznalhato_babuk)



def profil_menu(profil: logika.Profil):
    """
    Egy men?t jelen?t meg az adott profilhoz, ahol a j?t?kos v?laszthat a k?l?nb?z? opci?k k?z?tt, mint p?ld?ul
    ?j p?lya kezd?se, kor?bbi p?ly?k jav?t?sa, profil adatainak megtekint?se, vagy visszat?r?s a f?men?be.
    A men? dinamikusan v?ltozik a profil pontsz?m?t?l f?gg?en.

    :param logika.Profil profil: A j?t?kos profilja.
    :return: Nincs visszat?r?si ?rt?k.
    :rtype: None
    """

    while True:
        print_fejlec(profil)

        # Alapinform?ci?k megjelen?t?se
        con.gotoxy(10, 3)
        print(f"Profil: {profil.gamertag}")
        con.gotoxy(10, 5)
        print(f"?sszpontsz?m: {profil.osszpontszam}")

        # Csak a j?t?k ind?t?s lehet?s?ge, ha m?g nincsenek pontok
        if profil.osszpontszam == 0:
            con.textcolor(con.White)
            con.gotoxy(10, 9)
            print("1. J?t?k kezd?se")

            con.textcolor(con.Red)
            con.gotoxy(10, 13)
            print("2. Vissza a f?men?be")
            con.textcolor(con.White)

            key = con.getch()

            if key == '1':
                palya_fajlnev = logika.kovetkezo_palya(profil)
                if palya_fajlnev:
                    jatek_futtatas(profil, palya_fajlnev)
                    continue
                else:
                    print("Minden p?lya m?r teljes?tve.")
                    continue
            elif key == '2':
                return
        else:
            # A teljes men? megjelen?t?se, ha m?r vannak pontok
            con.textcolor(con.White)
            con.gotoxy(10, 9)
            print("1. K?vetkez? p?lya kipr?b?l?sa")
            con.gotoxy(10, 11)
            print("2. Kor?bbi p?ly?k jav?t?sa")
            con.gotoxy(10, 13)
            print("3. Profil adatainak megjelen?t?se")

            con.textcolor(con.Red)
            con.gotoxy(10, 17)
            print("4. Vissza a f?men?be")
            con.textcolor(con.White)

            key = con.getch()
                       
            if key == '1':
                palya_fajlnev = logika.kovetkezo_palya(profil)
                if palya_fajlnev:
                    jatek_futtatas(profil, palya_fajlnev)
                    continue
                else:
                    print("Minden p?lya m?r teljes?tve.")
                    continue

            elif key == '2':
                palya_fajlnev = logika.korabbi_palyak_kivalasztasa(profil)
                if palya_fajlnev:
                    if jatek_futtatas(profil, palya_fajlnev):
                        # Friss?tj?k a profil adatait, ha sz?ks?ges
                        continue
                continue  
            
            elif key == '3':
                print_fejlec(profil)
                print("\n")
                print(profil)
                print("Visszat?r?shez nyomdd meg a 0-?t!")
                visszateres = con.getch()
                if visszateres == '0':
                    continue

            elif key == '4':
                break


def main():
    """
    A f?men?t ?s a program f? v?grehajt?si ciklus?t tartalmazza. Itt v?laszthat a felhaszn?l? az ?j profil l?trehoz?sa,
    megl?v? profil bet?lt?se, dics?s?glista megtekint?se vagy a programb?l val? kil?p?s k?z?tt.
    Az egyes men?pontok almen?ket ?s tov?bbi interakci?kat nyitnak meg.

    :return: Nincs visszat?r?si ?rt?k.
    :rtype: None
    """

    while True:
        print_fejlec()
        con.textcolor(con.White)
        con.gotoxy(10, 5)
        print("1. ?j profil l?trehoz?sa")
        con.gotoxy(10, 7)
        print("2. Profil bet?lt?se")
        
        con.textcolor(con.Yellow)
        con.gotoxy(10, 9)
        print("3. Dics?s?glista")
        
        con.textcolor(con.Red)
        con.gotoxy(10, 13)
        print("4. Kil?p?s")
        con.textcolor(con.White)

        key = con.getch()

        if key == '1':
            while True:
                print_fejlec()
                con.gotoxy(10, 5)
                con.textcolor(con.White)
                gamertag = input("Add meg az ?j profil nev?t (vagy ?rd be, hogy 'vissza' a f?men?be l?p?shez): ")

                if gamertag.lower() == 'vissza':
                    break  # Visszat?r a f?men?be

                if gamertag in logika.Profil.profilok_listazasa():
                    print("Ez a gamertag m?r l?tezik. K?rlek, v?lassz egy m?sikat.")
                    time.sleep(2)
                    continue

                profil = logika.Profil(gamertag)
                profil_menu(profil)

        elif key == '2':
            profil = logika.Profil.menus_betoltes()
            if profil:
                profil_menu(profil)

        elif key == '3':
            print_fejlec()
            print_dicsoseglista()
            visszalepes = input("\nVisszal?p?shez nyomdd meg az entert!")
            if visszalepes == '':
                continue

        elif key == '4':
            break  # Kil?p?s a programb?l

    return 0



    

main()
