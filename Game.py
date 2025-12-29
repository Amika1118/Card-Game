import random

# Create a dictionary for all suits
suits = {
    "Hearts": ["♥A","♥2","♥3","♥4","♥5","♥6","♥7","♥8","♥9","♥10","♥J","♥K","♥Q"],
    "Diamonds": ["♦A","♦2","♦3","♦4","♦5","♦6","♦7","♦8","♦9","♦10","♦J","♦K","♦Q"],
    "Clubs": ["♣A","♣2","♣3","♣4","♣5","♣6","♣7","♣8","♣9","♣10","♣J","♣K","♣Q"],
    "Spades": ["♠A","♠2","♠3","♠4","♠5","♠6","♠7","♠8","♠9","♠10","♠J","♠K","♠Q"]
}

trumps = ""

player = []
AI_1 = []
AI_2 = []
AI_3 = []

Cards = []
for i in range(5,13):
    Cards.append(suits["Hearts"][i])
    Cards.append(suits["Diamonds"][i])
    Cards.append(suits["Clubs"][i])
    Cards.append(suits["Spades"][i])

def shuffle_cards():
    while True:
        try:
            user_in = int(input("How many times do want to shuffle the deck ? "))
            if 10 < user_in or 4 > user_in:
                print("Please enter a number between 5 and 13")
            else:
                break
        except ValueError:
            print("Please enter a number.")


    for i in range(user_in):
        random.shuffle(Cards)   #    You can see that this shuffles the times
    #    print(Cards)           #    you want to shuffle just remove "#"


def give_cards():
    got_trumps = False
    for i in range(len(Cards)):
        j = i + 1

        if j % 4 == 1:
            player.append(Cards[i])       # Here also remove the "#" to
            #print(player)                # see how cards are being given in each round
        elif j % 4 == 2:
            AI_1.append(Cards[i])
            #print(AI_1)
        elif j % 4 == 3:
            AI_2.append(Cards[i])
            #print(AI_2)
        elif j % 4 == 0:
            AI_3.append(Cards[i])
            #print(AI_3)

        if j <= 15:
            continue
        else:
            print()
            print( " " * 7 + "My Cards")
            print("-------------------------")
            print(" " * 4 , end= "")
            for my_card in player:
                print(my_card,end="  ")
            print("\n-------------------------")
            if not got_trumps:
                print("\nAs you have 4 cards in your hand,\nSo now you need to say what are the trump cards.")
                while True:
                    choice = input("What are the trump cards : ")
                    if choice.capitalize() in suits.keys():
                        trump = choice.capitalize()
                        print("\nThe trumps are : " + trump)
                        got_trumps = True
                        break
                    else:
                        print("Please enter trumps form one of given below.")
                        for suit in suits.keys():
                            print(suit)
            else:
                continue
shuffle_cards()
give_cards()