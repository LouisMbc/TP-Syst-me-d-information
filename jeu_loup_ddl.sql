DROP TABLE IF EXISTS parties,roles,players,players_in_parties,players_play,turns;

create table settings_parties(
    id_settings int PRIMARY KEY,
    nbr_ligne int,
    nbr_col int,
    wait_time int,
    nbr_tour int,
    nbr_obstacle int,
    nbr_player int
);

create table parties (
    id_party int PRIMARY KEY,
    id_settings int,
    FOREIGN KEY (id_settings) REFERENCES settings_parties(id_settings),
    title_party text
);

create table roles (
    id_role int PRIMARY KEY,
    description_role text
);

create table players (
    id_player int PRIMARY KEY,
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
    id_turn int PRIMARY KEY,
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

