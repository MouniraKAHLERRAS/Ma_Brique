import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'config.dart';

class MonPointagePage extends StatefulWidget {
  final int idEmploye;

  const MonPointagePage({super.key, required this.idEmploye});

  @override
  State<MonPointagePage> createState() => _MonPointagePageState();
}

class _MonPointagePageState extends State<MonPointagePage> {
  List pointages = [];
  bool loading = true;

  @override
  void initState() {
    super.initState();
    fetchPointages();
  }

  Future<void> fetchPointages() async {
    final url = getUri('/pointage/${widget.idEmploye}');
    try {
      final response = await http.get(url);
      if (response.statusCode == 200) {
        setState(() {
          pointages = json.decode(response.body);
          loading = false;
        });
      } else {
        setState(() => loading = false);
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text("Erreur lors du chargement du pointage."),
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
        title: const Text('Mon Pointage'),
        backgroundColor: const Color.fromARGB(255, 24, 101, 215),
      ),
      body:
          loading
              ? const Center(child: CircularProgressIndicator())
              : pointages.isEmpty
              ? const Center(child: Text("Aucun pointage trouvé."))
              : ListView.builder(
                padding: const EdgeInsets.all(16),
                itemCount: pointages.length,
                itemBuilder: (context, index) {
                  final pointage = pointages[index];
                  return Card(
                    margin: const EdgeInsets.symmetric(vertical: 8),
                    child: ListTile(
                      leading: const Icon(Icons.access_time),
                      title: Text("Date : ${pointage['date']}"),
                      subtitle: Text(
                        "Heure d'arrivée : ${pointage['heure_arrive']}\n"
                        "Heure de départ : ${pointage['heure_depart']}",
                      ),
                    ),
                  );
                },
              ),
    );
  }
}
