<?php

namespace Components\CustomObjects;

use Components\Helpers\DbHelper;
use Telegram\Bot\Objects\CallbackQuery;
use Telegram\Bot\Objects\ChosenInlineResult;
use Telegram\Bot\Objects\EditedMessage;
use Telegram\Bot\Objects\InlineQuery;
use Telegram\Bot\Objects\Update;

class CustomUpdate extends Update
{
    public function relations()
    {
        return [
            'message'              => CustomMessage::class,
            'edited_message'       => EditedMessage::class,
            'inline_query'         => InlineQuery::class,
            'chosen_inline_result' => ChosenInlineResult::class,
            'callback_query'       => CallbackQuery::class,
        ];
    }

    public function save()
    {
        if($message = $this->getMessage()){
            if($message instanceof CustomMessage){
                $message->save();
            }
            if($user = $message->getFrom()){
                if($user instanceof CustomUser){
                    $user->save();
                }
            }
        }

        if($chat = $this->getChat()){
            if($chat instanceof CustomChat){
                $chat->save();
            }
        }

        $data = [
            'updateId' => $this->getUpdateId(),
            'content' => '' // todo
        ];
        DbHelper::getInstance()->saveRecord(DbHelper::UPDATES_TABLE, $data);
    }
}