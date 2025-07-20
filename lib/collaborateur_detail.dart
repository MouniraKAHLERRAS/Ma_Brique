import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'config.dart';

class CollaborateurDetailPage extends StatefulWidget {
  final int idEmploye;
  const CollaborateurDetailPage({super.key, required this.idEmploye});

  @override
  State<CollaborateurDetailPage> createState() =>
      _CollaborateurDetailPageState();
}

class _CollaborateurDetailPageState extends State<CollaborateurDetailPage> {
  Map<String, dynamic>? data;
  bool loading = true;

  @override
  void initState() {
    super.initState();
    fetchDetail();
  }

  Future<void> fetchDetail() async {
    try {
      final response = await http.get(
        getUri('/collaborateur/${widget.idEmploye}'),
      );
      if (!mounted) return;

      if (response.statusCode == 200) {
        setState(() {
          data = json.decode(response.body);
          loading = false;
        });
      } else {
        setState(() {
          data = null;
          loading = false;
        });
      }
    } catch (e) {
      setState(() {
        data = null;
        loading = false;
      });
    }
  }

  Widget buildInfoRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Text("$label : $value", style: const TextStyle(fontSize: 16)),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Détail Collaborateur"),
        backgroundColor: const Color.fromARGB(255, 24, 101, 215),
      ),
      body:
          loading
              ? const Center(child: CircularProgressIndicator())
              : data == null
              ? const Center(child: Text("Collaborateur non trouvé."))
              : Padding(
                padding: const EdgeInsets.all(20),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      "${data!['nom']} ${data!['prenom']}",
                      style: const TextStyle(
                        fontSize: 20,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 16),
                    buildInfoRow("📍 Adresse", data!['adresse'] ?? '-'),
                    buildInfoRow("📞 Téléphone", data!['telephone'] ?? '-'),
                    buildInfoRow("📧 Email", data!['email'] ?? '-'),
                    buildInfoRow(
                      "📅 Recrutement",
                      data!['date_recrutement'] ?? '-',
                    ),
                    buildInfoRow(
                      "🩸 Groupe sanguin",
                      data!['groupe_sanguin'] ?? '-',
                    ),
                    buildInfoRow(
                      "👪 Situation familiale",
                      data!['situation_familiale'] ?? '-',
                    ),
                  ],
                ),
              ),
    );
  }
}
