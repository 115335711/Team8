<?php
include 'basic.php';
HTML_start('Multi-Player Version');
if (isset($_SESSION['user_name'])) {
	//if the user is logged in, display the contents of the page
	//createCanvasAndChat();
	print('<br><br><br>'."\n");
	print('<p>To play the multi-player version, please <a href="/game/game.zip" download>download</a> the ZIP folder containing the game files. After downloading the folder, please unzip it and follow the instructions in the README.txt file to set up and play the game.</p>'."\n");
	print('<br><br><br>'."\n");
	print('<p>A permanent Internet connection is required to play this game as well as a knowledge of the host&#39;s IP address.</p>'."\n");
	print('<p>We do not recommend messing with the .py files and we are not responsible for what may happen if you do so.</p>');
}
HTML_end();
if (!isset($_SESSION['user_name'])) {
	//if the user is logged out, ask him/her to log in and redirect him/her
	echo "<script type='text/javascript'>alert('Please login to play');</script>";  
	echo "<script type='text/javascript'>window.location.replace('login.php');</script>";
}
?>