from random import shuffle

class Card(object):

    def __init__(self, cardNum, cardKin, cardVal):
        """Creates a Card object with a number, suit and value."""
        self._num = cardNum
        self._kin = cardKin
        self._val = cardVal

    def __str__(self):
        """Overwrites the print() method to neatly print out the variables of a Card object."""
        if self._num == "Ace":
            return "Ace of %s, worth 1 or 11" % (self._kin)
        else:
            return "%s of %s, worth %s" % (self._num, self._kin, self._val)

class Deck(object):

    def __init__(self):
        """Creates a Deck object into which Card objects can be added, from which Card objects can be removed and which can be shuffled."""
        self._body = []
        self._size = 0

    def __str__(self):
        """Overwrites the print() method to neatly print out the cards inside a Deck object."""
        string = ""
        for card in self._body:
            string += str(card)
            string += "\n"
        return string

    def size(self):
        """Returns the size of the deck."""
        return self._size

    def add(self, card):
        """Adds 'card' to the deck if it's a Card type object."""
        if isinstance(card, Card):
            self._body.append(card)
            self._size += 1
        return

    def rem(self):
        """Removes the last card from the deck and returns it."""
        if self._size > 0:
            self._size -= 1
            return self._body.pop()
        else:
            return

    def shuffle(self, n):
        """Shuffles the deck 'n' times."""
        for i in range(n):
            shuffle(self._body)
        return

def Generator(deckNum, shflNum):
    """Creates 'deckNum' number of decks, combines them into one, shuffles it 'shflNum' number times and returns it."""
    cardKins = ["Hearts", "Diamonds", "Spades", "Clubs"]
    cardNums = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
    cardVals = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "10", "10", "10"]
    deck = Deck()
    for i in range(deckNum):
        for suit in range(len(cardKins)):
            for numb in range(len(cardNums)):
                card = Card(cardNums[numb], cardKins[suit], cardVals[numb])
                deck.add(card)
    deck.shuffle(shflNum)
    return deck
