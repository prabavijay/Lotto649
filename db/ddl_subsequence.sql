-- public.subsequence definition

-- Drop table

-- DROP TABLE subsequence;

CREATE TABLE subsequence (
	id serial4 NOT NULL,
	ball_num int2 NOT NULL,
	base_num int2 NOT NULL,
	subseq_num int2 NOT NULL,
	frequency int2 NULL,
	CONSTRAINT subsequence_pkey PRIMARY KEY (id)
);