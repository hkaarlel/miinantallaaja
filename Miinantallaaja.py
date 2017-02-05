#-*- coding: utf-8 -*-
import random
import time
import datetime

def alkuvalikko():
    """Näyttää pelin alussa näytettävät alkutekstit sekä kysyy käyttäjältä mitä tehdään."""
    print "\nMiinantallaaja 1.0"
    print "=================="
    print "\nKeltainen valtio on aloittanut sotatoimet maatamme kohtaan."
    print "Teidän on raivattava miinakenttä jotta joukkomme voivat edetä."
    print "Valitkaa ensin jokin allaolevista toiminnoista kirjoittamalla sen alkukirjain."
    print "(A)loita uusi operaatio"
    print "(T)utki vanhojen operaatioiden lokeja"
    print "(P)akene veksiin eli lopeta"
    print "Jos haluatte tehdä pelin aikana pikaisen perääntymisen, painakaa Ctrl+C"
    print "Voitte toimia"
    print "=============\n"
    while True:
        valinta = raw_input("Valinta: ").lower()
        if valinta == "a" or valinta == "t" or valinta == "p":
            return valinta
        else:
            print "Valitse A, T tai P"        

def nayta_tilastot(tiedoston_nimi):
    """Aukaisee tilastotiedoston ja näyttää sen sisällön"""
    tiedosto = open(tiedoston_nimi, "r")
    rivit = tiedosto.readlines()
    sisalto = ("").join(rivit)
    tiedosto.close()        
    return sisalto
    
def kirjoita_tilastoihin(tiedoston_nimi, sisalto):
    """Kirjoittaa tilastotiedostoon pelin tuloksen ja keston"""
    tiedosto = open(tiedoston_nimi, "a")
    tiedosto.write("%s" % (sisalto))
    tiedosto.close()

def pyyda_korkeus():
    """Pyytää kentän korkeuden syötteessä ja tarkistaa sen oikeuden"""
    while True:
        try:
            korkeus = int(raw_input("Anna pelilaudan korkeus: "))
            if korkeus > 1 and korkeus < 21:
                return korkeus
            else:
                print "Korkeuden tulee olla kokonaisluku 2-20"
        except ValueError:
            print "Korkeuden tulee olla kokonaisluku 2-20"
            
def pyyda_leveys():
    """Pyytää kentän leveyden syötteessä ja tarkistaa sen oikeuden"""
    while True:
        try:
            leveys = int(raw_input("Anna pelilaudan leveys: "))
            if leveys > 1 and leveys < 51:
                return leveys
            else:
                print "Leveyden tulee olla kokonaisluku 2-50"
        except ValueError:
            print "Leveyden tulee olla kokonaisluku 2-50"

def pyyda_miinat():
    """Pyytää miinojen lukumäärän syötteessä ja tarkistaa sen. Lisäksi pyytää varmistusta mikäli miinoja on liikaa/liian vähän kenttään nähden"""
    while True:
        try:
            miinat = int(raw_input("Montako miinaa laitetaan? "))
            if miinat > 0 and miinat < (leveys * korkeus - 1):
                if miinat < (leveys * korkeus / 10) and leveys >= 10 and korkeus >= 10:
                    if raw_input("Varoitus! Näin vähän miinoja saattaa hidastaa latauksia!\nPaina K jos olet varma: ").lower() == "k":
                        return miinat
                elif (leveys * korkeus - miinat) < 10 and korkeus == 20 and leveys > 20:
                    if raw_input("Varoitus! Näin paljon miinoja saattaa hidastaa latauksia!\nPaina K jos olet varma: ").lower() == "k":
                        return miinat
                else:
                    return miinat
            else:
                print "Miinojen määrän tulee olla kokonaisluku välillä 1-%s" % (leveys * korkeus - 2)
        except ValueError:
            print "Miinojen määrän tulee olla kokonaisluku välillä 1-%s" % (leveys * korkeus - 2)           
            
