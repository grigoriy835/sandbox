<?php

namespace Artisan\Console\Commands;

use Components\Helpers\DbHelper;
use Illuminate\Console\Command;
use Telegram\Bot\Api;

class GetUpdates extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'bot:updates';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Load and handle updates for bot @todo';

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
        // todo
    }
}
