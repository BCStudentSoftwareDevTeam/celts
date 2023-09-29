-- Note: Single quotes are ok, double quotes are not. Queries must be one-liners

-- Randomize background checks, 5% failed, 15% submitted, rest passing
UPDATE backgroundcheck SET backgroundCheckStatus=CASE WHEN RAND() < .05 THEN 'Failed' WHEN RAND() < .2 THEN 'Submitted' ELSE 'Passed' END

-- remove files, because we don't have the actual files stored
DELETE FROM eventfile

-- Remove comments and notes
UPDATE note set noteContent='Notes are not visible except in the production environment'

-- randomize program ban users
UPDATE programban set user_id=(SELECT username from user ORDER BY RAND() LIMIT 1)

-- reset phone numbers
UPDATE user set phoneNumber='(111)111-1111' where phoneNumber is not null

-- scrub emergency contact
UPDATE emergencycontact set name='<Redacted>', relationship='<Redacted>',homePhone=null,workPhone=null,cellPhone='1111111111', emailAddress='', homeAddress=''

-- scrub insurance info 
UPDATE insuranceinfo set insuranceType=1,policyHolderName='<Redacted>',policyHolderRelationship='<Redacted>',insuranceCompany='<Redacted>',policyNumber='<Redacted>',groupNumber='<Redacted>',healthIssues='<Redacted>'

-- scrub admin logs
UPDATE adminlog set logContent='<Redacted>' where logContent REGEXP 'Banned|Unbanned|dietary|background check'
