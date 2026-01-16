<?php
$host     = 'db';   // atau 'localhost'
$user     = 'root';
$password = 'root';
$db       = 'quizpengupil';
$port     = 3306;         // port MySQL Docker

$con = mysqli_connect($host, $user, $password, $db, $port);
if (!$con) {
    die("Connection failed: " . mysqli_connect_error());
}
?>
