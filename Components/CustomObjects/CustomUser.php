<?php

namespace Components\CustomObjects;

use Components\Helpers\DbHelper;
use Telegram\Bot\Objects\User;

class CustomUser extends User
{
    public function save()
    {
        $data = [
            'id' => $this->getId(),
            'firstName' => $this->getFirstName(),
            'lastName' => $this->getLastName(),
            'username'=> $this->getUsername()
        ];
        DbHelper::getInstance()->saveRecord(DbHelper::USERS_TABLE, $data);
    }
}