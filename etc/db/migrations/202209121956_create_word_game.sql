-- migrate:up


CREATE TABLE word_game
(
    id          SERIAL PRIMARY KEY,
    user_id     bigint  NOT NULL REFERENCES users (user_id) ON DELETE CASCADE,
    ctime       TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() at time zone 'utc'),
    etime       TIMESTAMP WITHOUT TIME ZONE,
    is_finished BOOLEAN NOT NULL            DEFAULT FALSE
);


-- migrate:down


DROP TABLE word_game CASCADE;