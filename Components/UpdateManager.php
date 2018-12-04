<?php
namespace Components;

use Components\Commands\StatisticCommand;
use Components\CustomObjects\CustomUpdate;
use Telegram\Bot\Api;

class UpdateManager
{
    private $telegram;

    public function processUpdate($update)
    {
        $update = new CustomUpdate($update);
        $this->getApi()->processCommand($update);
        $this->handleUpdate($update);
    }

    public function getApi()
    {
        if(!$this->telegram){
            $this->telegram = new Api(getenv('BOT_TOKEN'));
            $this->telegram->addCommands([
                StatisticCommand::class,
            ]);
        }

        return $this->telegram;
    }

    /**
     * @param $update CustomUpdate
     */
    public function handleUpdate($update)
    {
        $update->save();
    }
}