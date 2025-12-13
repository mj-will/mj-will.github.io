

# # Leaflet cluster map of talk locations
#
# (c) 2016-2017 R. Stuart Geiger, released under the MIT license
#
# Run this from the markdown_generator directory:
#   python talkmap.py ../_talks
#
# This scrapes the location YAML field from each .md file in _talks, geolocates
# with geopy/Nominatim, and writes a custom Leaflet map that can render
# different marker shapes for online vs in-person talks.
#
# Requires: PyYAML, geopy

from __future__ import annotations

import json
import sys
from pathlib import Path
import yaml
from geopy import Nominatim


def parse_front_matter(md_text: str) -> dict:
    """Return YAML front matter dict or {} if not found."""
    stripped = md_text.lstrip()
    if not stripped.startswith("---"):
        return {}
    parts = stripped.split("---", 2)
    if len(parts) < 3:
        return {}
    try:
        return yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        return {}


def mode_normalized(meta: dict) -> str:
    """Normalize mode to 'online' or 'in-person'."""
    mode = (meta.get("mode") or "").strip().lower()
    return mode if mode in {"online", "in-person"} else "in-person"


def write_data_file(points: list[dict], output_dir: Path) -> None:
    """Write talkPoints data file consumed by the map."""
    output_dir.mkdir(parents=True, exist_ok=True)
    data_path = output_dir / "talks.js"
    with open(data_path, "w", encoding="utf-8") as f:
        f.write("var talkPoints = ")
        json.dump(points, f, indent=2)
        f.write(";\n")
    print(f"Wrote {data_path}")


def write_map_html(output_dir: Path) -> None:
    """Write map.html that uses talkPoints with mode-aware markers."""
    map_path = output_dir / "map.html"
    html = """<!DOCTYPE html>
<html>
<head>
  <title>Talk map</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.css" />
  <script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.js"></script>
  <link rel="stylesheet" href="leaflet_dist/MarkerCluster.css" />
  <link rel="stylesheet" href="leaflet_dist/MarkerCluster.Default.css" />
  <script src="leaflet_dist/leaflet.markercluster-src.js"></script>
  <script src="talks.js"></script>
  <style>
    html, body { height: 100%; margin: 0; }
    #map { height: 700px; }
    .marker { width: 14px; height: 14px; border: 2px solid #fff; box-shadow: 0 0 2px rgba(0,0,0,0.4); }
    .marker-in-person { background: #1f7a8c; border-radius: 50%; }
    .marker-online { background: #c0392b; border-radius: 2px; }
  </style>
</head>
<body>
  <div id="map"></div>
  <script>
    var tiles = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 18,
      attribution: '&copy; OpenStreetMap contributors'
    });
    var map = L.map('map', {center: [20, 0], zoom: 2, layers: [tiles]});
    var markers = L.markerClusterGroup({ showCoverageOnHover: false, maxClusterRadius: 70 });

    var icons = {
      "in-person": L.divIcon({ className: 'marker marker-in-person', iconSize: [14,14], iconAnchor: [7,7] }),
      "online":    L.divIcon({ className: 'marker marker-online', iconSize: [14,14], iconAnchor: [7,7] })
    };

    talkPoints.forEach(function(pt) {
      if (pt.lat === undefined || pt.lng === undefined) return;
      var icon = icons[pt.mode] || icons["in-person"];
      var popup = '<strong>' + (pt.title || '') + '</strong><br>' + (pt.location || '');
      if (pt.permalink) {
        popup += '<br><a href=\"' + pt.permalink + '\">View talk</a>';
      }
      markers.addLayer(L.marker([pt.lat, pt.lng], { icon: icon, title: pt.title || pt.location }).bindPopup(popup));
    });

    if (markers.getLayers().length > 0) {
      map.addLayer(markers);
      map.fitBounds(markers.getBounds(), { padding: [20, 20] });
    } else {
      map.setView([20, 0], 2);
    }
  </script>
</body>
</html>
"""
    with open(map_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Wrote {map_path}")


def main(path_to_talks: str | Path) -> int:
    path_to_talks = Path(path_to_talks)
    if not path_to_talks.is_dir():
        print(f"Talk directory not found: {path_to_talks}")
        return 1

    geocoder = Nominatim(user_agent="talkmap_generator", timeout=10)
    geocode_cache: dict[str, tuple[float, float]] = {}
    points: list[dict] = []

    for file in sorted(path_to_talks.glob("*.md")):
        with open(file, "r", encoding="utf-8") as f:
            meta = parse_front_matter(f.read())

        location = meta.get("location")
        if not location:
            print(f"No location found in {file.name}, skipping...")
            continue

        if location not in geocode_cache:
            coords = geocoder.geocode(location)
            if coords is None:
                print(f"Could not geocode '{location}' in {file.name}, skipping...")
                continue
            geocode_cache[location] = (coords.latitude, coords.longitude)
            print(f"{file.name}: {location} -> {coords.latitude}, {coords.longitude}")

        lat, lng = geocode_cache[location]
        points.append(
            {
                "title": meta.get("title"),
                "location": location,
                "lat": lat,
                "lng": lng,
                "mode": mode_normalized(meta),
                "permalink": meta.get("permalink"),
            }
        )

    if not points:
        print("No geocoded locations found; map not generated.")
        return 1

    output_dir = path_to_talks.parent / "talkmap"
    write_data_file(points, output_dir)
    write_map_html(output_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "../_talks"))
