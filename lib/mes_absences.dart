import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'config.dart';

class MesAbsencesPage extends StatefulWidget {
  final int idEmploye;

  const MesAbsencesPage({super.key, required this.idEmploye});

  @override
  State<MesAbsencesPage> createState() => _MesAbsencesPageState();
}

class _MesAbsencesPageState extends State<MesAbsencesPage> {
  List absences = [];
  bool loading = true;

  @override
  void initState() {
    super.initState();
    fetchAbsences();
  }

  Future<void> fetchAbsences() async {
    final url = getUri('/absences/${widget.idEmploye}');
    try {
      final response = await http.get(url);
      if (response.statusCode == 200) {
        setState(() {
          absences = json.decode(response.body);
          loading = false;
        });
      } else {
        setState(() => loading = false);
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text("Erreur lors du chargement des absences."),
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
        title: const Text('Mes Absences'),
        backgroundColor: Color.fromARGB(255, 24, 101, 215),
      ),
      body:
          loading
              ? const Center(child: CircularProgressIndicator())
              : absences.isEmpty
              ? const Center(child: Text("Aucune absence trouvée."))
              : ListView.builder(
                padding: const EdgeInsets.all(16),
                itemCount: absences.length,
                itemBuilder: (context, index) {
                  final absence = absences[index];
                  return Card(
                    margin: const EdgeInsets.symmetric(vertical: 8),
                    child: ListTile(
                      leading: const Icon(Icons.cancel_schedule_send),
                      title: Text(
                        "Absence le ${absence['date']}",
                        style: const TextStyle(fontWeight: FontWeight.bold),
                      ),
                      subtitle: Text(
                        "${absence['details']}\n"
                        "Heure d'arrivée : ${absence['heure_arrive']}\n"
                        "Heure de départ : ${absence['heure_depart']}",
                      ),
                    ),
                  );
                },
              ),
    );
  }
}
