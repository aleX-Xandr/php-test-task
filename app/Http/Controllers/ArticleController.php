<?php

namespace App\Http\Controllers;

use App\Models\Article;
use App\Http\Controllers\Controller;

class ArticleController extends Controller
{
    public function index()
    {
        $articles = Article::orderBy('author')->get();
        return view('articles', compact('articles'));
    }
}