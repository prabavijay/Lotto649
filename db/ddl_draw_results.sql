-- public.draw_results definition

-- Drop table

-- DROP TABLE draw_results;

CREATE TABLE draw_results (
	id serial4 NOT NULL,
	draw_date date NOT NULL,
	ball_1 int2 NOT NULL,
	ball_2 int2 NOT NULL,
	ball_3 int2 NOT NULL,
	ball_4 int2 NOT NULL,
	ball_5 int2 NOT NULL,
	ball_6 int2 NOT NULL,
	ball_7 int2 NOT NULL,
	CONSTRAINT draw_results_pkey PRIMARY KEY (id)
);