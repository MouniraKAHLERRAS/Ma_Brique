import 'package:flutter/material.dart';

class MaPositionPage extends StatelessWidget {
  const MaPositionPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Ma Position'),
        backgroundColor: const Color.fromARGB(255, 24, 101, 215),
      ),
      body: ListView(
        padding: const EdgeInsets.all(20),
        children: [
          _buildListItem(Icons.beach_access, 'Mes droits à congé', Colors.blue),
          _buildListItem(
            Icons.calendar_today,
            'Mes plannings de congé',
            Colors.orange,
          ),
          _buildListItem(Icons.access_time, 'Mon pointage', Colors.green),
          _buildListItem(
            Icons.holiday_village,
            'Mes weekends/jours fériés travaillés',
            Colors.purple,
          ),
          _buildListItem(
            Icons.cancel_schedule_send,
            'Mes absences avec/sans solde',
            Colors.red,
          ),
          _buildListItem(Icons.flight_takeoff, 'Mes missions', Colors.teal),
        ],
      ),
    );
  }

  Widget _buildListItem(IconData icon, String title, Color iconColor) {
    return Card(
      elevation: 2,
      margin: const EdgeInsets.symmetric(vertical: 10),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
      child: ListTile(
        leading: Icon(icon, color: iconColor),
        title: Text(title, style: const TextStyle(fontSize: 16)),
        onTap: () {
          // Ici tu peux ajouter des actions plus tard
        },
      ),
    );
  }
}
