import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'config.dart';

class MesPlanningsCongePage extends StatefulWidget {
  final int idEmploye;
  const MesPlanningsCongePage({super.key, required this.idEmploye});

  @override
  State<MesPlanningsCongePage> createState() => _MesPlanningsCongePageState();
}

class _MesPlanningsCongePageState extends State<MesPlanningsCongePage> {
  List plannings = [];
  bool loading = true;

  @override
  void initState() {
    super.initState();
    fetchPlannings();
  }

  Future<void> fetchPlannings() async {
    final response = await http.get(
      getUri('/plannings_conge/${widget.idEmploye}'),
    );

    if (response.statusCode == 200) {
      setState(() {
        plannings = json.decode(response.body);
        loading = false;
      });
    } else {
      setState(() => loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Mes Plannings de Congé'),
        backgroundColor: Color.fromARGB(255, 24, 101, 215),
      ),
      body:
          loading
              ? const Center(child: CircularProgressIndicator())
              : plannings.isEmpty
              ? const Center(child: Text("Aucun planning de congé trouvé."))
              : ListView.builder(
                padding: const EdgeInsets.all(16),
                itemCount: plannings.length,
                itemBuilder: (context, index) {
                  final c = plannings[index];
                  return Card(
                    margin: const EdgeInsets.symmetric(vertical: 8),
                    child: ListTile(
                      title: Text(c['designation']),
                      subtitle: Text(
                        "Du ${c['date_depart']} au ${c['date_reprise']}",
                      ),
                      leading: const Icon(Icons.calendar_month),
                    ),
                  );
                },
              ),
    );
  }
}
