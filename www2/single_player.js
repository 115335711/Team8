(function() {
	
	//variables for setting up
	var context, height, width, deckNum, deck;
	var mainID, eyesID;
	var cards = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "King", "Queen"];
	var suits = ["Hearts", "Diamonds", "Spades", "Clubs"];
	var points = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10];
	var started = false;
	var ending = "";
	var gotDeck = false;
	var madeBet = false;
	var tooMuch = false;
	var betOps = [5, 10, 15, 20, 50];
	//variables for playing
	var playing = false;
	var done = false;
	var player = {
		money: 100,
		mainBet: 0,
		sideBet: 0,
		insured: false,
		hand: [],
		minPoints: 0,
		points: [],
	};
	var playerX;
	var playerY;
	var dealer = {
		hand: [],
		minPoints: 0,
		points: [],
	};
	var dealerX;
	var dealerY;
	
	document.addEventListener('DOMContentLoaded', init, false);
	
	function init() {
		var canvas = document.querySelector('canvas');
		context = canvas.getContext('2d');
		height = canvas.height;
		width = canvas.width;
		window.addEventListener('keydown', activate, false);
		mainID = window.setInterval(main, 60);
		eyesID = window.setInterval(eyes, 60);
	}
	
	function main() {
		/**
		*Gets information from the player regarding how he/she wishes to play ands calls all the methods needed to play the game.
		*/
		clear(0, 0, width, height);
		context.fillStyle = "#D4AF37";
		if (started == false && gotDeck == false && madeBet == false) {
			context.font = "80px Lucida Console";
			context.fillText("Welcome!", 10, (height/4)-40);
			context.font = "12px Lucida Console";
			context.fillText("Please answer the following question by pressing the appropriate number keys.", 10, (height/2)-6);
			context.fillText("Please press 'Enter' when you are ready to begin.", 10, (height/2)+24);
		}
		else if (started == true && gotDeck == false && madeBet == false) {
			context.fillText("Would you like to play with 1)one, 2)two, 3)three, 4)four or 5)five decks?", 10, (height/2)-6);
		}
		else if (started == true && gotDeck == true && madeBet == false) {
			context.fillText("Would you like to bet 1)"+betOps[0]+", 2)"+betOps[1]+", 3)"+betOps[2]+", 4)"+betOps[3]+" or 5)"+betOps[4]+" Euros?", 10, (height/2)-6);
			if (tooMuch == true) {
				context.fillText("Please place a bet that doesn't put you in a deficit", 10, ((height/4)*3)-6);
			}
		}
		else {
			window.clearInterval(mainID);
			tooMuch = false;
			deck = [];
			generateDeck(deckNum);
			shuffle(deck);
			play();
		}
	}
		
	function eyes() {
		/**
		*Keeps the player updated regarding his/her various "statuses".
		*/
		if (madeBet == true) {
			clear(0, ((height/4)*3)+1, width, (height/4));
			context.fillStyle = "#D4AF37";
			context.font = "12px Lucida Console";
			context.fillText("Funds:     "+player.money, 12, ((height/4)*3)+24);
			context.fillText("Betted:    "+player.mainBet, 12, ((height/4)*3)+42);
			context.fillText("Insurance: "+player.sideBet, 12, ((height/4)*3)+60);
			var p = "";
			for (var i = 0; i < player.points.length; i++) {
				p += player.points[i]+" ";
			}
			context.fillText("Points:    "+p, 12, ((height/4)*3)+78);
			context.beginPath();
			context.moveTo((width/2), (height/4)*3);
			context.lineTo((width/2), height);
			context.stroke();
			if (done == false) {
				context.fillText("1)Hit", (width/2)+12, ((height/4)*3)+24);
				context.fillText("2)Stick", (width/2)+12, ((height/4)*3)+42);
				if (player.money >= player.mainBet) {
					context.fillText("3)Double Down", (width/2)+12, ((height/4)*3)+60);
				}
				else{
					context.fillText("3)Double Down [Unavailable]", (width/2)+12, ((height/4)*3)+60);
				}
				if (player.hand.length == 2) {
					if (player.insured == false && dealer.hand[0].card == "Ace") {
						context.fillText("4)Take Out Insurance", (width/2)+12, ((height/4)*3)+78);
					}
					else {
						context.fillText("4)Take Out Insurance [Unavailable]", (width/2)+12, ((height/4)*3)+78);
					}
					context.fillText("5)Surrender", (width/2)+12, ((height/4)*3)+96);
				}
				else {
					context.fillText("4)Take Out Insurance [Unavailable]", (width/2)+12, ((height/4)*3)+78);
					context.fillText("5)Surrender [Unavailable]", (width/2)+12, ((height/4)*3)+96);
				}
			}
			else {
				if (ending == "playerBlackjack") {
					context.fillText("You won by getting a blackjack!", (width/2)+12, ((height/4)*3)+24);
				}
				else if (ending == "dealerBlackjack") {
					context.fillText("The dealer won by getting a blackjack!", (width/2)+12, ((height/4)*3)+24);
				}
				else if (ending == "winning") {
					context.fillText("You won by being the closest to 21!", (width/2)+12, ((height/4)*3)+24);
				}
				else if (ending == "losing") {
					context.fillText("The dealer won by being the closest to 21!", (width/2)+12, ((height/4)*3)+24);
				}
				else if (ending == "surrender") {
					context.fillText("You surrendered!", (width/2)+12, ((height/4)*3)+24);
				}
				else {
					context.fillText("It's a draw!", (width/2)+12, ((height/4)*3)+24);
				}
				context.fillText("Please press 'Enter' to play again.", (width/2)+12, ((height/4)*3)+48);
				context.fillText("Please press 'Backspace' to quit.", (width/2)+12, ((height/4)*3)+72);
			}
		}
	}
	
	function clear(x, y, w, h) {
		/**
		*Sets up the canvas.
		*/
		context.clearRect(x, y, w, h);
		context.rect(x, y, w, h);
		context.fillStyle = "#228B22";
		context.fill();
	}
	
	function placeBet(array, index) {
		/**
		*Checks if the player can place a bet and either places the bet or tells the player he/she can't place that bet.
		*/
		if (player.money >= array[index]) {
			player.mainBet = array[index];
			player.money -= array[index];
			if (array == betOps) {
				madeBet = true;
			}
		}
		else {
			tooMuch = true;
		}
	}

	function generateDeck(numOfDecks) {
		/**
		*Creates the 52 card deck(s) needed to play the game.
		*/
		for (var i = 1; i <= numOfDecks; i++) {
			for (var j = 0; j < suits.length; j++) {
				for (var k = 0; k < cards.length; k++) {
					var c = {
						card: cards[k],
						suit: suits[j],
						point: points[k],
					};
					deck.push(c);
				}
			}
		}
	}
	
	function shuffle(array) {
		/**
		*Shuffles the deck(s) 3 times.
		*/
		var currIndex, randIndex, tempValue;
		for (var i = 0; i < 3; i++) {
			currIndex = array.length;
			while (0 !== currIndex) {
				currIndex -= 1;
				randIndex = Math.floor(Math.random() * (currIndex+1));
				tempValue = array[currIndex];
				array[currIndex] = array[randIndex];
				array[randIndex] = tempValue;
			}
		}
		return;
	}

	function play() {
		/**
		*Sets up the game and takes care of the logic needed to run it.
		*/
		playing = true;
		playerX = (width/2)+12;
		playerY = 12;
		dealerX = 12;
		dealerY = 12;
		clear(0, 0, width, height);
		context.fillStyle = "#D4AF37";
		context.font = "12px Lucida Console";
		context.beginPath();
		context.moveTo(0, (height/4)*3);
		context.lineTo(width, (height/4)*3);
		context.stroke();
		context.moveTo((width/2), 0);
		context.lineTo((width/2), (height/4)*3);
		context.stroke();
		player.hand.push(deck.pop());
		player.hand.push(deck.pop());
		dealer.hand.push(deck.pop());
		dealer.hand.push(deck.pop());
		context.fillText("Player", playerX, playerY);
		playerY += 48;
		context.fillText("Dealer", dealerX, dealerY);
		dealerY += 48;
		for (var i = 0; i < 2; i++) {
			context.fillText(player.hand[i].card+" of "+player.hand[i].suit, playerX, playerY);
			playerY += 12;
			calcPoints(player, player.hand[i]);
			calcPoints(dealer, dealer.hand[i]);
		}
		if ((player.hand[0].card == "Ace" && player.hand[1].point == 10) || (player.hand[1].card == "Ace" && player.hand[0].point == 10)) {
			//player has blackjack;
			ending = "playerBlackjack";
		}
		context.fillText(dealer.hand[0].card+" of "+dealer.hand[0].suit, dealerX, dealerY);
		dealerY += 12;
	}
	
	function calcPoints(person, card) {
		/**
		*Calculates the points of the player and the dealer.
		*/
		person.minPoints += card.point;
		if (person.points.length == 0) {
			person.points.push(person.minPoints);
		}
		else {
			for (var i = 0; i < person.points.length; i++) {
				person.points[i] += card.point;
			}
		}
		if (card.card == "Ace") {
			var temp;
			for (var j = 0; j < person.points.length; j++) {
				if (j == person.points.length - 1) {
					temp = (person.points[j]+10);
				}
			}
			person.points.push(temp);
		}
		remvPoints(person);
	}
	
	function remvPoints(person) {
		/**
		*Removes points from the player and the dealer that are over 21.
		*/
		for (var i = person.points.length - 1; i >= 0; i--) {
			if (person.points[i] > 21) {
				person.points.pop(i);
			}
		}
		if (person.points.length == 0) {
			playing = false;
			if (person == player) {
				ending = "losing";
				done = true;
				getDealerToPlay();
			}
			else {
				ending = "winning";
				done = true;
			}
		}
	}
	
	function getDealerToPlay() {
		/**
		*Makes the dealer play blackjack, stopping at or above a soft 17.
		*/
		context.fillText(dealer.hand[1].card+" of "+dealer.hand[1].suit, dealerX, dealerY);
		dealerY += 12;
		if (dealer.hand[0].card == "Ace") {
			if (player.insured == true) {
				//player is insured...
				player.insured = false;
				if (dealer.hand[1].point == 10){
					//...and dealer has a blackjack
					player.money += (player.mainBet + (player.sideBet*2));
					player.mainBet = 0;
					ending = "dealerBlackjack";
					done = true;
				}
				else {
					//...dealer doesn't have a blackjack
				}
				player.sideBet = 0;
			}
		}
		if ((dealer.hand[0].card == "Ace" && dealer.hand[1].point == 10) || (dealer.hand[1].card == "Ace" && dealer.hand[0].point == 10) && done == false) {
			//dealer has a blackjack...
			if (ending == "playerBlackjack") {
				//...and player too; push
				player.money += player.mainBet;
			}
			else {
				//...but player doesn't
				ending = "dealerBlackjack";
			}
			player.mainBet = 0;
			done = true;
		}
		else if (ending == "playerBlackjack") {
			//player has a blackjack but dealer doesn't
			player.money += ((player.mainBet*2) + (player.mainBet/2));
			player.mainBet = 0;
			done = true;
		}
		else {
			//neither party has a blackjack
			var i = 1;
			while (done == false && 17 > dealer.points[dealer.points.length - 1]) {
				//get at least a soft 17
				i++;
				dealer.hand.push(deck.pop());
				context.fillText(dealer.hand[i].card+" of "+dealer.hand[i].suit, dealerX, dealerY);
				calcPoints(dealer, dealer.hand[i]);
				dealerY += 12;
			}
			if ((dealer.points.length == 0 && player.points.length > 0) || Math.max.apply(null, player.points) > Math.max.apply(null, dealer.points)) {
				//player has more points
				ending = "winning";
				player.money += (player.mainBet*2);
			}
			else if ((player.points.length == 0 && dealer.points.length > 0) || Math.max.apply(null, player.points) < Math.max.apply(null, dealer.points)) {
				//player has less points
				ending = "losing";
			}
			else {
				//both parties have the same points
				ending = "push";
				player.money += player.mainBet;
			}
			player.mainBet = 0;
			done = true;
		}
	}

	function activate(event) {
		/**
		*Takes key strokes as input.
		*/
		var keyCode = event.keyCode;
		if (started == false) {
			//Start the game.
			if (keyCode == 13) {
				started = true;
			}
		}
		else if (gotDeck == false) {
			//Set the number of decks used.
			if (keyCode == 49 || keyCode == 97) {
				deckNum = 1;
				gotDeck = true;
			}
			else if (keyCode == 50 || keyCode == 98) {
				deckNum = 2;
				gotDeck = true;
			}
			else if (keyCode == 51 || keyCode == 99) {
				deckNum = 3;
				gotDeck = true;
			}
			else if (keyCode == 52 || keyCode == 100) {
				deckNum = 4;
				gotDeck = true;
			}
			else if (keyCode == 53 || keyCode == 101) {
				deckNum = 5;
				gotDeck = true;
			}
		}
		else if (madeBet == false) {
			//Set the amount betted.
			if (keyCode == 49 || keyCode == 97) {
				placeBet(betOps, 0);
			}
			else if (keyCode == 50 || keyCode == 98) {
				placeBet(betOps, 1);
			}
			else if (keyCode == 51 || keyCode == 99) {
				placeBet(betOps, 2);
			}
			else if (keyCode == 52 || keyCode == 100) {
				placeBet(betOps, 3);
			}
			else if (keyCode == 53 || keyCode == 101) {
				placeBet(betOps, 4);
			}
		}
		else if (playing == true) {
			//Play the game
			if (keyCode == 49 || keyCode == 97) {
				//hit
				ending = "";
				player.hand.push(deck.pop());
				context.fillText(player.hand[player.hand.length - 1].card+" of "+player.hand[player.hand.length - 1].suit, playerX, playerY);
				playerY += 12;
				calcPoints(player, player.hand[player.hand.length - 1]);
			}
			else if (keyCode == 50 || keyCode == 98) {
				//stick
				playing = false;
				getDealerToPlay();
			}
			else if (keyCode == 51 || keyCode == 99) {
				//double down
				if (player.money >= player.mainBet) {
					player.money -= player.mainBet;
					player.mainBet *= 2;
					player.hand.push(deck.pop());
					context.fillText(player.hand[player.hand.length - 1].card+" of "+player.hand[player.hand.length - 1].suit, playerX, playerY);
					playerY += 12;
					calcPoints(player, player.hand[player.hand.length - 1]);
					playing = false;
					getDealerToPlay();
				}
			}
			if (player.hand.length == 2) {
				if (keyCode == 52 || keyCode == 100) {
					//insure
					if (player.insured == false && dealer.hand[0].card == "Ace") {
						player.insured = true;
						player.sideBet = (player.mainBet/2);
						player.money -= (player.mainBet/2);
					}
				}
				else if (keyCode == 53 || keyCode == 101) {
					//surrender
					playing = false;
					done = true;
					player.money += (player.mainBet/2);
					player.mainBet = 0;
					ending = "surrender";
				}
			}
		}
		else if (done == true) {
			//End the game.
			if (keyCode == 13) 
			{
				restart();
			}
			else if(keyCode == 8)
			{
				quit();
			}
		}
	}
	
	function log() {
		console.log(ending);
	}
	
	function restart() {
		/**
		*Either resets and restarts the game or prompts the user to refresh the page is he/she wishes to play again.
		*/
		window.clearInterval(eyesID);
		clear(0, 0, width, height);
		log();
		if (player.money >= Math.min.apply(null, betOps)) {
			window.removeEventListener('keydown', activate, false);
			//Reset/Restart
			gotDeck = false;
			madeBet = false;
			tooMuch = false;
			player.hand = [];
			player.minPoints = 0;
			player.points = [];
			dealer.hand = [];
			dealer.minPoints = 0;
			dealer.points = [];
			ending = "";
			playing = false;
			done = false;
			init();
		}
		else {
			//Prompt
			context.fillStyle = "#D4AF37";
			context.font = "80px Lucida Console";
			context.fillText("Game Over!", 10, (height/4)-40);
			context.font = "12px Lucida Console";
			context.fillText("You do not have enough money to continue!", 10, (height/2)-6);
			context.fillText("Please press 'Backspace' to go to the home page or reload the page to reset everything!", 10, (height/2)+24);
		}
	}
	
	function quit() {	
		/**
		*Quits the user out of the game.
		*/
		window.removeEventListener('keydown', activate, false);
		window.clearInterval(eyesID);
		window.location.href = "index.php";
	}

})();