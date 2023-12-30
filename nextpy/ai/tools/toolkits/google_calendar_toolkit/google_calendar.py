# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

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

from typing import List

from nextpy.ai.tools.basetool import BaseTool
from nextpy.ai.tools.toolkits.base import BaseToolkit
from nextpy.ai.tools.toolkits.google_calendar_toolkit.google_calendar.base import (
    CreateEvent,
    GetDate,
    LoadData,
)

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
