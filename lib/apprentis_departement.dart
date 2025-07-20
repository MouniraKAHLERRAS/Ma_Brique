import 'package:flutter/material.dart';
import 'config.dart';
import 'dart:convert';

import 'package:http/http.dart' as http;

class ApprentisDepartementPage extends StatefulWidget {
  const ApprentisDepartementPage({super.key});

  @override
  State<ApprentisDepartementPage> createState() =>
      _ApprentisDepartementPageState();
}

class _ApprentisDepartementPageState extends State<ApprentisDepartementPage> {
  List apprentis = [];
  bool loading = true;
  String? error;

  @override
  void initState() {
    super.initState();
    fetchApprentis();
  }

  Future<void> fetchApprentis() async {
    try {
      final response = await http.get(getUri('/apprentis_departement_ti'));
      if (response.statusCode == 200) {
        setState(() {
          apprentis = json.decode(response.body);
          loading = false;
        });
      } else {
        setState(() {
          error = "Erreur de chargement";
          loading = false;
        });
      }
    } catch (e) {
      setState(() {
        error = "Erreur réseau : $e";
        loading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Apprentis Département'),
        backgroundColor: const Color.fromARGB(255, 24, 101, 215),
      ),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child:
            loading
                ? const Center(child: CircularProgressIndicator())
                : error != null
                ? Center(
                  child: Text(
                    error!,
                    style: const TextStyle(color: Colors.red),
                  ),
                )
                : apprentis.isEmpty
                ? const Center(
                  child: Text("Aucun apprenti du département TI trouvé."),
                )
                : ListView.builder(
                  itemCount: apprentis.length,
                  itemBuilder: (context, index) {
                    final apprenti = apprentis[index];
                    return Card(
                      margin: const EdgeInsets.symmetric(vertical: 8),
                      child: ListTile(
                        leading: const Icon(Icons.person, color: Colors.teal),
                        title: Text(
                          '${apprenti['nom']} (${apprenti['specialite']})',
                        ),
                        subtitle: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text('Organisme : ${apprenti['organisme']}'),
                            Text('Début : ${apprenti['date_debut']}'),
                            Text('Fin : ${apprenti['date_fin']}'),
                            if (apprenti['observation'] != null &&
                                apprenti['observation']
                                    .toString()
                                    .trim()
                                    .isNotEmpty)
                              Text('Observation : ${apprenti['observation']}'),
                          ],
                        ),
                      ),
                    );
                  },
                ),
      ),
    );
  }
}
