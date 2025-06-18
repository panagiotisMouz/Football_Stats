USE whybother;


CREATE TABLE countries (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    name            VARCHAR(100) NOT NULL UNIQUE,
    iso_code        CHAR(3),
    continent       VARCHAR(50),
    region          VARCHAR(50),
    status          VARCHAR(50),
    developed       VARCHAR(15),
    population      BIGINT,
    area_sq_km      INT
) ENGINE=InnoDB;

CREATE TABLE former_names (
    id             INT AUTO_INCREMENT PRIMARY KEY,
    current_name   VARCHAR(100) NOT NULL,
    former_name    VARCHAR(100) NOT NULL,
    start_date     DATE,
    end_date       DATE,
    country_id     INT,
    FOREIGN KEY (country_id) REFERENCES countries(id)
) ENGINE=InnoDB;

CREATE TABLE matches (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    match_date      DATE NOT NULL,
    home_team_id    INT NOT NULL,
    away_team_id    INT NOT NULL,
    home_score      INT,
    away_score      INT,
    tournament      VARCHAR(100),
    city            VARCHAR(100),
    country_id      INT,
    neutral         BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (home_team_id) REFERENCES countries(id),
    FOREIGN KEY (away_team_id) REFERENCES countries(id),
    FOREIGN KEY (country_id) REFERENCES countries(id)
);

CREATE TABLE players (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    name         VARCHAR(100) NOT NULL,
    country_id   INT NOT NULL,
    FOREIGN KEY (country_id) REFERENCES countries(id)
);

CREATE TABLE goalscorers (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    match_id   INT NOT NULL,
    player_id  INT NOT NULL,
    team_id    INT NOT NULL,
    minute     INT,
    own_goal   BOOLEAN DEFAULT FALSE,
    penalty    BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (match_id) REFERENCES matches(id),
    FOREIGN KEY (player_id) REFERENCES players(id),
    FOREIGN KEY (team_id) REFERENCES countries(id)
);

CREATE TABLE shootouts (
    id               INT AUTO_INCREMENT PRIMARY KEY,
    match_date       DATE NOT NULL,
    home_team_id     INT NOT NULL,
    away_team_id     INT NOT NULL,
    winner_id        INT NOT NULL,
    first_shooter_id INT,
    match_id         INT,
    FOREIGN KEY (home_team_id) REFERENCES countries(id),
    FOREIGN KEY (away_team_id) REFERENCES countries(id),
    FOREIGN KEY (winner_id) REFERENCES countries(id),
    FOREIGN KEY (first_shooter_id) REFERENCES countries(id),
    FOREIGN KEY (match_id) REFERENCES matches(id)
);