def luo_kentta(leveys, korkeus, miinat):
    """Luo kentän käyttäjän antaman leveyden, korkeuden ja miinojen lukumäärän mukaan"""
    kentta = []                         
    for rivi in range(korkeus):
        kentta.append(["O"] * leveys)
    jaljella = []                       
    for x in range(leveys):
        for y in range(korkeus):
            jaljella.append((x, y))
    for i in range(miinat):             
        koordinaatit = miinoita_satunnainen(kentta, jaljella)
        jaljella.remove(koordinaatit)
    return kentta

def miinoita_satunnainen(kentta, jaljella):
    """Miinoittaa yhden satunnaisen ruudun annetun kaksiulotteisen kenttälistan vapaista koordinaateista."""
    koordinaatit = random.choice(jaljella)
    koordilista =  list(koordinaatit)
    kentta[koordilista[1]][koordilista[0]] = "x" 
    return koordinaatit                             
    
def koordinaattien_valinta(korkeus, leveys, kentta, miinat):
    """Pyydetään käyttäjältä koordinaatit ja testataan niiden sopivuus"""
    askel = []
    while True:
        eiint = 0
        koordinaatit = raw_input("Anna koordinaatit muodossa korkeus leveys: ")
        askel = koordinaatit.split(" ")
        if len(askel) != 2:
            print "Koordinaatit on annettava kokonaislukuina muodossa \"korkeus leveys\", esim. 2 3"
        else:
            try:
                askel[0] = int(askel[0]) - 1
            except ValueError:
                eiint = 1
                print "Koordinaatit on annettava kokonaislukuina muodossa \"korkeus leveys\", esim. 2 3"
            try:
                askel[1] = int(askel[1]) - 1
            except ValueError:
                if eiint == 0:
                    print "Koordinaatit on annettava kokonaislukuina muodossa \"korkeus leveys\", esim. 2 3" 
                eiint = 1
            if eiint == 0:
                if askel[0] < 0 or askel[0] > (korkeus - 1) or askel[1] < 0 or askel[1] > (leveys - 1):
                    print "Osuit kentän ulkopuolelle!"
                else:
                    return askel
    
def ruutujen_avaus(ruudut, x, y):
    """Avaa tyhjät ruudut ja laitimmaiset numeroruudut lähtien annetuista koordinaateista, palauttaa 1:n jos pelaaja osuu miinaan"""
    if ruudut[y][x] == "x":
        return 1                        
    else:
        pino = []
        tappio = []
        pino.append((x, y))
        while len(pino) > 0:
            lista = list(pino[0])
            try:
                pino.pop(0)
            except KeyboardInterrupt:
                return "sammutus"
            if lista[0] >= 0 and lista[1] >= 0 and lista[0] <= len(ruudut[0]) and lista[1] <= len(ruudut):
                ruudut[lista[1]][lista[0]] = laske_ymparoivat_miinat(lista[0], lista[1], ruudut) 
                if ruudut[lista[1]][lista[0]] == "0":                                               
                    ruudut[lista[1]][lista[0]] = " "
            if lista[0] > 0:                                                                           
                if ruudut[lista[1]][lista[0] - 1] == "O" and ruudut[lista[1]][lista[0]] == " ": 
                    pino.append(((lista[0] - 1), (lista[1])))           
            if lista[1] > 0:                                            
                if ruudut[lista[1] - 1][lista[0]] == "O" and ruudut[lista[1]][lista[0]] == " ":
                    pino.append(((lista[0]), (lista[1] - 1)))
            if lista[0] < (len(ruudut[0]) - 1):
                if ruudut[lista[1]][lista[0] + 1] == "O" and ruudut[lista[1]][lista[0]] == " ":
                    pino.append(((lista[0] + 1, lista[1])))
            if lista[1] < (len(ruudut) - 1):
                if ruudut[lista[1] + 1][lista[0]] == "O" and ruudut[lista[1]][lista[0]] == " ":
                    pino.append(((lista[0], lista[1] + 1)))
        return 0

