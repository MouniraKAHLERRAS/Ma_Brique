import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'config.dart';

class MonEtatCivilPage extends StatefulWidget {
  final int idEmploye;
  const MonEtatCivilPage({super.key, required this.idEmploye});

  @override
  State<MonEtatCivilPage> createState() => _MonEtatCivilPageState();
}

class _MonEtatCivilPageState extends State<MonEtatCivilPage> {
  Map<String, dynamic>? info;
  bool loading = true;

  @override
  void initState() {
    super.initState();
    fetchEtatCivil();
  }

  Future<void> fetchEtatCivil() async {
    final response = await http.get(getUri('/etat_civil/${widget.idEmploye}'));

    if (response.statusCode == 200) {
      setState(() {
        info = json.decode(response.body);
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
        title: const Text('Mon État Civil'),
        backgroundColor: const Color.fromARGB(255, 24, 101, 215),
      ),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child:
            loading
                ? const Center(child: CircularProgressIndicator())
                : info == null
                ? const Center(child: Text('Aucune information trouvée.'))
                : SingleChildScrollView(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      // Texte statique du prof
                      const Text(
                        'Pour mettre à jour vos informations, veuillez vous présenter au département GRH muni de pièces justificatives.\n'
                        '• Département GRH : personnel (Siège+ Oued Smar)\n'
                        '• Département AFG/OPE : personnel OPE-HMD\n',
                        style: TextStyle(
                          fontSize: 15,
                          color: Colors.deepOrange,
                          fontWeight: FontWeight.w600,
                        ),
                      ),
                      const SizedBox(height: 20),
                      // Bloc informations
                      Card(
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(12),
                        ),
                        elevation: 2,
                        child: Padding(
                          padding: const EdgeInsets.all(16),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              const Text(
                                'Vos informations personnelles :',
                                style: TextStyle(
                                  fontSize: 18,
                                  fontWeight: FontWeight.bold,
                                  color: Colors.teal,
                                ),
                              ),
                              const SizedBox(height: 12),
                              infoRow(
                                "Matricule",
                                info!['matricule'].toString(),
                              ),
                              infoRow(
                                "Nom & Prénom",
                                "${info!['nom']} ${info!['prenom']}",
                              ),
                              infoRow(
                                "Date & lieu de naissance",
                                "${info!['date_naissance']} à ${info!['lieu_naissance']}",
                              ),
                              infoRow(
                                "Situation familiale",
                                info!['situation_familiale'],
                              ),
                              if (info!['situation_familiale'].toLowerCase() ==
                                      "marié" ||
                                  info!['situation_familiale'].toLowerCase() ==
                                      "mariée")
                                infoRow(
                                  "Nombre d'enfants",
                                  info!['nb_enfants'].toString(),
                                ),
                              infoRow("Adresse", info!['adresse']),
                            ],
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
      ),
    );
  }

  Widget infoRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Row(
        children: [
          Text(
            "$label : ",
            style: const TextStyle(fontWeight: FontWeight.w600),
          ),
          Expanded(
            child: Text(
              value,
              style: const TextStyle(fontWeight: FontWeight.normal),
            ),
          ),
        ],
      ),
    );
  }
}
