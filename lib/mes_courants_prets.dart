import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'config.dart';

class MesCourantsPretsPage extends StatefulWidget {
  final int idEmploye;
  const MesCourantsPretsPage({super.key, required this.idEmploye});

  @override
  State<MesCourantsPretsPage> createState() => _MesCourantsPretsPageState();
}

class _MesCourantsPretsPageState extends State<MesCourantsPretsPage> {
  List prets = [];
  bool loading = true;

  @override
  void initState() {
    super.initState();
    fetchPrets();
  }

  Future<void> fetchPrets() async {
    final response = await http.get(
      getUri('/mes_courants_prets/${widget.idEmploye}'),
    );

    if (response.statusCode == 200) {
      setState(() {
        prets = json.decode(response.body);
        loading = false;
      });
    } else {
      setState(() {
        loading = false;
      });
      // Optionnel : afficher une erreur
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Mes Courants de Prêts'),
        backgroundColor: Color.fromARGB(255, 24, 101, 215),
      ),
      body:
          loading
              ? const Center(child: CircularProgressIndicator())
              : prets.isEmpty
              ? const Center(child: Text("Aucun prêt trouvé."))
              : ListView.builder(
                padding: const EdgeInsets.all(16),
                itemCount: prets.length,
                itemBuilder: (context, index) {
                  final p = prets[index];
                  return Card(
                    margin: const EdgeInsets.symmetric(vertical: 8),
                    child: ListTile(
                      title: Text('Contrat n°: ${p['numero_contract'] ?? ""}'),
                      subtitle: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            "Montant : ${p['montant'] ?? ""} DA",
                            style: const TextStyle(fontWeight: FontWeight.bold),
                          ),
                          Text("Nombre de mensualités : ${p['duree'] ?? ""}"),
                          Text(
                            "Date début remboursement : ${p['date_debut_remboursement'] ?? "-----"}",
                          ),
                          Text(
                            "Statut : ${p['rembourse'] == true ? "Remboursé" : "En cours"}",
                            style: TextStyle(
                              color:
                                  p['rembourse'] == true
                                      ? Colors.green
                                      : Colors.orange,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ],
                      ),
                      leading: const Icon(Icons.account_balance),
                    ),
                  );
                },
              ),
    );
  }
}