def laske_ymparoivat_miinat(x, y, huone):
    """Laskee valittua pistettä ympäröivät miinat ja palauttaa niiden lukumäärän"""
    lukumaara = 0 
    rivit = 0
    sarakkeet = 0
    for i in huone:
        rivit = rivit + 1
    for j in huone[0]:
        sarakkeet = sarakkeet + 1
    if x+1 < sarakkeet and y+1 < rivit:                           
        if huone[y+1][x+1] == "x" and y+1 != 0 and x+1 != 0:        
            lukumaara = lukumaara + 1
    if y+1 < rivit:                             
        if huone[y+1][x-1] == "x" and y+1 != 0 and x-1 >= 0:
            lukumaara = lukumaara + 1
        if huone[y+1][x] == "x" and y+1 != 0:
            lukumaara = lukumaara + 1
    if x+1 < sarakkeet and y-1 >= 0:
        if huone[y-1][x+1] == "x" and y-1 >= 0 and x+1 != 0:
            lukumaara = lukumaara + 1
    if x+1 < sarakkeet:
        if huone[y][x+1] == "x" and x+1 != 0:
            lukumaara = lukumaara + 1    
    if y-1 >= 0:
        if huone[y-1][x] == "x" and y-1 >= 0:
            lukumaara = lukumaara + 1
    if y-1 >= 0 and x-1 >= 0:
        if huone[y-1][x-1] == "x" and y-1 >= 0 and x-1 >= 0:
            lukumaara = lukumaara + 1
    if huone[y][x-1] == "x" and x-1 >= 0:
        lukumaara = lukumaara + 1
    lukumaara = "%s" % lukumaara
    return lukumaara
                    
def laske_miinat(kentta, korkeus, miinat):
    """Laskee onko kaikki muut paikat paitsi miinat auottu eli onko peli voitettu"""
    alkio = 0
    lukumaara = 0
    for i in range(korkeus):
        rivi = "".join(kentta[alkio])
        lukumaara = lukumaara + rivi.count("O")
        alkio = alkio + 1    
    return lukumaara

def tulosta_kentta(korkeus, leveys, kentta, voitto, tappio):
    """Tulostaa kentän ja sille laidat (erilaiset laidat kun leveys ja korkeus ovat yli tai ali 10) sekä peittää miinojen paikat mikäli peli ei ole ohi"""
    rivitulostus1 = ""
    rivitulostus2 = ""
    k = -1
    for i in range(leveys+2):                            
        if i > 1:
            if k == 10:
                k = 0
            rivitulostus2 = rivitulostus2 + ("%s" % k)
        else:
            rivitulostus2 = rivitulostus2 + (" ")
        k = k + 1
        if i > 10:
            rivitulostus1 = rivitulostus1 + "%s" % (int((i-1)/10))
        else:
            rivitulostus1 = rivitulostus1 + (" ")
    if korkeus < 10:                                    
        if leveys >= 10:
            print "%s" % rivitulostus1
        print "%s\n" % rivitulostus2                    
    if korkeus >= 10:
        if leveys >= 10:
            print " %s" % rivitulostus1
        print " %s\n" % rivitulostus2
    rivinumero = 1
    for i in range(korkeus):               
        rivi = "".join(kentta[rivinumero - 1])
        if voitto == 0 and tappio == 0:
            rivi = "%s" % rivi.replace("x", "O")   
        if korkeus >= 10 and rivinumero >= 10:
            print "%s %s %s" % (rivinumero, rivi, rivinumero)
        elif korkeus >= 10 and rivinumero < 10:
            print "%s  %s %s" % (rivinumero, rivi, rivinumero)
        elif korkeus < 10:
            print "%s %s %s" % (rivinumero, rivi, rivinumero)
        rivinumero = rivinumero + 1
    if korkeus < 10:                                   
        if leveys >= 10:
            print "\n%s" % rivitulostus1
            print "%s\n" % rivitulostus2
        else:
            print "\n%s\n" % rivitulostus2
    if korkeus >= 10:
        if leveys >= 10:
            print "\n %s" % rivitulostus1
            print " %s\n" % rivitulostus2
        else:
            print "\n %s\n" % rivitulostus2
              
