<?php
function HTML_start($title) {
	print('<!DOCTYPE html>'."\n");
	print('<html lang="en">'."\n");
	print('<head>'."\n");
	print("<title>$title</title>"."\n");
	print('<link rel="stylesheet" href="basic.css">'."\n");
	if ($title == 'Single-Player (Trial) Version') {
		print('<script src="single_player.js"></script>'."\n");
	}
	else if ($title == 'Multi-PlayerVersion') {
		//print('<script src="multi_player.js"></script>'."\n");
	}
	print('</head>'."\n");
	print('<body>'."\n");
	print('<div id="left">'."\n");
	print('</div>'."\n");
	print('<div id="middle">'."\n");
	print('<div id="menu">'."\n");
	print('<div class="menu">'."\n");
	print('<button class="button"><a href="index.php" class="menu-button">Home</a></button>'."\n");
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
	print('<div class="menu">'."\n");
	print('<button class="button"><a href="login.php" class="menu-button">Login</a></button>'."\n");
	print('</div>'."\n");
	print('<div class="menu">'."\n");
	print('<button class="button"><a href="register.php" class="menu-button">Register</a></button>'."\n");
	print('</div>'."\n");
	print('</div>'."\n");
	print('<br><br><br>'."\n");
}

function HTML_end() {
	print('</div>'."\n");
	print('<div id="right">'."\n");
	print('</div>'."\n");
	print('</body>'."\n");
	print('</html>'."\n");
}

function createCanvas() {
	print('<br>'."\n");
	print('<canvas width="640" height="480" style="border: 3px solid black; display: block; margin-left: auto; margin-right: auto;>"'."\n");
	print('</canvas>'."\n");
	print('<br>'."\n");
}

function createCanvasAndChat() {
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