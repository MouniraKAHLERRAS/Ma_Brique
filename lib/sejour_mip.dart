import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'config.dart';

class SejourMipPage extends StatefulWidget {
  final int idEmploye;
  const SejourMipPage({super.key, required this.idEmploye});

  @override
  State<SejourMipPage> createState() => _SejourMipPageState();
}

class _SejourMipPageState extends State<SejourMipPage> {
  List sejours = [];
  bool loading = true;

  @override
  void initState() {
    super.initState();
    fetchSejours();
  }

  Future<void> fetchSejours() async {
    final response = await http.get(getUri('/sejours_mip/${widget.idEmploye}'));

    if (response.statusCode == 200) {
      setState(() {
        sejours = json.decode(response.body);
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
        title: const Text('Séjour MIP'),
        backgroundColor: Color.fromARGB(255, 24, 101, 215),
      ),
      body:
          loading
              ? const Center(child: CircularProgressIndicator())
              : sejours.isEmpty
              ? const Center(child: Text("Aucun séjour MIP trouvé."))
              : ListView.builder(
                padding: const EdgeInsets.all(16),
                itemCount: sejours.length,
                itemBuilder: (context, index) {
                  final s = sejours[index];
                  return Card(
                    margin: const EdgeInsets.symmetric(vertical: 8),
                    child: ListTile(
                      leading: const Icon(Icons.hotel),
                      title: Text(s['sejour'] ?? ''),
                      subtitle: Text('Date : ${s['date']}'),
                    ),
                  );
                },
              ),
    );
  }
}
