-- Fonction pour attribuer une position aléatoire qui n'a jamais été utilisée dans une partie
CREATE OR REPLACE FUNCTION random_position() 
RETURNS TABLE(col TEXT, ligne TEXT) AS $$  
BEGIN
    RETURN QUERY 
    SELECT 
        LPAD(TRUNC(random() * 10)::TEXT, 2, '0') AS col,  
        LPAD(TRUNC(random() * 10)::TEXT, 2, '0') AS ligne;  
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


drop function func_username_to_lower;
create or replace function func_username_to_lower() returns trigger AS $$
BEGIN
    call username_to_lower();
    return NEW;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION complete_tour() 
RETURNS TRIGGER AS $$
BEGIN
    -- Ici, ajoute la logique de fin de tour en utilisant NEW.id_turn et NEW.id_party
    PERFORM some_action(NEW.id_turn, NEW.id_party);  

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
