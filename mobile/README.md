# KodKids Mobile App

Aplikacja mobilna platformy KodKids zbudowana z React Native i Expo.

## Instalacja

1. Zainstaluj Expo CLI:
```bash
npm install -g expo-cli
```

2. Zainstaluj zależności:
```bash
cd mobile
npm install
```

3. Skonfiguruj API URL w `services/api.js`

4. Uruchom aplikację:
```bash
# iOS Simulator
npm run ios

# Android Emulator
npm run android

# Expo Go (telefon)
npm start
```

## Funkcje

- Logowanie i rejestracja
- Dashboard z statystykami
- Przeglądanie kursów
- Rozwiązywanie lekcji
- Profil użytkownika
- Śledzenie postępów

## Struktura

```
mobile/
├── screens/          # Ekrany aplikacji
├── services/         # API i usługi
├── components/       # Komponenty wielokrotnego użytku
├── navigation/       # Konfiguracja nawigacji
└── assets/          # Obrazy, czcionki, itp.
```