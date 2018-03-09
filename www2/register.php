<?php
   include("basic.php");
   HTML_start('Register');
   include("config.php");
   if($_SERVER["REQUEST_METHOD"] == "POST") {
      // username and password sent from form 
      $myusername = mysqli_real_escape_string($db,$_POST['username']);
      $mypassword = mysqli_real_escape_string($db,$_POST['password']);
      $sql = "SELECT id FROM logins WHERE username = '$myusername'";
      $result = mysqli_query($db,$sql);
      $count = mysqli_num_rows($result);
	  if($count == 1) {
         // If the result matched $myusername and $mypassword, table row must be 1 row
		 $message = "Username already exists!";
		 echo "<script type='text/javascript'>alert('$message');</script>";  
	  }else {
		 $sql = "INSERT INTO logins (username, password) VALUES ('$myusername', '$mypassword')";
		 if ($db->query($sql) === TRUE) {
			$message = "Account created successfully, please login";
			echo "<script type='text/javascript'>alert('$message');</script>";  
			echo "<script type='text/javascript'>window.location.replace('login.php');</script>";
			//header("location: login.php");
		 }else {
			echo "Error: " . $sql . "<br>" . $db->error;
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
			<!--<div style = "font-size:11px; color:#cc0000; margin-top:10px"><?php echo $error; ?></div>-->
		</div>
	</div>
</div>
<?php
HTML_end();
?>