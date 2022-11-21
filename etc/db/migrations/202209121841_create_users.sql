-- migrate:up


CREATE TABLE users(
    user_id bigint PRIMARY KEY,
    name VARCHAR(100) DEFAULT NULL,
    ctime TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() at time zone 'utc')
);

CREATE UNIQUE INDEX users_unique ON users(user_id);


-- migrate:down


DROP TABLE users CASCADE;
DROP INDEX users_unique;