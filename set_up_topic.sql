CREATE TABLE topic (
  id   INTEGER PRIMARY KEY,
  topic_name TEXT NOT NULL UNIQUE
       CHECK (LOWER(topic_name) IN ('politics', 'health', 'sport', 'tech'))
);