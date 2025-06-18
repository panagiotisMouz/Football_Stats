
USE whybother;
-- ✅ 1. Νικητής ανά αγώνα
CREATE OR REPLACE VIEW view_match_winners AS
SELECT
    m.id AS match_id,
    c1.name AS home_team,
    c2.name AS away_team,
    m.home_score,
    m.away_score,
    s.winner_id IS NOT NULL AS has_shootout,
    CASE
        WHEN m.home_score > m.away_score THEN c1.name
        WHEN m.home_score < m.away_score THEN c2.name
        WHEN s.winner_id IS NOT NULL THEN cw.name
        ELSE 'Draw'
    END AS winner
FROM matches m
JOIN countries c1 ON m.home_team_id = c1.id
JOIN countries c2 ON m.away_team_id = c2.id
LEFT JOIN shootouts s ON m.id = s.match_id
LEFT JOIN countries cw ON s.winner_id = cw.id;

-- ✅ 2. Στατιστικά χώρας (νίκες, ισοπαλίες, ήττες)
CREATE OR REPLACE VIEW view_country_stats AS
SELECT
    country,
    COUNT(*) AS matches_played,
    SUM(result = 'Win') AS wins,
    SUM(result = 'Loss') AS losses,
    SUM(result = 'Draw') AS draws
FROM (
    SELECT c1.name AS country,
           CASE
               WHEN m.home_score > m.away_score THEN 'Win'
               WHEN m.home_score < m.away_score THEN 'Loss'
               ELSE 'Draw'
           END AS result
    FROM matches m
    JOIN countries c1 ON m.home_team_id = c1.id

    UNION ALL

    SELECT c2.name AS country,
           CASE
               WHEN m.away_score > m.home_score THEN 'Win'
               WHEN m.away_score < m.home_score THEN 'Loss'
               ELSE 'Draw'
           END AS result
    FROM matches m
    JOIN countries c2 ON m.away_team_id = c2.id
) AS sub
GROUP BY country;

-- ✅ 3. Top σκόρερς
CREATE OR REPLACE VIEW view_top_scorers AS
SELECT p.name AS player_name, c.name AS country, COUNT(*) AS goals
FROM goalscorers g
JOIN players p ON g.player_id = p.id
JOIN countries c ON p.country_id = c.id
WHERE g.own_goal = FALSE
GROUP BY p.id
ORDER BY goals DESC;

-- ✅ 4. Σύνοψη τουρνουά
CREATE OR REPLACE VIEW view_tournament_summary AS
SELECT
    m.tournament,
    YEAR(m.match_date) AS year,
    COUNT(*) AS total_matches,
    COUNT(DISTINCT m.home_team_id) + COUNT(DISTINCT m.away_team_id) AS total_teams
FROM matches m
GROUP BY m.tournament, YEAR(m.match_date);

-- ✅ 5. Νικητές στα πέναλτι
CREATE OR REPLACE VIEW view_penalty_winners AS
SELECT
    s.match_id,
    m.match_date,
    hc.name AS home_team,
    ac.name AS away_team,
    wc.name AS winner
FROM shootouts s
JOIN matches m ON s.match_id = m.id
JOIN countries hc ON s.home_team_id = hc.id
JOIN countries ac ON s.away_team_id = ac.id
JOIN countries wc ON s.winner_id = wc.id;

-- ✅ 6. Αγώνες μιας χώρας
CREATE OR REPLACE VIEW view_country_matches AS
SELECT m.*, c1.name AS home_team_name, c2.name AS away_team_name
FROM matches m
JOIN countries c1 ON m.home_team_id = c1.id
JOIN countries c2 ON m.away_team_id = c2.id;

-- ✅ 7. Γκολ ανά παίκτη
CREATE OR REPLACE VIEW view_player_goals AS
SELECT p.name AS player_name, COUNT(*) AS total_goals
FROM goalscorers g
JOIN players p ON g.player_id = p.id
GROUP BY p.id;

-- ✅ 8. Head-to-head δυο χωρών
-- (Μπορεί να χρειαστεί ερώτημα με φίλτρο σε αυτή τη view)
CREATE OR REPLACE VIEW view_country_vs_country AS
SELECT
    c1.name AS home_team,
    c2.name AS away_team,
    COUNT(*) AS matches_played,
    SUM(m.home_score > m.away_score) AS home_wins,
    SUM(m.home_score < m.away_score) AS away_wins,
    SUM(m.home_score = m.away_score) AS draws
FROM matches m
JOIN countries c1 ON m.home_team_id = c1.id
JOIN countries c2 ON m.away_team_id = c2.id
GROUP BY c1.name, c2.name;

-- ✅ 9. Γκολ ανά έτος
CREATE OR REPLACE VIEW view_goals_per_year AS
SELECT YEAR(m.match_date) AS year, COUNT(g.id) AS total_goals
FROM goalscorers g
JOIN matches m ON g.match_id = m.id
GROUP BY YEAR(m.match_date)
ORDER BY year;

-- ✅ 10. Πόλεις με αγώνες
CREATE OR REPLACE VIEW view_match_locations AS
SELECT city, COUNT(*) AS matches
FROM matches
WHERE city IS NOT NULL AND city != ''
GROUP BY city
ORDER BY matches DESC;
