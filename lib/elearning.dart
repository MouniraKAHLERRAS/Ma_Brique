import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';
import 'config.dart';

class ELearningPage extends StatelessWidget {
  const ELearningPage({super.key});

  // Méthode pour ouvrir l’URL
  void _openELearning() async {
    final url = getUri('/bibexplo/');
    if (await canLaunchUrl(url)) {
      await launchUrl(url, mode: LaunchMode.externalApplication);
    } else {
      // Facultatif : afficher une erreur si le lien ne peut pas s’ouvrir
      throw 'Impossible d’ouvrir le lien $url';
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('E-learning'),
        backgroundColor: Color.fromARGB(255, 24, 101, 215),
      ),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Text(
              "Si vous voulez accéder à la page E-learning, veuillez cliquer sur le bouton ci-dessous.",
              style: TextStyle(fontSize: 16, height: 1.5),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 40),
            ElevatedButton.icon(
              onPressed: _openELearning,
              icon: const Icon(Icons.open_in_new),
              label: const Text("Accéder à E-learning"),
              style: ElevatedButton.styleFrom(
                backgroundColor: Color.fromARGB(255, 24, 101, 215),
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
