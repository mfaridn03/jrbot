CREATE TABLE IF NOT EXISTS user_info (
  userid BIGINT PRIMARY KEY,
  creation_date NUMERIC DEFAULT (strftime('%s', 'now'))
);

CREATE TABLE IF NOT EXISTS user_balance (
  userid BIGINT NOT NULL REFERENCES user_info(userid) ON DELETE CASCADE,
  balance NUMERIC NOT NULL DEFAULT 0
);
