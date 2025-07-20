import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:url_launcher/url_launcher.dart';
import 'config.dart';

class DocumentsUtilesTab extends StatefulWidget {
  const DocumentsUtilesTab({super.key});

  @override
  State<DocumentsUtilesTab> createState() => _DocumentsUtilesTabState();
}

class _DocumentsUtilesTabState extends State<DocumentsUtilesTab> {
  List documents = [];
  bool loading = true;

  @override
  void initState() {
    super.initState();
    fetchDocuments();
  }

  Future<void> fetchDocuments() async {
    final response = await http.get(getUri('/documents'));
    if (response.statusCode == 200) {
      setState(() {
        documents = json.decode(response.body);
        loading = false;
      });
    } else {
      setState(() {
        loading = false;
      });
    }
  }

  Future<void> _openDocument(String chemin) async {
    String url = chemin.trim();
    // Vérifie si c'est déjà un lien complet (http ou https)
    if (!url.startsWith('http://') && !url.startsWith('https://')) {
      url = '/docs/$url';
    }
    final uri = getUri(url);

    if (await canLaunchUrl(uri)) {
      await launchUrl(uri, mode: LaunchMode.externalApplication);
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Impossible d’ouvrir le document.')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(20),
      child:
          loading
              ? const Center(child: CircularProgressIndicator())
              : documents.isEmpty
              ? const Text("Aucun document disponible.")
              : ListView.separated(
                shrinkWrap: true,
                itemCount: documents.length,
                separatorBuilder: (_, __) => const Divider(),
                itemBuilder: (context, index) {
                  final doc = documents[index];
                  return ListTile(
                    leading: const Icon(
                      Icons.picture_as_pdf,
                      color: Colors.red,
                    ),
                    title: Text(doc['titre']),
                    // Supprimer le bouton téléchargement si tu veux juste ouvrir le PDF :
                    onTap: () => _openDocument(doc['chemin']),
                  );
                },
              ),
    );
  }
}
