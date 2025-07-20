import 'package:flutter/material.dart';

class DemandesPage extends StatelessWidget {
  const DemandesPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Demandes'),
        backgroundColor: Color.fromARGB(255, 24, 101, 215),
      ),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: const SingleChildScrollView(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                'Gestion de vos Demandes :',
                style: TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                  color: Colors.teal,
                ),
              ),
              SizedBox(height: 20),
              Text(
                'Dans cette section, vous pouvez :\n\n'
                '- Faire vos demandes d\'attestation de travail.\n'
                '- Suivre l\'état de traitement de vos demandes RH.\n'
                '- Télécharger vos documents administratifs.\n\n'
                'Toutes les demandes sont traitées par votre service RH.',
                style: TextStyle(fontSize: 16, height: 1.5),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
