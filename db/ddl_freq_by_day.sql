-- public.freq_by_day definition

-- Drop table

-- DROP TABLE freq_by_day;

CREATE TABLE freq_by_day (
	drawn_number serial4 NOT NULL,
	wed int2 NULL,
	sat int2 NULL,
	CONSTRAINT freq_by_day_pkey PRIMARY KEY (drawn_number)
);