from nextpy.backend.vars import Var
from nextpy.frontend.components.component import Component
from nextpy.frontend.style import Style


class LeafletLib(Component):
    library = "react-leaflet"
    def _get_imports(self):
        return {}

    @classmethod
    def create(cls, *children, **props):
        custom_style = props.pop("style", {})

        # Transfer style props to the custom style prop.
        for key, value in props.items():
            if key not in cls.get_fields():
                custom_style[key] = value

        # Create the component.
        return super().create(
            *children,
            **props,
            custom_style=Style(custom_style),
        )

    def _add_style(self, style):
        self.custom_style = self.custom_style or {}
        self.custom_style.update(style)  # type: ignore

    def _render(self):
        out = super()._render()
        return out.add_props(style=self.custom_style).remove_props("custom_style")


class MapContainer(LeafletLib):
    
    tag = "MapContainer"

    center: Var[list[float]]
    zoom: Var[int]
    scroll_wheel_zoom: Var[bool]

    def _get_custom_code(self) -> str:
        return """import "leaflet/dist/leaflet.css";
import dynamic from 'next/dynamic'
const MapContainer = dynamic(() => import('react-leaflet').then((mod) => mod.MapContainer), { ssr: false });
"""


class TileLayer(LeafletLib):
    
    tag = "TileLayer"

    def _get_custom_code(self) -> str:
        return """const TileLayer = dynamic(() => import('react-leaflet').then((mod) => mod.TileLayer), { ssr: false });"""

    attribution: Var[str]
    url: Var[str]


class UseMap(LeafletLib):
    
    tag = "useMap"


class Marker(LeafletLib):
    
    tag = "Marker"

    def _get_custom_code(self) -> str:
        return """const Marker = dynamic(() => import('react-leaflet').then((mod) => mod.Marker), { ssr: false });"""

    position: Var[list[float]]
    icon: Var[dict]


class Popup(LeafletLib):
    
    tag = "Popup"

    def _get_custom_code(self) -> str:
        return """const Popup = dynamic(() => import('react-leaflet').then((mod) => mod.Popup), { ssr: false });"""
