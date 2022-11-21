-- migrate:up

CREATE TYPE answer_source_enum AS ENUM ('user', 'bot');


CREATE TABLE word_game_history
(
    id            SERIAL PRIMARY KEY,
    game_id       bigint             NOT NULL REFERENCES word_game (id) ON DELETE CASCADE,
    word_id       bigint             NOT NULL REFERENCES words (id) ON DELETE CASCADE,
    answer_source answer_source_enum NOT NULL,
    ctime         TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() at time zone 'utc')
);


-- migrate:down

DROP TABLE word_game_history CASCADE;
DROP TYPE answer_source_enum CASCADE;