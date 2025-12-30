import random
import os
import time
import re
from typing import List, Tuple, Dict


# ANSI color codes for better visuals
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BG_RED = '\033[101m'
    BG_GREEN = '\033[102m'
    BG_BLUE = '\033[104m'


# Card symbols with colors
SUIT_SYMBOLS = {
    "Hearts": f"{Colors.RED}♥{Colors.RESET}",
    "Diamonds": f"{Colors.RED}♦{Colors.RESET}",
    "Clubs": f"{Colors.WHITE}♣{Colors.RESET}",
    "Spades": f"{Colors.WHITE}♠{Colors.RESET}"
}

# Game state
suits = {
    "Hearts": ["♥2", "♥3", "♥4", "♥5", "♥6", "♥7", "♥8", "♥9", "♥10", "♥J", "♥K", "♥Q", "♥A"],
    "Diamonds": ["♦2", "♦3", "♦4", "♦5", "♦6", "♦7", "♦8", "♦9", "♦10", "♦J", "♦K", "♦Q", "♦A"],
    "Clubs": ["♣2", "♣3", "♣4", "♣5", "♣6", "♣7", "♣8", "♣9", "♣10", "♣J", "♣K", "♣Q", "♣A"],
    "Spades": ["♠2", "♠3", "♠4", "♠5", "♠6", "♠7", "♠8", "♠9", "♠10", "♠J", "♠K", "♠Q", "♠A"]
}

player_name = ""
trump = ""
player = []
AI_1 = []
AI_2 = []
AI_3 = []
tricks_won = {"Player": 0, "AI_1": 0, "AI_2": 0, "AI_3": 0}
Cards = []
current_leader = "Player"


def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(text: str, color=Colors.CYAN):
    """Print a styled header"""
    width = 70
    print(f"\n{color}{'═' * width}")
    print(f"║{text.center(width - 2)}║")
    print(f"{'═' * width}{Colors.RESET}\n")


def print_box(text: str, color=Colors.BLUE):
    """Print text in a box"""
    lines = text.split('\n')
    max_length = max(len(line) for line in lines)
    print(f"{color}┌{'─' * (max_length + 2)}┐")
    for line in lines:
        print(f"│ {line.ljust(max_length)} │")
    print(f"└{'─' * (max_length + 2)}┘{Colors.RESET}")


def clean_ansi_codes(text: str) -> str:
    """Remove ANSI escape sequences from text"""
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)


def colorize_card(card: str) -> str:
    """Add color to card display"""
    clean_card = clean_ansi_codes(card)
    if '♥' in clean_card or '♦' in clean_card:
        return f"{Colors.RED}{card}{Colors.RESET}"
    return f"{Colors.WHITE}{card}{Colors.RESET}"


def display_cards_grid(cards: List[str], title: str = "Your Cards"):
    """Display cards in a nice grid format"""
    print(f"\n{Colors.BOLD}{Colors.YELLOW}╔{'═' * 60}╗")
    print(f"║{title.center(60)}║")
    print(f"╚{'═' * 60}╝{Colors.RESET}\n")

    # Display cards in rows of 4
    for i in range(0, len(cards), 4):
        row = cards[i:i + 4]
        print("  ", end="")
        for idx, card in enumerate(row):
            card_num = i + idx + 1
            print(f"{Colors.CYAN}[{card_num}]{Colors.RESET} {colorize_card(card)}".ljust(25), end="")
        print()
    print()


def animated_text(text: str, delay: float = 0.03):
    """Print text with animation effect"""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()


# Initialize deck
for i in range(5, 13):
    Cards.append(suits["Hearts"][i])
    Cards.append(suits["Diamonds"][i])
    Cards.append(suits["Clubs"][i])
    Cards.append(suits["Spades"][i])


def shuffle_cards():
    """Shuffle the deck with user input"""
    print_header("SHUFFLING DECK", Colors.MAGENTA)

    while True:
        try:
            user_in = input(f"{Colors.CYAN}How many times would you like to shuffle? (4-10): {Colors.RESET}")
            user_in = int(user_in)
            if 4 <= user_in <= 10:
                print(f"\n{Colors.YELLOW}Shuffling", end="")
                for i in range(user_in):
                    random.shuffle(Cards)
                    print(".", end="", flush=True)
                    time.sleep(0.3)
                print(f" Done! ✓{Colors.RESET}\n")
                time.sleep(0.5)
                break
            else:
                print(f"{Colors.RED}Please enter a number between 4 and 10{Colors.RESET}")
        except ValueError:
            print(f"{Colors.RED}Please enter a valid number.{Colors.RESET}")


