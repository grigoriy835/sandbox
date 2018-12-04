<?php

namespace Artisan\Console\Commands;

use Illuminate\Console\Command;
use Telegram\Bot\Api;

class InitBot extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'bot:init';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Set webhooks';

    /**
     * Create a new command instance.
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
        $telegram = new Api(getenv('BOT_TOKEN'));
        $params = [
            'url' => getenv('BOT_URL'),
            'certificate' => getenv('CERTIFICATE'),
        ];
        $response = $telegram->setWebhook($params);

        $this->info($response->getResult() ? 'so, all right, i think' : 'something went wrong((');
    }
}
