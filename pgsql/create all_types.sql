CREATE TABLE IF NOT EXISTS all_types (
	type_id SERIAL PRIMARY KEY,
	type_name VARCHAR(50) UNIQUE NOT NULL
);

INSERT INTO all_types (type_name) VALUES 
	('Normal'),
	('Fighting'),
	('Poison'),
	('Ground'),
	('Flying'),
	('Bug'),
	('Rock'),
	('Ghost'),
	('Steel'),
	('Fire'),
	('Water'),
	('Grass'),
	('Elecrtic'),
	('Ice'),
	('Psychic'),
	('Dragon'),
	('Dark')
