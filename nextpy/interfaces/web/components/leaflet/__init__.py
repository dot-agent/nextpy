# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

"""Leaflet mapping components."""

from .leaflet import (
    MapContainer,
    Marker,
    Popup,
    TileLayer,
    UseMap,
)

map_container = MapContainer.create
tile_layer = TileLayer.create
use_map = UseMap.create
marker = Marker.create
popup = Popup.create
