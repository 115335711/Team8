<?php
   include("basic.php");
   HTML_start('Login');
   session_start();
   include("config.php");
   if($_SERVER["REQUEST_METHOD"] == "POST") {
      // username and password sent from form 
      $myusername = mysqli_real_escape_string($db,$_POST['username']);
      $mypassword = mysqli_real_escape_string($db,$_POST['password']);
      $sql = "SELECT id FROM logins WHERE username = '$myusername' and password = '$mypassword'";
      $result = mysqli_query($db,$sql);
      $count = mysqli_num_rows($result);
      if($count == 1) {
         // if the result matched $myusername and $mypassword, table row must be 1 row
         $_SESSION['login_user'] = $myusername;
         header("location: home.php");
      }else {
         $error = "Your Login Name or Password is invalid";
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
			<!--<div style = "font-size:11px; color:#cc0000; margin-top:10px"><?php echo $error; ?></div>-->
		</div>
	</div>
</div>
<?php
HTML_end();
?>