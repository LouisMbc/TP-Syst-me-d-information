DROP VIEW IF EXISTS v_players, v_parties, v_roles, v_players_in_parties, v_players_play;

-- Vues de base pour chaque table
CREATE VIEW v_parties AS
SELECT * FROM parties;

CREATE VIEW v_plateaux AS
SELECT * FROM plateaux;

CREATE VIEW v_obstacles AS
SELECT * FROM obstacles;

CREATE VIEW v_roles AS
SELECT * FROM roles;

CREATE VIEW v_players AS
SELECT * FROM players;

CREATE VIEW v_players_in_parties AS
SELECT * FROM players_in_parties;

CREATE VIEW v_turns AS
SELECT * FROM turns;

CREATE VIEW v_players_play AS
SELECT * FROM players_play;

-- 1. Vue ALL_PLAYERS
CREATE VIEW ALL_PLAYERS AS
SELECT 
    p.pseudo AS "nom du joueur",
    COUNT(DISTINCT pip.id_party) AS "nombre de parties jouées",
    COUNT(DISTINCT pp.id_turn) AS "nombre de tours joués",
    MIN(t.start_time) AS "date et heure de la première participation",
    MAX(pp.end_time) AS "date et heure de la dernière action"
FROM 
    players p
    JOIN players_in_parties pip ON p.id_player = pip.id_player
    JOIN players_play pp ON p.id_player = pp.id_player
    JOIN turns t ON pp.id_turn = t.id_turn
GROUP BY 
    p.id_player, p.pseudo
ORDER BY 
    "nombre de parties jouées" DESC,
    "date et heure de la première participation" ASC,
    "date et heure de la dernière action" ASC,
    "nom du joueur" ASC;

-- 2. Vue ALL_PLAYERS_ELAPSED_GAME (corrigée)
CREATE VIEW ALL_PLAYERS_ELAPSED_GAME AS
SELECT 
    p.pseudo AS "nom du joueur",
    pa.title_party AS "nom de la partie",
    COUNT(DISTINCT pip2.id_player) AS "nombre de participants",
    MIN(pp.start_time) AS "date et heure de la première action du joueur dans la partie",
    MAX(pp.end_time) AS "date et heure de la dernière action du joueur dans la partie",
    EXTRACT(EPOCH FROM (MAX(pp.end_time)::timestamp - MIN(pp.start_time)::timestamp)) AS "nb de secondes passées dans la partie pour le joueur"
FROM 
    players p
    JOIN players_in_parties pip ON p.id_player = pip.id_player
    JOIN parties pa ON pip.id_party = pa.id_party
    JOIN players_in_parties pip2 ON pa.id_party = pip2.id_party
    JOIN turns t ON pa.id_party = t.id_party
    JOIN players_play pp ON p.id_player = pp.id_player AND t.id_turn = pp.id_turn
GROUP BY 
    p.id_player, p.pseudo, pa.id_party, pa.title_party;

-- 3. Vue ALL_PLAYERS_ELAPSED_TOUR (corrigée)
CREATE VIEW ALL_PLAYERS_ELAPSED_TOUR AS
SELECT 
    p.pseudo AS "nom du joueur",
    pa.title_party AS "nom de la partie",
    t.id_turn AS "n° du tour",
    t.start_time AS "date et heure du début du tour",
    pp.start_time AS "date et heure de la prise de décision du joueur dans le tour",
    EXTRACT(EPOCH FROM (pp.start_time::timestamp - t.start_time::timestamp)) AS "nb de secondes passées dans le tour pour le joueur"
FROM 
    players p
    JOIN players_play pp ON p.id_player = pp.id_player
    JOIN turns t ON pp.id_turn = t.id_turn
    JOIN parties pa ON t.id_party = pa.id_party;

-- 4. Vue ALL_PLAYERS_STATS (corrigée)
CREATE VIEW ALL_PLAYERS_STATS AS
SELECT 
    p.pseudo AS "nom du joueur",
    r.description_role AS "role parmi loup et villageois",
    pa.title_party AS "nom de la partie",
    COUNT(DISTINCT pp.id_turn) AS "nb de tours joués par le joueur",
    COUNT(DISTINCT t.id_turn) AS "nb total de tours de la partie",
    CASE 
        WHEN r.description_role = 'loup' AND EXISTS (
            SELECT 1 FROM players_in_parties pip2 
            WHERE pip2.id_party = pa.id_party 
            AND pip2.id_role = (SELECT id_role FROM roles WHERE description_role = 'loup')
            AND pip2.is_alive = 'true'
        ) THEN 'Loups'
        WHEN r.description_role = 'villageois' AND NOT EXISTS (
            SELECT 1 FROM players_in_parties pip2 
            WHERE pip2.id_party = pa.id_party 
            AND pip2.id_role = (SELECT id_role FROM roles WHERE description_role = 'loup')
            AND pip2.is_alive = 'true'
        ) THEN 'Villageois'
        ELSE 'Aucun'
    END AS "vainqueur dépendant du rôle du joueur",
    AVG(EXTRACT(EPOCH FROM (pp.start_time::timestamp - t.start_time::timestamp))) AS "temps moyen de prise de décision du joueur"
FROM 
    players p
    JOIN players_in_parties pip ON p.id_player = pip.id_player
    JOIN roles r ON pip.id_role = r.id_role
    JOIN parties pa ON pip.id_party = pa.id_party
    JOIN turns t ON pa.id_party = t.id_party
    JOIN players_play pp ON p.id_player = pp.id_player AND t.id_turn = pp.id_turn
GROUP BY 
    p.id_player, p.pseudo, r.description_role, pa.id_party, pa.title_party;