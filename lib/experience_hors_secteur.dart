import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'config.dart';

class ExperienceHorsSecteurPage extends StatefulWidget {
  final int idEmploye;

  const ExperienceHorsSecteurPage({super.key, required this.idEmploye});

  @override
  State<ExperienceHorsSecteurPage> createState() =>
      _ExperienceHorsSecteurPageState();
}

class _ExperienceHorsSecteurPageState extends State<ExperienceHorsSecteurPage> {
  List experiences = [];
  bool loading = true;

  @override
  void initState() {
    super.initState();
    fetchExperiences();
  }

  Future<void> fetchExperiences() async {
    try {
      final response = await http.get(
        getUri(
          '/exp_hors_secteur/${widget.idEmploye}', // ✅ MODIFIÉ
        ),
      );

      if (!mounted) return;

      if (response.statusCode == 200) {
        setState(() {
          experiences = json.decode(response.body);
          loading = false;
        });
      } else {
        setState(() => loading = false);
      }
    } catch (e) {
      if (!mounted) return;
      setState(() => loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Expérience Hors Secteur'),
        backgroundColor: Color.fromARGB(255, 24, 101, 215),
      ),
      body:
          loading
              ? const Center(child: CircularProgressIndicator())
              : experiences.isEmpty
              ? const Center(child: Text("Aucune expérience trouvée."))
              : ListView.builder(
                padding: const EdgeInsets.all(16),
                itemCount: experiences.length,
                itemBuilder: (context, index) {
                  final e = experiences[index];
                  return Card(
                    margin: const EdgeInsets.symmetric(vertical: 8),
                    child: ListTile(
                      title: Text(e['poste'] ?? ""),
                      subtitle: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text("Employeur : ${e['employeur'] ?? ""}"),
                          Text(
                            "Du ${e['date_debut'] ?? ""} au ${e['date_fin'] ?? ""}",
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
