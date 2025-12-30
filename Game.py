import random

# Create a dictionary for all suits
suits = {
    "Hearts": ["♥2", "♥3", "♥4", "♥5", "♥6", "♥7", "♥8", "♥9", "♥10", "♥J", "♥K", "♥Q", "♥A"],
    "Diamonds": ["♦2", "♦3", "♦4", "♦5", "♦6", "♦7", "♦8", "♦9", "♦10", "♦J", "♦K", "♦Q", "♦A"],
    "Clubs": ["♣2", "♣3", "♣4", "♣5", "♣6", "♣7", "♣8", "♣9", "♣10", "♣J", "♣K", "♣Q", "♣A"],
    "Spades": ["♠2", "♠3", "♠4", "♠5", "♠6", "♠7", "♠8", "♠9", "♠10", "♠J", "♣K", "♠Q", "♠A"]
}

player_name = ""
trump = ""
player = []
AI_1 = []
AI_2 = []
AI_3 = []
scores = {"Player": 0, "AI_1": 0, "AI_2": 0, "AI_3": 0}
tricks_won = {"Player": 0, "AI_1": 0, "AI_2": 0, "AI_3": 0}
Cards = []
current_leader = "Player"  # Track who leads each round

# Removing the cards from 1 to 5 as we do not use them for playing
for i in range(5, 13):
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
        random.shuffle(Cards)


def give_cards():
    global trump, player, AI_1, AI_2, AI_3
    # Clear hands
    player.clear()
    AI_1.clear()
    AI_2.clear()
    AI_3.clear()

    got_trumps = False
    for i in range(len(Cards)):
        j = i + 1

        if j % 4 == 1:
            player.append(Cards[i])
        elif j % 4 == 2:
            AI_1.append(Cards[i])
        elif j % 4 == 3:
            AI_2.append(Cards[i])
        elif j % 4 == 0:
            AI_3.append(Cards[i])

        # Ask for trumps after each player has 4 cards (after 16 cards dealt)
        if j == 16 and not got_trumps:
            print("\n" + "=" * 50)
            print(" " * 7 + "My Cards")
            print("=" * 50)
            print(" " * 4, end="")
            for idx, my_card in enumerate(player):
                print(f"{idx + 1:2}. {my_card}   ", end="")
            print("\n" + "=" * 50)

            print("\nAs you have 4 cards in your hand,")
            print("Now you need to choose the trump suit.")

            while True:
                choice = input(
                    "\nWhat are the trump cards ?\n01. Hearts ♥\n02. Clubs ♣\n03. Diamonds ♦\n04. Spades ♠\n----------------> ")

                # Handle different input formats
                if choice in ["1", "01", "h", "H", "♥", "hearts", "Hearts"]:
                    trump = "Hearts"
                    break
                elif choice in ["2", "02", "c", "C", "♣", "clubs", "Clubs"]:
                    trump = "Clubs"
                    break
                elif choice in ["3", "03", "d", "D", "♦", "diamonds", "Diamonds"]:
                    trump = "Diamonds"
                    break
                elif choice in ["4", "04", "s", "S", "♠", "spades", "Spades"]:
                    trump = "Spades"
                    break
                else:
                    print("Please enter a valid choice (01, 02, 03, or 04)")

            # Map trump suits to their symbols
            symbol_map = {"Hearts": "♥", "Clubs": "♣", "Diamonds": "♦", "Spades": "♠"}
            print(f"\nThe trumps are: {trump} {symbol_map.get(trump, '')}")
            got_trumps = True


def get_card_value(card):
    """Get numeric value of card for comparison"""
    value = card[1:]  # Remove suit symbol
    if value == "A":
        return 14
    elif value == "K":
        return 13
    elif value == "Q":
        return 12
    elif value == "J":
        return 11
    else:
        return int(value)


def get_card_suit(card):
    """Get suit of a card"""
    if "♥" in card:
        return "Hearts"
    elif "♦" in card:
        return "Diamonds"
    elif "♣" in card:
        return "Clubs"
    elif "♠" in card:
        return "Spades"
    return None


