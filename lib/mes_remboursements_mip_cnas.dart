import 'package:flutter/material.dart';
import 'dart:convert';
import 'config.dart';
import 'package:http/http.dart' as http;

class MesRemboursementsMipCnasPage extends StatefulWidget {
  final int idEmploye;
  const MesRemboursementsMipCnasPage({super.key, required this.idEmploye});

  @override
  State<MesRemboursementsMipCnasPage> createState() =>
      _MesRemboursementsMipCnasPageState();
}

class _MesRemboursementsMipCnasPageState
    extends State<MesRemboursementsMipCnasPage> {
  List remboursements = [];
  bool loading = true;

  @override
  void initState() {
    super.initState();
    fetchRemboursements();
  }

  Future<void> fetchRemboursements() async {
    final response = await http.get(
      getUri('/remboursements_mip_cnas/${widget.idEmploye}'),
    );
    if (response.statusCode == 200) {
      setState(() {
        remboursements = json.decode(response.body);
        loading = false;
      });
    } else {
      setState(() => loading = false);
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Erreur lors du chargement.")),
      );
    }
  }

  Color getTypeColor(String type) {
    if (type == 'MIP') return Colors.green[400]!;
    if (type == 'CNAS') return Colors.lightBlue[200]!;
    return Colors.grey[300]!;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Mes Remboursements MIP/CNAS'),
        backgroundColor: const Color.fromARGB(255, 24, 101, 215),
      ),
      body:
          loading
              ? const Center(child: CircularProgressIndicator())
              : remboursements.isEmpty
              ? const Center(child: Text("Aucun remboursement trouvé."))
              : ListView.builder(
                padding: const EdgeInsets.all(16),
                itemCount: remboursements.length,
                itemBuilder: (context, index) {
                  final r = remboursements[index];
                  return Card(
                    color: getTypeColor(r['type']),
                    elevation: 2,
                    margin: const EdgeInsets.symmetric(vertical: 8),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(10),
                    ),
                    child: ListTile(
                      leading: Icon(Icons.monetization_on, color: Colors.white),
                      title: Text(
                        "${r['type']} - ${r['montant']} DA",
                        style: const TextStyle(
                          fontWeight: FontWeight.bold,
                          color: Colors.white,
                        ),
                      ),
                      subtitle: Text(
                        "Date : ${r['date_remboursement']}",
                        style: const TextStyle(color: Colors.white70),
                      ),
                    ),
                  );
                },
              ),
    );
  }
}
