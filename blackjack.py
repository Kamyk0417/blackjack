import random
import math 

list = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]

def wynik():
    print(f"gracz: {gracz}      krupier: {krupier}")

def hit():
    g = random.choice(list)
    gracz.append(g)

def stand():
    k = random.choice(list)
    krupier.append(k)

def double_down():
    with open("tokeny.txt", "r+"):
        global bet
        bet *= 2
        print(f"Postawiłeś {bet} żetonów, zostało ci {int(tokeny)-bet}")

def win_tokens(winner):                                                 #function that gives tokens based on score
    if winner == "cr":                                                                        # if croupier scored
        with open("tokeny.txt", "r+") as f:
            f.truncate(0)
            f.write(str(int(tokeny)-bet))
            print(f"Straciłeś {bet} żetonów, zostało ci {int(tokeny)-bet}")
    if winner == "pl":                                                                           #if player scored
        with open("tokeny.txt", "r+") as f:
            f.truncate(0)
            f.write(str(int(tokeny)+bet))
            print(f"Wygrałeś dodatkowe {bet} żetonów, teraz masz {int(tokeny)+bet}")
    if winner == "draw":                                                                                  #if draw
        with open("tokeny.txt", "r+") as f:
            print(f"Dalej masz {int(tokeny)} żetonów")

def wincons():
    if sum(gracz) > 21 or (sum(krupier) <= 21 and sum(krupier) > sum(gracz)):
        print("Krupier wygrał".upper())
        win_tokens("cr")
    elif sum(krupier) > 21 or sum(gracz) > sum(krupier):  # winning cons
        print("Gracz wygrał".upper())
        win_tokens("pl")
    elif sum(krupier) == sum(gracz):
        print("Remis".upper())
        win_tokens("draw")

koniec = 0
while koniec != 1:
    with open("tokeny.txt", "r+") as f:                                      #making and displaying tokens and bet
        tokeny = f.read()
        print(f"Twoje żetony: {tokeny}")
        bet = int(input("Ile stawiasz: "))
        assert bet <= int(tokeny), "Masz za mało żetonów"
        print(f"Twoje żetony: {int(tokeny)-bet}        stawka: {bet}")
    gracz = [random.choice(list), random.choice(list)]                                      #random starting hands
    krupier = [0, random.choice(list)]                                #with one of croupier's cards hidden under 0
    wynik()
    dd = True
    if sum(gracz) == 21:                                                         #checks if player has a blackjack
        krupier[0] = random.choice(list)
        wynik()
        if sum(krupier) != 21:                                                        #croupier has no a blackjack
            print("Gracz wygrał z blackjackiem".upper())
            with open("tokeny.txt", "r+") as f:
                f.truncate(0)
                f.write(str(int(tokeny) + math.floor(1.5*bet)))
                print(f"Wygrałeś dodatkowe {math.floor(1.5*bet)} żetonów, teraz masz {int(tokeny) + math.floor(1.5*bet)}")
            koniec = int(input("Jeżeli chcesz skończyć - naciśnij 1, jeżeli nie - naciśnij 0: "))
            continue
        if sum(krupier) == 21:                                                       #croupier has a blackjack too
            print(f"Remis, dalej masz {tokeny}")
            koniec = int(input("Jeżeli chcesz skończyć - naciśnij 1, jeżeli nie - naciśnij 0: "))
            continue
    while True:
        if dd == True:
            dzialanie = input("hit, stand, double down, split czy insurance?")
        else:
            dzialanie = input("hit, stand, split czy insurance?")
                      #choosing action
        if dzialanie.lower() == "hit":
            dd = False                                                                        #hit
            hit()
            wynik()
            if sum(gracz) > 21 and 11 in gracz:                                        #changing ace value 11 to 1
                gracz[gracz.index(11)] = 1
                wynik()
                if sum(gracz) > 21:
                    print("Krupier wygrał".upper())
                    win_tokens("cr")
                    break
            elif sum(gracz) > 21:                                                     #player has no ace and busts
                wynik()
                print("Krupier wygrał".upper())
                win_tokens("cr")
                break
        if dzialanie.lower() == "stand":
            dd = False                                                                    #stand
            krupier[0] = random.choice(list)
            while sum(krupier) < 17:
                stand()
            wynik()
            wincons()
            break
        if dzialanie.lower() == "double down":
            if not dd:
                with open("tokeny.txt", "r+") as f:
                    f.truncate(0)
                    f.write(str(int(tokeny) - bet))
            assert dd, "Następnym razem wybierz możliwe działanie, straciłeś zakład"
            double_down()
            hit()
            krupier[0] = random.choice(list)
            while sum(krupier) < 17:
                stand()
            wynik()
            wincons()
            break
    koniec = int(input("Jeżeli chcesz skończyć - naciśnij 1, jeżeli nie - naciśnij 0: "))          #restart choice

