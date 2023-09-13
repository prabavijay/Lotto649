-- public.freq_and_missn definition

-- Drop table

-- DROP TABLE freq_and_missn;

CREATE TABLE freq_and_missn (
	id serial4 NOT NULL,
	draw_date date NOT NULL,
	frequented_nums varchar(255) NULL,
	missing_nums varchar(255) NULL,
	freq_and_missing varchar(255) NULL,
	CONSTRAINT freq_and_missn_pkey PRIMARY KEY (id)
);