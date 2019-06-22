import time, numpy as np


class Card:
    ranks = ['2', '3', '4', '5', '6',
             '7', '8', '9', '10', 'J',
             'Q', 'K', 'A']
    suits = ['S', 'H', 'C', 'D']
    Rank = ''
    Suit = ''

    def __init__(self, r, s):
        if r in self.ranks or r in range(2, 10):
            self.Rank = str(r)
        if s in self.suits:
            self.Suit = s

    def show(self):
        return self.Rank+self.Suit

    @staticmethod
    def same_cards(c1, c2):
        if c1.Rank==c2.Rank and c1.Suit==c2.Suit:
            return True
        else:
            return False


class Deck:
    cards = list()

    def __init__(self):
        self.initialize()

    def initialize(self):
        for rank in Card.ranks:
            for suit in Card.suits:
                self.cards.append(Card(rank, suit))
        np.random.shuffle(self.cards)

    def deal(self, n_cards):
        cards = []
        if len(self.cards) > n_cards:
            [cards.append(self.cards.pop()) for c in range(n_cards)]
        return cards


class Hand:
    Hands = {'High Card': '',
             'Pair': set(),
             'Two Pair': set(),
             'Three Kind': set(),
             'Straight': set(),
             'Flush': set(),
             'Full House': set(),
             'Four Kind': set(),
             'Straight Flush': set(),
             'Royal Flush': set()}

    MADE = {'High Card': False,
            'Pair': False,
            'Two Pair': False,
            'Three Kind': False,
            'Straight': False,
            'Flush': False,
            'Full House': False,
            'Four Kind': False,
            'Straight Flush': False,
            'Royal Flush': False}

    Cards = []
    label = ''
    rank_order = {'2': 2, '3': 3, '4': 4,
                  '5': 5, '6': 6, '7': 7,
                  '8': 8, '9': 9, '10': 10,
                  'J': 11, 'Q': 12, 'K': 13,
                  'A': 14}

    def __init__(self, cards):
        self.Cards = cards

    def add_cards(self, cards):
        for card in cards:
            self.Cards.append(card)

    def evaluate_cards(self):
        hands = {'Pair': [], 'Two Pair': [],
                 'Three Kind': [], 'Straight': [],
                 'Flush': [], 'Full House': [],
                 'Four Kind': [], 'Straight Flush': [],
                 'Royal Flush': []}

        for c1 in self.Cards:
            for c2 in self.Cards:
                if not Card.same_cards(c1, c2):
                    if c1.Rank == c2.Rank:
                        hands['Pair'].append(c1.show())
                        hands['Pair'].append(c2.show())
                    if c1.Suit == c2.Suit:
                        hands['Flush'].append(c1.show())
                        hands['Flush'].append(c2.show())
                    if np.abs(self.rank_order[c1.Rank]-self.rank_order[c2.Rank]) <=5:
                        hands['Straight'].append(c1.show())
                        hands['Straight'].append(c2.show())

        self.Hands['Pair'] = set(hands['Pair'])
        self.Hands['Flush'] = set(hands['Flush'])
        self.Hands['Straight'] = set(hands['Straight'])
        if 3 > len(self.Hands['Pair']) > 1:
            self.MADE['Pair'] = True
        if len(self.Hands['Pair']) >= 4:    # TODO: Could also be four of a kind!
            self.Hands['Two Pair'] = self.Hands['Pair']
            self.MADE['Pair'] = True
            self.MADE['Two Pair'] = True
        if len(self.Hands['Pair']) == 3:
            self.Hands['Three Kind'] = self.Hands['Pair']
            self.MADE['Three Kind'] = True
        if len(self.Hands['Flush']) >= 5:
            # Check suits for flush!
            suits = {'S': 0, 'D': 0, 'H': 0, 'C': 0}
            for card in self.Hands['Flush']:
                for s in suits.keys():
                    if s in card:
                        suits[s] += 1
            for suit in suits.keys():
                if suits[suit] == 5:
                    self.MADE['Flush'] = True
        # TODO: Check For Straight
        # Show which hands were made
        for style in self.Hands.keys():
            if self.MADE[style]:
                print style + '\t' + str(self.Hands[style])
        return hands


def show_game(pocket, table):
    p = ''
    for card in pocket:
        p += card.Rank + card.Suit+' '
    t = ''
    for c in table:
        t += c.Rank + c.Suit+' '
    print 'Pocket: ' + p
    print 'Table: ' + t
    print '---------------'
    return p, t


def main():
    start = time.time()
    training = {}
    n_rounds = 5001
    ii = 0
    for round in range(n_rounds):
        game = Deck()
        while len(game.cards) > 7:
            pocket = game.deal(2)
            table = game.deal(3)
            table.append(game.deal(1).pop())
            table.append(game.deal(1).pop())
            # p, t = show_game(pocket, table)
            training[ii] = [pocket, table]
            ii += 1
    print str(ii)+' Hands Simulated'
    print '\033[1mFINISHED\t'+str(time.time()-start)+'s Elapsed\033[0m'

    show_game(training[ii - 1][0],training[ii - 1][1])
    test_hand = Hand(training[ii-1][0])
    test_hand.add_cards(training[ii-1][1])
    test_hand.evaluate_cards()
    '''
    Hands Recognized By Evaluation:
    ===============================
    * Pair          * Three Kind
    * Two Pair      * Flush 
    
    Remaining:
    * Straight      * Straight Flush
    * Full House    * Royal Flush
    * Four Kind
    '''


if __name__ == '__main__':
    main()

