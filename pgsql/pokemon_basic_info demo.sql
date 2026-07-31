CREATE TABLE IF NOT EXISTS pokemon_basic_info (
	pokemon_id SERIAL PRIMARY KEY,
	pokemon_name VARCHAR(50) UNIQUE NOT NULL,
	description VARCHAR(500),
	height REAL, 
	weight REAL,
	gender SMALLINT,
	category VARCHAR(15) NOT NULL,
	file_name VARCHAR(50) UNIQUE NOT NULL
);

INSERT INTO pokemon_basic_info (pokemon_name, description, height, weight, gender, category, file_name) VALUES 
	('Ditto', 'Its transformation ability is perfect. However, if made to laugh, it can’t maintain its disguise.', 0.3, 4.0, 0, 'Transform', 'Ditto.png'),
	('Eevee', 'Thanks to its unstable genetic makeup, this special Pokémon conceals many different possible evolutions.', 0.3, 6.5, 3, 'Evolution', 'Eevee.png'),
	('Fearow', 'A Pokémon that dates back many years. If it senses danger, it flies high and away, instantly.', 1.2, 38.0, 3, 'Beak', 'Fearow.png'),
	('Flareon', 'Inhaled air is carried to its flame sac, heated, and exhaled as fire that reaches over 3,000 degrees Fahrenheit.', 0.9, 25.0, 3, 'Flame', 'Flareon.png'),
	('Jigglypuff', 'When its huge eyes waver, it sings a mysteriously soothing melody that lulls its enemies to sleep.', 0.5, 5.5, 3, 'Balloon', 'Jigglypuff.png'),
	('Jolteon', 'It concentrates the weak electric charges emitted by its cells and launches wicked lightning bolts.', 0.8, 24.5, 3, 'Lightning', 'Jolteon.png'),
	('Machoke', 'Its muscular body is so powerful, it must wear a power-save belt to be able to regulate its motions.', 1.5, 70.5, 3, 'Superpower', 'Machoke.png'),
	('Snorlax', 'This gluttonous Pokémon eats constantly, apart from when it’s asleep. It devours nearly 900 pounds of food per day.', 2.1, 460.0, 3, 'Sleeping', 'Snorlax.png'),
	('Vaporeon', 'It lives close to water. Its long tail is ridged with a fin, which is often mistaken for a mermaid’s.', 1.0, 29.0, 3, 'Bubble Jet', 'Vaporeon.png'),
	('Venusaur', 'After a rainy day, the flower on its back smells stronger. The scent attracts other Pokémon.', 2.0, 100.0, 3, 'Seed', 'Venusaur.png');
