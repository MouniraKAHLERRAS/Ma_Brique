import 'package:flutter/material.dart';

class MedaillesGratificationsPage extends StatelessWidget {
  const MedaillesGratificationsPage({super.key});

  final List<Map<String, String>> medailles = const [
    {
      "nom": "Bronze",
      "anciennete": "15 ans (180 mois)",
      "image": "assets/bronze.png",
    },
    {
      "nom": "Argent",
      "anciennete": "20 ans (240 mois)",
      "image": "assets/argent.png",
    },
    {"nom": "Or", "anciennete": "25 ans (300 mois)", "image": "assets/or.png"},
    {
      "nom": "Vermeil",
      "anciennete": "30 ans (360 mois)",
      "image": "assets/vernelle.png",
    },
    {
      "nom": "Platine",
      "anciennete": "35 ans (420 mois)",
      "image": "assets/platine.png",
    },
    {
      "nom": "Couronne",
      "anciennete": "40 ans (480 mois)",
      "image": "assets/comme.png",
    },
  ];

  final List<String> datesRemise = const [
    "📌 24 février – Anniversaire de nationalisation des hydrocarbures",
    "📌 1er mai – Fête du Travail",
    "📌 5 juillet – Fête de l’indépendance",
    "📌 1er novembre – Anniversaire de la révolution",
    "📌 31 décembre – Anniversaire de création de Sonatrach",
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Médailles / Gratifications'),
        backgroundColor: Color.fromARGB(255, 24, 101, 215),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              "Les modalités d'octroi des médailles honorifiques de travail et les gratifications correspondantes sont définies dans la circulaire suivante : N° 7.08.1 R4\n\n"
              "Il est institué au sein de la société Sonatrach six (06) types de médailles en fonction de l'ancienneté :",
              style: TextStyle(fontSize: 16, height: 1.5),
            ),
            const SizedBox(height: 20),
            ...medailles.map(
              (medaille) => Card(
                margin: const EdgeInsets.symmetric(vertical: 10),
                child: ListTile(
                  leading: Image.asset(
                    medaille['image']!,
                    width: 60,
                    height: 60,
                    fit: BoxFit.contain,
                  ),
                  title: Text(medaille['nom']!),
                  subtitle: Text("Ancienneté : ${medaille['anciennete']}"),
                ),
              ),
            ),
            const SizedBox(height: 30),
            const Text(
              "🎖 Remise des Médailles",
              style: TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
                color: Colors.teal,
              ),
            ),
            const SizedBox(height: 10),
            const Text(
              "La remise des médailles se fait à la date des événements suivants :",
              style: TextStyle(fontSize: 16),
            ),
            const SizedBox(height: 10),
            ...datesRemise.map(
              (event) => Padding(
                padding: const EdgeInsets.symmetric(vertical: 4),
                child: Text(event, style: const TextStyle(fontSize: 15)),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
