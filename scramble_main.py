# Card class represents a single letter card with a point value.
class Card:
    def __init__(self, letter, points):
        self.letter = letter  
        self.points = points  

    def __str__(self):
        return self.letter  

# Deck class represents the collection of all cards in the game.
class Deck:
    def __init__(self):
        self.cards = []  
        self.create_deck()  

    def create_deck(self):
        # Dictionary to define points for each letter
        letters_points = {
            'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2,
            'H': 4, 'I': 1, 'J': 8, 'K': 5, 'L': 1, 'M': 3, 'N': 1,
            'O': 1, 'P': 3, 'Q': 10, 'R': 1, 'S': 1, 'T': 1, 'U': 1,
            'V': 4, 'W': 4, 'X': 8, 'Y': 4, 'Z': 10
        }

        # Add more vowels with higher frequency
        vowels = ['A', 'E', 'I', 'O', 'U']
        for vowel in vowels:
            for _ in range(6):  
                self.cards.append(Card(vowel, letters_points[vowel]))

        # Add common consonants with higher frequency
        common_consonants = ['R', 'S', 'T', 'L', 'N', 'B', 'C', 'D', 'F', 'G', 'H', 'K', 'M', 'P']
        for letter in common_consonants:
            for _ in range(4):  
                self.cards.append(Card(letter, letters_points[letter]))

        # Add rare consonants with lower frequency
        rare_consonants = ['Q', 'X', 'Z', 'V', 'W', 'Y', 'J']
        for letter in rare_consonants:
            for _ in range(1):  
                self.cards.append(Card(letter, letters_points[letter]))

        # Add 6 Joker cards, which can represent any letter
        for _ in range(6):
            self.cards.append(Card('JOKER', 0))  # Joker has 0 points

    def shuffle(self):
        random.shuffle(self.cards)  
    def deal_card(self):
        return self.cards.pop() if self.cards else None  

# Player class represents a player in the game with a hand of cards and a score.
class Player:
    def __init__(self, name):
        self.name = name  
        self.hand = []  
        self.score = 0  

    def draw_card(self, deck):
        card = deck.deal_card()  
        if card:
            self.hand.append(card)  

    def play_word(self, word):
        points = 0  # Points earned for the word
        used_jokers = 0  # Track how many jokers are used

        for letter in word:
            if letter == '_':  # If it's a joker (underscore)
                if used_jokers < self.hand.count('JOKER'):  # Check if the player has joker cards
                    points += 0  # Joker doesn't add points
                    used_jokers += 1  # Mark joker as used
                    self.hand.remove('JOKER')  # Remove one joker from the hand
                else:
                    print(f"Cannot play word '{word}', missing joker card.")
                    return 0  # Word is not valid
            else:
                for card in self.hand:
                    if card.letter == letter or card.letter == 'JOKER':  # Match the letter or joker
                        points += card.points
                        self.hand.remove(card)
                        break
                else:
                    print(f"Cannot play word '{word}', missing letter '{letter}'")  # If letter is not found
                    return 0  # Word is not valid

        self.score += points  # Add points to the player's score
        return points

    def remaining_points(self):
        return sum(card.points for card in self.hand)  # Calculate remaining points in hand

    def __str__(self):
        return f"{self.name}: {' '.join(str(card) for card in self.hand)} (Score: {self.score})"  # Display player's hand and score

# WordGame class manages the game flow, players, and deck.
class WordGame:
    def __init__(self):
        self.deck = Deck()  
        self.players = []  

    def setup_game(self, player_names):
        self.deck.shuffle()  # Shuffle the deck
        for name in player_names:
            player = Player(name.strip())  
            for _ in range(7):  
                player.draw_card(self.deck)
            self.players.append(player)

    def play_game(self):
        turn = 0  # Start with the first player
        while True:
            current_player = self.players[turn % len(self.players)]  
            print(f"\n{current_player.name}'s turn")  
            print(current_player)

            word = input("Enter a word to play (use '_' for joker) or 'draw' to pick a card: ").upper()  
            if word == 'DRAW':
                current_player.draw_card(self.deck)  
            else:
                points = current_player.play_word(word)  # Play the word and calculate points
                if points > 0:
                    print(f"Word '{word}' played for {points} points!")

            if not current_player.hand:  # If player has no cards left, they win
                print(f"\n{current_player.name} wins with a score of {current_player.score}!")
                self.calculate_remaining_scores(current_player)  # Calculate remaining points for other players
                break

            turn += 1  

    def calculate_remaining_scores(self, winner):
        for player in self.players:
            if player != winner:
                remaining_points = player.remaining_points()  # Calculate remaining points for losing players
                print(f"{player.name} loses with {remaining_points} points left in their hand!")

# Main block to start the game
if __name__ == "__main__":
    print("Welcome to the Word Game!")
    print("Each player takes turns to either play a word using their cards or type 'DRAW' to pick a card.")
    print("You can use a 'JOKER' card as any letter by typing '_' in place of the joker letter.")
    print("The game ends when a player runs out of cards. The player with the highest score wins!\n")
    
    player_names = input("Enter player names separated by commas: ").split(',')
    print(player_names)  
    game = WordGame()  
    game.setup_game([name.strip() for name in player_names])  
    game.play_game()  
