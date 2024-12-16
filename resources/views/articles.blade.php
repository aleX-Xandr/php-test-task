<table>
    <thead>
        <tr>
            <th>Publication Date</th>
            <th>Title</th>
            <th>Author</th>
            <th>Tags</th>
        </tr>
    </thead>
    <tbody>
        @foreach ($articles as $article)
        <tr>
            <td>{{ $article->publication_date }}</td>
            <td><a href="{{ $article->url }}">{{ $article->title }}</a></td>
            <td>{{ $article->author }}</td>
            <td>{{ $article->tags }}</td>
        </tr>
        @endforeach
    </tbody>
</table>
