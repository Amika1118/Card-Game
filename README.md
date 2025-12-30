# 🎴 Trick-Taking Card Game

A professional, terminal-based card game built with Python featuring an enhanced user interface, AI opponents, and strategic trick-taking gameplay.

![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-success)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [How to Play](#how-to-play)
- [Game Rules](#game-rules)
- [Screenshots](#screenshots)
- [Technical Details](#technical-details)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## 🎮 Overview

This is a classic trick-taking card game where you compete against three AI opponents. The game features a beautiful terminal interface with color-coded cards, animated effects, and strategic gameplay that will challenge your card-playing skills.

## ✨ Features

- **Beautiful Terminal UI**: Color-coded cards, ASCII art borders, and smooth animations
- **Smart AI Opponents**: Three AI players with strategic card-playing logic
- **Trump System**: Choose your trump suit for strategic advantage
- **Real-time Scoring**: Visual progress bars and live trick counts
- **Professional Design**: Clean menus, clear instructions, and intuitive gameplay
- **Error Handling**: Robust input validation and user-friendly error messages
- **Replay Option**: Play multiple rounds without restarting the program

## 🚀 Installation

### Prerequisites

- Python 3.6 or higher
- Terminal that supports ANSI color codes (most modern terminals)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Amika1118/Card-Game.git
cd Card-Game
```

2. Run the game:
```bash
python Game.py
```

No additional dependencies required - uses only Python standard library!

## 🎯 How to Play

1. **Start the Game**: Choose "Start New Game" from the main menu
2. **Enter Your Name**: Personalize your gaming experience
3. **Shuffle the Deck**: Select how many times to shuffle (4-10)
4. **Choose Trump**: After receiving 4 cards, select the trump suit
5. **Play Cards**: Follow suit when possible, or play trump cards strategically
6. **Win Tricks**: Highest card of the leading suit wins (unless trumped)
7. **Victory**: Player with the most tricks after 8 rounds wins!

## 📜 Game Rules

### Basic Rules

- **Players**: 4 (You + 3 AI opponents)
- **Cards per Player**: 8 cards each
- **Rounds**: 8 rounds total
- **Deck**: Standard 52-card deck (cards 6-A used)

### Gameplay Mechanics

1. **Following Suit**: You must play a card of the same suit as the leading card if you have one
2. **Trump Cards**: Trump suit cards beat all other suits
3. **Winning Tricks**: Highest card of the leading suit wins, unless a trump card is played
4. **Leading**: The winner of each trick leads the next round
5. **Scoring**: Each trick won counts as one point

### Strategy Tips

- 💡 Save high trump cards for crucial moments
- 💡 Remember which cards have been played
- 💡 Lead with strong cards when you control the round
- 💡 Use trump cards wisely to win important tricks

## 📸 Screenshots

```
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║              🎴  TRICK-TAKING CARD GAME  🎴                   ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

*Beautiful card display with color-coded suits and organized layout*

## 🔧 Technical Details

### File Structure

```
trick-taking-card-game/
│
├── Game.py              # Main game file
├── README.md            # This file
└── LICENSE              # License information
```

### Key Components

- **Colors Class**: ANSI color codes for terminal styling
- **Card Management**: Shuffle, deal, and display functions
- **AI Logic**: Smart card selection based on game state
- **Round Management**: Turn order, winner determination, and scoring
- **UI Functions**: Headers, boxes, grids, and animations

### Code Highlights

- Type hints for better code documentation
- Modular function design for easy maintenance
- Clear separation of concerns (UI, game logic, AI)
- Robust error handling and input validation

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Ideas for Contributions

- Add multiplayer support (local network)
- Implement different game modes
- Add sound effects
- Create a GUI version
- Add more AI difficulty levels
- Implement save/load game functionality

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Contact

**Amika Alankara**

- Email: amikaranmeth085@gmail.com
- GitHub: [@Amika1118](https://github.com/Amika1118)
- Repository: [Card-Game](https://github.com/Amika1118/Card-Game)

## 🙏 Acknowledgments

- Thanks to the Python community for excellent documentation
- Inspired by classic trick-taking card games
- Built with passion for terminal-based gaming

## 📈 Version History

- **v1.0.0** (Current)
  - Initial release
  - Full game functionality
  - Professional UI
  - AI opponents
  - Trump system

---

⭐ If you enjoyed this game, please consider giving it a star on GitHub!

Made with ❤️ by Amika Alankara
