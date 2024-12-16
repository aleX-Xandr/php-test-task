<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use App\Http\Services\ArticleFetcher;

class FetchArticles extends Command
{
    protected $signature = 'articles:fetch';
    protected $description = 'Fetch and store articles from Laravel News';

    public function handle()
    {
        app(ArticleFetcher::class)->fetchArticles();
        $this->info('Articles updated successfully!');
    }
}
