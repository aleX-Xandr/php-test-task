<?php

namespace App\Models;

use Carbon\Carbon;
use Illuminate\Database\Eloquent\Model;

class Article extends Model
{
    protected $fillable = ['publication_date', 'title', 'url', 'author', 'tags'];

    /**
     * Accessor to format the publication_date attribute.
     *
     * @return string
     */
    public function getPublicationDateAttribute($value)
    {
        return Carbon::parse($value)->format('d.m.Y');
    }
}
