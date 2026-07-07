from datetime import datetime
from os import abort
from flask import abort, jsonify
import requests, xmltodict
import xml.etree.ElementTree as ET

from app import app
from app.models.event import Event

EVENT_FIELDS = [
    "cg_event_id",          			# Integer — 0 to create, existing id to update
    "cg_group_acronym",     			# String
    "external_event_id",    			# String[100]
    "event_coordinator",    			# String[300], email
    "event_name",           			# String
    "quick_description",    			# String[4294967295]
    "event_type",           			# String[255]
    "event_start_date",                 # String[16]
    "event_start_time",                 # String[16]
    "event_end_date",                   # String[16]
    "event_end_time",                   # String[16]
    "event_location",                   # String[255]
    "room_id",                          # Integer
    "event_display_to",                 # Integer - see docs for magic numbers
    "allow_rsvp",                       # Integer, 0 or 1
    "event_open_to",                    # Integer - see docs for magic numbers
    "delete_event",                     # Integer, 0 or 1
    "hide_from_events_slider",          # Integer, 0 or 1
    "force_display_on_rooms_schedule",  # Integer, 0 or 1
    "location_type",                    # Integer, 0/2/3
    "event_audience",                   # Integer
]
 
REQUIRED_FIELDS = [        
    "cg_group_acronym",
    "event_name",
    "event_start_date",
    "event_start_time",
    "event_end_date",
    "event_end_time"
]

# The following are also required fields, but are NOT passed into CampusGroups objects (they are retrieved from the config files):
    # "api_key",              			# String[100], Required
    # "timestamp",            			# String[20], yyyy-MM-ddTHH:mm:ssZ (UTC)
    # "school",               			# String[30]

class CampusGroups:
	def __init__(self, campusGroupsEnv = "sandbox"):
		self.url = app.config["campusgroups"][campusGroupsEnv]["url"]
		self.secret = app.config["campusgroups"][campusGroupsEnv]["secret"]
		self.key = app.config["campusgroups"][campusGroupsEnv]["key"]
		self.school = app.config["campusgroups"][campusGroupsEnv]["school"]
		self.headers = {'X-CG-API-Secret': self.secret}

	def getEvents(self):
		"""
		Retrieve events from CampusGroups using the RSS feed.
		"""
		now = datetime.now()
		ts_now = now.isoformat().replace('+00:00', 'Z')
		rss_events_url = f'{self.url}/rss_events?ts={ts_now}&preauth={self.key}'
		
		try:
			response = requests.get(rss_events_url, headers = self.headers)
			response.raise_for_status()
			data_dict = xmltodict.parse(response.text)
			response.raise_for_status()
			return jsonify(data_dict)
		except requests.exceptions.RequestException as e:
			print("Error retrieving data from campusgroups: \n", e)
			abort(500)

	def addEvent(self, eventData):
		"""
		Add or update an event in CampusGroups using the CreateUpdateEvent SOAP API.
		"""
		createUpdateEvent_url = "https://berea-sandbox.campusgroups.com/WebServices/campusgroups.asmx?op=CreateUpdateEvent"
		xmlOut = self.build_event_xml(eventData)
		
		self.headers["SOAPAction"] = "http://campusgroups.com/CreateUpdateEvent"
		self.headers["Content-Type"] = "text/xml; charset=utf-8"

		try:
			response = requests.post(createUpdateEvent_url, data=xmlOut, headers=self.headers, timeout=15)
			response.raise_for_status()
			return self.parse_event_response(response.content)

		except requests.exceptions.RequestException as e:
			print("Error retrieving data from campusgroups: \n", e)
			abort(500)
	
	def parse_event_response(self, xml_content):
		"""Pull cg_event_id / message / message_code out of the SOAP response,
		tolerating either the namespaced or bare tag form."""
		responseData = xmltodict.parse(xml_content)		
		
		def find_text(tag):
			el = responseData['soap:Envelope']['soap:Body']['CreateUpdateEventResponse']['CreateUpdateEventResult'].get(tag)
			return el if el is not None else None
	
		return {
			"cg_event_id": find_text("cg_event_id"),
			"message": find_text("message"),
			"message_code": find_text("message_code"),
		}


	def build_event_xml(self, payload):
		"""
		Build the SOAP XML body for CreateUpdateEvent from a dictionary payload.
		"""
		missing = [f for f in REQUIRED_FIELDS if not payload.get(f)]
		if missing:
			raise ValueError(f"Missing required field(s): {', '.join(missing)}")
	
		envelope = ET.Element(
			"soap12:Envelope",
			{
				"xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
				"xmlns:xsd": "http://www.w3.org/2001/XMLSchema",
				"xmlns:soap12": "http://www.w3.org/2003/05/soap-envelope",
			},
		)
		body = ET.SubElement(envelope, "soap12:Body")
		op = ET.SubElement(body, "CreateUpdateEvent", {"xmlns": "http://campusgroups.com/"})
	
		# Always-required auth/context fields
		now = datetime.now()
		ts_now = now.isoformat().replace('+00:00', 'Z')

		ET.SubElement(op, "timestamp").text = (ts_now)
		ET.SubElement(op, "school").text = self.school
		ET.SubElement(op, "api_key").text = self.key
		# Event-specific fields — only send what's provided so partial
		# updates don't clobber existing values.
		for field in EVENT_FIELDS:
			value = payload.get(field)
			if value is not None and value != "":
				ET.SubElement(op, field).text = str(value)
	
		xml_bytes = ET.tostring(envelope, encoding="utf-8")
		return b'<?xml version="1.0" encoding="utf-8"?>' + xml_bytes
	
	def parseEventData(self, eventData):
		"""
		Parse the event data from Celts-link database into a dictionary.
		"""

		# TODO handle recurring events 

		event = Event.get_by_id(eventData)
		if not event:
			abort(404, description=f"No events with ID {eventData} found.")
		data = {}
		if event.campusGroupsId is None:
			data["cg_event_id"] = 0		# create a new event
		else:
			data["cg_event_id"] = event.campusGroupsId #update an existing event
		data["cg_group_acronym"] = "Celts"		# event.program?
		data["external_event_id"] = event.id
		data["event_coordinator"] = event.contactEmail
		data["event_name"] = event.name
		data["quick_description"] = event.description
		data["event_type"] = "Academic"
		data["event_start_date"] = event.startDate.strftime("%Y-%m-%d")
		data["event_start_time"] = event.timeStart.strftime("%H:%M")
		data["event_end_date"] = event.startDate.strftime("%Y-%m-%d")
		data["event_end_time"] = event.timeEnd.strftime("%H:%M")
		data["event_location"] = event.location

		# Check CampusGroups API documentation for magic numbers:
		data["event_display_to"] = 0
		data["allow_rsvp"] = 1
		data["event_open_to"] = 1
		data["delete_event"] = 0
		data["hide_from_events_slider"] = 0
		data["force_display_on_rooms_schedule"] = 0
		data["location_type"] = 0

		return data