import streamlit as st
import random

# --- Your existing Card, Deck, Player, WordGame classes go here ---
# (Paste the full content of your Card, Deck, Player, WordGame classes here from scramble_main.py)

class Card:
    def __init__(self, letter, points):
        self.letter = letter
        self.points = points

    def __str__(self):
        return self.letter

class Deck:
    def __init__(self):
        self.cards = []
        self.create_deck()

    def create_deck(self):
        letters_points = {
            'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2,
            'H': 4, 'I': 1, 'J': 8, 'K': 5, 'L': 1, 'M': 3, 'N': 1,
            'O': 1, 'P': 3, 'Q': 10, 'R': 1, 'S': 1, 'T': 1, 'U': 1,
            'V': 4, 'W': 4, 'X': 8, 'Y': 4, 'Z': 10
        }

        vowels = ['A', 'E', 'I', 'O', 'U']
        for vowel in vowels:
            for _ in range(6):
                self.cards.append(Card(vowel, letters_points[vowel]))

        common_consonants = ['R', 'S', 'T', 'L', 'N', 'B', 'C', 'D', 'F', 'G', 'H', 'K', 'M', 'P']
        for letter in common_consonants:
            for _ in range(4):
                self.cards.append(Card(letter, letters_points[letter]))

        rare_consonants = ['Q', 'X', 'Z', 'V', 'W', 'Y', 'J']
        for letter in rare_consonants:
            for _ in range(1):
                self.cards.append(Card(letter, letters_points[letter]))

        for _ in range(6):
            self.cards.append(Card('JOKER', 0))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop() if self.cards else None

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.score = 0

    def draw_card(self, deck):
        card = deck.deal_card()
        if card:
            self.hand.append(card)
            return True
        return False

    def play_word(self, word, game_word_list): # game_word_list is the set of valid dictionary words
        word_upper = word.upper()

        # 1. First, check if the word exists in the dictionary.
        if word_upper not in game_word_list:
            return 0, "not_in_dictionary" # Word is not recognized

        # 2. Check if the player has the necessary cards (using actual letters or jokers).
        temp_hand_letters = [card.letter for card in self.hand] # Get letters from current hand
        joker_count = temp_hand_letters.count('JOKER') # Count available jokers
        
        letters_needed_for_word = list(word_upper) # Letters required for the input word
        
        # Simulate taking cards from hand (first pass to check if word can be formed)
        can_form_word = True
        
        for letter in letters_needed_for_word:
            if letter in temp_hand_letters:
                temp_hand_letters.remove(letter) # Use actual letter
            elif joker_count > 0: # If exact letter not found, try to use a joker
                joker_count -= 1 # Use a joker
            else:
                can_form_word = False
                break # Cannot form the word, ran out of letters/jokers

        if not can_form_word:
            return 0, "not_enough_cards" # Player doesn't have the cards for this word

        # 3. If word is valid and can be formed, now actually remove cards and calculate points
        points = 0
        actual_jokers_used = 0
        
        # Make a copy of the hand to modify and then replace the original
        current_hand_copy = list(self.hand) 

        # Iterate through letters needed and remove from hand, calculating points
        for letter_needed in letters_needed_for_word:
            card_removed = False
            # Try to use an exact letter card first
            for i, card in enumerate(current_hand_copy):
                if card.letter == letter_needed:
                    points += card.points
                    current_hand_copy.pop(i) # Remove the actual Card object
                    card_removed = True
                    break
            
            # If exact letter card not found, use a joker if available
            if not card_removed:
                for i, card in enumerate(current_hand_copy):
                    if card.letter == 'JOKER':
                        # Jokers have 0 points
                        current_hand_copy.pop(i) # Remove the actual Joker Card object
                        actual_jokers_used += 1
                        card_removed = True
                        break
        
        # Update player's hand and score
        self.hand = current_hand_copy
        self.score += points

        if actual_jokers_used > 0:
            return points, "played_with_jokers"
        else:
            return points, "played_successfully"

    def remaining_points(self):
        return sum(card.points for card in self.hand)

    def __str__(self):
        return f"{self.name}: {' '.join(str(card) for card in self.hand)} (Score: {self.score})"

class WordGame:
    def __init__(self):
        self.deck = Deck()
        self.players = []
        self.word_list = self.load_dictionary("words.txt") # Call this to load the dictionary

    def load_dictionary(self, filepath):
        try:
            with open(filepath, 'r') as f:
                # Load words, convert to uppercase, strip whitespace, and store in a set
                words = {word.strip().upper() for word in f if word.strip()}
            st.success(f"Dictionary loaded successfully with {len(words)} words.")
            return words
        except FileNotFoundError:
            st.error(f"Error: Dictionary file '{filepath}' not found. Word validation will be skipped.")
            return set() # Return an empty set if file not found

    def setup_game(self, player_names):
        self.deck.shuffle()
        for name in player_names:
            player = Player(name.strip())
            for _ in range(7):
                player.draw_card(self.deck)
            self.players.append(player)

    def calculate_remaining_scores(self, winner_name):
        summary_messages = []
        for player in self.players:
            if player.name != winner_name:
                remaining_points = player.remaining_points()
                summary_messages.append(f"{player.name} had {remaining_points} points left in hand.")
        return summary_messages


# --- Streamlit Application Logic ---
def update_word_input_state():
    st.session_state.current_word_input = st.session_state.word_input_play_turn_key

# Initialize game state in Streamlit's session_state
if 'game' not in st.session_state:
    st.session_state.game = WordGame()
    st.session_state.current_player_index = 0
    st.session_state.game_started = False
    st.session_state.player_names_input = ""
    st.session_state.feedback_message = "Enter player names to start the game."
    st.session_state.game_over = False
    st.session_state.final_summary = []
    st.session_state.current_word_input = "" # NEW: To store the text input's live value

