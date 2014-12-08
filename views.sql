--
-- we add id to be Django compliant, don't care
-- about the value, must be unique
--
DROP VIEW IF EXISTS stats_view_alert_year;
DROP VIEW IF EXISTS stats_view_alert_month;
DROP VIEW IF EXISTS stats_view_users;
--
--
CREATE OR REPLACE VIEW stats_view_alert_year AS 
    SELECT alert_id, year, sum(created) created, 
    sum(modified) modified,
    sum(deleted) deleted, row_number() over() as id
    FROM stats_alertstats
    GROUP BY alert_id, "year";
--
--
CREATE OR REPLACE VIEW stats_view_alert_month AS 
    SELECT alert_id, "year", "month", sum(created) created, 
    sum(modified) modified,
    sum(deleted) deleted, row_number() over() as id
    FROM stats_alertstats
    GROUP BY alert_id, "year", "month";

--
--


CREATE OR REPLACE VIEW stats_view_users AS 
    SELECT 
    s.id , s.alert_id , s.date_stat,  s.created, s.modified, s. deleted, 
    s.userid, osmu.username, s.month, s.year,
    item.item, item.item_id
    FROM stats_alertuserstats AS s
    LEFT JOIN 
        (
        SELECT unnest(ARRAY[ 1,2,3 ]) as item_id,
               unnest(ARRAY[ 'node','way','relation' ]) as item
        ) AS item
    ON item.item_id = s.item
    LEFT JOIN stats_osmuser osmu ON osmu.osm_uid = s.userid;
