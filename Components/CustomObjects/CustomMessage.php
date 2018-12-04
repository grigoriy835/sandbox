<?php

namespace Components\CustomObjects;

use Components\Helpers\DbHelper;
use Telegram\Bot\Objects\Message;
use Telegram\Bot\Objects\User;
use Telegram\Bot\Objects\Chat;
use Telegram\Bot\Objects\MessageEntity;
use Telegram\Bot\Objects\Audio;
use Telegram\Bot\Objects\Document;
use Telegram\Bot\Objects\PhotoSize;
use Telegram\Bot\Objects\Sticker;
use Telegram\Bot\Objects\Video;
use Telegram\Bot\Objects\Voice;
use Telegram\Bot\Objects\Contact;
use Telegram\Bot\Objects\Location;
use Telegram\Bot\Objects\Venue;

class CustomMessage extends Message
{
    public function relations()
    {
        return [
            'from'             => CustomUser::class,
            'chat'             => CustomChat::class,
            'forward_from'     => User::class,
            'forward_from_chat'=> User::class,
            'reply_to_message' => self::class,
            'entities'         => MessageEntity::class,
            'audio'            => Audio::class,
            'document'         => Document::class,
            'photo'            => PhotoSize::class,
            'sticker'          => Sticker::class,
            'video'            => Video::class,
            'voice'            => Voice::class,
            'contact'          => Contact::class,
            'location'         => Location::class,
            'venue'            => Venue::class,
            'new_chat_member'  => User::class,
            'left_chat_member' => User::class,
            'new_chat_photo'   => PhotoSize::class,
            'pinned_message'   => Message::class,
        ];
    }

    public function save()
    {
        $data = [
            'messageId' => $this->getMessageId(),
            'from' => $this->getFrom()->getId(),
            'chat' => $this->getChat()->getId(),
            'updateId' => '', // todo
        ];
        DbHelper::getInstance()->saveRecord(DbHelper::MESSAGES_TABLE, $data);
    }

}