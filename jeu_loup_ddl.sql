DROP TABLE IF EXISTS parties,roles,players,players_in_parties,players_play,turns,plateaux,obstacles CASCADE;

-- create table settings_parties(
--     id_settings SERIAL PRIMARY KEY ,
--     nbr_ligne int,
--     nbr_col int,
--     wait_time int,
--     nbr_tour int,
--     nbr_obstacle int,
--     nbr_player int
-- );

create table parties (
    id_party SERIAL PRIMARY KEY,
    title_party text
);


create table plateaux(
    id_plateau int PRIMARY KEY,
    nbr_ligne int,
    nbr_col int,
    id_party int,
    FOREIGN KEY (id_party) REFERENCES parties(id_party),
    nbr_obstacle int
);

create table obstacles(
    pos_x int,
    pos_y int,
    id_plateau int,
    FOREIGN KEY (id_plateau) REFERENCES plateaux(id_plateau)
);




create table roles (
    id_role SERIAL PRIMARY KEY,
    description_role text
);

create table players (
    id_player SERIAL PRIMARY KEY,
    pseudo text
);

create table players_in_parties (
    id_party int,
    FOREIGN KEY (id_party) REFERENCES parties(id_party),
    id_player int,
     FOREIGN KEY (id_player) REFERENCES players(id_player),
    id_role int,
     FOREIGN KEY (id_role) REFERENCES roles(id_role),
    is_alive text
);

create table turns (
    id_turn SERIAL PRIMARY KEY,
    id_party int,
    FOREIGN KEY (id_party) REFERENCES parties(id_party),
    start_time date,
    end_time date
);

create table players_play (
    id_player int,
    FOREIGN KEY (id_player) REFERENCES players(id_player),
    id_turn int,
    FOREIGN KEY (id_turn) REFERENCES turns(id_turn),
    start_time date,
    end_time date,
    action varchar(10),
    origin_position_col text,
    origin_position_row text,
    target_position_col text,
    target_position_row text
);

INSERT INTO parties (title_party) VALUES ('Partie 1'), ('Partie 2'), ('Partie 3');
INSERT INTO players (pseudo) VALUES ('Alice'), ('Bob'), ('Charlie');
INSERT INTO roles (description_role) VALUES ('Loup'), ('Villageois');
INSERT INTO players_in_parties (id_party, id_player, id_role, is_alive) VALUES (1, 1, 1, 'yes'), (1, 2, 2, 'yes'), (2, 3, 1, 'no');
INSERT INTO turns (id_party, start_time) VALUES (1, '2023-10-01'), (2, '2023-10-02');
INSERT INTO players_play (id_player, id_turn, start_time, action, origin_position_col, origin_position_row, target_position_col, target_position_row) VALUES (1, 1, '2023-10-01', 'move', '00', '00', '01', '01'), (2, 1, '2023-10-01', 'move', '01', '01', '02', '02');

