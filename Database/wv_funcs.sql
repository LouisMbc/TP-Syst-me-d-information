-- Fonction pour attribuer une position aléatoire qui n'a jamais été utilisée dans une partie
CREATE FUNCTION random_position(party_id INT) RETURNS TABLE(col TEXT, "row" TEXT) AS $$
BEGIN
    RETURN QUERY 
    SELECT LEFT(md5(random()::TEXT), 2), LEFT(md5(random()::TEXT), 2)
    WHERE NOT EXISTS (
        SELECT 1 FROM players_play WHERE id_party = party_id 
        AND origin_position_col = col AND origin_position_row = "row"
    ) LIMIT 1;
END;
$$ LANGUAGE plpgsql;

-- Fonction pour attribuer un rôle aléatoire en respectant les quotas
CREATE FUNCTION random_role(party_id INT) RETURNS INT AS $$
DECLARE 
    total_wolves INT;
    total_villagers INT;
    max_wolves INT := 2; -- Ex: Limite max de loups
    role_id INT;
BEGIN
    SELECT COUNT(*) INTO total_wolves FROM players_in_parties WHERE id_party = party_id AND id_role = 1;
    SELECT COUNT(*) INTO total_villagers FROM players_in_parties WHERE id_party = party_id AND id_role = 2;
    
    IF total_wolves < max_wolves THEN
        role_id := 1; -- Loup
    ELSE
        role_id := 2; -- Villageois
    END IF;

    RETURN role_id;
END;
$$ LANGUAGE plpgsql;

-- Fonction pour récupérer les infos du gagnant d'une partie
CREATE FUNCTION get_the_winner(party_id INT) RETURNS TABLE(player_id INT, pseudo TEXT, role TEXT) AS $$
BEGIN
    RETURN QUERY 
    SELECT pip.id_player, p.pseudo, r.description_role 
    FROM players_in_parties pip
    JOIN players p ON pip.id_player = p.id_player
    JOIN roles r ON pip.id_role = r.id_role
    WHERE pip.id_party = party_id AND pip.is_alive = 'yes'
    LIMIT 1;
END;
$$ LANGUAGE plpgsql;
