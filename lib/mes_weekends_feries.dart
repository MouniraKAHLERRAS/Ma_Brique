import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'config.dart';

class MesWeekendsFeriesPage extends StatefulWidget {
  final int idEmploye;

  const MesWeekendsFeriesPage({super.key, required this.idEmploye});

  @override
  State<MesWeekendsFeriesPage> createState() => _MesWeekendsFeriesPageState();
}

class _MesWeekendsFeriesPageState extends State<MesWeekendsFeriesPage> {
  List joursTravailles = [];
  bool loading = true;

  @override
  void initState() {
    super.initState();
    fetchJoursTravailles();
  }

  Future<void> fetchJoursTravailles() async {
    final response = await http.get(
      getUri('/weekends_feries/${widget.idEmploye}'),
    );

    if (response.statusCode == 200) {
      setState(() {
        joursTravailles = json.decode(response.body);
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
        title: const Text('Weekends/Jours Fériés Travaillés'),
        backgroundColor: Color.fromARGB(255, 24, 101, 215),
      ),
      body:
          loading
              ? const Center(child: CircularProgressIndicator())
              : joursTravailles.isEmpty
              ? const Center(child: Text("Aucune donnée trouvée."))
              : ListView.builder(
                padding: const EdgeInsets.all(16),
                itemCount: joursTravailles.length,
                itemBuilder: (context, index) {
                  final j = joursTravailles[index];
                  return Card(
                    margin: const EdgeInsets.symmetric(vertical: 8),
                    child: ListTile(
                      leading: const Icon(Icons.calendar_today),
                      title: Text("${j['type_jour']} - ${j['date']}"),
                      subtitle: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            "🕒 De ${j['heure_arrive']} à ${j['heure_depart']}",
                          ),
                          Text("🎁 Compensation : ${j['compensation']}"),
                        ],
                      ),
                    ),
                  );
                },
              ),
    );
  }
}
