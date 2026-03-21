let manifest = null

async function loadManifest(staticUrl) {
  if (!manifest) {
    try {
      const response = await fetch(`${staticUrl}embedded/manifest.json`)
      manifest = await response.json()
    } catch (error) {
      console.error("Failed to load manifest.json:\n  ", error)
      return null
    }
  }
  return manifest
}

function injectCss(path) {
  const head = document.querySelector("head")
  const link = document.createElement("link")
  link.rel = "stylesheet"
  link.type = "text/css"
  link.href = path
  head.appendChild(link)
}

function isEntryPoint(key) {
  return Object.keys(manifest[key]).includes("isEntry") && manifest[key].isEntry
}

export default async function loadVue(staticUrl, filename) {
  manifest = await loadManifest(staticUrl)
  for (const key in manifest) {
    if (manifest[key].css) {
      for (const css of manifest[key].css) {
        injectCss(`/${css}`)
      }
    }
    if (isEntryPoint(key) && key.includes(filename)) {
      import(`/${manifest[key].file}`)
    }
  }
}
