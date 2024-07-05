from typing import Dict, Any, List

import sqlite3
from datetime import datetime


class DatabaseManager:
    def __init__(self, db_filepath: str) -> None:
        self.db_filepath = db_filepath

        self.conn = sqlite3.connect(self.db_filepath, )
        self.cursor = self.conn.cursor()
        self.create_db()

    def insert(self, 
               match_info: Dict[str, Any] = None,
               teams_in_match_info: List[Dict[str, Any]] = [],
               teams_in_set_info: List[Dict[str, Any]] = [],
               players_statistics: List[Dict[str, Any]] = []):
        self.insert_match_info(match_info=match_info)
        for team in teams_in_match_info:
            self.insert_team_in_match_info(team_in_match_info=team)
        for team in teams_in_set_info:
            self.insert_team_set_info(team_in_set_info=team)
        for player in players_statistics:
            self.insert_player_statistics(player_statistics=player)

    def create_db(self):
        # Match Information
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS Match (
                                match_id INT PRIMARY KEY,
                                stage TEXT,
                                step TEXT,
                                gender TEXT CHECK(gender IN ('Men', 'Women')),
                                no INTEGER,
                                country TEXT,
                                city TEXT,
                                date_and_time TEXT,
                                referee_1_name TEXT,
                                referee_1_nation TEXT,
                                referee_2_name TEXT,
                                referee_2_nation TEXT
                                )
                            ''')
        # Team In Match Information
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS TeamMatchResults (
                                match_id INT,
                                team_label TEXT CHECK(team_label IN ('A', 'B')),
                                team_name TEXT,
                                team_abbr TEXT,
                                team_score INT,
                                attack INT,
                                block INT,
                                serve INT,
                                opponent_error INT,
                                total INT,
                                dig INT,
                                reception INT,
                                `set` INT,
                                PRIMARY KEY (match_id, team_label),
                                FOREIGN KEY (match_id) REFERENCES Match(match_id)
                                )
                            ''')
        # Team In Set Information
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS TeamSetResults (
                                match_id INT,
                                set_no INT,
                                team_label TEXT CHECK(team_label IN ('A', 'B')),
                                team_name TEXT,
                                team_abbr TEXT,
                                team_score INT,
                                PRIMARY KEY (match_id, set_no, team_label),
                                FOREIGN KEY (match_id) REFERENCES Match(match_id)
                                )
                            ''')

        # Player Statistics Information
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS PlayerStatistics (
                                player_id INT,
                                match_id INT,
                                set_no INT,
                                team_name TEXT,
                                team_label TEXT,
                                shirtnumber INT,
                                position TEXT,
                                scoring_total_abs INT,
                                scoring_attacks  INT,
                                scoring_blocks INT,
                                scoring_serves INT,
                                scoring_errors INT,
                                scoring_efficiency_percentage REAL,
                                attack_points INT,
                                attack_errors INT,
                                attack_attempts INT,
                                attack_total INT,
                                attack_efficiency_percentage REAL,
                                block_points INT,
                                block_errors INT,
                                block_touches INT,
                                block_total INT,
                                block_efficiency_percentage REAL,
                                serve_points INT,
                                serve_errors INT,
                                serve_attempts INT,
                                serve_total INT,
                                serve_efficiency_percentage REAL,
                                reception_successful INT,
                                reception_errors INT,
                                reception_attempts INT,
                                reception_total INT,
                                reception_efficiency_percentage REAL,
                                dig_digs INT,
                                dig_errors INT,
                                dig_total INT,
                                dig_efficiency_percentage REAL,
                                set_points INT,
                                set_errors INT,
                                set_attempts INT,
                                set_total INT,
                                set_efficiency_percentage REAL,
                                PRIMARY KEY (match_id, set_no, player_id),
                                FOREIGN KEY (match_id) REFERENCES Match(match_id),
                                FOREIGN KEY (match_id, team_label) REFERENCES TeamMatchResults(match_id, team_label),
                                FOREIGN KEY (match_id, set_no, team_label) REFERENCES TeamSetResults(match_id, set_no, team_label)
                                )
                            ''')
        self.conn.commit()

    def insert_match_info(self, match_info: Dict[str, Any]):
        self.cursor.execute(f'''
                          INSERT OR REPLACE INTO Match (match_id, stage, step, gender, no, country, city, date_and_time, referee_1_name, referee_1_nation, referee_2_name, referee_2_nation)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                          (
                                match_info["match_id"], 
                                match_info["stage"], 
                                match_info["step"], 
                                match_info["gender"], 
                                match_info["no"], 
                                match_info["country"], 
                                match_info["city"], 
                                match_info["date_and_time"].strftime("%Y-%m-%d %H:%M:%S") if match_info["date_and_time"] else None, 
                                match_info["referee_1_name"], 
                                match_info["referee_1_nation"], 
                                match_info["referee_2_name"], 
                                match_info["referee_2_nation"]
                          )
        )

        self.conn.commit()

    def insert_team_in_match_info(self, team_in_match_info: Dict[str, Any]):
        self.cursor.execute(f''' 
                          INSERT OR REPLACE INTO TeamMatchResults (match_id, team_label, team_name, team_abbr, team_score, 
                                                        attack, block, serve, opponent_error, total, dig, reception, `set`)
                          VALUES (?, ?, ?, ?, ?,
                                  ?, ?, ?, ?, ?, ?, ?, ?)''', 
                          (
                              team_in_match_info["match_id"], team_in_match_info["team_label"], team_in_match_info["team_name"], team_in_match_info["team_abbr"], team_in_match_info["team_score"],
                              team_in_match_info["attack"], team_in_match_info["block"], team_in_match_info["serve"], team_in_match_info["opponent_error"], team_in_match_info["total"], team_in_match_info["dig"], team_in_match_info["reception"], team_in_match_info["set"]
                          )
        )

        self.conn.commit()

    def insert_team_set_info(self, team_in_set_info: Dict[str, Any]):
        self.cursor.execute(f'''
                          INSERT OR REPLACE INTO TeamSetResults (match_id, set_no, team_label, team_name, team_abbr, team_score)
                          VALUES (?, ?, ?, ?, ?, ?)''',
                          (
                              team_in_set_info["match_id"],
                              team_in_set_info["set_no"],
                              team_in_set_info["team_label"],
                              team_in_set_info["team_name"],
                              team_in_set_info["team_abbr"],
                              team_in_set_info["team_score"]
                          )
        )

        self.conn.commit()

    def insert_player_statistics(self, player_statistics: Dict[str, Any]):
        self.cursor.execute('''
                          INSERT OR REPLACE INTO PlayerStatistics (player_id, match_id, set_no, team_name, team_label, shirtnumber, position, 
                                                        scoring_total_abs, scoring_attacks, scoring_blocks, scoring_serves, scoring_errors, scoring_efficiency_percentage, 
                                                        attack_points, attack_errors, attack_attempts, attack_total, attack_efficiency_percentage, 
                                                        block_points, block_errors, block_touches, block_total, block_efficiency_percentage, 
                                                        serve_points, serve_errors, serve_attempts, serve_total, serve_efficiency_percentage, 
                                                        reception_successful, reception_errors, reception_attempts, reception_total, reception_efficiency_percentage,
                                                        dig_digs, dig_errors, dig_total, dig_efficiency_percentage, 
                                                        set_points, set_errors, set_attempts, set_total, set_efficiency_percentage
                          )
                          VALUES (?, ?, ?, ?, ?, ?, ?,
                          ?, ?, ?, ?, ?, ?, 
                          ?, ?, ?, ?, ?, 
                          ?, ?, ?, ?, ?, 
                          ?, ?, ?, ?, ?, 
                          ?, ?, ?, ?, ?, 
                          ?, ?, ?, ?, 
                          ?, ?, ?, ?, ?
                          )''',
                          (
                              player_statistics["player_id"], player_statistics["match_id"], player_statistics["set_no"], player_statistics["team_name"] ,player_statistics["team_label"], player_statistics["shirtnumber"], player_statistics["position"],
                              player_statistics["scoring_total_abs"], player_statistics["scoring_attacks"], player_statistics["scoring_blocks"], player_statistics["scoring_serves"], player_statistics["scoring_errors"], player_statistics["scoring_efficiency_percentage"],
                              player_statistics["attack_points"], player_statistics["attack_errors"], player_statistics["attack_attempts"], player_statistics["attack_total"], player_statistics["attack_efficiency_percentage"],
                              player_statistics["block_points"], player_statistics["block_errors"], player_statistics["block_touches"], player_statistics["block_total"], player_statistics["block_efficiency_percentage"],
                              player_statistics["serve_points"], player_statistics["serve_errors"], player_statistics["serve_attempts"], player_statistics["serve_total"], player_statistics["serve_efficiency_percentage"],
                              player_statistics["reception_successful"], player_statistics["reception_errors"], player_statistics["reception_attempts"], player_statistics["reception_total"], player_statistics["reception_efficiency_percentage"],
                              player_statistics["dig_digs"], player_statistics["dig_errors"], player_statistics["dig_total"], player_statistics["dig_efficiency_percentage"],
                              player_statistics["set_points"], player_statistics["set_errors"], player_statistics["set_attempts"], player_statistics["set_total"], player_statistics["set_efficiency_percentage"]
                          )
        )
        self.conn.commit()

    def __del__(self):
        self.conn.close()
