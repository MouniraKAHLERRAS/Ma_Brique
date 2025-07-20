import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'config.dart';

class SanctionsDisciplinairesPage extends StatefulWidget {
  final int idEmploye;

  const SanctionsDisciplinairesPage({super.key, required this.idEmploye});

  @override
  State<SanctionsDisciplinairesPage> createState() =>
      _SanctionsDisciplinairesPageState();
}

class _SanctionsDisciplinairesPageState
    extends State<SanctionsDisciplinairesPage> {
  List sanctions = [];
  bool loading = true;

  @override
  void initState() {
    super.initState();
    fetchSanctions();
  }

  Future<void> fetchSanctions() async {
    final response = await http.get(getUri('/sanctions/${widget.idEmploye}'));

    if (response.statusCode == 200) {
      setState(() {
        sanctions = json.decode(response.body);
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
        title: const Text('Sanctions Disciplinaires'),
        backgroundColor: Color.fromARGB(255, 24, 101, 215),
      ),
      body:
          loading
              ? const Center(child: CircularProgressIndicator())
              : sanctions.isEmpty
              ? const Center(child: Text("Aucune sanction trouvée."))
              : ListView.builder(
                padding: const EdgeInsets.all(16),
                itemCount: sanctions.length,
                itemBuilder: (context, index) {
                  final s = sanctions[index];
                  return Card(
                    margin: const EdgeInsets.symmetric(vertical: 8),
                    child: ListTile(
                      leading: const Icon(Icons.warning_amber),
                      title: Text(s['designation']),
                      subtitle: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text("📅 Date : ${s['date']}"),
                          Text("SNC : ${s['snc']}"),
                          Text("DNC : ${s['dnc']}"),
                        ],
                      ),
                    ),
                  );
                },
              ),
    );
  }
}
