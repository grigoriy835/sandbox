<?php

namespace Components\Commands;

use Telegram\Bot\Commands\Command;

class StatisticCommand extends Command
{
    /**
     * @var string Command Name
     */
    protected $name = "statistic";

    /**
     * @var string Command Description
     */
    protected $description = "show statistic for current chat";

    /**
     * @inheritdoc
     */
    public function handle($arguments)
    {
    }
}