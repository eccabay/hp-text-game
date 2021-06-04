# hp-text-game
A text-based command-line version of the game Harry Potter: Hogwarts Battle

## How to play:
### Start the game: `python game.py --game <game_number> --players "<player1> <player2> ..."`
Players must be one of `harry | ron | hermione | neville`. The order they are entered is play order

The game begins automatically. It will print out the full status of the game, then draw and apply the first Dark Arts Event. If necessary, it will prompt you for any action you need to take.

### On your turn:
Players are prompted to choose their moves on their turns. Available options are:
* Play a card: enter any number corresponding to the cards displayed on screen to play it
* Buy a card (`"buy"`): moves you to the Hogwarts Card store, where you enter a number to buy a card
* Attack a villain (`"attack"`): moves you to the villains, where you choose which villain to attack and then the number of attacks to assign
* Check the status of the game:
 * `"status"`: see the active hero's current status
 * `"game status"`: see the full status of the game (as is printed between each turn)
 * `"location status"`: see which location is the current location, and how many metal there are currently
 * `"hero status"`: see the number of hearts, attacks, and influence that all heroes have
* End your turn (`"end"`): Only necessary if you have leftover cards, attacks, or influence you don't want to play or assign. Otherwise, this happens automatically.
