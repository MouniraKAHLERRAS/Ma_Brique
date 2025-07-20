import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'config.dart';

class AchatLogementCalPage extends StatefulWidget {
  final int idEmploye;
  const AchatLogementCalPage({super.key, required this.idEmploye});

  @override
  State<AchatLogementCalPage> createState() => _AchatLogementCalPageState();
}

class _AchatLogementCalPageState extends State<AchatLogementCalPage> {
  List pretsLogement = [];
  bool loading = true;
  String? error;

  @override
  void initState() {
    super.initState();
    fetchPretsLogement();
  }

  Future<void> fetchPretsLogement() async {
    try {
      final response = await http.get(
        getUri('/prets_logement_cal/${widget.idEmploye}'),
      );
      if (response.statusCode == 200) {
        setState(() {
          pretsLogement = json.decode(response.body);
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
        title: const Text('Achat Logement (CAL)'),
        backgroundColor: const Color.fromARGB(255, 24, 101, 215),
      ),
      body:
          loading
              ? const Center(child: CircularProgressIndicator())
              : error != null
              ? Center(
                child: Text(error!, style: const TextStyle(color: Colors.red)),
              )
              : pretsLogement.isEmpty
              ? const Center(
                child: Text("Aucun prêt logement remboursé trouvé."),
              )
              : ListView.builder(
                padding: const EdgeInsets.all(20),
                itemCount: pretsLogement.length,
                itemBuilder: (context, index) {
                  final p = pretsLogement[index];
                  return Card(
                    margin: const EdgeInsets.symmetric(vertical: 8),
                    child: ListTile(
                      leading: const Icon(Icons.house, color: Colors.orange),
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