def ai_choose_card(ai_hand, first_card=None, trump_suit=None):
    """Simple AI logic to choose a card to play"""
    if not ai_hand:
        return None

    # If no first card (AI is leading)
    if first_card is None:
        # Just pick a random card when leading
        return random.choice(ai_hand)

    # Get the suit to follow
    first_card_suit = get_card_suit(first_card)

    # Find cards of the same suit
    same_suit = []
    for card in ai_hand:
        if get_card_suit(card) == first_card_suit:
            same_suit.append(card)

    # If AI has cards of the same suit, play one
    if same_suit:
        # Play a random card of the same suit
        return random.choice(same_suit)

    # If no same suit, check for trump cards
    if trump_suit:
        trump_cards = []
        for card in ai_hand:
            if get_card_suit(card) == trump_suit:
                trump_cards.append(card)

        # If AI has trump cards, play one
        if trump_cards:
            return random.choice(trump_cards)

    # If no matching suit and no trump, play any card
    return random.choice(ai_hand)


def determine_round_winner(cards_played, trump_suit, first_card_index):
    """Determine who won the round"""
    first_card = cards_played[first_card_index][1]
    first_suit = get_card_suit(first_card)

    # Filter cards that follow suit or are trumps
    valid_cards = []
    for i, (player_name, card) in enumerate(cards_played):
        card_suit = get_card_suit(card)
        if card_suit == trump_suit or card_suit == first_suit:
            valid_cards.append((i, player_name, card, get_card_value(card), card_suit))

    if not valid_cards:
        return first_card_index  # First player wins if no valid cards

    # Sort by: 1) Trump suit, 2) Card value
    valid_cards.sort(key=lambda x: (x[4] != trump_suit, -x[3]))

    # Return the index of the winning player
    return valid_cards[0][0]


def play_round(round_num, leader):
    """Play one round with proper turn order"""
    print(f"\n{'=' * 60}")
    print(f"ROUND {round_num} - {leader if leader != 'Player' else player_name} leads")
    print(f"{'=' * 60}")

    played_cards = []
    players_order = []

    # Define player order starting from leader
    if leader == "Player":
        players_order = [("Player", player), ("AI_1", AI_1), ("AI_2", AI_2), ("AI_3", AI_3)]
    elif leader == "AI_1":
        players_order = [("AI_1", AI_1), ("AI_2", AI_2), ("AI_3", AI_3), ("Player", player)]
    elif leader == "AI_2":
        players_order = [("AI_2", AI_2), ("AI_3", AI_3), ("Player", player), ("AI_1", AI_1)]
    elif leader == "AI_3":
        players_order = [("AI_3", AI_3), ("Player", player), ("AI_1", AI_1), ("AI_2", AI_2)]

    # Play cards in order
    first_card = None
    first_player_index = 0

    for idx, (player_key, player_hand) in enumerate(players_order):
        print(f"\n{'=' * 40}")

        # Determine display name
        if player_key == "Player":
            display_name = player_name
        else:
            display_name = player_key

        if player_key == "Player":
            # Human player's turn
            print(f"\nYour turn, {display_name}!")
            print("Your cards:")
            for i, card in enumerate(player):
                print(f"{i + 1:2}. {card}", end="   ")
            print()

            # Show what's been played so far
            if played_cards:
                print("\nCards played so far:")
                for name_key, card in played_cards:
                    if name_key == "Player":
                        disp_name = player_name
                    else:
                        disp_name = name_key
                    print(f"  {disp_name}: {card}")

            while True:
                try:
                    choice = int(input(f"\nWhich card would you like to play? (1-{len(player)}): "))
                    if 1 <= choice <= len(player):
                        player_card = player[choice - 1]
                        print(f"You played: {player_card}")
                        played_cards.append((player_key, player_card))
                        player.remove(player_card)

                        if idx == 0:  # If player is leading
                            first_card = player_card
                            first_player_index = 0
                        break
                    else:
                        print(f"Please enter a number between 1 and {len(player)}")
                except ValueError:
                    print("Please enter a valid number.")
        else:
            # AI player's turn
            print(f"\n{display_name}'s turn...")

            # Show what's been played so far
            if played_cards:
                print("Cards played so far:")
                for name_key, card in played_cards:
                    if name_key == "Player":
                        disp_name = player_name
                    else:
                        disp_name = name_key
                    print(f"  {disp_name}: {card}")

            ai_card = ai_choose_card(player_hand, first_card, trump)
            if ai_card:
                print(f"{display_name} played: {ai_card}")
                played_cards.append((player_key, ai_card))
                player_hand.remove(ai_card)

                if idx == 0:  # If AI is leading
                    first_card = ai_card
                    first_player_index = idx

    # Determine winner
    winner_index = determine_round_winner(played_cards, trump, first_player_index)
    winner_key = played_cards[winner_index][0]
    tricks_won[winner_key] += 1

    # Display winner
    print(f"\n{'=' * 40}")
    print("Round Summary:")
    print(f"{'=' * 40}")
    for name_key, card in played_cards:
        if name_key == "Player":
            disp_name = player_name
        else:
            disp_name = name_key
        print(f"  {disp_name}: {card}")

    # Determine display name for winner
    if winner_key == "Player":
        display_winner = player_name
    else:
        display_winner = winner_key
    print(f"\n🎯 Round Winner: {display_winner}!")

    # Show current scores
    print(f"\nCurrent Tricks Won:")
    for player_key, tricks in tricks_won.items():
        if player_key == "Player":
            disp_name = player_name
        else:
            disp_name = player_key
        print(f"  {disp_name}: {tricks}")

    return winner_key  # Return who leads next round


