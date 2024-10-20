CREATE PROCEDURE AddSeriesId()
BEGIN
    IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'event' AND COLUMN_NAME = 'seriesId')
    THEN
        ALTER TABLE event ADD seriesId INT NULL;
    END IF;

    SET @row_id = 0;
    set @seriesId_value = COALESCE((SELECT MAX(seriesId) FROM event), 0);
    set @seriesId_value = @seriesId_value + 1;

    DECLARE series_cursor CURSOR FOR
        SELECT id FROM event WHERE recurringId IS NOT NULL OR multipleOfferingId IS NOT NULL ORDER BY id

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET @row_id = NULL;

    OPEN series_cursor;

    FETCH series_cursor INTO @row_id;

    WHILE @row_id IS NOT NULL DO
        UPDATE event
        SET seriesId = @seriesId_value
        WHERE id = @row_id;

        set @seriesId_value = @seriesId_value + 1;
        FETCH series_cursor INTO @row_id;
    END WHILE;
    CLOSE series_cursor;
END;

CALL AddSeriesId()