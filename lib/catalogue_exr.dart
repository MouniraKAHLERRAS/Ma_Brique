import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';
import 'config.dart';

class CatalogueExrPage extends StatelessWidget {
  const CatalogueExrPage({super.key});

  // Fonction pour ouvrir l’URL du catalogue EXR
  void _openCatalogue() async {
    final url = getUri('/catalogue/');
    if (await canLaunchUrl(url)) {
      await launchUrl(url, mode: LaunchMode.externalApplication);
    } else {
      throw 'Impossible d’ouvrir le lien $url';
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Catalogue Bibliothèque EXR'),
        backgroundColor: const Color.fromARGB(255, 24, 101, 215),
      ),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Text(
              "Accédez ici au catalogue complet des formations disponibles dans la bibliothèque EXR.\n\nCliquez sur le bouton ci-dessous pour ouvrir le site.",
              style: TextStyle(fontSize: 16, height: 1.5),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 40),
            ElevatedButton.icon(
              onPressed: _openCatalogue,
              icon: const Icon(Icons.open_in_new),
              label: const Text("Accéder au catalogue EXR"),
              style: ElevatedButton.styleFrom(
                backgroundColor: const Color.fromARGB(255, 24, 101, 215),
                foregroundColor: Colors.white,
                minimumSize: const Size(double.infinity, 45),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(8),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
