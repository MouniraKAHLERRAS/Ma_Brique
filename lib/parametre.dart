import 'package:flutter/material.dart';
import 'modifier_mot_de_passe.dart';

class ParametrePage extends StatelessWidget {
  final int idEmploye;
  const ParametrePage({super.key, required this.idEmploye});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Paramètre'),
        backgroundColor: Color.fromARGB(255, 24, 101, 215),
      ),
      body: ListView(
        padding: const EdgeInsets.all(20),
        children: [
          Card(
            elevation: 2,
            margin: const EdgeInsets.symmetric(vertical: 10),
            child: ListTile(
              leading: const Icon(Icons.lock, color: Colors.blue),
              title: const Text('Modifier le mot de passe'),
              onTap: () {
                // Par exemple dans ParametrePage
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder:
                        (context) =>
                            ModifierMotDePassePage(idEmploye: idEmploye),
                  ),
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}
