import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'config.dart';

class FormationsPrevisionnellesPage extends StatefulWidget {
  final int idEmploye;

  const FormationsPrevisionnellesPage({super.key, required this.idEmploye});

  @override
  State<FormationsPrevisionnellesPage> createState() =>
      _FormationsPrevisionnellesPageState();
}

class _FormationsPrevisionnellesPageState
    extends State<FormationsPrevisionnellesPage> {
  List formations = [];
  bool loading = true;

  @override
  void initState() {
    super.initState();
    fetchFormations();
  }

  Future<void> fetchFormations() async {
    final response = await http.get(
      getUri('/formations_previsionnelles/${widget.idEmploye}'),
    );

    if (response.statusCode == 200) {
      setState(() {
        formations = json.decode(response.body);
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
        title: const Text('Formations Prévisionnelles'),
        backgroundColor: Color.fromARGB(255, 24, 101, 215),
      ),
      body:
          loading
              ? const Center(child: CircularProgressIndicator())
              : formations.isEmpty
              ? const Center(
                child: Text("Aucune formation prévisionnelle trouvée."),
              )
              : ListView.builder(
                padding: const EdgeInsets.all(16),
                itemCount: formations.length,
                itemBuilder: (context, index) {
                  final f = formations[index];
                  return Card(
                    margin: const EdgeInsets.symmetric(vertical: 8),
                    child: ListTile(
                      title: Text(f['description'] ?? 'Sans titre'),
                      subtitle: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text("📅 Début : ${f['date_debut']}"),
                          Text("📅 Fin : ${f['date_fin']}"),
                        ],
                      ),
                    ),
                  );
                },
              ),
    );
  }
}
