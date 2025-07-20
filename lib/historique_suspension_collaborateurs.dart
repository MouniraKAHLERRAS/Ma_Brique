import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'config.dart';

class HistoriqueSuspensionCollaborateursPage extends StatefulWidget {
  final int idEmploye; // ID du manager

  const HistoriqueSuspensionCollaborateursPage({
    super.key,
    required this.idEmploye,
  });

  @override
  State<HistoriqueSuspensionCollaborateursPage> createState() =>
      _HistoriqueSuspensionCollaborateursPageState();
}

class _HistoriqueSuspensionCollaborateursPageState
    extends State<HistoriqueSuspensionCollaborateursPage> {
  List suspensions = [];
  bool loading = true;

  @override
  void initState() {
    super.initState();
    fetchSuspensions();
  }

  Future<void> fetchSuspensions() async {
    final response = await http.get(
      getUri('/suspensions_collaborateurs/${widget.idEmploye}'),
    );

    if (response.statusCode == 200) {
      setState(() {
        suspensions = json.decode(response.body);
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
        title: const Text('Suspensions Collaborateurs'),
        backgroundColor: Color.fromARGB(255, 24, 101, 215),
      ),
      body:
          loading
              ? const Center(child: CircularProgressIndicator())
              : suspensions.isEmpty
              ? const Center(child: Text("Aucune suspension trouvée."))
              : ListView.builder(
                padding: const EdgeInsets.all(16),
                itemCount: suspensions.length,
                itemBuilder: (context, index) {
                  final s = suspensions[index];
                  return Card(
                    margin: const EdgeInsets.symmetric(vertical: 8),
                    child: ListTile(
                      leading: const Icon(Icons.gavel, color: Colors.red),
                      title: Text('${s['designation']}'),
                      subtitle: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text('Collaborateur : ${s['nom']} ${s['prenom']}'),
                          Text('Date : ${s['date']}'),
                          Text('SNC : ${s['snc']}'),
                          Text('DNC : ${s['dnc']}'),
                        ],
                      ),
                    ),
                  );
                },
              ),
    );
  }
}
