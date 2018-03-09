<?php
	include("basic.php");
	HTML_start('Logout');
	if ($_SERVER["REQUEST_METHOD"] == "POST") {
		//if the user logged out, destroy the session and any associated variables
		session_start();
		if (session_destroy()) {
			echo "<script type='text/javascript'>window.location.replace('index.php');</script>";
		}
	}
?>
<br><br><br>
<div class="outerDiv" align="center">
	<div class="middleDiv" align="left">
		<div align="center">
			<b>Logout? Are you sure?</b>
		</div>
		<br><br><br>
		<div class="innerDiv">
			<form action="" method="post">
				<br><br>
				<input type="submit" value=" Submit " align="left"/>
				<br>
			</form>
			<br>
		</div>
	</div>
</div>
<?php
HTML_end();
?>