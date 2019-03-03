CREATE TABLE IF NOT EXISTS user_info (
    userid NUMERIC,
    creation_date NUMERIC DEFAULT (strftime('%s', 'now'))
);

CREATE TABLE IF NOT EXISTS user_balance (
    userid NUMERIC NOT NULL,
    balance NUMERIC NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS user_profile (
    userid NUMERIC NOT NULL
    name TEXT UNIQUE NOT NULL,
    multiplier NUMERIC NOT NULL DEFAULT 0
);
  
  
