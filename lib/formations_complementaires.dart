import 'package:flutter/material.dart';
import 'dart:convert';
import 'config.dart';
import 'package:http/http.dart' as http;

class FormationsComplementairesPage extends StatefulWidget {
  final int idEmploye;
  const FormationsComplementairesPage({super.key, required this.idEmploye});

  @override
  State<FormationsComplementairesPage> createState() =>
      _FormationsComplementairesPageState();
}

class _FormationsComplementairesPageState
    extends State<FormationsComplementairesPage> {
  List formations = [];
  bool loading = true;

  @override
  void initState() {
    super.initState();
    fetchFormations();
  }

  Future<void> fetchFormations() async {
    try {
      final response = await http.get(
        getUri('/formations_complementaires/${widget.idEmploye}'),
      );

      if (!mounted) return;

      if (response.statusCode == 200) {
        setState(() {
          formations = json.decode(response.body);
          loading = false;
        });
      } else {
        setState(() => loading = false);
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text("Erreur lors du chargement.")),
        );
      }
    } catch (e) {
      if (!mounted) return;
      setState(() => loading = false);
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(SnackBar(content: Text("Erreur réseau : $e")));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Formations Complémentaires'),
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
                    margin: const EdgeInsets.symmetric(vertical: 8),
                    elevation: 2,
                    child: ListTile(
                      title: Text(formation['intitule'] ?? ''),
                      subtitle: Text(
                        "Du ${formation['date_debut']} au ${formation['date_fin']}",
                      ),
                      leading: const Icon(Icons.school),
                    ),
                  );
                },
              ),
    );
  }
}
