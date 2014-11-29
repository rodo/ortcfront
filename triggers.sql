--
--
-- Functions appelées par les triggers
--
--
--
--
CREATE OR REPLACE FUNCTION stats_alertstats_update() RETURNS TRIGGER AS $BODY$
BEGIN

IF (TG_OP = 'DELETE') THEN

UPDATE stats_alertstats SET modified = stats.modified, created = stats.created, deleted = stats.deleted
        FROM (

        SELECT COALESCE(sum(created),0) as created, 
               COALESCE(sum(modified),0) as modified, 
               COALESCE(sum(deleted),0) as deleted 
        FROM stats_alertuserstats
        WHERE alert_id = OLD.alert_id AND item=OLD.item AND userid=OLD.userid AND date_stat=OLD.date_stat)
    AS stats

    WHERE alert_id = OLD.alert_id AND item=OLD.item AND date_stat=OLD.date_stat;


ELSE


UPDATE stats_alertstats SET modified = stats.modified, created = stats.created, deleted = stats.deleted
        FROM (

        SELECT COALESCE(sum(created),0) as created, 
               COALESCE(sum(modified),0) as modified, 
               COALESCE(sum(deleted),0) as deleted 
        FROM stats_alertuserstats
        WHERE alert_id = NEW.alert_id AND item=NEW.item AND date_stat=NEW.date_stat)
    AS stats

    WHERE alert_id = NEW.alert_id AND item=NEW.item AND date_stat=NEW.date_stat;

IF (FOUND) THEN RETURN NULL; END IF ;

INSERT INTO stats_alertstats (alert_id, date_stat, item, created, modified, deleted, month, year)
   SELECT NEW.alert_id, NEW.date_stat, NEW.item,
   sum(created) as created, sum(modified) as modified, sum(deleted) as deleted,
   NEW.month, NEW.year
   FROM stats_alertuserstats
   WHERE alert_id = NEW.alert_id AND date_stat=NEW.date_stat AND item=NEW.item AND userid=NEW.userid ;

END IF;









RETURN NULL; -- result is ignored since this is an AFTER trigger
END;
$BODY$ LANGUAGE plpgsql;

DROP TRIGGER stats_alertuserstats_trigger ON stats_alertuserstats;
CREATE TRIGGER stats_alertuserstats_trigger
    AFTER INSERT OR UPDATE OR DELETE ON stats_alertuserstats
    FOR EACH ROW
    EXECUTE PROCEDURE stats_alertstats_update();
