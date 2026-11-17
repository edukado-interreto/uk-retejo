# uk-aligxilo

## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run dev
```

### Compiles and minifies for production
```
npm run build
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).

## Tests

```
npm test              # run once (CI)
npm run test:watch    # rerun on file changes
npm run coverage      # with coverage, HTML report in coverage/index.html
```

The tests use [Vitest](https://vitest.dev/) with [Vue Test Utils](https://test-utils.vuejs.org/) and
[happy-dom](https://github.com/capricorn86/happy-dom). They do not check texts, labels or prices, but that:

- every embedded app (`src/embedded/*.vue`), page and form part renders with the real Vuex store and naive-ui,
  without any Vue or naive-ui warning: **any `console.warn` or `console.error` fails the test**;
- the behaviour works: fee types, payment methods, UEA code, validation, edit mode, hotels/trips/rooms, and so on;
- the pure helpers (`src/helpers/`) compute the right values.

```
tests/
  setup.js          global setup: plugins, fixed date, fake API, console checks
  support/api.js    fake backend for axios, serving ../backend/apps/devel/data/*.json
  support/mount.js  mountApp(), mountComponent()
  support/known-bugs.js, support/console.js
  helpers/          unit tests of src/helpers
  embedded/         the four embedded apps
  components/       registration form, edit form, booking, form fields
  pages/            price page, participants, pages no entrypoint uses (yet)
```

### API calls

No test reaches the network. `tests/support/api.js` answers the axios calls with the fixtures of the Django
`devel` app (`../backend/apps/devel/data/`). A request without a mock fails the test; add a route with
`mockApi("POST", "/url", response)` in the test itself.

### Known bugs

Some tests document known bugs with `it.fails` or `expectConsole()` (see `tests/support/known-bugs.js`). They fail
as soon as the bug is fixed: then replace `it.fails` with `it` or remove the `expectConsole()` line.

## CI

```
npm ci
npm test
```
