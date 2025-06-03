#BLACKJACK
import art
import random

tally = 0
player = 0
house = 0
def deal():
    """Deals a random card from the deck"""
    cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
    card = random.choice(cards)
    return card

def calculate_score(cards):
    """Calculates the value of cards in a hand"""
    if sum(cards)==21 and len(cards)==2:
        return 0

    if 11 in cards and sum(cards)>21:
        cards.remove(11)
        cards.append(1)

    return sum(cards)

def compare(user, computer):
    global tally, house, player
    """Compares the scores to determine a winner"""
    if computer==0:
        house += 1
        tally += 1
        return "The dealer has a blackjack!\nHOUSE WINS!"
    elif user==0:
        player += 1
        tally += 1
        return "You have a blackjack!\nYOU WIN!"
    elif computer==user:
        tally += 1
        return "Draw"
    elif user>21:
        tally += 1
        house += 1
        return "BUST!\nHOUSE WINS!"
    elif computer>21:
        player += 1
        tally += 1
        return "The house had a bust!\nYOU WIN!"
    elif user>computer:
        player += 1
        tally +=1
        return "YOU WIN!"
    else:
        tally +=1
        house +=1
        return "YOU LOSE!"

def blackjack():
    global tally, player,house
    print(art.intro)
    end=False
    players_hand=[]
    dealers_hand=[]
    players_score=-1
    dealers_score=-1

    for x in range (2):
        dealers_hand.append(deal())
        players_hand.append(deal())

    while not end:
        players_score=calculate_score(players_hand)
        dealers_score=calculate_score(dealers_hand)
        print(f"{players_hand}\nYou have been dealt a {players_hand[0]} and a {players_hand[1]} a total of {players_score}")
        print(f"The dealers first card is {dealers_hand[0]}")

        if dealers_score==0 or players_score==0 or players_score>21 or dealers_score>21:
            end=True
            if players_score==0:
                print(art.blackjack)
                print("BLACKJACK!")
            if dealers_score==0:
                print(art.logo)
        else:
            pick = input("Would you like to draw another card? Y or N?\n").lower()
            if pick=="y":
                players_hand.append(deal())
                print(f"You have been dealt a {players_hand[-1]}")

            else:
                end=True


    while dealers_score!=0 and dealers_score<17:
        dealers_hand.append(deal())
        dealers_score=calculate_score(dealers_hand)

    print(f"Your final hand: {players_hand} with a total of {players_score}")
    print(f"The dealer ended the game with: {dealers_hand} and a total of {dealers_score}")
    print(compare(players_score, dealers_score))
    # print(dealers_score, players_score)

    if end:
        # if compare(players_score,dealers_score)=="YOU LOSE!" or "BUST!\nHOUSE WINS!" or "The dealer has a blackjack!\nHOUSE WINS!":
        #     tally+=1
        #     house+=1
        # elif compare(players_score,dealers_score)=="You have a blackjack!\nYOU WIN!" or "The house had a bust!\nYOU WIN!" or "YOU WIN!":
        #     tally+=1
        #     player+=1
        # else:
        #     tally+=1
        #     player+=1

        print(f"For a total of {tally} games, you have won {player} and the dealer has won {house}")
        print("\n" * 10)
        if input("The dealer would like to deal again. Do you want to continue playing?\n").lower() == "y":
            print("\n" * 100)
            blackjack()
        else:
            return
if input("Would you like to play a game of blackjack?\n").lower() == "y":
    print("\n" * 100)
    blackjack()
