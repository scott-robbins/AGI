# Games 
I'd like to make a simple game playing agent. Thus far, I've
unfortunately chosen games I either don't understand well, or are 
intrinsically quite difficult to do this with, and therefore
have not had much success. (*Poker*, *Chess*, *Soduku,...*)

I'm leaving skeleton programs of those past attempts here, but 
now I'm going to try and return to basics and start with the most
simple games I can think of! 

## Tic Tac Toe 
This is pretty much one of the most basic games you could make. 
Creating a fairly trivial game, where the 'opponent' can only move
to a randomly chosen loction (so long as it's a legal move). By 
using this trivial utility function, in addition with the condition 
that game will not terminate until either board is full or a move has
satisfied one or more of 8 various vectors of 3 elements. 

`

        row1 = self.state[0, :]
        row2 = self.state[1, :]
        row3 = self.state[2, :]

        col1 = self.state[:, 0]
        col2 = self.state[:, 1]
        col3 = self.state[:, 2]

        dag1 = [self.state[0, 0], self.state[1, 1], self.state[2, 2]]
        dag2 = [self.state[0, 2], self.state[1, 1], self.state[2, 0]]`
Keeping track of X's and O's with 1s and 0s:

`
draw = {-1: ' ', 1: 'X', 0: 'O'}
states = {'X': 1, 'O': 0, 'x': 1, 'o': 0}`

![stochastic](https://raw.githubusercontent.com/scott-robbins/AGI/tree/master/codebase/easy_tic.png)