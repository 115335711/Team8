<?php
include 'basic.php';
HTML_start('Multi-Player Version');
if (isset($_SESSION['user_name'])) {
	//if the user is logged in, display the contents of the page
	createCanvasAndChat();
}
HTML_end();
if (!isset($_SESSION['user_name'])) {
	//if the user is logged out, ask him/her to log in and redirect him/her
	echo "<script type='text/javascript'>alert('Please login to play');</script>";  
	echo "<script type='text/javascript'>window.location.replace('login.php');</script>";
}
?>