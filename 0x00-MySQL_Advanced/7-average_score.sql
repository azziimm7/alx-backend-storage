-- A stored procedure that computes average score for a user
DELIMITER $$
CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
	UPDATE users
	SET average_score=(SELECT AVG(score) FROM corrections
                           WHERE corrections.user_id=user_id)
	WHERE users.id=user_id;
END
$$
DELIMITER ;
