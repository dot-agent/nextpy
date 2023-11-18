from openams.tools.basetool import BaseTool
from openams.schema import Document
from pydantic import BaseModel, Field
import datetime
import os
from typing import Any, List, Optional, Union, Type


SCOPES = ["https://www.googleapis.com/auth/calendar"]


class GoogleCalendar(BaseTool):
    """Google Calendar tool spec.

    Currently a simple wrapper around the data loader.
    TODO: add more methods to the Google Calendar tool.

    """
def _get_credentials(self) -> Any:
    """Get valid user credentials from storage.

    The file token.json stores the user's access and refresh tokens, and is
    created automatically when the authorization flow completes for the first
    time.

    Returns:
        Credentials, the obtained credential.
    """
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow

    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=8080)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return creds

class LoadDataArgsSchema(BaseModel):
    number_of_results: Optional[int] = Field(
        ...,
        description=" Information about the parameter. ",
    )
    start_date: Optional[Union[str, datetime.date]] = Field(
        ...,
        description=" Information about the parameter. ",
    )

class LoadData(GoogleCalendar):
    name : str = "Load Data"
    description : str = "Load data from user's calendar."
    args_schema : Type[LoadDataArgsSchema] = LoadDataArgsSchema
     
    def load_data(
            self,
            number_of_results: Optional[int] = 100,
            start_date: Optional[Union[str, datetime.date]] = None,
        ) -> List[Document]:

            """Load data from user's calendar.

            Args:
                number_of_results (Optional[int]): the number of events to return. Defaults to 100.
                start_date (Optional[Union[str, datetime.date]]): the start date to return events from in date isoformat. Defaults to today.
            """

            from googleapiclient.discovery import build

            credentials = _get_credentials()
            service = build("calendar", "v3", credentials=credentials)

            if start_date is None:
                start_date = datetime.date.today()
            elif isinstance(start_date, str):
                start_date = datetime.date.fromisoformat(start_date)

            start_datetime = datetime.datetime.combine(start_date, datetime.time.min)
            start_datetime_utc = start_datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

            events_result = (
                service.events()
                .list(
                    calendarId="primary",
                    timeMin=start_datetime_utc,
                    maxResults=number_of_results,
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )

            events = events_result.get("items", [])

            if not events:
                return []

            results = []
            for event in events:
                if "dateTime" in event["start"]:
                    start_time = event["start"]["dateTime"]
                else:
                    start_time = event["start"]["date"]

                if "dateTime" in event["end"]:
                    end_time = event["end"]["dateTime"]
                else:
                    end_time = event["end"]["date"]

                event_string = f"Status: {event['status']}, "
                event_string += f"Summary: {event['summary']}, "
                event_string += f"Start time: {start_time}, "
                event_string += f"End time: {end_time}, "

                organizer = event.get("organizer", {})
                display_name = organizer.get("displayName", "N/A")
                email = organizer.get("email", "N/A")
                if display_name != "N/A":
                    event_string += f"Organizer: {display_name} ({email})"
                else:
                    event_string += f"Organizer: {email}"

                results.append(Document(text=event_string))

            return results
    def run(
         self,
            number_of_results: Optional[int] = 100,
            start_date: Optional[Union[str, datetime.date]] = None,
    )->str:
        try:
            return self.load_data(self, number_of_results=number_of_results, start_date=start_date)
        except Exception as e:
            raise Exception(f"An error occurred: {e}")

class CreateEventArgsSchema(BaseModel):
    title: Optional[str] = Field(
        ...,
        description=" Information about the parameter. ",
    )
    description: Optional[str] = Field(
        ...,
        description=" Information about the parameter. ",
    )
    location: Optional[str] = Field(
        ...,
        description=" Information about the parameter. ",
    )
    start_datetime: Optional[Union[str, datetime.datetime]] = Field(
        ...,
        description=" Information about the parameter. ",
    )
    end_datetime: Optional[Union[str, datetime.datetime]] = Field(
        ...,
        description=" Information about the parameter. ",
    )
    attendees: Optional[List[str]] = Field(
        ...,
        description=" Information about the parameter. ",
    )

class CreateEvent(GoogleCalendar):
    name : str = "Create Event"
    description : str = "Create an event on the users calendar."
    args_schema : Type[CreateEventArgsSchema] = CreateEventArgsSchema

    def create_event(
        self,
        title: Optional[str] = None,
        description: Optional[str] = None,
        location: Optional[str] = None,
        start_datetime: Optional[Union[str, datetime.datetime]] = None,
        end_datetime: Optional[Union[str, datetime.datetime]] = None,
        attendees: Optional[List[str]] = None,
    ) -> str:
        """
            Create an event on the users calendar

        Args:
            title (Optional[str]): The title for the event
            description (Optional[str]): The description for the event
            location (Optional[str]): The location for the event
            start_datetime Optional[Union[str, datetime.datetime]]: The start datetime for the event
            end_datetime Optional[Union[str, datetime.datetime]]: The end datetime for the event
            attendees Optional[List[str]]: A list of email address to invite to the event
        """

        from googleapiclient.discovery import build

        credentials = _get_credentials()
        service = build("calendar", "v3", credentials=credentials)

        attendees_list = []
        for attendee in attendees:
            attendees_list.append({"email": attendee})
        start_time = (
            datetime.datetime.strptime(start_datetime, "%Y-%m-%dT%H:%M:%S")
            .astimezone()
            .strftime("%Y-%m-%dT%H:%M:%S.%f%z")
        )
        end_time = (
            datetime.datetime.strptime(end_datetime, "%Y-%m-%dT%H:%M:%S")
            .astimezone()
            .strftime("%Y-%m-%dT%H:%M:%S.%f%z")
        )

        event = {
            "summary": title,
            "location": location,
            "description": description,
            "start": {
                "dateTime": start_time,
            },
            "end": {
                "dateTime": end_time,
            },
            "attendees": attendees_list,
        }
        event = service.events().insert(calendarId="primary", body=event).execute()
        return "Your calendar event has been created successfully! You can move on to the next step."

    def run(
         self,
        title: Optional[str] = None,
        description: Optional[str] = None,
        location: Optional[str] = None,
        start_datetime: Optional[Union[str, datetime.datetime]] = None,
        end_datetime: Optional[Union[str, datetime.datetime]] = None,
        attendees: Optional[List[str]] = None,   
    )-> str:
        try:
            return self.create_event(self, title=title, description=description, location=location, start_datetime=start_datetime,end_datetime=end_datetime,attendees=attendees)
        except Exception as e:
              raise Exception(f"An error occurred: {e}")

class GetDate(GoogleCalendar):
    name : str = "Get date"
    description : str = "A function to return todays date. Call this before any other functions if you are unaware of the date."

    def get_date(self):
        """
        A function to return todays date. Call this before any other functions if you are unaware of the date
        """
        return datetime.date.today()
    
    def run(self):
        return(self.get_date())