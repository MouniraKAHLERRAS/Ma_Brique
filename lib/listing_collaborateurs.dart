import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'config.dart';

class ListingCollaborateursPage extends StatefulWidget {
  final int idEmploye;
  const ListingCollaborateursPage({super.key, required this.idEmploye});

  @override
  State<ListingCollaborateursPage> createState() =>
      _ListingCollaborateursPageState();
}

class _ListingCollaborateursPageState extends State<ListingCollaborateursPage> {
  List collaborateurs = [];
  bool loading = true;

  @override
  void initState() {
    super.initState();
    fetchCollaborateurs();
  }

  Future<void> fetchCollaborateurs() async {
    final response = await http.get(
      getUri('/listing_collaborateurs/${widget.idEmploye}'),
    );

    if (response.statusCode == 200) {
      setState(() {
        collaborateurs = json.decode(response.body);
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
        title: const Text('Mes Collaborateurs'),
        backgroundColor: Color.fromARGB(255, 24, 101, 215),
      ),
      body:
          loading
              ? const Center(child: CircularProgressIndicator())
              : collaborateurs.isEmpty
              ? const Center(child: Text("Aucun collaborateur trouvé."))
              : ListView.builder(
                padding: const EdgeInsets.all(16),
                itemCount: collaborateurs.length,
                itemBuilder: (context, index) {
                  final c = collaborateurs[index];
                  return Card(
                    margin: const EdgeInsets.symmetric(vertical: 8),
                    child: ListTile(
                      leading: const Icon(Icons.person),
                      title: Text("${c['nom']} ${c['prenom']}"),
                      subtitle: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text("Email : ${c['email']}"),
                          Text("Téléphone : ${c['numero_telephone']}"),
                        ],
                      ),
                    ),
                  );
                },
              ),
    );
  }
}
