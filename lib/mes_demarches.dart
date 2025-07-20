import 'package:flutter/material.dart';

class MesDemarchesTab extends StatelessWidget {
  const MesDemarchesTab({super.key});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(20),
      child: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              "Pour mon dossier de retraite j'anticipe mon départ",
              style: TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
                color: Colors.teal,
              ),
            ),
            const SizedBox(height: 24),
            Center(
              child: Image.asset(
                "assets/c7.png",
                width: 320, // Ajuste la largeur si besoin
                fit: BoxFit.contain,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
