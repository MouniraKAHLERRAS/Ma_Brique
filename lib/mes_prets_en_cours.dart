import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'config.dart';

class MesPretsEnCoursPage extends StatefulWidget {
  final int idEmploye;
  const MesPretsEnCoursPage({super.key, required this.idEmploye});

  @override
  State<MesPretsEnCoursPage> createState() => _MesPretsEnCoursPageState();
}

class _MesPretsEnCoursPageState extends State<MesPretsEnCoursPage> {
  List prets = [];
  bool loading = true;

  @override
  void initState() {
    super.initState();
    fetchPrets();
  }

  Future<void> fetchPrets() async {
    try {
      final response = await http.get(
        getUri('/mes_prets_en_cours/${widget.idEmploye}'),
      );
      if (!mounted) return;
      if (response.statusCode == 200) {
        setState(() {
          prets = json.decode(response.body);
          loading = false;
        });
      } else {
        setState(() => loading = false);
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text("Erreur lors du chargement des prêts.")),
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
        title: const Text('Mes Prêts en cours'),
        backgroundColor: const Color.fromARGB(255, 24, 101, 215),
      ),
      body:
          loading
              ? const Center(child: CircularProgressIndicator())
              : prets.isEmpty
              ? const Center(child: Text("Aucun prêt en cours trouvé."))
              : ListView.builder(
                padding: const EdgeInsets.all(16),
                itemCount: prets.length,
                itemBuilder: (context, index) {
                  final pret = prets[index];
                  return Card(
                    margin: const EdgeInsets.symmetric(vertical: 8),
                    child: ListTile(
                      leading: const Icon(
                        Icons.attach_money,
                        color: Colors.green,
                      ),
                      title: Text(
                        "Contrat n°: ${pret['numero_contract'] ?? ''}",
                        style: const TextStyle(fontWeight: FontWeight.bold),
                      ),
                      subtitle: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text("Montant: ${pret['montant']} DA"),
                          Text("Durée: ${pret['duree']} mois"),
                          Text("Motif: ${pret['motif_prets'] ?? '-'}"),
                          Text("Date dépôt: ${pret['date_depot'] ?? '-'}"),
                          Text(
                            "Statut: ${pret['is_accorde'] == true ? 'Accordé' : 'En attente'}",
                          ),
                        ],
                      ),
                      trailing:
                          pret['rembourse'] == true
                              ? const Icon(
                                Icons.check_circle,
                                color: Colors.grey,
                              )
                              : const Icon(
                                Icons.hourglass_bottom,
                                color: Colors.orange,
                              ),
                    ),
                  );
                },
              ),
    );
  }
}
