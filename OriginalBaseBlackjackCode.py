# File from: https://gist.github.com/saulcosta/13909e2e51f94ff7b37700c74b885ab6
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

# Deck class creates and contains the 52 cards that make up the deck 
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

class Hand:
    def __init__(self, dealer = False):
        self.dealer = dealer
        self.cards = []
        self.value = 0

    def add_card(self, card):
        self.cards.append(card)

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
        
    def get_value(self):
        self.calculate_value()
        return self.value

    def display(self):
        if self.dealer:
            print ("hidden")
            print(self.cards[1])
        else: 
            for card in self.cards:
                print(card)
            print("Value:", self.get_value())

class Game: 
    def __init__(self):
        pass

    def play(self):
        playing = True

        while playing:
            self.deck = Deck()
            self.deck.shuffle()

            self.player_hand = Hand()
            self.dealer_hand = Hand(dealer = True)

            for i in range(2):
                self.player_hand.add_card(self.deck.deal())
                self.dealer_hand.add_card(self.deck.deal())

            print ("Your hand is:")
            self.player_hand.display()
            print()
            print("Dealer's hand is:")
            self.dealer_hand.display()

            game_over = False

            while not game_over:
                player_has_blackjack, dealer_has_blackjack = self.check_for_blackjack()
                if player_has_blackjack or dealer_has_blackjack:
                    game_over = True
                    self.show_blackjack_results(player_has_blackjack, dealer_has_blackjack)
                    continue

                choice = input("Please choose [Hit/Stay]").lower()
                while choice not in ["h", "s", "hit", "stay"]: 
                    choice = input("Please enter 'hit' or 'stay' (or H/S) ").lower()
                if choice in ["hit", "h"]:
                    self.player_hand.add_card(self.deck.deal())
                    self.player_hand.display()
                    if self.player_is_over():
                        print("Bust! You've lost")
                        game_over = True

                else:
                    player_hand_value = self.player_hand.get_value()
                    dealer_hand_value = self.dealer_hand.get_value()

                    print("Final Results")
                    print("Your hand:", player_hand_value)
                    print("Dealer's hand:", dealer_hand_value)

                    if player_hand_value > dealer_hand_value:
                        print("You win!")
                    elif player_hand_value == dealer_hand_value:
                        print("You've tied!")
                    else: 
                        print("Dealer wins!")
                    game_over = True

            again = input ("Play Again? [Y/N] ")
            while again.lower() not in ["y", "n"]:
                again = input ("Please enter Y or N ")
            if again.lower() == "n":
                print("Thanks for playing!")
                playing = False
            else: 
                game_over = False

    def player_is_over(self):
        return self.player_hand.get_value() > 21

    def check_for_blackjack(self):
        player = False
        dealer = False
        if self.player_hand.get_value() == 21:
            player = True
        if self.dealer_hand.get_value() == 21:
            dealer = True

        return player, dealer

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

    

