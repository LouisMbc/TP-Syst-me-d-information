-- Procédure pour insérer des données initiales
CREATE PROCEDURE SEED_DATA(NB_PLAYERS INT, PARTY_ID INT) AS $$
DECLARE 
    i INT;
    new_role INT;
BEGIN
    FOR i IN 1..NB_PLAYERS LOOP
        new_role := random_role(PARTY_ID);
        INSERT INTO players_in_parties (id_party, id_player, id_role, is_alive)
        VALUES (PARTY_ID, i, new_role, 'yes');
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- Procédure pour finaliser un tour et appliquer les actions
CREATE PROCEDURE COMPLETE_TOUR(TOUR_ID INT, PARTY_ID INT) AS $$
BEGIN
    -- Appliquer les déplacements
    UPDATE players_play
    SET origin_position_col = target_position_col,
        origin_position_row = target_position_row
    WHERE id_turn = TOUR_ID;

    -- Éliminer les villageois si un loup est sur la même position
    DELETE FROM players_in_parties 
    WHERE id_party = PARTY_ID 
    AND id_role = 2 
    AND (id_player, id_party) IN (
        SELECT p1.id_player, p1.id_party FROM players_play p1
        JOIN players_play p2 ON p1.target_position_col = p2.target_position_col
        AND p1.target_position_row = p2.target_position_row
        WHERE p1.id_turn = TOUR_ID AND p2.id_turn = TOUR_ID AND p2.id_role = 1
    );
END;
$$ LANGUAGE plpgsql;

-- Procédure pour mettre les pseudos des joueurs en minuscules
CREATE PROCEDURE USERNAME_TO_LOWER() AS $$
BEGIN
    UPDATE players SET pseudo = LOWER(pseudo);
END;
$$ LANGUAGE plpgsql;
