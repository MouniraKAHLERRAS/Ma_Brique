import 'package:flutter/material.dart';

class PaiePage extends StatelessWidget {
  const PaiePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Paie'),
        backgroundColor: Color.fromARGB(255, 24, 101, 215),
      ),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: const SingleChildScrollView(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                'Informations sur votre Paie :',
                style: TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                  color: Colors.teal,
                ),
              ),
              SizedBox(height: 20),
              Text(
                'Dans cette section, vous pouvez :\n\n'
                '- Visualiser vos bulletins de paie.\n'
                '- Consulter vos primes, retenues et avantages.\n'
                '- Télécharger vos fiches de paie mensuelles.\n\n'
                'Toutes les données sont sécurisées et strictement confidentielles.',
                style: TextStyle(fontSize: 16, height: 1.5),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
