import 'dart:io';

/// Détecte la plateforme et retourne la bonne URL vers le serveur Flask.
Uri getUri(String path) {
  const String pcIp =
      '192.168.197.44'; // ← Mets ici l’IP de ton PC sur le réseau

  // Cas 1 : émulateur Android
  if (Platform.isAndroid && _isEmulator()) {
    return Uri.parse('http://10.0.2.2:5000$path');
  }

  // Cas 2 : téléphone Android réel, iOS, Web, Windows
  return Uri.parse('http://$pcIp:5000$path');
}

/// Vérifie si on est sur un émulateur Android (physique = false)
bool _isEmulator() {
  const env = String.fromEnvironment('FLUTTER_TEST');
  return Platform.environment.containsKey('ANDROID_EMULATOR_AVD') ||
      env == 'true';
}
