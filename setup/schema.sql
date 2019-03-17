CREATE TABLE IF NOT EXISTS user_info (
    userid NUMERIC,
    creation_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    commands_done NUMERIC NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS user_balance (
    userid NUMERIC NOT NULL,
    balance NUMERIC NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS user_profile (
    userid NUMERIC NOT NULL,
    name TEXT UNIQUE NOT NULL,
    multiplier NUMERIC NOT NULL DEFAULT 1,
    inventory TEXT
);

CREATE TABLE IF NOT EXISTS commands (
    total_commands NUMERIC NOT NULL DEFAULT 0,
);

CREATE TABLE IF NOT EXISTS guild_prefixes (
    guild_id NUMERIC NOT NULL,
    prefix VARCHAR(512) NOT NULL
);
    
