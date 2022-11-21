-- migrate:up


CREATE TABLE words
(
    id   SERIAL PRIMARY KEY,
    word VARCHAR(50)
);

CREATE UNIQUE INDEX words_unique ON words (word);


-- migrate:down


DROP TABLE words CASCADE;
DROP INDEX words_unique;