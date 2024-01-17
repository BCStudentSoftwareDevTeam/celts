
alter table event add program_id integer null;

begin;

	-- ProgramEvent -> program
	UPDATE event set program_id=(SELECT pe.program_id FROM programevent pe where pe.event_id = event.id and pe.program_id IS NOT NULL);

	INSERT INTO program VALUES(9, 'CELTS-Sponsored Event', null, 0,0,'','','CELTS hosts many events that are not under the umbrella of one of our existing programs','','https://www.berea.edu/centers/center-for-excellence-in-learning-through-service');

	update event set program_id=9 where program_id is null;

commit;

alter table event modify column program_id int not null;
alter table event add foreign key(program_id) references program(id);

-- Term Order

alter table term add termOrder varchar(255);
UPDATE term set termOrder = CONCAT(year,CASE WHEN description like 'Spring%' THEN '-1' WHEN description like 'Summer%' THEN '-2' ELSE '-3' END);
alter table term modify column termOrder varchar(255) not null;

-- Email Log sender change (bug in peewee-migrations?)
alter table emaillog add sender varchar(255) not null;
alter table emaillog drop constraint emaillog_ibfk_3;
alter table emaillog drop column sender_id;
