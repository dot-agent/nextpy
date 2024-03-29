# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

"""Alert components."""

from nextpy.backend.vars import Var
from nextpy.interfaces.web.components.chakra import (
    ChakraComponent,
    LiteralAlertVariant,
    LiteralStatus,
)
from nextpy.interfaces.web.components.component import Component


class Alert(ChakraComponent):
    """An alert feedback box."""

    tag = "Alert"

    # The status of the alert ("success" | "info" | "warning" | "error")
    status: Var[LiteralStatus]

    # "subtle" | "left-accent" | "top-accent" | "solid"
    variant: Var[LiteralAlertVariant]

    @classmethod
    def create(
        cls, *children, icon=True, title="Alert title", desc=None, **props
    ) -> Component:
        """Create an alert component.

        Args:
            *children: The children of the component.
            icon: The icon of the alert.
            title: The title of the alert.
            desc: The description of the alert
            **props: The properties of the component.

        Returns:
            The alert component.
        """
        if len(children) == 0:
            children = []

            if icon:
                children.append(AlertIcon.create())

            children.append(AlertTitle.create(title))

            if desc:
                children.append(AlertDescription.create(desc))

        return super().create(*children, **props)


class AlertIcon(ChakraComponent):
    """An icon displayed in the alert."""

    tag = "AlertIcon"


class AlertTitle(ChakraComponent):
    """The title of the alert."""

    tag = "AlertTitle"


class AlertDescription(ChakraComponent):
    """AlertDescription composes the Box component."""

    tag = "AlertDescription"



class Success(ChakraComponent):
    """An success feedback box."""

    tag = "Alert"

    status = "success"

    # "subtle" | "left-accent" | "top-accent" | "solid"
    variant: Var[LiteralAlertVariant]

    @classmethod
    def create(
        cls, *children, icon=True, title="Success title", desc=None, **props
    ) -> Component:
        if len(children) == 0:
            children = []

            if icon:
                children.append(AlertIcon.create())

            children.append(AlertTitle.create(title))

            if desc:
                children.append(AlertDescription.create(desc))

        return super().create(*children, **props)




class Info(ChakraComponent):
    """An success feedback box."""

    tag = "Alert"

    status = "info"

    # "subtle" | "left-accent" | "top-accent" | "solid"
    variant: Var[LiteralAlertVariant]

    @classmethod
    def create(
        cls, *children, icon=True, title="Info title", desc=None, **props
    ) -> Component:
        if len(children) == 0:
            children = []

            if icon:
                children.append(AlertIcon.create())

            children.append(AlertTitle.create(title))

            if desc:
                children.append(AlertDescription.create(desc))

        return super().create(*children, **props)


class Warning(ChakraComponent):
    """An success feedback box."""

    tag = "Alert"

    status = "warning"

    # "subtle" | "left-accent" | "top-accent" | "solid"
    variant: Var[LiteralAlertVariant]

    @classmethod
    def create(
        cls, *children, icon=True, title="Warning title", desc=None, **props
    ) -> Component:
        if len(children) == 0:
            children = []

            if icon:
                children.append(AlertIcon.create())

            children.append(AlertTitle.create(title))

            if desc:
                children.append(AlertDescription.create(desc))

        return super().create(*children, **props)


class Error(ChakraComponent):
    """An success feedback box."""

    tag = "Alert"

    status = "error"

    # "subtle" | "left-accent" | "top-accent" | "solid"
    variant: Var[LiteralAlertVariant]

    @classmethod
    def create(
        cls, *children, icon=True, title="Error title", desc=None, **props
    ) -> Component:
        if len(children) == 0:
            children = []

            if icon:
                children.append(AlertIcon.create())

            children.append(AlertTitle.create(title))

            if desc:
                children.append(AlertDescription.create(desc))

        return super().create(*children, **props)

