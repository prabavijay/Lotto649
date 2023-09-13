-- public.draw_stats definition

-- Drop table

-- DROP TABLE draw_stats;

CREATE TABLE draw_stats (
	id serial4 NOT NULL,
	repeated_nums varchar(255) NULL,
	repeated_balls varchar(255) NULL,
	frequented_nums varchar(255) NULL,
	missing_nums varchar(255) NULL,
	freq_and_missing varchar(255) NULL,
	CONSTRAINT draw_stats_pkey PRIMARY KEY (id)
);