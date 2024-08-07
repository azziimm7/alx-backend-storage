-- A stored procedure that computes average weighted score for a user
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
	UPDATE users
	SET average_score=(SELECT SUM(corrections.score * projects.weight) / (SUM(projects.weight))
			   FROM corrections INNER JOIN projects
			   ON corrections.project_id = projects.id
                           WHERE corrections.user_id=user_id)
	WHERE users.id=user_id;
END
$$
DELIMITER ;
