-- migrate:up

ALTER TABLE words
    ADD COLUMN difficulty INTEGER NOT NULL DEFAULT 1;

ALTER TABLE word_game
    ADD COLUMN difficulty INTEGER NOT NULL DEFAULT 1;

-- migrate:down

ALTER TABLE words
    DROP COLUMN difficulty CASCADE;

ALTER TABLE word_game
    DROP COLUMN difficulty CASCADE;