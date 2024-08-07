-- A stored procedure that computes average weighted score for all users
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
	UPDATE users AS U, (SELECT user_id,
			    SUM(score * weight) / SUM(weight) AS w_Avg
                            FROM corrections INNER JOIN projects
                            ON corrections.project_id = projects.id
                            GROUP BY user_id) AS WA
	SET U.average_score=WA.w_Avg
	WHERE U.id = WA.user_id;
END
$$
DELIMITER ;
