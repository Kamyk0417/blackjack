import random
import math

list = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]

def wynik():
    print(f"gracz: {gracz}      krupier: {krupier}")

def hit_stand(hand):
    gc = random.choice(list)
    hand.append(gc)

def double_down():
    with open("tokeny.txt", "r+"):
        global bet
        bet *= 2
        print(f"Postawiłeś {bet} żetonów, zostało ci {int(tokeny)-bet}")

def split():
    global gracz2
    gracz2 = [gracz[0], random.choice(list)]
    gracz[1] = random.choice(list)
    with open("tokeny.txt", "r+") as f:
        global bet
        bet1, bet2 = bet
        print(f"Zostało ci {int(tokeny)-2*bet} żetonów\nRęka pierwsza: {gracz}          Ręka druga: {gracz2}\n"
              f"Zakład pierwszy: {bet}          Zakład drugi: {bet}")




#function that gives tokens based on score
def win_tokens(winner):
    #if croupier scored
    if winner == "cr":
        with open("tokeny.txt", "r+") as f:
            f.truncate(0)
            f.write(str(int(tokeny)-bet))
            print(f"Straciłeś {bet} żetonów, zostało ci {int(tokeny)-bet}")
    #if player scored
    if winner == "pl":
        with open("tokeny.txt", "r+") as f:
            f.truncate(0)
            f.write(str(int(tokeny)+bet))
            print(f"Wygrałeś dodatkowe {bet} żetonów, teraz masz {int(tokeny)+bet}")
    #if draw
    if winner == "draw":
        with open("tokeny.txt", "r+") as f:
            print(f"Dalej masz {int(tokeny)} żetonów")

# winning cons
def wincons():
    if sum(gracz) > 21 or (sum(krupier) <= 21 and sum(krupier) > sum(gracz)):
        print("Krupier wygrał".upper())
        win_tokens("cr")
    elif sum(krupier) > 21 or sum(gracz) > sum(krupier):
        print("Gracz wygrał".upper())
        win_tokens("pl")
    elif sum(krupier) == sum(gracz):
        print("Remis".upper())
        win_tokens("draw")

koniec = 0
while koniec != 1:
    #making and displaying tokens and bet
    with open("tokeny.txt", "r+") as f:
        tokeny = f.read()
        print(f"Twoje żetony: {tokeny}")
        bet = int(input("Ile stawiasz: "))
        assert bet <= int(tokeny), "Masz za mało żetonów"
        print(f"Twoje żetony: {int(tokeny)-bet}        stawka: {bet}")
    #random starting hands with one of croupier's cards hidden under 0
    gracz = [random.choice(list), random.choice(list)]
    krupier = [0, random.choice(list)]
    wynik()
    dd = True
    #checks if player has a blackjack
    if sum(gracz) == 21:
        krupier[0] = random.choice(list)
        wynik()
        #croupier has no a blackjack
        if sum(krupier) != 21:
            print("Gracz wygrał z blackjackiem".upper())
            with open("tokeny.txt", "r+") as f:
                f.truncate(0)
                f.write(str(int(tokeny) + math.floor(1.5*bet)))
                print(f"Wygrałeś dodatkowe {math.floor(1.5*bet)} żetonów, teraz masz {int(tokeny) + math.floor(1.5*bet)}")
            koniec = int(input("Jeżeli chcesz skończyć - naciśnij 1, jeżeli nie - naciśnij 0: "))
            continue
        #croupier has a blackjack too
        if sum(krupier) == 21:
            print(f"Remis, dalej masz {tokeny}")
            koniec = int(input("Jeżeli chcesz skończyć - naciśnij 1, jeżeli nie - naciśnij 0: "))
            continue
    while True:
        #choosing action
        if dd == True:
            dzialanie = input("hit, stand, double down, split czy insurance?")
        else:
            dzialanie = input("hit, stand, split czy insurance?")
        #hit
        if dzialanie.lower() == "hit":
            dd = False
            hit_stand(gracz)
            wynik()
            #changing ace value 11 to 1
            if sum(gracz) > 21 and 11 in gracz:
                gracz[gracz.index(11)] = 1
                wynik()
                if sum(gracz) > 21:
                    print("Krupier wygrał".upper())
                    win_tokens("cr")
                    break
            #player has no ace and busts
            elif sum(gracz) > 21:
                wynik()
                print("Krupier wygrał".upper())
                win_tokens("cr")
                break
        #stand
        if dzialanie.lower() == "stand":
            dd = False
            krupier[0] = random.choice(list)
            while sum(krupier) < 17:
                hit_stand(krupier)
            wynik()
            wincons()
            break
        #double down
        if dzialanie.lower() == "double down":
            #dd not available
            if not dd:
                with open("tokeny.txt", "r+") as f:
                    f.truncate(0)
                    f.write(str(int(tokeny) - bet))
            assert dd, "Następnym razem wybierz możliwe działanie, straciłeś zakład"
            #dd available
            double_down()
            hit_stand(gracz)
            krupier[0] = random.choice(list)
            while sum(krupier) < 17:
                hit_stand(krupier)
            wynik()
            wincons()
            break
    #restart choice
    koniec = int(input("\nJeżeli chcesz skończyć - naciśnij 1, jeżeli nie - naciśnij 0: "))


