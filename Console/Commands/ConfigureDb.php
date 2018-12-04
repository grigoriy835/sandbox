<?php

namespace Artisan\Console\Commands;

use Components\Helpers\DbHelper;
use Illuminate\Console\Command;

class ConfigureDb extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'db:initDb';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'create base tables in sqlite base';

    /**
     * Create a new command instance.
     *
     * @return void
     */
    public function __construct()
    {
        parent::__construct();
    }

    /**
     * Execute the console command.
     *
     * @return mixed
     */
    public function handle()
    {
        $helper = DbHelper::getInstance();
        foreach ($this->getQueries() as $query){
            $helper->execSql($query);
        }
    }

    private function getQueries()
    {
        return [
            'CREATE TABLE IF NOT EXISTS ' . DbHelper::USERS_TABLE . ' (
                        id   VARCHAR (255) PRIMARY KEY,
                        firstName TEXT NOT NULL,
                        lastName TEXT DEFAULT NULL,
                        username TEXT DEFAULT NULL                   
                      )',
            'CREATE TABLE IF NOT EXISTS ' . DbHelper::CHATS_TABLE . ' (
                        id   VARCHAR (255) PRIMARY KEY,
                        `type` VARCHAR (255) NOT NULL,
                        title TEXT DEFAULT NULL,
                        username TEXT DEFAULT NULL,
                        firstName TEXT DEFAULT NULL,
                        lastName TEXT DEFAULT NULL        
                      )',
            'CREATE TABLE IF NOT EXISTS ' . DbHelper::MESSAGES_TABLE . ' (
                        id   INTEGER PRIMARY KEY AUTOINCREMENT,
                        messageId VARCHAR (255) NOT NULL,
                        `from` VARCHAR (255) DEFAULT NULL,
                        chat VARCHAR (255) DEFAULT NULL,
                        updateId VARCHAR (255) NOT NULL
                      )',
            'CREATE TABLE IF NOT EXISTS ' . DbHelper::UPDATES_TABLE . ' (
                        updateId VARCHAR (255) PRIMARY KEY,
                        content TEXT NOT NULL
                      )',
        ];
    }
}
