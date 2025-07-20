import 'package:flutter/material.dart';
import 'package:try_1/achat_vehicule.dart';
import 'package:try_1/social_pret.dart';
import 'package:try_1/achat_logement_cal.dart';

class MesRemboursementsPage extends StatelessWidget {
  final int idEmploye;
  const MesRemboursementsPage({super.key, required this.idEmploye});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Mes Remboursements de Prêts'),
        backgroundColor: const Color.fromARGB(255, 24, 101, 215),
      ),
      body: ListView(
        padding: const EdgeInsets.all(20),
        children: [
          _buildListItem(
            context,
            Icons.directions_car,
            'Achat véhicule',
            Colors.blue,
          ),
          _buildListItem(context, Icons.favorite, 'Social', Colors.red),
          _buildListItem(
            context,
            Icons.house,
            'Achat Logement (CAL)',
            Colors.orange,
          ),
        ],
      ),
    );
  }

  Widget _buildListItem(
    BuildContext context,
    IconData icon,
    String title,
    Color iconColor,
  ) {
    return Card(
      elevation: 2,
      margin: const EdgeInsets.symmetric(vertical: 10),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
      child: ListTile(
        leading: Icon(icon, color: iconColor),
        title: Text(title, style: const TextStyle(fontSize: 16)),
        onTap: () {
          if (title == 'Achat véhicule') {
            Navigator.push(
              context,
              MaterialPageRoute(
                builder: (context) => AchatVehiculePage(idEmploye: idEmploye),
              ),
            );
          } else if (title == 'Social') {
            Navigator.push(
              context,
              MaterialPageRoute(
                builder: (context) => SocialPretPage(idEmploye: idEmploye),
              ),
            );
          } else if (title == 'Achat Logement (CAL)') {
            Navigator.push(
              context,
              MaterialPageRoute(
                builder:
                    (context) => AchatLogementCalPage(idEmploye: idEmploye),
              ),
            );
          }
        },
      ),
    );
  }
}
