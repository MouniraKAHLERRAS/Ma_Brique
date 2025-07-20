import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'config.dart';

class DroitsCongeCollaborateursPage extends StatefulWidget {
  final int idEmploye; // ID du manager

  const DroitsCongeCollaborateursPage({super.key, required this.idEmploye});

  @override
  State<DroitsCongeCollaborateursPage> createState() =>
      _DroitsCongeCollaborateursPageState();
}

class _DroitsCongeCollaborateursPageState
    extends State<DroitsCongeCollaborateursPage> {
  List collaborateurs = [];
  bool loading = true;

  @override
  void initState() {
    super.initState();
    fetchDroitsConge();
  }

  Future<void> fetchDroitsConge() async {
    final response = await http.get(
      getUri('/droits_conge_collaborateurs/${widget.idEmploye}'),
    );

    if (response.statusCode == 200) {
      setState(() {
        collaborateurs = json.decode(response.body);
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
        title: const Text('Droits à congé des collaborateurs'),
        backgroundColor: Color.fromARGB(255, 24, 101, 215),
      ),
      body:
          loading
              ? const Center(child: CircularProgressIndicator())
              : collaborateurs.isEmpty
              ? const Center(child: Text("Aucun collaborateur trouvé."))
              : ListView.builder(
                padding: const EdgeInsets.all(16),
                itemCount: collaborateurs.length,
                itemBuilder: (context, index) {
                  final c = collaborateurs[index];
                  return Card(
                    margin: const EdgeInsets.symmetric(vertical: 8),
                    child: ListTile(
                      leading: const Icon(Icons.person),
                      title: Text('${c['nom']} ${c['prenom']}'),
                      subtitle: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text("Congé annuel : ${c['conge_annuelle'] ?? '-'}"),
                          Text(
                            "Congé de récupération : ${c['conge_recup'] ?? '-'}",
                          ),
                          Text("Congé SCEV : ${c['conge_scev'] ?? '-'}"),
                        ],
                      ),
                    ),
                  );
                },
              ),
    );
  }
}
