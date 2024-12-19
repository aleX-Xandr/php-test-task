<?php

namespace App\Http\Controllers;

use App\Models\Article;
use Illuminate\Http\Request;
use App\Http\Controllers\Controller;

class ArticleController extends Controller
{
    public function index(Request $request)
    {
        $sortField = $request->query('sorting', 'author'); 
        $allowedSortFields = ['author', 'publication_date', 'title'];

        // Validate and set the sort field, fallback to 'author' if invalid
        if (!in_array($sortField, $allowedSortFields)) {
            $sortField = 'author';
        }
        $sortDirection = $sortField === 'publication_date' ? 'desc' : 'asc';

        // Fetch and sort articles
        $articles = Article::orderBy($sortField, $sortDirection)->get();

        return view('articles', compact('articles'));
    }
}