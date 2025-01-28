DELIMITER //

create procedure populateRequirementMatch()
    begin
        declare @event_id int;
        declare @event_name varchar(20);
        declare event_info cursor for select event.id, event.name from celts.event where program_id=10;
        open event_info;
        fetch event_info into @event_id, @event_name;
        declare continue handler for not found set done = TRUE;

        while 1 > 0 DO

        end while;
        close event_info;
    end //
DELIIMITER ;

call populateRequirementMatch()