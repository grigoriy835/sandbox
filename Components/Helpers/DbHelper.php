<?php

namespace Components\Helpers;

use SimpleCrud\SimpleCrud;

class DbHelper
{
    const USERS_TABLE = 'users';
    const CHATS_TABLE = 'chats';
    const MESSAGES_TABLE = 'messages';
    const UPDATES_TABLE = 'updates';

    /**
     * @var self
     */
    private static $instance;

    /**
     * @var SimpleCrud
     */
    private $db;

    /**
     * @var \PDO
     */
    private $pdo;

    public static function getInstance()
    {
        if(!self::$instance){
            $obj = self::$instance = new self();
            $obj->pdo = new \PDO('sqlite:'.STORAGE_PATH.'/database/main.sq3');
            $obj->db = new SimpleCrud($obj->pdo);
        }

        return self::$instance;
    }

    public function execSql($sql)
    {
        $this->pdo->exec($sql);
    }

    public function saveRecord($table, $data)
    {
        $this->db->$table->create($data);
    }

}