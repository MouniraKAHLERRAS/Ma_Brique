import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'config.dart';

class MesDroitsCongePage extends StatefulWidget {
  final int idEmploye;

  const MesDroitsCongePage({super.key, required this.idEmploye});

  @override
  State<MesDroitsCongePage> createState() => _MesDroitsCongePageState();
}

class _MesDroitsCongePageState extends State<MesDroitsCongePage> {
  Map<String, dynamic>? droits;
  bool loading = true;

  @override
  void initState() {
    super.initState();
    fetchDroitsConge();
  }

  Future<void> fetchDroitsConge() async {
    final response = await http.get(
      getUri('/droits_conge/${widget.idEmploye}'),
    );

    if (response.statusCode == 200) {
      setState(() {
        droits = json.decode(response.body);
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
        title: const Text('Mes Droits à Congé'),
        backgroundColor: Color.fromARGB(255, 24, 101, 215),
      ),
      body:
          loading
              ? const Center(child: CircularProgressIndicator())
              : droits == null
              ? const Center(child: Text("Aucun droit à congé trouvé."))
              : Padding(
                padding: const EdgeInsets.all(20),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    _buildRow("🟢 Congé Annuel :", droits!['conge_annuelle']),
                    const SizedBox(height: 12),
                    _buildRow(
                      "🟠 Congé de Récupération :",
                      droits!['conge_recup'],
                    ),
                    const SizedBox(height: 12),
                    _buildRow("🔵 Congé SCEV :", droits!['conge_scev']),
                  ],
                ),
              ),
    );
  }

  Widget _buildRow(String label, dynamic value) {
    return Row(
      children: [
        Text(label, style: const TextStyle(fontWeight: FontWeight.bold)),
        const SizedBox(width: 10),
        Text(value?.toString() ?? "Non spécifié"),
      ],
    );
  }
}
