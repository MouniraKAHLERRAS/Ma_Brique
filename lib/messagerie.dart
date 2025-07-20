import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'chat_page.dart';
import 'config.dart';

class MessageriePage extends StatefulWidget {
  final int idEmploye;
  const MessageriePage({super.key, required this.idEmploye});

  @override
  State<MessageriePage> createState() => _MessageriePageState();
}

class _MessageriePageState extends State<MessageriePage> {
  List conversations = [];
  List employes = [];
  String search = '';
  bool loading = false;
  int totalNonLus = 0;

  @override
  void initState() {
    super.initState();
    fetchConversations();
  }

  Future<void> fetchConversations() async {
    setState(() {
      loading = true;
    });
    final res = await http.get(
      getUri('/messages/conversations/${widget.idEmploye}'),
    );
    if (res.statusCode == 200) {
      final List data = json.decode(res.body);
      setState(() {
        conversations = data;
        totalNonLus = data.fold(0, (a, c) => a + (c['non_lus'] as int));
        loading = false;
      });
    }
  }

  Future<void> rechercherEmployes(String query) async {
    setState(() {
      loading = true;
    });
    final response = await http.get(getUri('/employes/recherche?query=$query'));
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

  void goToChat(int autreId, String nom, String prenom) async {
    // Marque tous les messages reçus comme lus avant d’ouvrir la page
    await http.post(
      getUri('/messages/lire'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({
        'expediteur_id': autreId,
        'destinataire_id': widget.idEmploye,
      }),
    );
    if (!mounted) return; // Ajouté pour éviter le warning context async
    await Navigator.push(
      context,
      MaterialPageRoute(
        builder:
            (context) => ChatPage(
              monId: widget.idEmploye,
              destinataireId: autreId,
              nomDest: '$nom $prenom',
            ),
      ),
    );
    fetchConversations(); // Refresh à la sortie du chat
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Stack(
          children: [
            const Text('Messagerie'),
            if (totalNonLus > 0)
              Positioned(
                right: -5,
                top: 0,
                child: Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 6,
                    vertical: 2,
                  ),
                  decoration: BoxDecoration(
                    color: Colors.red,
                    borderRadius: BorderRadius.circular(10),
                  ),
                  child: Text(
                    '$totalNonLus',
                    style: const TextStyle(color: Colors.white, fontSize: 12),
                  ),
                ),
              ),
          ],
        ),
        backgroundColor: Colors.blueAccent,
      ),
      body: Column(
        children: [
          // Barre de recherche
          Padding(
            padding: const EdgeInsets.all(10),
            child: TextField(
              decoration: const InputDecoration(
                labelText: 'Rechercher un employé (Nom, Prénom ou ID)',
                prefixIcon: Icon(Icons.search),
                border: OutlineInputBorder(),
              ),
              onChanged: (value) {
                setState(() {
                  search = value;
                });
                if (value.isEmpty) {
                  fetchConversations();
                } else {
                  rechercherEmployes(value);
                }
              },
            ),
          ),
          Expanded(
            child:
                loading
                    ? const Center(child: CircularProgressIndicator())
                    : search.isEmpty
                    ? ListView.builder(
                      itemCount: conversations.length,
                      itemBuilder: (context, index) {
                        final conv = conversations[index];
                        return ListTile(
                          leading: Stack(
                            children: [
                              const CircleAvatar(child: Icon(Icons.person)),
                              if (conv['non_lus'] > 0)
                                Positioned(
                                  right: 0,
                                  top: 0,
                                  child: Container(
                                    padding: const EdgeInsets.all(5),
                                    decoration: const BoxDecoration(
                                      color: Colors.red,
                                      shape: BoxShape.circle,
                                    ),
                                    child: Text(
                                      '${conv['non_lus']}',
                                      style: const TextStyle(
                                        color: Colors.white,
                                        fontSize: 10,
                                      ),
                                    ),
                                  ),
                                ),
                            ],
                          ),
                          title: Text(
                            '${conv['nom']} ${conv['prenom']}',
                            style: TextStyle(
                              fontWeight:
                                  conv['non_lus'] > 0
                                      ? FontWeight.bold
                                      : FontWeight.normal,
                            ),
                          ),
                          subtitle: Text(
                            conv['dernier_message'] ?? '',
                            style: TextStyle(
                              fontWeight:
                                  conv['non_lus'] > 0
                                      ? FontWeight.bold
                                      : FontWeight.normal,
                            ),
                          ),
                          trailing: Text(conv['date_envoi'].toString()),
                          onTap:
                              () => goToChat(
                                conv['autre_id'],
                                conv['nom'],
                                conv['prenom'],
                              ),
                        );
                      },
                    )
                    : employes.isEmpty
                    ? const Center(child: Text("Aucun employé trouvé."))
                    : ListView.builder(
                      itemCount: employes.length,
                      itemBuilder: (context, index) {
                        final emp = employes[index];
                        if (emp['id_employe'] == widget.idEmploye) {
                          return Container();
                        }
                        return ListTile(
                          leading: const CircleAvatar(
                            child: Icon(Icons.person),
                          ),
                          title: Text('${emp['nom']} ${emp['prenom']}'),
                          subtitle: Text('ID: ${emp['id_employe']}'),
                          onTap:
                              () => goToChat(
                                emp['id_employe'],
                                emp['nom'],
                                emp['prenom'],
                              ),
                        );
                      },
                    ),
          ),
        ],
      ),
    );
  }
}
