# Python Word Game

## Overview

This project implements a text-based, multiplayer word game designed to be played in the terminal. Players draw letter cards from a custom deck, form words to score points, and aim to be the first to empty their hand or have the highest score when the game concludes. The game includes features like variable letter point values, letter frequencies, and the use of joker cards.

## Features

* **Custom Deck:** A deck is generated with specific frequencies and point values for letters (including common vowels, common consonants, rare consonants, and multiple joker cards).
* **Card Management:** Players can draw cards from the deck and play words using the cards in their hand.
* **Joker Support:** Joker cards (represented by `JOKER` in hand and `_` when playing a word) can be used as any letter.
* **Scoring System:** Points are awarded based on the letter values of the cards used in a valid word.
* **Multiplayer Gameplay:** Supports multiple players who take turns.
* **Win Condition:** The game ends when a player successfully plays all cards from their hand. Remaining points in other players' hands are subtracted from their scores at the end of the game.

## How to Play

1.  **Run the Game:** Execute the `scramble_main.py` script from your terminal.
2.  **Enter Player Names:** You will be prompted to enter the names of the players, separated by commas.
3.  **Draw/Play:** Each player starts with 7 cards. On your turn, you can either:
    * Type a `word` using the letters in your hand (use `_` for a joker).
    * Type `DRAW` to pick an additional card from the deck.
4.  **Scoring:** Points are automatically calculated and added to your score when you play a valid word.
5.  **Winning:** The game continues until one player successfully plays all cards from their hand. That player wins, and remaining points in other players' hands are deducted.

## Installation and Setup

This project uses standard Python libraries. No external dependencies are required.

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YourUsername/Python-Word-Game.git](https://github.com/YourUsername/Python-Word-Game.git)
    cd Python-Word-Game
    ```
    (Replace `YourUsername` and `Python-Word-Game` with your actual GitHub username and repository name.)

2.  **Ensure you have Python installed:**
    This game requires Python 3. You can check your Python version with:
    ```bash
    python --version
    # or
    python3 --version
    ```

## How to Run

Execute the main script from your terminal:

```bash
python scramble_main.py
# or
python3 scramble_main.py