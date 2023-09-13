-- public.freq_by_ball definition

-- Drop table

-- DROP TABLE freq_by_ball;

CREATE TABLE freq_by_ball (
	drawn_number serial4 NOT NULL,
	ball_1 int2 NULL,
	ball_2 int2 NULL,
	ball_3 int2 NULL,
	ball_4 int2 NULL,
	ball_5 int2 NULL,
	ball_6 int2 NULL,
	ball_7 int2 NULL,
	CONSTRAINT freq_by_ball_pkey PRIMARY KEY (drawn_number)
);