CREATE OR REPLACE VIEW view_match_results AS
SELECT
  m.id AS match_id,
  m.match_date,
  m.home_team_id,
  m.away_team_id,
  m.home_score,
  m.away_score,
  CASE
    WHEN m.home_score > m.away_score THEN m.home_team_id
    WHEN m.away_score > m.home_score THEN m.away_team_id
    ELSE NULL
  END AS winner_id,
  CASE
    WHEN m.home_score = m.away_score AND s.winner_id IS NOT NULL THEN s.winner_id
    ELSE NULL
  END AS shootout_winner_id
FROM matches m
LEFT JOIN shootouts s ON m.id = s.match_id;


CREATE OR REPLACE VIEW view_top_scorers AS
SELECT
  p.id AS player_id,
  p.name AS player_name,
  c.name AS country_name,
  COUNT(g.id) AS total_goals
FROM players p
JOIN goalscorers g ON g.player_id = p.id
JOIN countries c ON p.country_id = c.id
GROUP BY p.id, p.name, c.name;

CREATE OR REPLACE VIEW view_goals_per_country_per_year AS
SELECT
  c.id AS country_id,
  c.name AS country_name,
  YEAR(m.match_date) AS year,
  SUM(CASE WHEN m.home_team_id = c.id THEN m.home_score
           WHEN m.away_team_id = c.id THEN m.away_score
           ELSE 0 END) AS goals
FROM countries c
JOIN matches m ON c.id IN (m.home_team_id, m.away_team_id)
GROUP BY c.id, c.name, year;

CREATE OR REPLACE VIEW view_country_points AS
SELECT
  c.id AS country_id,
  c.name AS country_name,
  SUM(CASE
      WHEN (m.home_team_id = c.id AND m.home_score > m.away_score) OR
           (m.away_team_id = c.id AND m.away_score > m.home_score)
        THEN 3
      WHEN m.home_score = m.away_score THEN 1
      ELSE 0
  END) AS points
FROM countries c
JOIN matches m ON c.id IN (m.home_team_id, m.away_team_id)
GROUP BY c.id, c.name;