<?php

define('DEBUG', False);

require_once "./../bootstrap.php";

if($message = json_decode(file_get_contents('php://input'), true)) {
    $tt = new Components\UpdateManager();
    $tt->processUpdate($message);
}
