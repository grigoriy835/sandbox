<?php

namespace Components\CustomObjects;

use Components\Helpers\DbHelper;
use Telegram\Bot\Objects\Chat;

class CustomChat extends Chat
{
    public function save()
    {
        $data = [
            'id' => $this->getId(),
            'type' => $this->getType(),
            'title' => $this->getTitle(),
            'username' => $this->getUsername(),
            'firstName' => $this->getFirstName(),
            'lastName' => $this->getLastName(),
        ];
        DbHelper::getInstance()->saveRecord(DbHelper::USERS_TABLE, $data);
    }
}