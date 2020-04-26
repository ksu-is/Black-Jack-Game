# Allows us to shuffle the deck randomly
import random

# Class representing playing cards. 
class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    # repr takes the object(s) and returns a string representation of the object(s)
    def __repr__(self):
        return " of ".join((self.value, self.suit))

# Deck class creates and contains the 52 cards that make up the deck & other methods that deals and shuffles the cards
class Deck:
    # List created with all 52 cards
    def __init__(self):
        self.cards = [Card(s, v) for s in ["Spades", "Clubs", "Hearts", "Diamonds"] for v in ["A", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K",]]
    
    # Shuffles deck if deck is greater than 1
    def shuffle(self):
        if len(self.cards) > 1:
            random.shuffle(self.cards)

    # Deals the card and pops it out of the list to prevent redealing of a used card    
    def deal(self):
        if len(self.cards) > 1:
            return self.cards.pop(0)

# Hand class contains values about player and dealer hands and betting banks
class Hand:
    def __init__(self, dealer = False):
        self.dealer = dealer
        self.cards = []
        self.value = 0
        self.bet_bank = 1000
        self.bet_amount = 0

    # Resets the hand to clean state
    def reset_hand(self):
        self.cards = []
        self.value = 0

    # Asks player amount to bet 
    def bet(self):
        print("You have this much to bet: ", self.bet_bank)
        bet_amount = int(input ("How much would you like to bet?"))
        if bet_amount > 0 and bet_amount <= self.bet_bank:
            self.bet_amount = int(bet_amount)
        else:
            while bet_amount <= 0 or bet_amount > self.bet_bank:
                print("Invalid bet. Must be greater than 0 or less than or equal to your bank amount.")
                bet_amount = int(input ("How much would you like to bet?"))
        self.bet_amount = int(bet_amount)

    # Calculates bet loss/gain after
    def calc_bet(self, win):
        if win:
            self.bet_bank += self.bet_amount
        elif win == False:
            self.bet_bank -= self.bet_amount
        self.bet_amount = 0

    # Add card to hand
    def add_card(self, card):
        self.cards.append(card)

    # Calculates the point value for cards in hand
    def calculate_value(self): 
        self.value = 0
        has_ace = False
        for card in self.cards:
            if card.value.isnumeric():
                self.value += int(card.value)
            else:
                if card.value == "A":
                    has_ace = True
                    self.value += 11
                else: 
                    self.value += 10
        if has_ace and self.value > 21:
            self.value -= 10
        
    # Returns value of cards in hand    
    def get_value(self):
        self.calculate_value()
        return self.value

    # Displays cards in hand
    def display(self, game_over):
        if game_over:
            if self.dealer:
                for card in self.cards:
                    print(card)
                print("Value:", self.get_value())
        else:
            if self.dealer:
                print ("hidden")
                print (self.cards[1])
            else: 
                for card in self.cards:
                    print(card)
                print("Value:", self.get_value())

# Contains the core gameplay
class Game: 
    def __init__(self):
        pass

    def play(self):
        playing = True

        # Starts the hand class and initializes variables for clean hand, betting bank of 1000
        self.player_hand = Hand()
        self.dealer_hand = Hand(dealer = True)

        # Loop to keep playing until game terminates
        while playing:
            self.player_hand.reset_hand()
            self.dealer_hand.reset_hand()
            self.deck = Deck()
            self.deck.shuffle()

            # Deal cards
            for i in range(2):
                self.player_hand.add_card(self.deck.deal())
                self.dealer_hand.add_card(self.deck.deal())

            game_over = False

            # Display player cards and 1 dealer card
            print ("Your hand is:")
            self.player_hand.display(game_over)
            print()
            print("Dealer's hand is:")
            self.dealer_hand.display(game_over)
            self.player_hand.bet() 

            # Checks for blackjack 
            while not game_over:
                player_has_blackjack, dealer_has_blackjack = self.check_for_blackjack()
                if player_has_blackjack or dealer_has_blackjack:
                    game_over = True
                    if player_has_blackjack:
                        self.player_hand.calc_bet(True)
                    elif dealer_has_blackjack: 
                        self.player_hand.calc_bet(False)
                    self.show_blackjack_results(player_has_blackjack, dealer_has_blackjack)
                    continue

                # If no blackjack, allows player to hit or stay
                choice = input("Please choose [Hit/Stay]").lower()
                while choice not in ["h", "s", "hit", "stay"]: 
                    choice = input("Please enter 'hit' or 'stay' (or H/S) ").lower()

                # If "hit" or "h", displays hand plus added dealt card
                if choice in ["hit", "h"]:
                    self.player_hand.add_card(self.deck.deal())
                    self.player_hand.display(game_over)
                    
                    # If value is over 21, player loses.
                    if self.player_is_over():
                        print("Bust! You've lost")
                        self.player_hand.calc_bet(False)
                        game_over = True
                        print("Dealer's hand: ")
                        self.dealer_hand.display(game_over)

                # If player doesn't hit/h game ends and values are calculated and printed
                else:
                    player_hand_value = self.player_hand.get_value()
                    dealer_hand_value = self.dealer_hand.get_value()
                    print("Final Results")
                    print("Your hand:", player_hand_value)
                    print("Dealer's hand:", dealer_hand_value)

                    # Final scores presented
                    if player_hand_value > dealer_hand_value:
                        print("You win!")
                        self.player_hand.calc_bet(True)
                        print(self.player_hand.bet_bank)
                    elif player_hand_value == dealer_hand_value:
                        print("You've tied!")
                        self.player_hand.calc_bet(None)
                        print(self.player_hand.bet_bank)
                    else: 
                        print("Dealer wins!")
                        self.player_hand.calc_bet(False)
                        print(self.player_hand.bet_bank)
                    game_over = True

            # Checks if player is out of money, if so game ends. 
            if self.player_hand.bet_bank <= 0:
                print("You've run out of money, loser. \n \n \n \nGame Over")
                playing = False
                continue

            # Asks if player would like to play again
            again = input ("Play Again? [Y/N] ")
            while again.lower() not in ["y", "n"]:
                again = input ("Please enter Y or N ")
            if again.lower() == "n":
                print("Thanks for playing!")
                playing = False
            else: 
                game_over = False

    # Checks if player value is over 21/bust
    def player_is_over(self):
        return self.player_hand.get_value() > 21

    # Checks for black jack 
    def check_for_blackjack(self):
        player = False
        dealer = False
        if self.player_hand.get_value() == 21:
            player = True
        if self.dealer_hand.get_value() == 21:
            dealer = True
        return player, dealer

    # Prints winning statement
    def show_blackjack_results(self, player_has_blackjack, dealer_has_blackjack):
        if player_has_blackjack and dealer_has_blackjack:
            print ("Both players have blackjack! Tied")

        elif player_has_blackjack:
            print("You have blackjack! You Win")

        elif dealer_has_blackjack:
            print("Dealer has blackjack! Dealer wins")


if __name__ == "__main__":
    g = Game()
    g.play()

    

