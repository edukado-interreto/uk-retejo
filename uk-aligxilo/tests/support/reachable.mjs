// Files of src/ that the entrypoints actually use, found by following their imports.
// Used for the coverage: code that no entrypoint reaches is not a target of the tests.
import { existsSync, readFileSync, statSync } from "node:fs"
import path from "node:path"

const ROOT = path.resolve(import.meta.dirname, "../..")
const IMPORT = /(?:\bfrom\s*|\bimport\s*\(\s*|\bimport\s+)["']([^"']+)["']/g
const EXTENSIONS = ["", ".js", ".vue", ".mjs", "/index.js", "/index.vue"]

function resolveImport(specifier, importer) {
  let base
  if (specifier.startsWith("@/")) base = path.join(ROOT, "src", specifier.slice(2))
  else if (specifier.startsWith(".")) base = path.resolve(path.dirname(importer), specifier)
  else return null // package
  return EXTENSIONS.map((ext) => base + ext).find((file) => existsSync(file) && statSync(file).isFile())
}

/** Paths relative to the project root, e.g. "src/components/MainForm.vue", sorted. */
export function reachableFromEntrypoints(entrypoints) {
  const seen = new Set()
  const visit = (file) => {
    if (seen.has(file)) return
    seen.add(file)
    if (!/\.(js|vue|mjs)$/.test(file)) return
    for (const [, specifier] of readFileSync(file, "utf8").matchAll(IMPORT)) {
      const target = resolveImport(specifier, file)
      if (target) visit(target)
    }
  }
  entrypoints.forEach((entry) => visit(path.join(ROOT, entry)))
  return [...seen]
    .filter((file) => file.startsWith(path.join(ROOT, "src") + path.sep) && /\.(js|vue)$/.test(file))
    .map((file) => path.relative(ROOT, file))
    .sort()
}
