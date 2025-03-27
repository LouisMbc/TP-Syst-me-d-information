-- Trigger : Mettre les pseudos en minuscules à l'insertion d'un joueur
CREATE TRIGGER TRG_USERNAME_TO_LOWER
BEFORE INSERT OR UPDATE ON players
FOR EACH ROW
EXECUTE FUNCTION username_to_lower();

-- Trigger : Appliquer la procédure COMPLETE_TOUR à la fin d'un tour
CREATE TRIGGER TRG_COMPLETE_TOUR
AFTER UPDATE ON turns
FOR EACH ROW
WHEN (NEW.end_time IS NOT NULL)
EXECUTE PROCEDURE complete_tour(NEW.id_turn, NEW.id_party);