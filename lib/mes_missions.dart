import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'config.dart';

class MesMissionsPage extends StatefulWidget {
  final int idEmploye;

  const MesMissionsPage({super.key, required this.idEmploye});

  @override
  State<MesMissionsPage> createState() => _MesMissionsPageState();
}

class _MesMissionsPageState extends State<MesMissionsPage> {
  List missions = [];
  bool loading = true;

  @override
  void initState() {
    super.initState();
    fetchMissions();
  }

  Future<void> fetchMissions() async {
    try {
      final response = await http.get(getUri('/missions/${widget.idEmploye}'));

      if (response.statusCode == 200) {
        setState(() {
          missions = json.decode(response.body);
          loading = false;
        });
      } else {
        setState(() => loading = false);
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text("Erreur lors du chargement des missions"),
          ),
        );
      }
    } catch (e) {
      setState(() => loading = false);
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(SnackBar(content: Text("Erreur réseau : $e")));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Mes Missions'),
        backgroundColor: Color.fromARGB(255, 24, 101, 215),
      ),
      body:
          loading
              ? const Center(child: CircularProgressIndicator())
              : missions.isEmpty
              ? const Center(child: Text("Aucune mission trouvée."))
              : ListView.builder(
                padding: const EdgeInsets.all(16),
                itemCount: missions.length,
                itemBuilder: (context, index) {
                  final mission = missions[index];
                  return Card(
                    margin: const EdgeInsets.symmetric(vertical: 8),
                    elevation: 2,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: ListTile(
                      leading: const Icon(Icons.work_outline),
                      title: Text(mission['objet'] ?? ''),
                      subtitle: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const SizedBox(height: 5),
                          Text("Lieu : ${mission['lieu']}"),
                          Text("Itinéraire : ${mission['itineraire']}"),
                          Text(
                            "Du ${mission['date_debut']} au ${mission['date_fin']}",
                            style: const TextStyle(color: Colors.grey),
                          ),
                        ],
                      ),
                    ),
                  );
                },
              ),
    );
  }
}
