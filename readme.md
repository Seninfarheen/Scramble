# My Python Word Game

This repository contains a simple word game developed in Python, demonstrating both a console-based version and a modern web application built with Streamlit.

## Project Overview

This game allows players to draw letter cards and form valid English words to score points. The goal is to be the first to clear your hand of cards. Jokers act as wildcards.

## Two Ways to Play:

This project offers two distinct ways to experience the game:

### 1. Web Application (Streamlit)

`app.py` is the Streamlit-powered web application version of the game. It provides a graphical user interface (GUI) that runs in your web browser, making it more interactive and visually appealing.

**Live Demo:** [https://scramble-senin.streamlit.app/](https://scramble-senin.streamlit.app/)


**Features:**
* Interactive user interface with turn-based gameplay.
* Clear display of player hands and scores.
* Real-time feedback on word validity and card availability.
* Automatic handling of Joker cards as wildcards (if available in hand).
* Easy turn management (Play Word / Draw Card).
* Automatic clearing of input fields and turn progression.
* Game over screen with final scores.

**How to Run the Web App Locally:**

1.  **Ensure you have Python installed.**
2.  **Install Streamlit:**
    ```bash
    pip install streamlit
    ```
3.  **Make sure you have the `words.txt` file** (containing a list of valid English words) in the same directory as `app.py`.
4.  **Navigate to your project directory** in your terminal.
5.  **Run the Streamlit app:**
    ```bash
    streamlit run app.py
    ```
    Your browser should automatically open to the app.

---

### 2. Console-Based Game

`scramble_main.py` is the original command-line interface (CLI) version of the game. It runs directly in your terminal, providing a text-based interactive experience.

**Features:**
* Text-based gameplay in the terminal.
* Basic turn-based interaction.
* Fundamental game logic (drawing cards, playing words, scoring).
* Supports Joker card usage (by typing `_` in place of the joker letter).

**How to Run the Console Game Locally:**

1.  **Ensure you have Python installed.**
2.  **Make sure you have the `words.txt` file** (containing a list of valid English words) in the same directory as `scramble_main.py`.
3.  **Navigate to your project directory** in your terminal.
4.  **Run the Python script:**
    ```bash
    python scramble_main.py
    ```
    Follow the prompts in your terminal.

---

## Requirements

To run either version of the game, you'll need:

* Python 3.x
* A `words.txt` file containing a list of valid English words. This word list is sourced from [dwyl/english-words](https://github.com/dwyl/english-words/blob/master/words.txt).

For the **Streamlit Web App** (`app.py`), you also need:

* `streamlit` library (install via `pip install streamlit`)

The `requirements.txt` file in this repository lists the necessary Python packages for the Streamlit app.

---

## Files in this Repository

* `app.py`: The main Streamlit web application.
* `scramble_main.py`: The original console-based game script.
* `words.txt`: The dictionary file used for word validation.
* `requirements.txt`: Lists Python dependencies for Streamlit deployment.

---