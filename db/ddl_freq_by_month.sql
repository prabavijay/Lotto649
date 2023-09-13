-- public.freq_by_month definition

-- Drop table

-- DROP TABLE freq_by_month;

CREATE TABLE freq_by_month (
	drawn_number serial4 NOT NULL,
	jan int2 NULL,
	feb int2 NULL,
	mar int2 NULL,
	apr int2 NULL,
	may int2 NULL,
	jun int2 NULL,
	jul int2 NULL,
	aug int2 NULL,
	sep int2 NULL,
	oct int2 NULL,
	nov int2 NULL,
	"dec" int2 NULL,
	CONSTRAINT freq_by_month_pkey PRIMARY KEY (drawn_number)
);