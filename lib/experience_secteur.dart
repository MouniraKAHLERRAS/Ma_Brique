import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'config.dart';

class ExperienceSecteurPage extends StatefulWidget {
  final int idEmploye;
  const ExperienceSecteurPage({super.key, required this.idEmploye});

  @override
  State<ExperienceSecteurPage> createState() => _ExperienceSecteurPageState();
}

class _ExperienceSecteurPageState extends State<ExperienceSecteurPage> {
  List experiences = [];
  bool loading = true;

  @override
  void initState() {
    super.initState();
    fetchExperiences();
  }

  Future<void> fetchExperiences() async {
    final response = await http.get(
      getUri('/experience_secteur/${widget.idEmploye}'),
    );

    if (response.statusCode == 200) {
      setState(() {
        experiences = json.decode(response.body);
        loading = false;
      });
    } else {
      setState(() {
        loading = false;
      });
      // Tu peux afficher une erreur ici si tu veux
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Mon Expérience Secteur'),
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
                  final exp = experiences[index];
                  return Card(
                    margin: const EdgeInsets.symmetric(vertical: 8),
                    elevation: 2,
                    child: ListTile(
                      title: Text(exp['poste'] ?? ''),
                      subtitle: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text("Employeur : ${exp['employeur'] ?? ''}"),
                          Text("Du ${exp['date_debut']} au ${exp['date_fin']}"),
                        ],
                      ),
                      leading: const Icon(Icons.business_center),
                    ),
                  );
                },
              ),
    );
  }
}
