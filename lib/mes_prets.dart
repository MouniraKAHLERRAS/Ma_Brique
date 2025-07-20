import 'package:flutter/material.dart';
import 'package:try_1/mes_remboursements.dart';
import 'package:try_1/mes_prets_en_cours.dart';
import 'package:try_1/mes_courants_prets.dart';

class MesPretsPage extends StatelessWidget {
  final int idEmploye;
  const MesPretsPage({super.key, required this.idEmploye});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Mes Prêts'),
        backgroundColor: const Color.fromARGB(255, 24, 101, 215),
      ),
      body: ListView(
        padding: const EdgeInsets.all(20),
        children: [
          _buildListItem(
            context,
            Icons.monetization_on,
            'Mes prêts en cours',
            Colors.blue,
          ),
          _buildListItem(
            context,
            Icons.credit_card,
            'Mes remboursements de prêts',
            Colors.green,
          ),
          _buildListItem(
            context,
            Icons.account_balance,
            'Mes courants de prêts',
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
          if (title == 'Mes remboursements de prêts') {
            Navigator.push(
              context,
              MaterialPageRoute(
                builder:
                    (context) => MesRemboursementsPage(idEmploye: idEmploye),
              ),
            );
          } else if (title == 'Mes prêts en cours') {
            Navigator.push(
              context,
              MaterialPageRoute(
                builder: (context) => MesPretsEnCoursPage(idEmploye: idEmploye),
              ),
            );
          } else if (title == 'Mes courants de prêts') {
            Navigator.push(
              context,
              MaterialPageRoute(
                builder:
                    (context) => MesCourantsPretsPage(idEmploye: idEmploye),
              ),
            );
          }
        },
      ),
    );
  }
}
