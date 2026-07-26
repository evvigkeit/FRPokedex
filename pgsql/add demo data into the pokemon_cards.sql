CREATE TABLE IF NOT EXISTS pokemon_cards (
	pokemon_id SERIAL PRIMARY KEY,
	pokemon_name VARCHAR(50) UNIQUE NOT NULL,
	file_name VARCHAR(50) UNIQUE NOT NULL
);

INSERT INTO pokemon_cards (pokemon_name, file_name) VALUES 
	('Ditto', 'Ditto.png'),
	('Eevee', 'Eevee.png'),
	('Fearow', 'Fearow.png'),
	('Flareon', 'Flareon.png'),
	('Jigglypuff', 'Jigglypuff.png'),
	('Jolteon', 'Jolteon.png'),
	('Machoke', 'Machoke.png'),
	('Snorlax', 'Snorlax.png'),
	('Vaporeon', 'Vaporeon.png'),
	('Venusaur', 'Venusaur.png');