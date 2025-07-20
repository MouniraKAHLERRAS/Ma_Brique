import 'package:flutter/material.dart';

class AccueilManagerPage extends StatelessWidget {
  const AccueilManagerPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Accueil Manager'),
        backgroundColor: const Color.fromARGB(255, 24, 101, 215),
      ),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: SingleChildScrollView(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: const [
              Text(
                'Bienvenue dans l\'espace Manager :',
                style: TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                  color: Colors.teal,
                ),
              ),
              SizedBox(height: 20),
              Text(
                'Cet espace vous permet de :\n\n'
                '- Consulter les informations de vos collaborateurs.\n'
                '- Gérer les congés et formations de votre équipe.\n'
                '- Suivre l\'assiduité et les performances.\n'
                '- Accéder aux historiques de suspensions et sanctions.\n\n'
                'Utilisez les options proposées pour faciliter votre gestion au quotidien.',
                style: TextStyle(fontSize: 16, height: 1.5),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
