<?php
function HTML_start($title) {
	//start a session and set the variables depending whether the user is logged in or not
	session_start();
	if (isset($_SESSION['user_name'])) {
		$loggedIn = true;
		$index = 'Account';
	}
	else {
		$loggedIn = false;
		$index = 'Home';
	}
	print('<!DOCTYPE html>'."\n");
	print('<html lang="en">'."\n");
	print('<head>'."\n");
	print("<title>$title</title>"."\n");
	print('<link rel="stylesheet" href="basic.css">'."\n");
	if ($title == 'Multi-PlayerVersion' && $loggedIn) {
		//if the user is logged in and is on the multi-player page, load the related JavaScript
		//print('<script src="multi_player.js"></script>'."\n");
	}
	else if ($title == 'Single-Player (Trial) Version' && $loggedIn) {
		//if the user is logged in and is on the single-player page, load the related JavaScript
		print('<script src="single_player.js"></script>'."\n");
	}
	print('</head>'."\n");
	print('<body>'."\n");
	//add the left border to the page
	print('<div id="left">'."\n");
	print('</div>'."\n");
	//add the menu options to the page
	print('<div id="middle">'."\n");
	print('<div id="menu">'."\n");
	print('<div class="menu">'."\n");
	print('<button class="button"><a href="index.php" class="menu-button">'.$index.'</a></button>'."\n");
	print('</div>'."\n");
	print('<div class="menu">'."\n");
	print('<button class="button">Game</button>'."\n");
	print('<div class="content">'."\n");
	print('<a href="multi_player.php" class="menu-button">Multi-Player</a>'."\n");
	print('<a href="single_player.php" class="menu-button">Single-Player</a>'."\n");
	print('</div>'."\n");
	print('</div>'."\n");
	print('<div class="menu">'."\n");
	print('<button class="button"><a href="tutorial.php" class="menu-button">Tutorial</a></button>'."\n");
	print('</div>'."\n");
	if ($loggedIn) {
		//if the user is logged in, show the logout menu option
		print('<div class="menu">'."\n");
		print('<button class="button"><a href="logout.php" class="menu-button">Logout</a></button>'."\n");
		print('</div>'."\n");
	}
	else {
		//if the user is logged out, show the login and register menu options
		print('<div class="menu">'."\n");
		print('<button class="button"><a href="login.php" class="menu-button">Login</a></button>'."\n");
		print('</div>'."\n");
		print('<div class="menu">'."\n");
		print('<button class="button"><a href="register.php" class="menu-button">Register</a></button>'."\n");
		print('</div>'."\n");
	}
	print('</div>'."\n");
	print('<br><br><br>'."\n");
}

function HTML_end() {
	print('</div>'."\n");
	//add the right border to the page
	print('<div id="right">'."\n");
	print('</div>'."\n");
	print('</body>'."\n");
	print('</html>'."\n");
}

function createFooter() {
	print('<br><br><br>'."\n");
	//add a footer with a totally, 100% without a doubt correct copyright notice
	print('<footer>'."\n");
	print('<p>This website has been created by the collective effort of the members of Team 8: Aaron Rossiter, Botond Kreicz, Conor Sheil, David Crowley, Dylon Condon, Jason Power, María Martínez de Rute, Oisin O&#39;Riordan and Sean McCarthy.</p>'."\n");
	print('<p>Copyright &copy; 2018 Team 8 of CS3305, UCC. All rights reserved.</p>'."\n");
	print('</footer>'."\n");
}

function createCanvas() {
	//create a 640x480px canvas with a 3px border and centre it
	print('<br>'."\n");
	print('<canvas width="640" height="480" style="border: 3px solid black; display: block; margin-left: auto; margin-right: auto;>"'."\n");
	print('</canvas>'."\n");
	print('<br>'."\n");
}

function createCanvasAndChat() {
	//create a 640x480px canvas with a 3px border, 2 text areas on top of each other and a button and centre it all
	print('<br>'."\n");
	print('<div>'."\n");
	print('<canvas width="640" height="480" style="border: 3px solid black;">');
	print('</canvas>'."\n");
	print('<div style="position: absolute; top: 75px; right: 0px;">'."\n");
	print('<textarea id="recv" rows="26" cols="39" disabled>'."\n");
	print('</textarea>'."\n");
	print('<br>'."\n");
	print('<textarea id="send" rows="3" cols="39" placeholder="Type here what you want to say...">'."\n");
	print('</textarea>'."\n");
	print('<br>'."\n");
	print('<button type="submit">Send'."\n");
	print('</button>'."\n");
	print('</div>'."\n");
	print('</div>'."\n");
	print('<br>'."\n");
}
?>