def give_cards():
    """Deal cards to all players"""
    global trump, player, AI_1, AI_2, AI_3

    player.clear()
    AI_1.clear()
    AI_2.clear()
    AI_3.clear()

    print_header("DEALING CARDS", Colors.GREEN)
    animated_text("Dealing cards to all players...")

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

        if j == 16 and not got_trumps:
            clear_screen()
            display_cards_grid(player, "Your First 4 Cards")

            print_header("CHOOSE TRUMP SUIT", Colors.YELLOW)
            print(f"{Colors.BOLD}Trump cards will beat all other suits!{Colors.RESET}\n")

            options = [
                f"[1] {Colors.RED}Hearts   ♥{Colors.RESET}",
                f"[2] {Colors.WHITE}Clubs    ♣{Colors.RESET}",
                f"[3] {Colors.RED}Diamonds ♦{Colors.RESET}",
                f"[4] {Colors.WHITE}Spades   ♠{Colors.RESET}"
            ]

            for opt in options:
                print(f"  {opt}")

            while True:
                choice = input(f"\n{Colors.CYAN}Select trump suit (1-4): {Colors.RESET}").strip()

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
                    print(f"{Colors.RED}Invalid choice. Please enter 1, 2, 3, or 4{Colors.RESET}")

            symbol_map = {"Hearts": "♥", "Clubs": "♣", "Diamonds": "♦", "Spades": "♠"}
            color = Colors.RED if trump in ["Hearts", "Diamonds"] else Colors.WHITE
            print(f"\n{Colors.GREEN}✓ Trump suit selected: {color}{trump} {symbol_map[trump]}{Colors.RESET}")
            got_trumps = True
            time.sleep(1.5)


def get_card_value(card: str) -> int:
    """Get numeric value of card for comparison"""
    clean_card = clean_ansi_codes(card)
    value = clean_card[1:] if len(clean_card) > 1 else ""
    value_map = {"A": 14, "K": 13, "Q": 12, "J": 11}

    if value == "10":
        return 10
    elif value in value_map:
        return value_map[value]
    elif value and value[0].isdigit():
        return int(value[0])
    return 0


def get_card_suit(card: str) -> str:
    """Get suit of a card"""
    clean_card = clean_ansi_codes(card)
    if not clean_card:
        return None

    suit_map = {"♥": "Hearts", "♦": "Diamonds", "♣": "Clubs", "♠": "Spades"}
    return suit_map.get(clean_card[0], None)


def ai_choose_card(ai_hand: List[str], first_card: str = None, trump_suit: str = None) -> str:
    """Enhanced AI logic to choose a card"""
    if not ai_hand:
        return None

    if first_card is None:
        return random.choice(ai_hand)

    first_card_suit = get_card_suit(first_card)
    same_suit = [c for c in ai_hand if get_card_suit(c) == first_card_suit]

    if same_suit:
        return random.choice(same_suit)

    if trump_suit:
        trump_cards = [c for c in ai_hand if get_card_suit(c) == trump_suit]
        if trump_cards:
            return random.choice(trump_cards)

    return random.choice(ai_hand)


def determine_round_winner(cards_played: List[Tuple[str, str]], trump_suit: str, first_card_index: int) -> int:
    """Determine who won the round"""
    if not cards_played or first_card_index >= len(cards_played):
        return first_card_index

    first_card = cards_played[first_card_index][1]
    first_suit = get_card_suit(first_card)

    # Find all valid cards (trump or same suit as first card)
    valid_cards = []
    for i, (player_name, card) in enumerate(cards_played):
        card_suit = get_card_suit(card)
        if card_suit is not None:  # Ensure we have a valid suit
            if card_suit == trump_suit or card_suit == first_suit:
                valid_cards.append((i, player_name, card, get_card_value(card), card_suit))

    if not valid_cards:
        return first_card_index

    # Sort: trump cards first, then by value (highest first)
    # x[4] != trump_suit: True for non-trump (1), False for trump (0)
    # So trumps (0) come before non-trumps (1)
    # Then sort by value descending (highest value first)
    valid_cards.sort(key=lambda x: (x[4] != trump_suit, -x[3]))
    return valid_cards[0][0]


