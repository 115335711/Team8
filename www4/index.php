<?php
include 'basic.php';
HTML_start('Index Page');
if (isset($_SESSION['user_name'])) {
	//if the user is logged in, display the account page with the account name and the statistics
	print('<h1 align="center">Hello '.$_SESSION['user_name'].'</h1>'."\n");
	print('<br><br><br>'."\n");
	print('<h2>Statistics</h2>'."\n");
	print('<br>'."\n");
	print('<p>Balance: '.$_SESSION['user_balance'].'</p>'."\n");
	print('<p>Games Won: '.$_SESSION['games_won'].'</p>'."\n");
	print('<p>Games Lost: '.$_SESSION['games_lost'].'</p>'."\n");
	print('<p>Money Won: '.$_SESSION['money_won'].'</p>'."\n");
	print('<p>Money Lost: '.$_SESSION['money_lost'].'</p>'."\n");
}
else {
	//if the user is logged out, display the home page
	print('<h1 align="center">Welcome!</h1>'."\n");
	print('<br><br><br>'."\n");
	print('<p>Please use the menu above to navigate our website!</p>');
	print('<p>Please log in to access our games or register if you do not have an account with us yet. Registration and membership is free</p>'."\n");
	createFooter();
}
HTML_end();
?>