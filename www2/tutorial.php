<?php
include 'basic.php';
HTML_start('Tutorial');
?>
<h2>Overview:</h2>
<p>The dealer deals two cards to the player face up, and two cards to himself/herself with one being face up and the other being face down. The player is asked if he/she would like another card. If he/she does, then he/she is given another card. This is repeated until the player no longer wishes to get anymore cards. The dealer then turns his/her second card face up and keeps dealing himself/herself cards until he/she has 17 or more points, reaches 21 or goes over 21.<p>
<p>The aim for the player is to reach 21 points or to get as close to it as possible without going over it while having more points than the dealer. The aim for the dealer is to reach 21 points or to get as close to it as possible without going over it while having more points than the player. If either party reaches 21 points, the other party automatically loses. Similarly, if either party goes over 21, the other party automatically wins. If both parties have 21 points or a blackjack, it's a draw.</p>
<br><br><br>
<h2>Scoring:</h2>
<p>The cards are allocated points as follows:</p>
<ul>
	<li>Ace is worth 1 or 11 points.</li>
	<li>2 is worth 2 points.</li>
	<li>3 is worth 3 points.</li>
	<li>4 is worth 4 points.</li>
	<li>5 is worth 5 points.</li>
	<li>6 is worth 6 points.</li>
	<li>7 is worth 7 points.</li>
	<li>8 is worth 8 points.</li>
	<li>9 is worth 9 points.</li>
	<li>10, Jack, King and Queen are each worth 10 points.</li>
</ul>
<p>If the player wins but doesn't get exactly 21 points, he/she is given double the amount that he/she has bet. If he/she wins with exactly 21 points, he/she receives double his/her bet plus an additional 50% of his/her bet.</p>
<br><br><br>
<h2>Terminology:</h2>
<p><b>Hit</b>: ask for another card</p>
<p><b>Stick</b>: end your turn, staying with the cards you have</p>
<p><b>Insurance</b>: place a side bet that the dealer has a blackjack (can only be done when the dealer's face up card is an ace)</p>
<p><b>Double Down</b>: double your bet and get one and only one more card (can only be done when you have 2 cards)</p>
<p><b>Surrender</b>: discard your cards and recover half of your bet (can only be done when you have 2 cards)</p>
<br><br><br>
<p>Please note that we do not allow <b>hand splitting</b> and we discourage <b>card counting</b>.</p>
<br><br><br>
<?php
HTML_end();
?>