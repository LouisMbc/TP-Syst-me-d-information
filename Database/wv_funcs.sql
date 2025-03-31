DROP FUNCTION IF EXISTS random_position();
DROP FUNCTION IF EXISTS random_position(INT);
DROP FUNCTION IF EXISTS random_role(INT);
DROP FUNCTION IF EXISTS get_the_winner(INT);
DROP FUNCTION IF EXISTS func_username_to_lower();
DROP FUNCTION IF EXISTS complete_tour();



-- Fonction pour attribuer une position aléatoire qui n'a jamais été utilisée dans une partie
CREATE OR REPLACE FUNCTION random_position(party_id INT) 
RETURNS TABLE(col TEXT, ligne TEXT) AS $$  
DECLARE
    plateau_cols INT;
    plateau_rows INT;
    found BOOLEAN := FALSE;
    random_col TEXT;
    random_row TEXT;
BEGIN
    -- Récupérer les dimensions du plateau pour cette partie
    SELECT nbr_col, nbr_ligne INTO plateau_cols, plateau_rows
    FROM plateaux
    WHERE id_party = party_id;
    
    -- Générer des positions aléatoires jusqu'à en trouver une non utilisée
    WHILE NOT found LOOP
        -- Générer des coordonnées aléatoires dans les limites du plateau
        random_col := LPAD(TRUNC(random() * plateau_cols)::TEXT, 2, '0');
        random_row := LPAD(TRUNC(random() * plateau_rows)::TEXT, 2, '0');
        
        -- Vérifier si cette position a déjà été utilisée dans cette partie
        PERFORM 1
        FROM players_play pp
        JOIN turns t ON pp.id_turn = t.id_turn
        WHERE t.id_party = party_id 
        AND (
            (pp.origin_position_col = random_col AND pp.origin_position_row = random_row) OR
            (pp.target_position_col = random_col AND pp.target_position_row = random_row)
        );
        
        -- Vérifier si la position est occupée par un obstacle
        PERFORM 1
        FROM obstacles o
        JOIN plateaux p ON o.id_plateau = p.id_plateau
        WHERE p.id_party = party_id
        AND o.pos_x::TEXT = random_col 
        AND o.pos_y::TEXT = random_row;
        
        -- Si position libre, sortir de la boucle
        IF NOT FOUND THEN
            found := TRUE;
        END IF;
    END LOOP;
    
    RETURN QUERY 
    SELECT random_col, random_row;
END;
$$ LANGUAGE plpgsql;

-- Fonction pour attribuer un rôle en respectant les quotas de loups et villageois
CREATE OR REPLACE FUNCTION random_role(party_id INT) RETURNS INT AS $$
DECLARE 
    total_players INT;
    total_wolves INT;
    max_wolves INT;
    role_id INT;
BEGIN
    -- Compter le nombre total de joueurs dans la partie
    SELECT COUNT(*) INTO total_players 
    FROM players_in_parties 
    WHERE id_party = party_id;
    
    -- Compter le nombre de loups déjà attribués
    SELECT COUNT(*) INTO total_wolves 
    FROM players_in_parties
    JOIN roles ON players_in_parties.id_role = roles.id_role
    WHERE id_party = party_id AND roles.description_role = 'loup';
    
    -- Calculer le nombre maximum de loups (environ 1/3 des joueurs)
    max_wolves := GREATEST(1, FLOOR(total_players / 3));
    
    -- Déterminer le prochain rôle à attribuer
    IF total_wolves < max_wolves THEN
        -- Sélectionner l'ID du rôle "loup"
        SELECT id_role INTO role_id FROM roles WHERE description_role = 'loup';
    ELSE
        -- Sélectionner l'ID du rôle "villageois"
        SELECT id_role INTO role_id FROM roles WHERE description_role = 'villageois';
    END IF;

    RETURN role_id;
END;
$$ LANGUAGE plpgsql;

-- Fonction pour récupérer les infos du gagnant d'une partie avec statistiques détaillées
CREATE OR REPLACE FUNCTION get_the_winner(party_id INT) 
RETURNS TABLE(
    nom_joueur TEXT,
    role TEXT,
    nom_partie TEXT,
    nb_tours_joues BIGINT,
    nb_total_tours BIGINT,
    temps_moyen_decision NUMERIC
) AS $$
DECLARE
    winning_role TEXT;
BEGIN
    -- Déterminer le rôle gagnant (loups ou villageois)
    SELECT CASE
        WHEN EXISTS (
            SELECT 1 FROM players_in_parties pip
            JOIN roles r ON pip.id_role = r.id_role
            WHERE pip.id_party = party_id 
            AND r.description_role = 'loup'
            AND pip.is_alive = 'true'
        ) THEN 'loup'
        ELSE 'villageois'
    END INTO winning_role;
    
    RETURN QUERY 
    SELECT 
        p.pseudo AS nom_joueur,
        r.description_role AS role,
        pa.title_party AS nom_partie,
        COUNT(DISTINCT pp.id_turn) AS nb_tours_joues,
        (SELECT COUNT(*) FROM turns WHERE id_party = party_id) AS nb_total_tours,
        AVG(EXTRACT(EPOCH FROM (pp.start_time - t.start_time))) AS temps_moyen_decision
    FROM players_in_parties pip
    JOIN players p ON pip.id_player = p.id_player
    JOIN roles r ON pip.id_role = r.id_role
    JOIN parties pa ON pip.id_party = pa.id_party
    JOIN turns t ON pa.id_party = t.id_party
    LEFT JOIN players_play pp ON p.id_player = pp.id_player AND t.id_turn = pp.id_turn
    WHERE pip.id_party = party_id
    AND r.description_role = winning_role
    AND pip.is_alive = 'true'
    GROUP BY p.id_player, p.pseudo, r.description_role, pa.id_party, pa.title_party
    ORDER BY nb_tours_joues DESC, temps_moyen_decision ASC
    LIMIT 1;
END;
$$ LANGUAGE plpgsql;

-- Fonction pour convertir le nom d'utilisateur en minuscules
CREATE OR REPLACE FUNCTION func_username_to_lower() RETURNS TRIGGER AS $$
BEGIN
    NEW.pseudo := LOWER(NEW.pseudo);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Fonction pour compléter un tour
CREATE OR REPLACE FUNCTION complete_tour() 
RETURNS TRIGGER AS $$
BEGIN
    -- Mettre à jour la date de fin du tour
    UPDATE turns 
    SET end_time = CURRENT_TIMESTAMP
    WHERE id_turn = NEW.id_turn;
    
    -- Vérifier si la partie est terminée (tous les loups morts ou tous les villageois morts)
    IF NOT EXISTS (
        SELECT 1 FROM players_in_parties pip
        JOIN roles r ON pip.id_role = r.id_role
        WHERE pip.id_party = NEW.id_party 
        AND r.description_role = 'loup'
        AND pip.is_alive = 'true'
    ) OR NOT EXISTS (
        SELECT 1 FROM players_in_parties pip
        JOIN roles r ON pip.id_role = r.id_role
        WHERE pip.id_party = NEW.id_party 
        AND r.description_role = 'villageois'
        AND pip.is_alive = 'true'
    ) THEN
        -- La partie est terminée, on pourrait ajouter des actions supplémentaires ici
        NULL;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;