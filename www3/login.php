<?php
	include("config.php");
	include("basic.php");
	HTML_start('Login');
	if ($_SERVER["REQUEST_METHOD"] == "POST") {
		//if the user tries to log in, get his/her username and password, sent from the form, and see if they are valid by querying them against the table in the database
		$username = mysqli_real_escape_string($db, $_POST['username']);
		$password = mysqli_real_escape_string($db, $_POST['password']);
		$sql_check = "SELECT id FROM logins WHERE username = '$username' and password = '$password'";
		$result = mysqli_query($db, $sql_check);
		$count = mysqli_num_rows($result);
		if ($count == 1) {
			//if there is 1 table row returned, the username and the password must be valid
			$_SESSION['user_name'] = $username;
			//fetch the user's information and store them in an array
			$sql_fetch = "SELECT balance, gamesWon, gamesLost, moneyWon, moneyLost, loginDate FROM details WHERE username = '$username'";
			$result = mysqli_query($db, $sql_fetch);
			$row = $result->fetch_assoc();
			$_SESSION['user_balance'] = $row['balance'];
			$_SESSION['games_won'] = $row['gamesWon'];
			$_SESSION['games_lost'] = $row['gamesLost'];
			$_SESSION['money_won'] = $row['moneyWon'];
			$_SESSION['money_lost'] = $row['moneyLost'];
			$_SESSION['login_date'] = $row['loginDate'];
			//get the current date and the last time the user logged in
			$date = date('Y-m-d');
			$old_date = $row['loginDate'];
			if ($_SESSION['login_date'] != $date) {
				//if the last time the user logged in wasn't today, get the day difference between today and that day
				$sql_select = "SELECT DATEDIFF('$date', '$old_date') AS dateDiff";
				$result = mysqli_query($db, $sql_select);
				$row = $result->fetch_assoc();
				$date_diff = $row['dateDiff'];
				//give the user 50 currency for every day since his/her last log in and update his/her last log in date
				$extra_money = $date_diff * 50;
				$sql_update = "UPDATE details SET balance = balance + '$extra_money', loginDate = '$date' WHERE username = '$myusername'";
				$result = mysqli_query($db, $sql_update);
			}
			echo "<script type='text/javascript'>window.location.replace('index.php');</script>";
		}
		else {
			$error = "Your login userame or password is invalid";
		}
	}
?>
<br><br><br>
<div class="outerDiv" align="center">
	<div class="middleDiv" align="left">
		<div align="center">
			<b>Login</b>
		</div>
		<br><br><br>
		<div class="innerDiv">
			<form action="" method="post">
				<label>Username:&#9;</label>
				<input type="text" name="username" class="box"/>
				<br><br>
				<label>Password:&#9;</label>
				<input type="password" name="password" class="box" />
				<br><br>
				<input type="submit" value=" Submit " align="left"/>
				<br>
			</form>
			<br>
			<a href="register.php">Create a New Account</a>
		</div>
	</div>
</div>
<!--<div style = "font-size:11px; color:#cc0000; margin-top:10px"><?php echo $error; ?></div>-->
<?php
HTML_end();
?>