st.title("Python Word Game")
st.write("Welcome to the Word Game!")
st.write("Each player takes turns to either play a word using their cards or pick a card.")
st.write("You can use a 'JOKER' card as any letter.")
st.write("The game ends when a player runs out of cards. The player with the highest score wins!")


# Display general feedback message at the top, if any
if st.session_state.feedback_message:
    st.info(st.session_state.feedback_message)
    st.session_state.feedback_message = "" # Clear after displaying

# Game Setup Phase
if not st.session_state.game_started:
    st.session_state.player_names_input = st.text_input("Enter player names separated by commas (e.g., Alice, Bob):", value=st.session_state.player_names_input, key="player_names_input_setup")
    if st.button("Start Game"):
        if st.session_state.player_names_input:
            player_names = [name.strip() for name in st.session_state.player_names_input.split(',') if name.strip()]
            if player_names:
                st.session_state.game.setup_game(player_names)
                st.session_state.game_started = True
                st.session_state.feedback_message = f"Game started! It's {st.session_state.game.players[st.session_state.current_player_index].name}'s turn."
                st.rerun() # Rerun to switch to game play interface
            else:
                st.session_state.feedback_message = "Please enter at least one valid player name."
        else:
            st.session_state.feedback_message = "Player names cannot be empty."

# Game Play Phase
elif not st.session_state.game_over:
    current_player = st.session_state.game.players[st.session_state.current_player_index]
    st.header(f"✨ {current_player.name}'s Turn! ✨") # More prominent turn announcement
    st.write(f"Your hand: **{' '.join(str(card) for card in current_player.hand)}**")
    st.write(f"Your score: **{current_player.score}**")

    # The word input box, controlled by session_state.word_input_value
    word_input = st.text_input(
    "Enter a valid English word to play (jokers will be used from your hand if the letter is not present):",
    value=st.session_state.current_word_input, # Use the session state value
    key="word_input_play_turn_key", # Changed key name slightly for clarity
    on_change=update_word_input_state # Call this function when input changes
    )

    col1, col2 = st.columns(2) # Using columns for buttons side-by-side
    with col1:
        if st.button("Play Word", key="play_word_button"):
            # Clear textbox immediately for next render
            st.session_state.word_input_value = "" 

            if word_input.strip():
                points_gained, status = current_player.play_word(word_input.upper(), st.session_state.game.word_list)

                if status == "played_successfully" or status == "played_with_jokers":
                    st.success(f"Word '{word_input.upper()}' played for {points_gained} points!")
                    if status == "played_with_jokers":
                        st.info("Joker(s) used for this word!") # This message will reappear
                    
                    # Clear textbox after a successful play
                    st.session_state.current_word_input = ""
                    
                    # Check for win condition after playing word
                    if not current_player.hand:
                        st.session_state.game_over = True
                        st.session_state.feedback_message = f"🎉 **{current_player.name} wins with a score of {current_player.score}!** 🎉"
                        st.session_state.final_summary = st.session_state.game.calculate_remaining_scores(current_player.name)
                        st.rerun() # Rerun to show game over screen
                    else:
                        # Move to next player if game not over
                        st.session_state.current_player_index = (st.session_state.current_player_index + 1) % len(st.session_state.game.players)
                        st.session_state.feedback_message = f"It's now {st.session_state.game.players[st.session_state.current_player_index].name}'s turn."
                        st.rerun() # Rerun to update UI for next player

                elif status == "not_in_dictionary":
                    st.session_state.feedback_message = f" Word '{word_input.upper()}' is not a valid English word. Please try again. It's still your turn!"
                    # Player does NOT lose turn for invalid word - current_player_index is not advanced
                    st.rerun() # Rerun to display error message and clear textbox
                elif status == "not_enough_cards":
                    st.session_state.feedback_message = f" You don't have the cards for '{word_input.upper()}' (or enough jokers). Please try again. It's still your turn!"
                    # Player does NOT lose turn for not enough cards - current_player_index is not advanced
                    st.rerun() # Rerun to display error message and clear textbox

            else: # This handles the case where the user clicks "Play Word" with an empty textbox
                st.session_state.feedback_message = "Please enter a word to play, or Draw a Card."
                st.rerun() # Rerun to display error


    with col2:
        if st.button("Draw Card", key="draw_card_button"):
            st.session_state.word_input_value = "" # Clear textbox
            if current_player.draw_card(st.session_state.game.deck):
                st.success(f"{current_player.name} drew a card.")
            else:
                st.warning("Deck is empty! Cannot draw more cards.")

            # Move to next player after drawing
            st.session_state.current_player_index = (st.session_state.current_player_index + 1) % len(st.session_state.game.players)
            st.session_state.feedback_message = f"It's now {st.session_state.game.players[st.session_state.current_player_index].name}'s turn."
            st.rerun() # Always rerun to update UI for next player

# Game Over Phase
else: # st.session_state.game_over is True
    st.header("Game Over!")
    st.success(st.session_state.feedback_message) # Display winner message
    st.subheader("Final Scores:")
    # Sort players by score for clearer display
    sorted_players = sorted(st.session_state.game.players, key=lambda p: p.score, reverse=True)
    for player in sorted_players:
        st.write(f"**{player.name}**: {player.score} points")

    if st.session_state.final_summary:
        st.subheader("Remaining Hand Scores:")
        for msg in st.session_state.final_summary:
            st.write(msg)

    if st.button("Play Again?"):
        # Reset session state to restart the game
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun() # Rerun the script to re-initialize