def play_cards(game_choice):
    global player_name, current_leader
    if game_choice.lower() in ["1", "01", "single player"]:
        print("\nYou're playing as " + game_choice)
        print("Let's Start the game.!!!")
        print("=" * 50)
        player_name = input("First Please enter your name: ")

        # Reset leader to Player for first round
        current_leader = "Player"

        # Play 8 rounds (each player starts with 8 cards)
        for round_num in range(1, 9):
            current_leader = play_round(round_num, current_leader)

            # Check if game is over
            if round_num == 8:
                print(f"\n{'=' * 60}")
                print("GAME OVER!")
                print(f"{'=' * 60}")

                # Display final scores
                print("\nFINAL SCORES:")
                print("-" * 30)
                for player_key, tricks in tricks_won.items():
                    if player_key == "Player":
                        disp_name = player_name
                    else:
                        disp_name = player_key
                    print(f"{disp_name}: {tricks} tricks")

                # Determine final winner
                max_tricks = max(tricks_won.values())
                winners = []
                for player_key, tricks in tricks_won.items():
                    if tricks == max_tricks:
                        if player_key == "Player":
                            winners.append(player_name)
                        else:
                            winners.append(player_key)

                if len(winners) == 1:
                    print(f"\n🎉 CONGRATULATIONS! WINNER: {winners[0]} with {max_tricks} tricks! 🎉")
                else:
                    print(f"\nIt's a tie between {', '.join(winners)} with {max_tricks} tricks each!")

                # Ask to play again
                play_again = input("\nDo you want to play again? (yes/no): ")
                if play_again.lower() in ["yes", "y"]:
                    # Reset game
                    tricks_won.update({"Player": 0, "AI_1": 0, "AI_2": 0, "AI_3": 0})
                    current_leader = "Player"
                    shuffle_cards()
                    give_cards()
                    play_cards("Single Player")
                else:
                    print(f"\nThanks for playing, {player_name}!")
                    break


def main():
    """Main game function"""
    print("WELCOME TO THE CARD GAME!")
    print("=" * 50)

    while True:
        print("\nMAIN MENU")
        print("1. Single Player (vs 3 AI)")
        print("2. How to Play")
        print("3. Exit")

        choice = input("\nEnter your choice (1-3): ")

        if choice in ["1", "01"]:
            shuffle_cards()
            give_cards()
            play_cards("Single Player")
        elif choice == "2":
            print("\nHOW TO PLAY:")
            print("- The game is played with 4 players (you vs 3 AI)")
            print("- Each player gets 8 cards")
            print("- After receiving 4 cards, you choose the trump suit")
            print("- Trump suit cards beat other suits")
            print("- You must follow the suit of the first card played if possible")
            print("- The player who wins a trick leads the next round")
            print("- The player with the most tricks at the end wins!")
            input("\nPress Enter to continue...")
        elif choice == "3":
            print("Thank you for playing! Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


# Start the game
if __name__ == "__main__":
    main()