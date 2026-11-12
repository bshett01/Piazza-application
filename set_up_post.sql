CREATE TABLE post (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expires_at DATETIME NOT NULL,

    status TEXT NOT NULL
           CHECK (LOWER(status) IN ('live', 'expired'))
           DEFAULT 'live',

    like_count INTEGER NOT NULL DEFAULT 0,
    dislike_count INTEGER NOT NULL DEFAULT 0,
    comments TEXT,

    FOREIGN KEY (author_id) REFERENCES users(id)
);