CREATE VIEW v_players AS 
SELECT id_player, pseudo FROM players;

CREATE VIEW v_parties AS 
SELECT id_party, title_party FROM parties;

CREATE VIEW v_roles AS 
SELECT id_role, description_role FROM roles;

CREATE VIEW v_players_in_parties AS 
SELECT p.id_player, p.pseudo, r.description_role, pip.is_alive, par.title_party 
FROM players_in_parties pip
JOIN players p ON pip.id_player = p.id_player
JOIN roles r ON pip.id_role = r.id_role
JOIN parties par ON pip.id_party = par.id_party;


CREATE VIEW v_players_play AS 
SELECT pp.id_player, p.pseudo, pp.id_turn, pp.start_time, pp.end_time, pp.action,
       pp.origin_position_col, pp.origin_position_row, pp.target_position_col, pp.target_position_row
FROM players_play pp
JOIN players p ON pp.id_player = p.id_player;
