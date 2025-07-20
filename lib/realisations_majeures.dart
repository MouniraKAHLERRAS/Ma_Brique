import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'config.dart';

class RealisationMajeuresPage extends StatefulWidget {
  final int idEmploye;

  const RealisationMajeuresPage({super.key, required this.idEmploye});

  @override
  State<RealisationMajeuresPage> createState() =>
      _RealisationMajeuresPageState();
}

class _RealisationMajeuresPageState extends State<RealisationMajeuresPage> {
  List realisations = [];
  bool loading = true;

  @override
  void initState() {
    super.initState();
    fetchRealisations();
  }

  Future<void> fetchRealisations() async {
    try {
      final response = await http.get(
        getUri('/realisations/${widget.idEmploye}'),
      );

      if (!mounted) return;

      if (response.statusCode == 200) {
        setState(() {
          realisations = json.decode(response.body);
          loading = false;
        });
      } else {
        setState(() => loading = false);
      }
    } catch (e) {
      if (!mounted) return;
      setState(() => loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Mes Réalisations Majeures'),
        backgroundColor: Color.fromARGB(255, 24, 101, 215),
      ),
      body:
          loading
              ? const Center(child: CircularProgressIndicator())
              : realisations.isEmpty
              ? const Center(child: Text("Aucune réalisation trouvée."))
              : ListView.builder(
                padding: const EdgeInsets.all(16),
                itemCount: realisations.length,
                itemBuilder: (context, index) {
                  final r = realisations[index];
                  return Card(
                    margin: const EdgeInsets.symmetric(vertical: 8),
                    child: ListTile(
                      leading: const Icon(Icons.star),
                      title: Text(r['description'] ?? 'Sans description'),
                      subtitle: Text("Date : ${r['date'] ?? '-'}"),
                    ),
                  );
                },
              ),
    );
  }
}
