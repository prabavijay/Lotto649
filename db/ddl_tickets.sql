-- public.tickets definition

-- Drop table

-- DROP TABLE tickets;

CREATE TABLE tickets (
	id serial4 NOT NULL,
	ticket varchar(255) NULL,
	numbers_pool varchar(255) NULL,
	target_date date NOT NULL,
	predicted_nums varchar(255) NULL,
	predicted_posts varchar(255) NULL,
	CONSTRAINT tickets_pkey PRIMARY KEY (id)
);