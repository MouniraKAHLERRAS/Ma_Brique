import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'config.dart';

class CongesPage extends StatefulWidget {
  final int idEmploye;

  const CongesPage({super.key, required this.idEmploye});

  @override
  State<CongesPage> createState() => _CongesPageState();
}

class _CongesPageState extends State<CongesPage> {
  List conges = [];
  bool loading = true;

  @override
  void initState() {
    super.initState();
    fetchConges();
  }

  Future<void> fetchConges() async {
    final url = getUri('/conges/${widget.idEmploye}');
    try {
      final response = await http.get(url);

      if (response.statusCode == 200) {
        setState(() {
          conges = json.decode(response.body);
          loading = false;
        });
      } else {
        setState(() => loading = false);
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text("Erreur lors du chargement des congés."),
          ),
        );
      }
    } catch (e) {
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
        title: const Text('Mes Congés'),
        backgroundColor: Color.fromARGB(255, 24, 101, 215),
      ),
      body:
          loading
              ? const Center(child: CircularProgressIndicator())
              : conges.isEmpty
              ? const Center(child: Text("Aucun congé trouvé."))
              : ListView.builder(
                padding: const EdgeInsets.all(16),
                itemCount: conges.length,
                itemBuilder: (context, index) {
                  final conge = conges[index];
                  return Card(
                    margin: const EdgeInsets.symmetric(vertical: 8),
                    elevation: 2,
                    child: ListTile(
                      leading: const Icon(Icons.beach_access),
                      title: Text(conge['designation'] ?? ''),
                      subtitle: Text(
                        "Du ${conge['date_depart']} au ${conge['date_reprise']}",
                      ),
                    ),
                  );
                },
              ),
    );
  }
}
