import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'conditionretraite.dart';
import 'config.dart';

class MaRetraitePage extends StatefulWidget {
  final int idEmploye;
  const MaRetraitePage({super.key, required this.idEmploye});

  @override
  State<MaRetraitePage> createState() => _MaRetraitePageState();
}

class _MaRetraitePageState extends State<MaRetraitePage> {
  String statut = '';
  String message = '';
  String? dateDepot;
  String? datePrev;
  int? age;
  bool loading = true;

  @override
  void initState() {
    super.initState();
    fetchRetraiteInfo();
  }

  Future<void> fetchRetraiteInfo() async {
    setState(() {
      loading = true;
    });
    try {
      final res = await http.get(getUri('/retraite/${widget.idEmploye}'));
      if (res.statusCode == 200) {
        final data = json.decode(res.body);
        setState(() {
          statut = data['status'];
          message = data['message'];
          dateDepot = data['date_depot'];
          datePrev = data['date_previsionnelle'];
          age = data['age'];
          loading = false;
        });
      } else {
        setState(() {
          statut = 'erreur';
          message = 'Erreur lors du chargement.';
          loading = false;
        });
      }
    } catch (e) {
      setState(() {
        statut = 'erreur';
        message = 'Erreur de connexion.';
        loading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Ma Retraite'),
        backgroundColor: const Color.fromARGB(255, 24, 101, 215),
      ),
      body:
          loading
              ? const Center(child: CircularProgressIndicator())
              : Padding(
                padding: const EdgeInsets.all(20),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    // Si l'employé n'est pas concerné (moins de 60 ans)
                    if (statut == 'non_concerne') ...[
                      Text(
                        message,
                        style: const TextStyle(
                          fontWeight: FontWeight.bold,
                          fontSize: 17,
                          color: Colors.orange,
                        ),
                      ),
                    ] else ...[
                      Text(
                        message,
                        style: TextStyle(
                          fontWeight: FontWeight.bold,
                          fontSize: 17,
                          color:
                              statut == 'retraite_normale'
                                  ? Colors.green
                                  : (statut == 'poursuite'
                                      ? Colors.blue
                                      : Colors.red),
                        ),
                      ),
                      if (statut == 'retraite_normale') ...[
                        const SizedBox(height: 10),
                        if (dateDepot != null)
                          Text("Date dépôt dossier : $dateDepot"),
                        if (datePrev != null)
                          Text("Date prévisionnelle retraite : $datePrev"),
                      ],
                      const SizedBox(height: 30),
                      Center(
                        child: ElevatedButton.icon(
                          icon: const Icon(Icons.info_outline),
                          label: const Text(
                            "Conditions et modalités de mise à la retraite",
                          ),
                          style: ElevatedButton.styleFrom(
                            backgroundColor: const Color.fromARGB(
                              255,
                              24,
                              101,
                              215,
                            ),
                            foregroundColor: Colors.white,
                            minimumSize: const Size(double.infinity, 45),
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(8),
                            ),
                          ),
                          onPressed: () {
                            Navigator.push(
                              context,
                              MaterialPageRoute(
                                builder:
                                    (context) => const ConditionRetraitePage(),
                              ),
                            );
                          },
                        ),
                      ),
                    ],
                  ],
                ),
              ),
    );
  }
}
