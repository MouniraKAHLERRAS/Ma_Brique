import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'config.dart';

class FormationsPrevisionnellesCollaborateursPage extends StatefulWidget {
  final int idEmploye; // ID du manager

  const FormationsPrevisionnellesCollaborateursPage({
    super.key,
    required this.idEmploye,
  });

  @override
  State<FormationsPrevisionnellesCollaborateursPage> createState() =>
      _FormationsPrevisionnellesCollaborateursPageState();
}

class _FormationsPrevisionnellesCollaborateursPageState
    extends State<FormationsPrevisionnellesCollaborateursPage> {
  List formations = [];
  bool loading = true;

  @override
  void initState() {
    super.initState();
    fetchFormations();
  }

  Future<void> fetchFormations() async {
    final response = await http.get(
      getUri('/formations_previsionnelles_collaborateurs/${widget.idEmploye}'),
    );

    if (response.statusCode == 200) {
      setState(() {
        formations = json.decode(response.body);
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
        title: const Text('Formations Prévisionnelles des Collaborateurs'),
        backgroundColor: Color.fromARGB(255, 24, 101, 215),
      ),
      body:
          loading
              ? const Center(child: CircularProgressIndicator())
              : formations.isEmpty
              ? const Center(child: Text("Aucune formation trouvée."))
              : ListView.builder(
                padding: const EdgeInsets.all(16),
                itemCount: formations.length,
                itemBuilder: (context, index) {
                  final f = formations[index];
                  return Card(
                    margin: const EdgeInsets.symmetric(vertical: 8),
                    child: ListTile(
                      leading: const Icon(Icons.school),
                      title: Text('${f['description']}'),
                      subtitle: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text('Collaborateur : ${f['nom']} ${f['prenom']}'),
                          Text('Début : ${f['date_debut']}'),
                          Text('Fin : ${f['date_fin']}'),
                        ],
                      ),
                    ),
                  );
                },
              ),
    );
  }
}
