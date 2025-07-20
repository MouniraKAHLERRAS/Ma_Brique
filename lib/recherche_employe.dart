import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'config.dart';

class RechercheEmployePage extends StatefulWidget {
  const RechercheEmployePage({super.key});

  @override
  State<RechercheEmployePage> createState() => _RechercheEmployePageState();
}

class _RechercheEmployePageState extends State<RechercheEmployePage> {
  List employes = [];
  String search = '';
  bool loading = false;

  Future<void> rechercherEmployes(String query) async {
    setState(() => loading = true);
    final response = await http.get(
      getUri('/employes/recherche_global?query=$query'),
    );
    if (response.statusCode == 200) {
      setState(() {
        employes = json.decode(response.body);
        loading = false;
      });
    } else {
      setState(() {
        employes = [];
        loading = false;
      });
    }
  }

  void showDetail(Map emp) {
    showDialog(
      context: context,
      builder:
          (context) => AlertDialog(
            title: Text('${emp['nom']} ${emp['prenom']}'),
            content: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('Adresse : ${emp['adresse'] ?? "Non renseignée"}'),
                Text('Email : ${emp['email'] ?? "Non renseigné"}'),
                Text(
                  'Téléphone : ${emp['numero_telephone'] ?? "Non renseigné"}',
                ),
                Text('Poste : ${emp['poste'] ?? "Non renseigné"}'),
                Text('Service : ${emp['service'] ?? "Non renseigné"}'),
                Text('Direction : ${emp['direction'] ?? "Non renseigné"}'),
                Text('Département : ${emp['departement'] ?? "Non renseigné"}'),
              ],
            ),
            actions: [
              TextButton(
                child: const Text('Fermer'),
                onPressed: () => Navigator.of(context).pop(),
              ),
            ],
          ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Recherche Employé'),
        backgroundColor: const Color.fromARGB(255, 24, 101, 215),
      ),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(15),
            child: TextField(
              decoration: const InputDecoration(
                labelText: 'Nom, prénom, département...',
                prefixIcon: Icon(Icons.search),
                border: OutlineInputBorder(),
              ),
              onChanged: (value) {
                search = value;
                if (value.isNotEmpty) {
                  rechercherEmployes(value);
                } else {
                  setState(() => employes = []);
                }
              },
            ),
          ),
          Expanded(
            child:
                loading
                    ? const Center(child: CircularProgressIndicator())
                    : employes.isEmpty
                    ? const Center(child: Text("Aucun employé trouvé."))
                    : ListView.builder(
                      itemCount: employes.length,
                      itemBuilder: (context, index) {
                        final emp = employes[index];
                        return ListTile(
                          leading: const CircleAvatar(
                            child: Icon(Icons.person),
                          ),
                          title: Text('${emp['nom']} ${emp['prenom']}'),
                          subtitle: Text(
                            'Département : ${emp['departement'] ?? "?"}',
                          ),
                          onTap: () => showDetail(emp),
                        );
                      },
                    ),
          ),
        ],
      ),
    );
  }
}
