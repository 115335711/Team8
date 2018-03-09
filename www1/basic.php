<?php
function HTML_start($title) {
	print('<!DOCTYPE html>');
	print('<html lang="en">');
	print('<head>');
	print("<title>$title</title>");
	print('<link rel="stylesheet" href="basic.css">');
	print('</head>');
	print('<body>');
	print('<div id="left">');
	print('</div>');
	print('<div id="middle">');
	print('<div id="menu">');
	print('<div class="menu">');
	print('<button class="button"><a href="index.php" class="menu-button">Home</a></button>');
	print('</div>');
	print('<div class="menu">');
	print('<button class="button">Game</button>');
	print('<div class="content">');
	print('<a href="multi_player.php" class="menu-button">Multi-Player</a>');
	print('<a href="single_player.php" class="menu-button">Single-Player</a>');
	print('</div>');
	print('</div>');
	print('<div class="menu">');
	print('<button class="button"><a href="tutorial.php" class="menu-button">Tutorial</a></button>');
	print('</div>');
	print('</div>');
	print('<br><br><br>');
}

function HTML_end() {
	print('</div>');
	print('<div id="right">');
	print('</div>');
	print('</body>');
	print('</html>');
}

function canvas() {
	print('<br>');
	print('<canvas style="border: 3px solid black;">');
	print('</canvas>');
	print('<br>');
}
?>