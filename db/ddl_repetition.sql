-- public.repetition definition

-- Drop table

-- DROP TABLE repetition;

CREATE TABLE repetition (
	id serial4 NOT NULL,
	draw_date date NOT NULL,
	repeated_nums varchar(255) NULL,
	repeated_balls varchar(255) NULL,
	total_repeated int2 NULL,
	CONSTRAINT repetition_pkey PRIMARY KEY (id)
);