-- This is where new changes go while in development

ALTER TABLE `event`
ADD COLUMN `requiresAllVolunteerTraining` tinyint(1) NOT NULL DEFAULT 0;

ALTER TABLE `event`
ADD COLUMN `requiresProgramTraining` tinyint(1) NOT NULL DEFAULT 0;