"""Google Calendar toolkit."""

# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from openams.tools.toolkits.base import BaseToolkit
from openams.tools.basetool import BaseTool
from openams.tools.toolkits.google_calendar_toolkit.google_calendar.base import LoadData, CreateEvent, GetDate
from typing import List

SCOPES = ["https://www.googleapis.com/auth/calendar"]


class GoogleCalendarToolkit(BaseToolkit):
    """Google Calendar toolkit.

    Currently a simple wrapper around the data loader.
    TODO: add more methods to the Google Calendar toolkit.

    """

    def get_tools(self) -> List[BaseTool]:
        """Get the tools in the toolkit."""
        return [
            LoadData(),
            CreateEvent(),
            GetDate(),   
        ]

    