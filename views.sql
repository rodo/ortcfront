--
-- we add id to be Django compliant, don't care
-- about the value, must be unique
--
DROP VIEW IF EXISTS stats_view_alert_year;

CREATE OR REPLACE VIEW stats_view_alert_year AS 
    SELECT alert_id, year, sum(created) created, 
    sum(modified) modified,
    sum(deleted) deleted, row_number() over() as id
    FROM stats_alertstats
    GROUP BY alert_id, "year";
