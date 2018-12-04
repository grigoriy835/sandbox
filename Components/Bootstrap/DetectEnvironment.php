<?php
namespace Components\Bootstrap;

use Dotenv\Dotenv;

class DetectEnvironment
{
    public static function bootstrap()
    {
        $dotenv = new Dotenv(ROOT_DIR);
        $dotenv->load();
    }
}