def play_round(round_num: int, leader: str) -> str:
    """Play one round with enhanced UI"""
    clear_screen()

    print_header(f"ROUND {round_num} OF 8", Colors.CYAN)

    leader_display = player_name if leader == "Player" else leader
    print(f"{Colors.BOLD}Leader: {Colors.YELLOW}{leader_display}{Colors.RESET}")
    print(f"{Colors.BOLD}Trump: {colorize_card(trump[0])} {trump}{Colors.RESET}\n")

    played_cards = []
    players_order = []

    if leader == "Player":
        players_order = [("Player", player), ("AI_1", AI_1), ("AI_2", AI_2), ("AI_3", AI_3)]
    elif leader == "AI_1":
        players_order = [("AI_1", AI_1), ("AI_2", AI_2), ("AI_3", AI_3), ("Player", player)]
    elif leader == "AI_2":
        players_order = [("AI_2", AI_2), ("AI_3", AI_3), ("Player", player), ("AI_1", AI_1)]
    elif leader == "AI_3":
        players_order = [("AI_3", AI_3), ("Player", player), ("AI_1", AI_1), ("AI_2", AI_2)]

    first_card = None
    first_player_index = 0

    for idx, (player_key, player_hand) in enumerate(players_order):
        display_name = player_name if player_key == "Player" else player_key

        if player_key == "Player":
            display_cards_grid(player, f"{player_name}'s Hand")

            if played_cards:
                print(f"{Colors.BOLD}Cards Played:{Colors.RESET}")
                for name_key, card in played_cards:
                    disp = player_name if name_key == "Player" else name_key
                    print(f"  {Colors.CYAN}{disp}:{Colors.RESET} {colorize_card(card)}")
                print()

            while True:
                try:
                    choice = input(f"{Colors.GREEN}Choose your card (1-{len(player)}): {Colors.RESET}")
                    choice = int(choice)
                    if 1 <= choice <= len(player):
                        player_card = player[choice - 1]
                        print(f"\n{Colors.YELLOW}You played: {colorize_card(player_card)}{Colors.RESET}")
                        played_cards.append((player_key, player_card))
                        player.remove(player_card)

                        if idx == 0:
                            first_card = player_card
                            first_player_index = 0
                        time.sleep(1)
                        break
                    else:
                        print(f"{Colors.RED}Please enter a number between 1 and {len(player)}{Colors.RESET}")
                except ValueError:
                    print(f"{Colors.RED}Please enter a valid number.{Colors.RESET}")
        else:
            print(f"\n{Colors.CYAN}{display_name} is thinking...{Colors.RESET}")
            time.sleep(1)

            ai_card = ai_choose_card(player_hand, first_card, trump)
            if ai_card:
                print(f"{Colors.YELLOW}{display_name} played: {colorize_card(ai_card)}{Colors.RESET}")
                played_cards.append((player_key, ai_card))
                player_hand.remove(ai_card)

                if idx == 0:
                    first_card = ai_card
                    first_player_index = idx
                time.sleep(1)

    winner_index = determine_round_winner(played_cards, trump, first_player_index)
    winner_key = played_cards[winner_index][0]
    tricks_won[winner_key] += 1

    print(f"\n{Colors.BOLD}{'─' * 50}{Colors.RESET}")
    print(f"{Colors.BOLD}ROUND SUMMARY:{Colors.RESET}")
    print(f"{Colors.BOLD}{'─' * 50}{Colors.RESET}")

    for name_key, card in played_cards:
        disp = player_name if name_key == "Player" else name_key
        marker = " 👑" if name_key == winner_key else ""
        print(f"  {Colors.CYAN}{disp}:{Colors.RESET} {colorize_card(card)}{marker}")

    display_winner = player_name if winner_key == "Player" else winner_key
    print(f"\n{Colors.GREEN}🎯 Round Winner: {Colors.BOLD}{display_winner}!{Colors.RESET}")

    print(f"\n{Colors.BOLD}Tricks Won:{Colors.RESET}")
    for player_key, tricks in tricks_won.items():
        disp = player_name if player_key == "Player" else player_key
        bar = "█" * tricks
        print(f"  {disp}: {Colors.YELLOW}{bar}{Colors.RESET} {tricks}")

    input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")
    return winner_key


