<?php

$fromPackage = __DIR__."/vendor/autoload.php";

if (file_exists($fromPackage)) {
    require_once $fromPackage;
} else {
    require_once "./vendor/autoload.php";
}

define('STORAGE_PATH', __DIR__.'/storage');
define('ROOT_DIR', __DIR__);

$boottstrapers = [
    'Components\Bootstrap\DetectEnvironment',
    'Components\Bootstrap\ErrorHandler'
];

foreach ($boottstrapers as $boottstraper) {
    $boottstraper::bootstrap();
}