import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'config.dart';

class SocialPretPage extends StatefulWidget {
  final int idEmploye;
  const SocialPretPage({super.key, required this.idEmploye});

  @override
  State<SocialPretPage> createState() => _SocialPretPageState();
}

class _SocialPretPageState extends State<SocialPretPage> {
  List pretsSociaux = [];
  bool loading = true;
  String? error;

  @override
  void initState() {
    super.initState();
    fetchPretsSociaux();
  }

  Future<void> fetchPretsSociaux() async {
    try {
      final response = await http.get(
        getUri('/prets_sociaux/${widget.idEmploye}'),
      );
      if (response.statusCode == 200) {
        setState(() {
          pretsSociaux = json.decode(response.body);
          loading = false;
        });
      } else {
        setState(() {
          error = "Erreur de chargement";
          loading = false;
        });
      }
    } catch (e) {
      setState(() {
        error = "Erreur réseau : $e";
        loading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Prêt Social'),
        backgroundColor: const Color.fromARGB(255, 24, 101, 215),
      ),
      body:
          loading
              ? const Center(child: CircularProgressIndicator())
              : error != null
              ? Center(
                child: Text(error!, style: const TextStyle(color: Colors.red)),
              )
              : pretsSociaux.isEmpty
              ? const Center(child: Text("Aucun prêt social remboursé trouvé."))
              : ListView.builder(
                padding: const EdgeInsets.all(20),
                itemCount: pretsSociaux.length,
                itemBuilder: (context, index) {
                  final p = pretsSociaux[index];
                  return Card(
                    margin: const EdgeInsets.symmetric(vertical: 8),
                    child: ListTile(
                      leading: const Icon(Icons.favorite, color: Colors.red),
                      title: Text("Contrat : ${p['numero_contract']}"),
                      subtitle: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text("Date dépôt : ${p['date_depot']}"),
                          Text("Montant : ${p['montant']} DA"),
                          Text("Durée : ${p['duree']} mois"),
                          Text("Motif : ${p['motif_prets']}"),
                        ],
                      ),
                    ),
                  );
                },
              ),
    );
  }
}