def play_cards(game_choice: str):
    """Main game loop with enhanced UI"""
    global player_name, current_leader

    clear_screen()
    print_header("NEW GAME", Colors.GREEN)
    player_name = input(f"{Colors.CYAN}Enter your name: {Colors.RESET}").strip() or "Player"

    animated_text(f"\nWelcome, {player_name}! Let's begin...")
    time.sleep(1)

    current_leader = "Player"

    for round_num in range(1, 9):
        current_leader = play_round(round_num, current_leader)

        if round_num == 8:
            clear_screen()
            print_header("GAME OVER", Colors.MAGENTA)

            max_tricks = max(tricks_won.values())
            print(f"{Colors.BOLD}FINAL SCORES:{Colors.RESET}\n")

            for player_key, tricks in sorted(tricks_won.items(), key=lambda x: -x[1]):
                disp = player_name if player_key == "Player" else player_key
                bar = "█" * tricks
                print(f"  {disp}: {Colors.YELLOW}{bar}{Colors.RESET} {tricks} tricks")

            winners = [player_name if k == "Player" else k for k, v in tricks_won.items() if v == max_tricks]

            if len(winners) == 1:
                print(f"\n{Colors.GREEN}{'🎉' * 20}")
                print(f"{Colors.BOLD}WINNER: {winners[0].upper()} with {max_tricks} tricks!{Colors.RESET}")
                print(f"{Colors.GREEN}{'🎉' * 20}{Colors.RESET}\n")
            else:
                print(f"\n{Colors.YELLOW}It's a tie between {', '.join(winners)}!{Colors.RESET}\n")

            play_again = input(f"{Colors.CYAN}Play again? (yes/no): {Colors.RESET}").strip().lower()
            if play_again in ["yes", "y"]:
                tricks_won.update({"Player": 0, "AI_1": 0, "AI_2": 0, "AI_3": 0})
                current_leader = "Player"
                shuffle_cards()
                give_cards()
                play_cards("Single Player")
            else:
                clear_screen()
                print_header("THANKS FOR PLAYING!", Colors.GREEN)
                print(f"\n{Colors.CYAN}Goodbye, {player_name}! 👋{Colors.RESET}\n")
                break


def main():
    """Main menu with enhanced UI"""
    while True:
        clear_screen()
        print(f"{Colors.BOLD}{Colors.CYAN}")
        print("╔═══════════════════════════════════════════════════════════════╗")
        print("║                                                               ║")
        print("║              🎴  TRICK-TAKING CARD GAME  🎴                   ║")
        print("║                                                               ║")
        print("╚═══════════════════════════════════════════════════════════════╝")
        print(Colors.RESET)

        print(f"{Colors.BOLD}MAIN MENU{Colors.RESET}\n")
        print(f"  {Colors.GREEN}[1]{Colors.RESET} Start New Game (vs 3 AI)")
        print(f"  {Colors.YELLOW}[2]{Colors.RESET} How to Play")
        print(f"  {Colors.RED}[3]{Colors.RESET} Exit Game\n")

        choice = input(f"{Colors.CYAN}Select option (1-3): {Colors.RESET}").strip()

        if choice in ["1", "01"]:
            shuffle_cards()
            give_cards()
            play_cards("Single Player")
        elif choice in ["2", "02"]:
            clear_screen()
            print_header("HOW TO PLAY", Colors.YELLOW)
            rules = """
OBJECTIVE:
Win the most tricks to become the champion!

GAME SETUP:
• 4 players total (You + 3 AI opponents)
• Each player receives 8 cards
• After receiving 4 cards, YOU choose the trump suit

GAMEPLAY:
• Trump cards beat all other suits
• You must follow the suit of the first card if possible
• If you can't follow suit, you may play a trump or any card
• Highest card of the leading suit wins (unless trumped)
• Winner of each trick leads the next round

WINNING:
• The player with the most tricks at the end wins!
• In case of a tie, all tied players share victory

TIPS:
• Save your high trump cards for crucial moments
• Pay attention to which cards have been played
• Lead with strong cards when you have the advantage
            """
            print(rules)
            input(f"\n{Colors.CYAN}Press Enter to return to menu...{Colors.RESET}")
        elif choice in ["3", "03"]:
            clear_screen()
            print_header("GOODBYE!", Colors.MAGENTA)
            print(f"{Colors.CYAN}Thanks for playing! Come back soon! 👋{Colors.RESET}\n")
            break
        else:
            print(f"{Colors.RED}Invalid choice. Please enter 1, 2, or 3.{Colors.RESET}")
            time.sleep(1.5)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear_screen()
        print(f"\n{Colors.YELLOW}Game interrupted. Goodbye!{Colors.RESET}\n")
    except Exception as e:
        print(f"\n{Colors.RED}An error occurred: {e}{Colors.RESET}\n")