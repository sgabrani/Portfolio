<?php
//Mail sending function
$subject = $_POST['name'];
$from = "sahitigabrani@gmail.com";
$to = "sahitigabrani@gmail.com";
$message= $_POST['message'];

//Headers
$headers  = "MIME-Version: 1.0\r\n";
$headers .= "Content-type: text/html; charset=UTF-8\r\n";
$headers .= "From: <".$from. ">" ;

mail($to,$subject,$message,$headers);
echo "Mail Sent.";
?>
