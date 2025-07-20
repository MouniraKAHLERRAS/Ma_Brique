import 'package:flutter/material.dart';
import 'package:try_1/sejour_asl.dart'; // Import correct
import 'package:try_1/sejour_mip.dart';

class PrestationsSocialesPage extends StatelessWidget {
  final int idEmploye; // AJOUT

  const PrestationsSocialesPage({super.key, required this.idEmploye}); // AJOUT

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Mes Inscriptions'),
        backgroundColor: const Color.fromARGB(255, 24, 101, 215),
      ),
      body: ListView(
        padding: const EdgeInsets.all(20),
        children: [
          _buildListItem(
            context,
            Icons.beach_access,
            'Séjour ASL',
            Colors.blue,
          ),
          _buildListItem(context, Icons.hotel, 'Séjour MIP', Colors.orange),
        ],
      ),
    );
  }

  // Correction ici ➔ ajouter BuildContext dans _buildListItem
  Widget _buildListItem(
    BuildContext context,
    IconData icon,
    String title,
    Color color,
  ) {
    return Card(
      elevation: 2,
      margin: const EdgeInsets.symmetric(vertical: 10),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
      child: ListTile(
        leading: Icon(icon, color: color),
        title: Text(title, style: const TextStyle(fontSize: 16)),
        onTap: () {
          if (title == 'Séjour ASL') {
            Navigator.push(
              context,
              MaterialPageRoute(
                builder: (context) => SejourAslPage(idEmploye: idEmploye),
              ),
            );
          } else if (title == 'Séjour MIP') {
            Navigator.push(
              context,
              MaterialPageRoute(
                builder: (context) => SejourMipPage(idEmploye: idEmploye),
              ),
            );
          }
        },
      ),
    );
  }
}
