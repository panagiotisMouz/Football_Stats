use whybother;
CREATE OR REPLACE VIEW match_results AS
SELECT
    m.id AS match_id,
    m.match_date,
    c1.name AS home_team,
    m.home_score,
    c2.name AS away_team,
    m.away_score,
    m.tournament,
    m.city,
    c3.name AS host_country,
    m.neutral,
    CASE
        WHEN m.home_score > m.away_score THEN c1.name
        WHEN m.away_score > m.home_score THEN c2.name
        WHEN m.home_score = m.away_score THEN
            CASE
                WHEN s.winner_id = m.home_team_id THEN c1.name
                WHEN s.winner_id = m.away_team_id THEN c2.name
                ELSE NULL
            END
        ELSE NULL
    END AS winner
FROM matches m
LEFT JOIN countries c1 ON m.home_team_id = c1.id
LEFT JOIN countries c2 ON m.away_team_id = c2.id
LEFT JOIN countries c3 ON m.country_id = c3.id
LEFT JOIN shootouts s ON m.id = s.match_id;
CREATE OR REPLACE VIEW country_stats AS
SELECT
    name,
    COUNT(*) AS matches_played,
    SUM(wins) AS wins,
    SUM(draws) AS draws,
    SUM(losses) AS losses
FROM (
    SELECT
        c.name,
        CASE WHEN mr.winner = c.name THEN 1 ELSE 0 END AS wins,
        CASE WHEN mr.winner IS NULL THEN 1 ELSE 0 END AS draws,
        CASE WHEN mr.winner != c.name AND mr.winner IS NOT NULL THEN 1 ELSE 0 END AS losses
    FROM match_results mr
    JOIN countries c ON c.name IN (mr.home_team, mr.away_team)
) sub
GROUP BY name;
SELECT
    p.name AS player,
    c.name AS country,
    COUNT(*) AS goals
FROM goalscorers g
JOIN players p ON g.player_id = p.id
JOIN countries c ON p.country_id = c.id
GROUP BY p.name, c.name
ORDER BY goals DESC
LIMIT 20;
SELECT
    c.name AS country,
    m.tournament,
    COUNT(*) AS appearances
FROM matches m
JOIN countries c ON c.id IN (m.home_team_id, m.away_team_id)
GROUP BY c.name, m.tournament
ORDER BY appearances DESC;
SELECT
    m.match_date,
    ch.name AS home,
    m.home_score,
    ca.name AS away,
    m.away_score,
    mr.winner
FROM match_results mr
JOIN matches m ON mr.match_id = m.id
JOIN countries ch ON m.home_team_id = ch.id
JOIN countries ca ON m.away_team_id = ca.id
WHERE (ch.name = 'France' AND ca.name = 'Germany')
   OR (ch.name = 'Germany' AND ca.name = 'France')
ORDER BY m.match_date DESC;

CREATE OR REPLACE VIEW top_scorers AS
SELECT
    p.id AS player_id,
    p.name AS player,
    c.name AS country,
    COUNT(*) AS total_goals
FROM goalscorers g
JOIN players p ON g.player_id = p.id
JOIN countries c ON p.country_id = c.id
GROUP BY p.id, p.name, c.name
ORDER BY total_goals DESC;

CREATE OR REPLACE VIEW tournament_appearances AS
SELECT
    c.name AS country,
    m.tournament,
    COUNT(*) AS appearances
FROM matches m
JOIN countries c ON c.id IN (m.home_team_id, m.away_team_id)
GROUP BY c.name, m.tournament;

CREATE OR REPLACE VIEW france_vs_germany AS
SELECT
    m.match_date,
    ch.name AS home_team,
    m.home_score,
    ca.name AS away_team,
    m.away_score,
    mr.winner
FROM match_results mr
JOIN matches m ON mr.match_id = m.id
JOIN countries ch ON m.home_team_id = ch.id
JOIN countries ca ON m.away_team_id = ca.id
WHERE (ch.name = 'France' AND ca.name = 'Germany')
   OR (ch.name = 'Germany' AND ca.name = 'France');
