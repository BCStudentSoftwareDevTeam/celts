DELIMITER //

create procedure populateRequirementMatch()
    begin
        declare event_id int;
        declare event_name varchar(20);

        -- bonner variables 
        declare bonner_orient, all_bonner, service_trip, soph_exchange, junior_recommitment int;
        declare legacy_training, learning_pres, bonner_congress, leadership_institute int;

        declare event_info cursor for select event.id, LOWER(event.name) from celts.event where program_id=10;
        open event_info;
        set new_req_id += 1;
        declare continue handler for not found set done = TRUE;

        events_loop: LOOP
            fetch event_info into event_id, event_name;
            if done then leave events_loop
            if event_name = "%orientatio%" then
                insert into celts.requirementmatch (requirement_id, event_id) values (1, event_id);
            elseif event_name = '%ll bonner meet%' then 
                insert into celts.requirementmatch (requirement_id, event_id) values (2, event_id);
            elseif event_name = '%service trip%' then 
                insert into celts.requirementmatch (requirement_id, event_id) values (3, event_id);
            elseif event_name = '%xchange%' then 
                insert into celts.requirementmatch (requirement_id, event_id) values (4, event_id);
            elseif event_name = '%recommitment%' then 
                insert into celts.requirementmatch (requirement_id, event_id) values (5, event_id);
            elseif event_name = '%legacy%' then 
                insert into celts.requirementmatch (requirement_id, event_id) values (6, event_id);
            elseif event_name = '%presentation%' then 
                insert into celts.requirementmatch (requirement_id, event_id) values (7, event_id);
            elseif event_name = '%congress%' then 
                insert into celts.requirementmatch (requirement_id, event_id) values (8, event_id);
            elseif event_name = '%institute%' then 
                insert into celts.requirementmatch (requirement_id, event_id) values (9, event_id);
            else select event_id;
            /* selecting it so we can see the failing event on the console */
        end loop end_loop;
        close event_info;
    end //
DELIIMITER ;

call populateRequirementMatch()