if __name__ == "__main__":
    while True:
        askel = []
        try:                    #KeyboardInterruptin try
            aloitus = alkuvalikko()
            if aloitus == "p":
                break
            elif aloitus == "t":
                try:
                    print nayta_tilastot("miinantallaaja.mtt")
                except IOError:
                    print "Aikaisempia operaatioita ei ollut.\nMikäli olisi pitänyt olla niin tiedustelkaa esikunnan kirjurilta."
                if raw_input("Painakaa K jos haluatte aloittaa uuden pelin, muuten lopetetaan: ").lower() != "k":
                    break    
            pelaajan_nimi = raw_input("Nimenne oli? ")
            korkeus = int(pyyda_korkeus())
            leveys = int(pyyda_leveys())
            miinat = pyyda_miinat()
            kentta = luo_kentta(leveys, korkeus, miinat)
            kierros = 0
            alkuaika = time.time()
            while True:
                askel = koordinaattien_valinta(korkeus, leveys, kentta, miinat)
                kierros = kierros + 1
                while True:
                    if kentta[askel[0]][askel[1]] == "x" and kierros == 1:  #Mikäli ekalla kierroksella osutaan miinaan, arvotaan uusi kenttä
                        kentta = luo_kentta(leveys, korkeus, miinat)
                    else:
                        break
                tappio = ruutujen_avaus(kentta, askel[1], askel[0])
                aukaisemattomia = laske_miinat(kentta, korkeus, miinat)
                if aukaisemattomia == 0:                                    
                    voitto = 1
                else:
                    voitto = 0
                if tappio == "sammutus":                                    #Ctrl-C-sammutuksen ilmoitus (käyttäjä voi tehdä jos ruutujen avaaminen jumittaa)
                    print "Pakotettiin sammutus käyttäjän toiveesta"
                    break
                tulosta_kentta(korkeus, leveys, kentta, voitto, tappio)
                if tappio == 1 or voitto == 1:                              
                    aika = int(time.time() - alkuaika)
                    minuutit = int(aika/60)
                    sekunnit = aika-(int(aika/60))*60
                    if sekunnit < 10:
                        sekunnit = "0%s" % sekunnit
                    aika = "%s:%s" % (minuutit, sekunnit)
                    ajankohta = str(datetime.datetime.now())
                    ajankohta = ajankohta[:-7]
                if tappio == 1:                                            
                    print "Aijai, nyt sattui leukaan. Eikun buranaa poskeen.\nTappio %s kierroksessa ja ajassa %s" % (kierros, aika)
                    sisalto = "%s: %s, kesto %s, vuoroja %s, TAPPIO, avaamattomia %s\n" % (pelaajan_nimi, ajankohta, aika, kierros, aukaisemattomia)
                    try:
                        kirjoita_tilastoihin("miinantallaaja.mtt", sisalto)
                    except IOError:
                        print "Tilastoihin kirjoitus ei onnistunut"
                    break   
                if voitto == 1:                                            
                    print "Nyt suositellaan kuntsaria.\nVoitto %s kierroksessa ja ajassa %s" % (kierros, aika)
                    sisalto = "%s: %s, kesto %s, vuoroja %s, VOITTO\n" % (pelaajan_nimi, ajankohta, aika, kierros)
                    try:
                        kirjoita_tilastoihin("miinantallaaja.mtt", sisalto)
                    except IOError:
                        print "Tilastoihin kirjoitus ei onnistunut" 
                    break
        except KeyboardInterrupt:
            print "\nPakotettiin sammutus käyttäjän toiveesta"
        if raw_input("Painakaa K jos haluatte palata alkuvalikkoon, muuten lopetetaan: ").lower() != "k": 
                break