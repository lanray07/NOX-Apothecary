# NOX Apothecary

Luxury ritual wellness powered by AI.

## Build

Open `NOX Apothecary.xcodeproj` in Xcode and run the `NOX Apothecary` scheme on an iOS 17+ simulator or device.

GitHub Actions is configured in `.github/workflows/ios-xcode-build.yml`.

- Pushes to `main` run an unsigned iOS Simulator build.
- Manual workflow runs can archive and upload to App Store Connect when `upload_to_app_store` is set to `true` and the required GitHub Secrets are configured.

Required GitHub Secrets for App Store upload:

- `APP_STORE_CONNECT_API_KEY_ID`
- `APP_STORE_CONNECT_ISSUER_ID`
- `APP_STORE_CONNECT_API_KEY_BASE64`
- `APPLE_TEAM_ID`

Never commit App Store Connect private keys, signing certificates, provisioning profiles, or other secrets.

The app uses:

- SwiftUI with `NavigationStack`
- MVVM-oriented view models
- SwiftData local persistence
- StoreKit 2 subscription scaffolding
- Local notifications
- Swift Charts
- Native share sheet rendering
- Multi-language app state with English, Spanish, French, German, and Portuguese
- Mock AI enabled by default
- Compile-safe WidgetKit and Apple Watch placeholders

## AI

Mock AI is injected in `NOXApothecaryApp.swift`.

Remote AI is scaffolded in `RemoteAIService.swift`:

`POST https://YOUR_BACKEND_URL.com/nox-apothecary`

Request body:

```json
{
  "module": "",
  "mood": "",
  "stressLevel": "",
  "focusLevel": "",
  "energyLevel": "",
  "sleepQuality": "",
  "ritualStyle": "",
  "weather": "",
  "availableTime": 0,
  "languageCode": "",
  "languageName": ""
}
```

Do not store API keys in the iOS app. Keep secrets on the backend.

The internal AI prompt is defined in `NoxAIPrompt.system`.

The selected app language is persisted in `UserDefaults` by `LocalizationService`, injected through the SwiftUI environment, and sent with AI requests so remote responses can match the interface language.
`RemoteAIService` also sends the selected language as the `Accept-Language` header.

## StoreKit Products

- `com.nox.apothecary.premium.monthly`
- `com.nox.apothecary.premium.yearly`
- `com.nox.apothecary.black.monthly`

Mock purchases are enabled in `SubscriptionService` for local development.

## Wellness Positioning

NOX Apothecary is a wellness and lifestyle app. It does not provide medical advice, psychological therapy, diagnosis, treatment, or guaranteed outcomes.
