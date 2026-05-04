document.addEventListener("DOMContentLoaded", () => {
  const MAP_ELEMENTS = document.querySelectorAll(".osm-map")
  if (MAP_ELEMENTS.length < 1) return

  const LANG = document.documentElement.lang.slice(0, 2)
  const languages = Array.from(
    new Set([LANG, ...navigator.languages.map((l) => l.slice(0, 2))]),
  )

  function coalesce() {
    return ["coalesce", ...Array.from(arguments).map((arg) => ["get", arg])]
  }
  const name = coalesce(...languages.map((code) => `name:${code}`), "name")
  const name_latin = coalesce(...languages.map((code) => `name:${code}`), "name:latin")
  const formatted_name = [
    "case",
    ["has", "name:nonlatin"],
    ["concat", name_latin, " ", ["get", "name:nonlatin"]],
    name,
  ]

  // Commun layers in Positron, Bright and Liberty which have `name_en` in the `text-field` property:
  const MAP_LAYERS = [
    "airport",
    "highway-name-major",
    "highway-name-minor",
    "highway-name-path",
    "label_city",
    "label_city_capital",
    "label_country_1",
    "label_country_2",
    "label_country_3",
    "label_other",
    "label_state",
    "label_town",
    "label_village",
    "poi_r1",
    "poi_r20",
    "poi_r7",
    "poi_transit",
    "water_name_line_label",
    "water_name_point_label",
    "waterway_line_label",
  ]

  function initOSM(el) {
    const options = JSON.parse(document.getElementById(el.dataset.json).textContent)
    const map = new maplibregl.Map({
      container: el,
      style: `https://tiles.openfreemap.org/styles/${options.style}`,
      center: [options.lng, options.lat],
      zoom: options.zoom,
    })

    map.addControl(new maplibregl.NavigationControl({ showCompass: false }))

    if (options.marker) {
      new maplibregl.Marker({ color: `var(${options.color})` })
        .setLngLat([options.lng, options.lat])
        .addTo(map)
    }

    // Translate the layers
    if (LANG && LANG !== "en") {
      map.on("load", async () => {
        MAP_LAYERS.filter((id) => map.getLayer(id)).forEach((id) => {
          map.setLayoutProperty(id, "text-field", formatted_name)
        })
      })
    }

  }

  Array.from(MAP_ELEMENTS).map(initOSM)
})
