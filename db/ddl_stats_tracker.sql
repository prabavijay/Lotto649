-- public.stats_tracker definition

-- Drop table

-- DROP TABLE stats_tracker;

CREATE TABLE stats_tracker (
	id serial4 NOT NULL,
	stats_table varchar(255) NULL,
	draw_processed int4 NULL
);