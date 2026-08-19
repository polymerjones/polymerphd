# Polymer Ph.D. — iOS app

A WKWebView wrapper around `app/index.html`. The whole reference is bundled inside the app,
so it works in airplane mode with no server and no network. The only thing that leaves the
app is a YouTube timestamp link, which opens in Safari.

## Building it onto your phone

1. **Regenerate** after any change to the web app:
   ```
   python3 scripts/build_app_data.py     # rebuild app/index.html
   python3 scripts/make_xcodeproj.py     # regenerate the project, sync the bundled copy
   ```
   The second step copies `app/index.html` into `ios/PolymerPhD/Resources/`. Skipping it means
   shipping a stale corpus.

2. **Open** `ios/PolymerPhD.xcodeproj` in Xcode.

3. **Set a signing team.** Select the `PolymerPhD` target → Signing & Capabilities → Team.
   If nothing is listed, add your Apple ID under Xcode → Settings → Accounts first. A free
   Apple ID works; no paid membership is needed to run it on your own device.

4. **Plug in the iPhone**, pick it as the run destination, and press ⌘R.

5. **Trust the certificate** on the phone the first time: Settings → General → VPN & Device
   Management → tap your developer profile → Trust.

## The seven-day limit

With a free Apple ID, the provisioning profile expires after **7 days** and the app stops
launching until you rebuild from Xcode. This is Apple's rule, not a project limitation.

To avoid it, the Apple Developer Program ($99/yr) extends profiles to a year and unlocks
TestFlight. Given the app is for your own use, re-running ⌘R once a week is usually the
cheaper trade.

## Notes

- Bundle id is `com.polymerphd.reference`. Change it in `scripts/make_xcodeproj.py` if it
  collides with something else on your account.
- Deployment target is iOS 17. Both iPhone and iPad are supported.
- The app icon comes from `images/drpaul.jpg`, resized into
  `PolymerPhD/Assets.xcassets/AppIcon.appiconset/`.
- `project.pbxproj` is generated, not hand-maintained. Edit `scripts/make_xcodeproj.py`
  instead, or Xcode's changes will be overwritten on the next regeneration.
