import 'package:flutter/material.dart';
import 'package:try_1/mes_droits_conge.dart';
import 'package:try_1/mes_plannings_conge.dart';
import 'package:try_1/mon_pointage.dart';
import 'package:try_1/mes_weekends_feries.dart';
import 'package:try_1/mes_absences.dart';
import 'package:try_1/mes_missions.dart';

class MaPositionPage extends StatelessWidget {
  final int idEmploye;

  const MaPositionPage({super.key, required this.idEmploye});

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
          _buildListItem(
            context,
            Icons.beach_access,
            'Mes droits à congé',
            Colors.blue,
          ),
          _buildListItem(
            context,
            Icons.calendar_today,
            'Mes plannings de congé',
            Colors.orange,
          ),
          _buildListItem(
            context,
            Icons.access_time,
            'Mon pointage',
            Colors.green,
          ),
          _buildListItem(
            context,
            Icons.holiday_village,
            'Mes weekends/jours fériés travaillés',
            Colors.purple,
          ),
          _buildListItem(
            context,
            Icons.cancel_schedule_send,
            'Mes absences ',
            Colors.red,
          ),
          _buildListItem(
            context,
            Icons.flight_takeoff,
            'Mes missions',
            Colors.teal,
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
          if (title == 'Mes droits à congé') {
            Navigator.push(
              context,
              MaterialPageRoute(
                builder: (context) => MesDroitsCongePage(idEmploye: idEmploye),
              ),
            );
          } else if (title == 'Mes plannings de congé') {
            Navigator.push(
              context,
              MaterialPageRoute(
                builder:
                    (context) => MesPlanningsCongePage(idEmploye: idEmploye),
              ),
            );
          } else if (title == 'Mon pointage') {
            Navigator.push(
              context,
              MaterialPageRoute(
                builder: (context) => MonPointagePage(idEmploye: idEmploye),
              ),
            );
          } else if (title == 'Mes weekends/jours fériés travaillés') {
            Navigator.push(
              context,
              MaterialPageRoute(
                builder:
                    (context) => MesWeekendsFeriesPage(idEmploye: idEmploye),
              ),
            );
          } else if (title == 'Mes absences ') {
            Navigator.push(
              context,
              MaterialPageRoute(
                builder: (context) => MesAbsencesPage(idEmploye: idEmploye),
              ),
            );
          } else if (title == 'Mes missions') {
            Navigator.push(
              context,
              MaterialPageRoute(
                builder: (context) => MesMissionsPage(idEmploye: idEmploye),
              ),
            );
          }
        },
      ),
    );
  }
}
