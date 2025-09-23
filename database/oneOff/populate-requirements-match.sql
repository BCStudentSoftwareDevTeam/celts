DROP PROCEDURE IF EXISTS populateRequirementMatch;
DELIMITER //

create procedure populateRequirementMatch()
    begin
        declare event_id int;
        declare event_name varchar(100);
        declare done boolean default false;

        -- bonner variables 
        declare bonner_orient, all_bonner, service_trip, soph_exchange, junior_recommitment int;
        declare legacy_training, learning_pres, bonner_congress, leadership_institute int;

        declare event_info cursor for select event.id, LOWER(event.name) from celts.event join celts.program on event.program_id=program.id where program.isBonnerScholars = 1;
        declare continue handler for not found set done = TRUE;

        open event_info;

        events_loop: LOOP
            fetch event_info into event_id, event_name;
            if done then leave events_loop; 
            end if;
            if event_name like "%orientatio%" then
                insert into celts.requirementmatch (requirement_id, event_id) values (1, event_id);
            elseif event_name like '%ll bonner meet%' then 
                insert into celts.requirementmatch (requirement_id, event_id) values (2, event_id);
            elseif event_name like '%service trip%' then 
                insert into celts.requirementmatch (requirement_id, event_id) values (3, event_id);
            elseif event_name like '%xchange%' then 
                insert into celts.requirementmatch (requirement_id, event_id) values (4, event_id);
            elseif event_name like '%recommitment%' then 
                insert into celts.requirementmatch (requirement_id, event_id) values (5, event_id);
            elseif event_name like '%legacy%' then 
                insert into celts.requirementmatch (requirement_id, event_id) values (6, event_id);
            elseif event_name like '%presentation%' then 
                insert into celts.requirementmatch (requirement_id, event_id) values (7, event_id);
            elseif event_name like '%congress%' then 
                insert into celts.requirementmatch (requirement_id, event_id) values (8, event_id);
            elseif event_name like '%institute%' then 
                insert into celts.requirementmatch (requirement_id, event_id) values (9, event_id);
            else select event_id, event_name;
            end if;
            /* selecting it so we can see the failing event on the console */
        end loop;
        close event_info;
    end //

DELIMITER ;

call populateRequirementMatch()