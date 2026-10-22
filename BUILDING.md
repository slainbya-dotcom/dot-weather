# Building Dot Weather

The `.msi` has to be built on Windows and the `.dmg` on macOS. The steps are the same as for Dot Clock.

## build locally

### Windows (makes the .msi)

1. Install the tools once, from Terminal. Skip this if you've already built one of the other apps on this PC:

   ```powershell
   winget install OpenJS.NodeJS.LTS
   winget install Rustlang.Rustup
   winget install Microsoft.VisualStudio.2022.BuildTools --override "--wait --passive --add Microsoft.VisualStudio.Workload.VCTools --includeRecommended"
   ```

2. Open a terminal in this folder. In File Explorer, type `powershell` in the address bar of the folder that contains `package.json`.
3. Run:

   ```powershell
   npm install
   npm run build:win
   ```

4. The installer is written to `src-tauri\target\release\bundle\msi\Dot Weather_1.0.0_x64_en-US.msi`.

### macOS (makes a universal .dmg)

```bash
rustup target add aarch64-apple-darwin x86_64-apple-darwin
npm install
npm run build:mac
```

The `.dmg` is written to `src-tauri/target/universal-apple-darwin/release/bundle/dmg/`.

For development, `npm run dev` runs the app with live reload. `npm test` runs the logic tests in Node, which cover weather codes, reading Open-Meteo's reply, old forecasts moving on with the clock, every style's size, the place reminder, 1–4 days, °F and 12-hour, animation, margins and settings repair.

## Project layout

```
src/                 UI (no build step)
  index.html         the widget window
  settings.html      the settings window
  js/weather.js      weather codes, reading the forecast, animated icons, the five styles
  js/forecast.js     fetches from Open-Meteo and keeps the last forecast for offline
  js/data.js, geo.js city list and search (shared with Dot Clock)
  js/dotmatrix.js    5×7 font, Dot Clock's layout, the row + loading bar
  js/worldtime.js    reads Dot Clock's settings and measures its widget
  js/time.js         time-zone helpers (needed to measure Dot Clock's rows)
  js/store.js        settings model + bridge to the native shell
src-tauri/           native shell (Rust), config, icons, capabilities
tools/               icon generator, preview builder
tests/               Node tests
```

## Things to know

- **The link to Dot Clock is by identifier.** "Match Dot Clock" finds Dot Clock's settings using its app identifier, `app.worldtime.dotmatrix`. If you change that identifier in Dot Clock's `tauri.conf.json`, also change `WORLD_TIME_ID` at the top of `src-tauri/src/lib.rs` here.
- **This is the only widget in the family that uses the internet.** It talks to one address, `api.open-meteo.com`, which is the only one allowed by the security policy (`csp` in `tauri.conf.json`). Nothing about you is sent except the place's latitude and longitude.
- **Open-Meteo's free service is for non-commercial use** (fewer than 10,000 requests a day; each widget makes about 2 an hour). If you ever sell Dot Weather, you'd need their paid plan. Their data is CC BY 4.0, so keep the "Weather data by Open-Meteo.com" credit in settings.
- **"Use my location"** asks Windows or macOS for the computer's location once. On a Mac the wording of that prompt is in `src-tauri/Info.plist`.
- **The installers aren't code-signed.** As with Dot Clock, Windows will show a SmartScreen warning and macOS needs **Privacy & Security › Open Anyway**.
- **Replace the placeholder identifier** `app.worldtime.dotweather` in `src-tauri/tauri.conf.json` if you like.
