import pytest
from flask import g
from app import app
from datetime import date, datetime, timedelta
from peewee import IntegrityError, fn

from app.models.user import User
from app.models import mainDB
from app.models.bonnerCohort import BonnerCohort
from app.models.eventRsvp import EventRsvp
from app.models.eventRsvpLog import EventRsvpLog
from app.models.event import Event
from app.models.program import Program

from app.logic.bonner import getBonnerCohorts, rsvpForBonnerCohort, addBonnerCohortToRsvpLog

@pytest.mark.integration
def test_getBonnerCohorts():

    with mainDB.atomic() as transaction:
        
        # reset pre-determined bonner cohorts
        BonnerCohort.delete().execute()

        # make sure it works without specifying the current year    
        currentYear = date.today().year

        cohorts = getBonnerCohorts()
        assert len(cohorts) == 5
        assert list(cohorts.keys()) == [currentYear-4,currentYear-3,currentYear-2,currentYear-1,currentYear]

        # always have the last 5, at least
        cohorts = getBonnerCohorts()
        assert len(cohorts) == 5
        assert list(cohorts.keys()) == [currentYear-4,currentYear-3,currentYear-2,currentYear-1,currentYear]

        # try a limit greater than our size
        cohorts = getBonnerCohorts(limit=6)
        assert len(cohorts) == 5

        currentYear = 2022 # reset for testing purposes

        BonnerCohort.create(user="lamichhanes2", year=currentYear-6)
        BonnerCohort.create(user="heggens", year=currentYear)
        BonnerCohort.create(user="khatts", year=currentYear)
        cohorts = getBonnerCohorts(currentYear=currentYear)
        assert len(cohorts) == 7
        assert len(cohorts[currentYear]) == 2
        assert len(cohorts[currentYear-6]) == 1

        BonnerCohort.create(user="lamichhanes2", year=currentYear-5)
        BonnerCohort.create(user="lamichhanes2", year=currentYear-4)
        BonnerCohort.create(user="lamichhanes2", year=currentYear-2)
        BonnerCohort.create(user="lamichhanes2", year=currentYear-1)
        BonnerCohort.create(user="ayisie", year=currentYear-1)
        BonnerCohort.create(user="khatts", year=currentYear-1)
        BonnerCohort.create(user="heggens", year=currentYear-1)

        cohorts = getBonnerCohorts(currentYear=currentYear)
        assert len(cohorts) == 7
        assert len(cohorts[currentYear-3]) == 0
        assert len(cohorts[currentYear]) == 2
        assert len(cohorts[currentYear-1]) == 4

        cohorts = getBonnerCohorts(limit=5,currentYear=currentYear)
        assert len(cohorts) == 5
        assert len(cohorts[currentYear-3]) == 0
        assert len(cohorts[currentYear]) == 2
        assert len(cohorts[currentYear-1]) == 4


        transaction.rollback()

@pytest.mark.integration
def test_bonnerRsvp():
    with mainDB.atomic() as transaction:
        # reset pre-determined bonner cohorts
        BonnerCohort.delete().execute()

        BonnerCohort.create(user="lamichhanes2", year=2022)
        BonnerCohort.create(user="ramsayb2", year=2022)
        BonnerCohort.create(user="khatts", year=2020)
        BonnerCohort.create(user="neillz", year=2020)
        event_id = 13
        year1 = 2020

        rsvpForBonnerCohort(year1, event_id)
        assert EventRsvp.select().where(EventRsvp.event == event_id, EventRsvp.user == "khatts").exists()
        assert EventRsvp.select().where(EventRsvp.event == event_id, EventRsvp.user == "neillz").exists()
        assert not EventRsvp.select().where(EventRsvp.event == event_id, EventRsvp.user == "ramsayb2").exists()

        # make sure there is no error for duplicates
        BonnerCohort.create(user="ayisie", year=2020)
        rsvpForBonnerCohort(2020, event_id)
        assert EventRsvp.select().where(EventRsvp.event == event_id).count() == 3

        transaction.rollback()  
        
@pytest.mark.integration
def test_addBonnerCohortToRsvpLog():
    with mainDB.atomic() as transaction:
        with app.app_context():
            g.current_user = "heggens"
            
            # reset pre-determined bonner cohorts
            BonnerCohort.delete().execute()
            
            currentYear = 2024
            
            # create BonnerCohort entries for a set of valid users for the given year.
            BonnerCohort.create(user="ramsayb2", year=currentYear)
            BonnerCohort.create(user="qasema", year=currentYear)
            BonnerCohort.create(user="neillz", year=currentYear)
            BonnerCohort.create(user="khatts", year=currentYear)
               
            testDate = datetime.strptime("2025-01-19 05:00","%Y-%m-%d %H:%M")
            
            # Create a test event associated with a Bonner Scholars program
            programEvent = Program.create(id = 15,
                                        programName = "Bonner Scholars",
                                        isVolunteerOpportunities = False,
                                        isBonnerScholars = True,
                                        contactEmail = "test@email",
                                        contactName = "testName")
            
            event = Event.create(name = "Upcoming Bonner Scholars Event",
                                term = 4,
                                description = "Test upcoming bonner event.",
                                location = "Stephenson Building",
                                startDate = testDate,
                                endDate = testDate + timedelta(days=1),
                                program = programEvent)
            
            addBonnerCohortToRsvpLog(currentYear, event)

            users = {
                'ramsayb2' : 'Brian Ramsay', 
                'khatts' : 'Sreynit Khatt',
                'qasema' : 'Ala Qasem', 
                'neillz' : 'Zach Neill'
            }
            
            # Assert that the RSVP log contains entries for all valid users in the BonnerCohort.
            for name in users.values():
                content = f"Added {name} to RSVP list."
                assert EventRsvpLog.select().where(EventRsvpLog.event == event, EventRsvpLog.rsvpLogContent == content).exists()

            invalidUsers = {
                'michels' : 'Stevenson Michel', 
                'blesoef' : 'Finn Bledsoe',
                'makindeo' : 'Oluwagbayi Makinde', 
                'zawn' : 'Nyan Zaw'
            }
            
            # Assert that no RSVP log entries are created for invalid users.
            for name in invalidUsers.values():
                content = f"Added {name} to RSVP list."
                assert not EventRsvpLog.select().where(EventRsvpLog.event == event, EventRsvpLog.rsvpLogContent == content).exists()
                
            # Verify that the total number of RSVP log entries matches the number of valid cohort users.
            assert EventRsvpLog.select().where(EventRsvpLog.event == event).count() == 4
            assert not EventRsvpLog.select().where(EventRsvpLog.event == event).count() == 7
            
            transaction.rollback()
            
            


