import 'package:flutter/material.dart';

class SantePage extends StatelessWidget {
  const SantePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Santé'),
        backgroundColor: Color.fromARGB(255, 24, 101, 215),
      ),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: const SingleChildScrollView(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                'Votre Santé au travail :',
                style: TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                  color: Colors.teal,
                ),
              ),
              SizedBox(height: 20),
              Text(
                'Dans cette section, vous pouvez :\n\n'
                '- Accéder à vos examens médicaux annuels.\n'
                '- Consulter vos bilans de santé.\n'
                '- Suivre vos arrêts maladie et déclarations médicales.\n\n'
                'Toutes les informations sont traitées par le service médical SONATRACH.',
                style: TextStyle(fontSize: 16, height: 1.5),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
