create table register_user (
	contest_name varchar(64),
	team_name varchar(64),
	discord_id bigint,
	summoner_name varchar(32),
	register_time timestamp
);

create table registered_message (
	contest_name varchar(64),
	message_id bigint
);
