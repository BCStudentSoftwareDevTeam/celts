DELIMITER //

create procedure handleSeries()
begin
    declare mofferingid int default 0;
    declare seriesIdvalue int default 0;
    declare done int default 0;
    declare cur1 cursor for select distinct multipleOfferingId from event where multipleOfferingId is not null;
    declare continue handler for sqlstate '02000' set done = 1;
    update event set seriesId=recurringId where recurringId is not null;
    set seriesIdvalue = coalesce((select max(seriesId) from event), 0) + 1;

    update event set seriesId=recurringId, isRepeating=1 where recurringId is not null;
    open cur1;

    fetch cur1 into mofferingid;
    while done = 0 DO
        
        select mofferingid;
        update event set seriesId = seriesIdvalue where multipleOfferingId = mofferingid;
        set seriesIdvalue = seriesIdvalue + 1;
        fetch cur1 into mofferingid;

    end while;
    close cur1;

END //

DELIMITER ;

call handleSeries()