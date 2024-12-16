<?php

namespace App\Http\Services;

use App\Models\Article;
use Illuminate\Support\Facades\Http;

class ArticleFetcher
{
    public function fetchArticles()
    {
        $response = Http::get('https://laravel-news.com/blog?tag=news');
        $articles = $response->json(); // Assuming JSON response

        foreach ($articles as $article) {
            Article::updateOrCreate(
                ['url' => $article['url']],
                [
                    'publication_date' => date('d.m.Y', strtotime($article['published_at'])),
                    'title' => $article['title'],
                    'url' => $article['url'],
                    'author' => $article['author'],
                    'tags' => implode(',', $article['tags']),
                ]
            );
        }
    }
}
