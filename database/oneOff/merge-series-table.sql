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

    INSERT INTO event (contactEmail, contactName, deletedBy, 
    deletionDate, description, endDate, 
    id, isAllVolunteerTraining, isCanceled, 
    isFoodProvided, isRsvpRequired, isService, isTraining, 
    location, multipleOfferingId, name, program_id, rsvpLimit, startDate, term_id, timeEnd, 
    timeStart) 
    VALUES 
    ('contact@example.com', 'James', '5', 
    '2024-10-29', 'New script test.', '2024-10-29', 989, FALSE, FALSE, TRUE, TRUE, FALSE, TRUE, '123 Event Location', 3, 
    'Test Event', 1, 100, '2024-10-22', 19, '18:00:00', '10:00:00'), 
    ('contact@example.com', 'James', '5', 
    '2024-10-29', 'New script test.', '2024-10-29', 67676, FALSE, FALSE, TRUE, TRUE, FALSE, TRUE, '123 Event Location', 3, 
    'Test Event', 1, 100, '2024-10-22', 19, '18:00:00', '10:00:00'), 
    ('contact@example.com', 'Anna', '5', 
    '2024-10-29', 'New script test.', '2024-10-29', 45454545, FALSE, FALSE, TRUE, TRUE, FALSE, TRUE, '123 Event Location', 4, 
    'Test Event', 1, 100, '2024-10-22', 19, '18:00:00', '10:00:00'), 
    ('contact@example.com', 'Anna', '5', 
    '2024-10-29', 'New script test.', '2024-10-29', 846756, FALSE, FALSE, TRUE, TRUE, FALSE, TRUE, '123 Event Location', 4, 
    'Test Event', 1, 100, '2024-10-22', 19, '18:00:00', '10:00:00'),
    ('contact@example.com', 'Brian', '5', 
    '2024-10-29', 'New script test.', '2024-10-29', 9090909, FALSE, FALSE, TRUE, TRUE, FALSE, TRUE, '123 Event Location', 5, 
    'Test Event', 1, 100, '2024-10-22', 19, '18:00:00', '10:00:00');


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