import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'config.dart';

class AncienneteSonatrachPage extends StatefulWidget {
  final int idEmploye;

  const AncienneteSonatrachPage({super.key, required this.idEmploye});

  @override
  State<AncienneteSonatrachPage> createState() =>
      _AncienneteSonatrachPageState();
}

class _AncienneteSonatrachPageState extends State<AncienneteSonatrachPage> {
  List anciennetes = [];
  bool loading = true;

  @override
  void initState() {
    super.initState();
    fetchAnciennetes();
  }

  Future<void> fetchAnciennetes() async {
    final response = await http.get(
      getUri('/anciennete_sonatrach/${widget.idEmploye}'),
    );

    if (response.statusCode == 200) {
      setState(() {
        anciennetes = json.decode(response.body);
        loading = false;
      });
    } else {
      setState(() {
        loading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Mon Ancienneté SONATRACH'),
        backgroundColor: Color.fromARGB(255, 24, 101, 215),
      ),
      body:
          loading
              ? const Center(child: CircularProgressIndicator())
              : anciennetes.isEmpty
              ? const Center(child: Text("Aucune information trouvée."))
              : ListView.builder(
                padding: const EdgeInsets.all(16),
                itemCount: anciennetes.length,
                itemBuilder: (context, index) {
                  final a = anciennetes[index];
                  return Card(
                    elevation: 2,
                    margin: const EdgeInsets.symmetric(vertical: 8),
                    child: ListTile(
                      title: Text("Poste : ${a['intitule'] ?? '-'}"),
                      subtitle: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            'Date de recrutement : ${a['date_recrutement'] ?? '-'}',
                          ),
                          Text('Ancienneté : ${a['anciennete'] ?? '-'}'),
                          Text('Service : ${a['service'] ?? '-'}'),
                          Text('Département : ${a['departement'] ?? '-'}'),
                          Text('Niveau : ${a['niveau'] ?? '-'}'),
                          Text('Échelle : ${a['echelle'] ?? '-'}'),
                        ],
                      ),
                    ),
                  );
                },
              ),
    );
  }
}
