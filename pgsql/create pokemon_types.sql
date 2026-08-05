CREATE TABLE IF NOT EXISTS pokemon_types (
	pokemon_id INTEGER REFERENCES pokemon_basic_info ON DELETE CASCADE,
	type_id INTEGER REFERENCES all_types ON DELETE CASCADE
);

INSERT INTO pokemon_types (pokemon_id, type_id) VALUES
	(1, 1),
	(2, 1),
	(3, 1),
	(3, 5),
	(4, 10),
	(5, 1),
	(6, 13),
	(7, 2),
	(8, 1),
	(9, 11),
	(10, 3),
	(10, 12);