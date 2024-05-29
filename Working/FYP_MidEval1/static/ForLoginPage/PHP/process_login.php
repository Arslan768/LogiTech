<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Retrieve the form data
    $username = $_POST["username"];
    $password = $_POST["password"];
    
    // Add your login logic here (e.g., check username and password against a database)
    
    // For demonstration purposes, echoing the values
    echo "Username: " . $username . "<br>";
    echo "Password: " . $password;
}