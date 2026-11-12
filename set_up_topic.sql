CREATE TABLE topic (
  id   INTEGER PRIMARY KEY,
  name TEXT NOT NULL UNIQUE
       CHECK (LOWER(name) IN ('politics', 'health', 'sport', 'tech'))
);