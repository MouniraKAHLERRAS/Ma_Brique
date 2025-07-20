import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'config.dart';

class RechercheCollaborateurPage extends StatefulWidget {
  final int idManager; // Passez l'id_manager à cette page

  const RechercheCollaborateurPage({super.key, required this.idManager});

  @override
  State<RechercheCollaborateurPage> createState() =>
      _RechercheCollaborateurPageState();
}

class _RechercheCollaborateurPageState
    extends State<RechercheCollaborateurPage> {
  final TextEditingController nomController = TextEditingController();
  final TextEditingController prenomController = TextEditingController();
  final TextEditingController matriculeController = TextEditingController();

  Map<String, dynamic>? result;
  bool loading = false;
  String? error;

  Future<void> rechercher() async {
    setState(() {
      loading = true;
      error = null;
      result = null;
    });

    try {
      final response = await http.post(
        getUri('/recherche_collaborateur_manager/${widget.idManager}'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'nom': nomController.text.trim(),
          'prenom': prenomController.text.trim(),
          'matricule': matriculeController.text.trim(),
        }),
      );

      if (!mounted) return;

      if (response.statusCode == 200) {
        setState(() {
          result = json.decode(response.body);
          loading = false;
        });
      } else {
        setState(() {
          error = "Aucun collaborateur trouvé.";
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

  Widget buildResultCard() {
    if (result == null) return const SizedBox();
    return Card(
      margin: const EdgeInsets.only(top: 20),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              "${result!['nom']} ${result!['prenom']}",
              style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 10),
            Text("📍 Adresse : ${result!['adresse']}"),
            Text("📞 Téléphone : ${result!['numero_telephone']}"),
            Text("📧 Email : ${result!['email']}"),
            Text("🗓 Date de recrutement : ${result!['date_recrutement']}"),
            Text("📦 Retenu Panier : ${result!['retenu_panier']}"),
            Text("🩸 Groupe sanguin : ${result!['groupe_sanguin']}"),
            Text("👪 Situation familiale : ${result!['situation_familiale']}"),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Recherche Collaborateur"),
        backgroundColor: Color.fromARGB(255, 24, 101, 215),
      ),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: SingleChildScrollView(
          child: Column(
            children: [
              TextField(
                controller: nomController,
                decoration: const InputDecoration(labelText: "Nom"),
              ),
              TextField(
                controller: prenomController,
                decoration: const InputDecoration(labelText: "Prénom"),
              ),
              TextField(
                controller: matriculeController,
                decoration: const InputDecoration(labelText: "Matricule"),
                keyboardType: TextInputType.number,
              ),
              const SizedBox(height: 20),
              ElevatedButton(
                onPressed: rechercher,
                child: const Text("Rechercher"),
              ),
              if (loading) const CircularProgressIndicator(),
              if (error != null)
                Padding(
                  padding: const EdgeInsets.only(top: 20),
                  child: Text(
                    error!,
                    style: const TextStyle(color: Colors.red),
                  ),
                ),
              buildResultCard(),
            ],
          ),
        ),
      ),
    );
  }
}
