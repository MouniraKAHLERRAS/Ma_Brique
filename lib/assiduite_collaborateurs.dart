import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'config.dart';

class AssiduiteCollaborateursPage extends StatefulWidget {
  final int idManager;
  const AssiduiteCollaborateursPage({super.key, required this.idManager});

  @override
  State<AssiduiteCollaborateursPage> createState() =>
      _AssiduiteCollaborateursPageState();
}

class _AssiduiteCollaborateursPageState
    extends State<AssiduiteCollaborateursPage> {
  List assiduite = [];
  bool loading = true;

  @override
  void initState() {
    super.initState();
    fetchAssiduite();
  }

  Future<void> fetchAssiduite() async {
    final response = await http.get(
      getUri('/assiduite_collaborateurs/${widget.idManager}'),
    );

    if (response.statusCode == 200) {
      setState(() {
        assiduite = json.decode(response.body);
        loading = false;
      });
    } else {
      setState(() => loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Assiduité des collaborateurs'),
        backgroundColor: Color.fromARGB(255, 24, 101, 215),
      ),
      body:
          loading
              ? const Center(child: CircularProgressIndicator())
              : assiduite.isEmpty
              ? const Center(child: Text("Aucun pointage trouvé."))
              : ListView.builder(
                padding: const EdgeInsets.all(16),
                itemCount: assiduite.length,
                itemBuilder: (context, index) {
                  final a = assiduite[index];
                  return Card(
                    margin: const EdgeInsets.symmetric(vertical: 8),
                    child: ListTile(
                      leading: const Icon(Icons.access_time),
                      title: Text('${a['nom']} ${a['prenom']}'),
                      subtitle: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text('Date : ${a['date']}'),
                          Text(
                            'Heure arrivée : ${a['heure_arrive'] ?? 'Non renseignée'}',
                          ),
                          Text(
                            'Heure départ : ${a['heure_depart'] ?? 'Non renseignée'}',
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
