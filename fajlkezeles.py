import logika
import os

#Pálya beolvasás
def beolvas_palyat(fajlnev):
    """
    Beolvassa és feldolgozza a megadott fájlban található pálya adatait. Létrehozza a pálya tábláját,
    és betölti a rajta található bábukat a fájlban megadott konfiguráció alapján.

    :param fajlnev: A beolvasandó pálya fájljának neve.
    :type fajlnev: str
    :return: Egy tuple, amely tartalmazza a létrehozott táblát, a felhasználható bábuk listáját,
             valamint a pálya azonosítóját és nehézségi szintjét.
    :rtype: tuple
    """
    tabla = logika.Tabla()
    felhasznalhato_babuk = []
    palya_id = None
    palya_nehezseg = None

    with open(fajlnev, 'r', encoding="Utf-8") as f:
        sorok = f.readlines()

    fix_babuk = False
    for sor in sorok:
        sor = sor.strip()
        if sor.startswith("Pálya:"):
            palya_id = sor.split(":")[1].strip()  
        elif sor.startswith("Nehézség:"):
            palya_nehezseg = sor.split(":")[1].strip()  
        if sor.startswith("Fix Bábuk:"):
            fix_babuk = True
            continue
        elif sor.startswith("Felhasználható Bábuk:"):
            fix_babuk = False
            continue

        if sor and not sor.startswith("Pálya:") and not sor.startswith("Nehézség:"):
            adatok = sor.split(",")
            tipus = adatok[0].strip()

            # Fix bábuk esetén
            if fix_babuk:
                if len(adatok) < 3:
                    print(f"Hiányzó adatok a sorban: {sor}")
                    continue
                tajolas = logika.IRANYOK.index(adatok[1].strip())
                pozicio = tuple(map(int, adatok[2].strip().split(";")))
                # Példányosítás a típus alapján
                babu = None
                if tipus == "Tükör":
                    babu = logika.Tukor(tipus, pozicio, tajolas)
                elif tipus == "ÁteresztőTükör":
                    babu = logika.AteresztoTukor(tipus, pozicio, tajolas)
                elif tipus == "SpaceRock":
                    babu = logika.SpaceRock(tipus, pozicio, tajolas)
                elif tipus == "Rakéta":
                    babu = logika.Raketa(tipus, pozicio, tajolas)

                if babu:
                    tabla.babu_elhelyez(babu, pozicio)

            # Mozgatható bábuk esetén
            else:
                if len(adatok) < 2:
                    print(f"Hiányzó adatok a mozgatható bábukhoz: {sor}")
                    continue

                darabszam = int(adatok[1].strip())
                # Példányosítás a típus alapján és hozzáadás a listához
                for _ in range(darabszam):
                    if tipus == "Tükör":
                        babu = logika.Tukor(tipus, (None, None))
                    elif tipus == "ÁteresztőTükör":
                        babu = logika.AteresztoTukor(tipus, (None, None))
                    elif tipus == "SpaceRock":
                        babu = logika.SpaceRock(tipus, (None, None))
                    elif tipus == "Rakéta":
                        babu = logika.Raketa(tipus, (None, None))
                    else:
                        continue  # Ismeretlen típus esetén továbblépünk

                    felhasznalhato_babuk.append(babu)
    palya_info = int(palya_id), palya_nehezseg

    return tabla, felhasznalhato_babuk, palya_info


#Dicsőséglista fajlkezelés
def dicsoseglista_keszitese_frissites():
    """
    Frissíti a dicsőséglistát a 'profilok' mappában található összes profil adatai alapján. A profilokat
    dicsőségpontok alapján rangsorolja, amelyek a teljesített pályák száma, az összpontszám és az összesen
    eltöltött idő alapján számítódnak ki.

    :return: None. A függvény csak mellékhatással rendelkezik, a dicsőséglista fájl frissítése a célja.
    :rtype: None
    """
    profilok = []
    for fajlnev in os.listdir('profilok'):
        if fajlnev.endswith('.txt'):
            profil = logika.Profil.betoltes_fajlnev_alapjan(fajlnev)
            if profil:
                profilok.append(profil)

    # Dicsőségpontok kiszámítása és rangsorolás
    rangsorolt_profilok = sorted(profilok, key=lambda p: (p.osszpontszam + len(p.teljesitett_palyak) * 100 - p.osszido), reverse=True)

    # Dicsőséglista mentése
    with open('dicsoseglista.txt', 'w') as f:
        for profil in rangsorolt_profilok:
            f.write(f"{profil.gamertag}: Dicsőségpontok: {profil.osszpontszam + len(profil.teljesitett_palyak) * 100- profil.osszido}, Teljesített kihívások: {len(profil.teljesitett_palyak)}, Összes elhasznált idő: {profil.osszido}mp\n")




