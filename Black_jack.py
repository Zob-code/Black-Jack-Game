# This a Black jack game

import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven',
         'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7,
         'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

playing = True

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank+ " of "+self.suit

class Deck:
    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank)) # built Card object and add them to the list

    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n'+ card.__str__() # add each Card object's print string
        return "The deck has: "+deck_comp

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()
        return single_card

class Hand:
    def __init__(self):
        self.cards = [] # starts with an empty list as we did in the Deck class
        self.value = 0 # starts with an zero value
        self.aces = 0 # add an attribute to keep track of the aces

    def add_card(self,card):
        # card passed in
        # from the deck.deal() ---> single_card(suit,rank)
        self.cards.append(card)
        self.value += values[card.rank]

        # track the aces
        if card == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):

        # if the total value is greater than 21 then i still have an ace
        # then change my ace to be a 1 instead of an 11

        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


class Chips:

    def __init__(self,total= 100):
        self.total = total # this can be set to default value or can be set by the user
        self.bet = 0

    def win_bet(self):
        self.total += self.total

    def lose_bet(self):
        self.total -= self.total


# The function for taking bets
def take_bet(chips):

    while True:

        try:
            chips.bet = int(input("How many chips you want to bet? "))
        except ValueError:
            print("Sorry please provide an Integer")
        else:
            if chips.bet > chips.total:
                print(f'Sorry you do not have enough chips! {chips.total}')
            else:
                break

# function for taking hits
def hit(deck,hand):

    single_card = deck.deal()
    hand.add_card(single_card)
    hand.adjust_for_ace()

# function for prompting the player to hit stand
def hit_or_stand(deck,hand):
    global playing

    while True:
        x = input('Hit or stand? Enter h or s')

        if x[0].lower() == 'h':
            hit(deck,hand)

        elif x[0].lower() == 's':
            print("Player stands Dealer's Turn")
            playing = False

        else:
            print("Sorry, I did not understand that, Please enter h or s only!")
            continue
        break

# function for diplaying the cards
def show_some(player,dealer):

    # Show only one of the dealer's card
    print("\n Dealer's hand: ")
    print("Frist card hidden!")
    print(dealer.cards[1])

    # show all (2 cards) of the player's hand/cards
    print("\n Player's Hand:")
    for card in player.cards:
        print(card)

def show_all(player,dealer):

    # show all the dealer's cards
    print("\n Dealer's Hand:")
    for card in dealer.cards:
        print(card)
    print(f"Value of Dealer's Hand is: {dealer.value}")

    # show all the player cards
    print("\n Player's Hand:")
    for card in player.cards:
        print(card)
    print(f"Value of Player's hand is: {player.value}")


# functions to handle and of game scenarios

def player_busts(player, dealer, chips):
    print("Bust Player!!!")
    chips.lose_bet()

def player_wins(player, dealer, chips):
    print("Player Wins!!!")
    chips.win_bet()

def dealer_busts(player,dealer,chips):
    print("Dealer Busts!!!")
    chips.win_bet()

def dealer_wins(player, dealer, chips):
    print("Dealer Wins!!!")
    chips.lose_bet()

def push(player, dealer):
    print("Dealer and Player tie! It's a push.")


if __name__ == '__main__':
    while True:

        print ("WELCOME TO BLACKJACK GAME!!!")

        # Create and shuffle the deck deal two cards to each player
        deck = Deck()
        deck.shuffle()

        player_hand = Hand()
        player_hand.add_card(deck.deal())
        player_hand.add_card(deck.deal())

        dealer_hand = Hand()
        dealer_hand.add_card(deck.deal())
        dealer_hand.add_card(deck.deal())

        # Set up the player's chips
        player_chips = Chips()

        # Prompt for Player for their bet
        take_bet(player_chips)

        # show cards ( but keep one dealer card hidden)
        show_some(player_hand, dealer_hand)

        while playing: # recall this variable from hit_or_stand function

            # Prompt for player to hit or stand
            hit_or_stand(deck,player_hand)

            # show cards (but keep one dealer's card hidden )
            show_some(player_hand,dealer_hand)

            # if the player's hand exceeds 21 , run player_busts() and break out of the loop
            if player_hand.value > 21:
                player_busts(player_hand,dealer_hand,player_chips)

                break

        # if the player hasn't busted, play Dealer's hand until Dealer reaches 17
        if player_hand.value <= 21:

            while dealer_hand.value < 17:
                hit(deck,dealer_hand)

            # show all cards
            show_all(player_hand,dealer_hand)

            # run different winning scenarios
            if dealer_hand.value > 21:
                dealer_busts(player_hand,dealer_hand,player_chips)
            elif dealer_hand.value > player_hand.value:
                dealer_wins(player_hand,dealer_hand,player_chips)
            elif dealer_hand.value < player_hand.value:
                player_wins(player_hand,dealer_hand,player_chips)
            else:
                push(player_hand,dealer_hand)

        # inform player of their chips total
        print(f"\n Player total chips are at: {player_chips.total}")

        # ask to play again
        new_game = input("Would you like to play another hand? y/n")

        if new_game[0].lower() == 'y':
            playing = True
            continue
        else:
            print("Thank you for playing!!!")

            break
