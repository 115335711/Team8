<?php
	include("config.php");
	include("basic.php");
	HTML_start('Registrater');
	if ($_SERVER["REQUEST_METHOD"] == "POST") {
		//get the username and the password, sent from the form, and see if the username is taken by querying it against the table in the database
		$myusername = mysqli_real_escape_string($db,$_POST['username']);
		$mypassword = mysqli_real_escape_string($db,$_POST['password']);
		$sql = "SELECT id FROM logins WHERE username = '$myusername'";
		$result = mysqli_query($db,$sql);
		$count = mysqli_num_rows($result);
		if($count == 1) {
			//if there is 1 table row returned, the username must already exist and the user must be told
			$message = "Username already exists!";
			echo "<script type='text/javascript'>alert('$message');</script>";  
		}
		else {
			$date = date('Y-m-d');
			//if there isn't a table row returned, the username is not taken so a new row must be added to the logins and details table
			$sql1 = "INSERT INTO logins (username, password) VALUES ('$myusername', '$mypassword')";
			$sql2 = "INSERT INTO details (username, balance, gamesWon, GamesLost, moneyWon, moneyLost, loginDate) VALUES ('$myusername', 500, 0, 0, 0, 0, '$date')";
			if ($db->query($sql1) === TRUE && $db->query($sql2) === TRUE) {
				//if the queries were successful, let the user know
				$message = "Account created successfully, please login";
				echo "<script type='text/javascript'>alert('$message');</script>";  
				echo "<script type='text/javascript'>window.location.replace('login.php');</script>";
			}
			else {
				//if the queries were unsuccessful, let the user know
				echo "Error: " . $sql . "<br>" . $db->$error;
			}
		}
	}
?>
<br><br><br>
<div class="outerDiv" align="center">
	<div class="middleDiv" align = "left">
		<div align="center">
			<b>Register</b>
		</div>
		<br><br><br>
		<div class="innerDiv">
			<form action="" method="post">
				<label>Username:&#9;</label>
				<input type="text" name="username" required="required" class="box"/>
				<br><br>
				<label>Password:&#9;</label>
				<input type="password" name="password" required="required" class="box" />
				<br><br>
				<input type="submit" value=" Submit "/>
				<br>
			</form>
		</div>
	</div>
</div>
<!--<div style = "font-size:11px; color:#cc0000; margin-top:10px"><?php echo $error; ?></div>-->
<?php
HTML_end();
?>