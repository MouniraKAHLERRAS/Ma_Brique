import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'config.dart';

class FormationBasePage extends StatefulWidget {
  final int idEmploye;

  const FormationBasePage({super.key, required this.idEmploye});

  @override
  State<FormationBasePage> createState() => _FormationBasePageState();
}

class _FormationBasePageState extends State<FormationBasePage> {
  List formations = [];
  bool loading = true;

  @override
  void initState() {
    super.initState();
    fetchFormations();
  }

  Future<void> fetchFormations() async {
    final response = await http.get(
      getUri('/formation_base/${widget.idEmploye}'),
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
        title: const Text('Formation de Base / Diplômes'),
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
                  final formation = formations[index];
                  return Card(
                    elevation: 2,
                    margin: const EdgeInsets.symmetric(vertical: 8),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(10),
                    ),
                    child: ListTile(
                      title: Text(formation['description'] ?? ''),
                      subtitle: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text('Date début : ${formation['date_debut']}'),
                          Text('Date fin : ${formation['date_fin']}'),
                        ],
                      ),
                      leading: const Icon(Icons.school),
                    ),
                  );
                },
              ),
    );
  }
}
