import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'config.dart';

class AchatVehiculePage extends StatefulWidget {
  final int idEmploye;

  const AchatVehiculePage({super.key, required this.idEmploye});

  @override
  State<AchatVehiculePage> createState() => _AchatVehiculePageState();
}

class _AchatVehiculePageState extends State<AchatVehiculePage> {
  List pretsVehicule = [];
  bool loading = true;
  String? error;

  @override
  void initState() {
    super.initState();
    fetchAchatsVehicule();
  }

  Future<void> fetchAchatsVehicule() async {
    try {
      final response = await http.get(
        getUri('/achats_vehicule/${widget.idEmploye}'),
      );
      if (response.statusCode == 200) {
        setState(() {
          pretsVehicule = json.decode(response.body);
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
        title: const Text('Achat Véhicule'),
        backgroundColor: const Color.fromARGB(255, 24, 101, 215),
      ),
      body:
          loading
              ? const Center(child: CircularProgressIndicator())
              : error != null
              ? Center(
                child: Text(error!, style: const TextStyle(color: Colors.red)),
              )
              : pretsVehicule.isEmpty
              ? const Center(
                child: Text("Aucun prêt véhicule remboursé trouvé."),
              )
              : ListView.builder(
                padding: const EdgeInsets.all(20),
                itemCount: pretsVehicule.length,
                itemBuilder: (context, index) {
                  final p = pretsVehicule[index];
                  return Card(
                    margin: const EdgeInsets.symmetric(vertical: 8),
                    child: ListTile(
                      leading: const Icon(
                        Icons.directions_car,
                        color: Colors.blue,
                      ),
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
