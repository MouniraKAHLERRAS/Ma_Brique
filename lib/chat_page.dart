import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'config.dart';

class ChatPage extends StatefulWidget {
  final int monId;
  final int destinataireId;
  final String nomDest;

  const ChatPage({
    super.key,
    required this.monId,
    required this.destinataireId,
    required this.nomDest,
  });

  @override
  State<ChatPage> createState() => _ChatPageState();
}

class _ChatPageState extends State<ChatPage> {
  List messages = [];
  bool loading = false;
  final TextEditingController _controller = TextEditingController();

  Future<void> fetchMessages() async {
    setState(() => loading = true);
    final response = await http.get(
      getUri(
        '/messages/conversation?expediteur_id=${widget.monId}&destinataire_id=${widget.destinataireId}',
      ),
    );
    if (response.statusCode == 200) {
      setState(() {
        messages = json.decode(response.body);
        loading = false;
      });
    } else {
      setState(() => loading = false);
    }
  }

  Future<void> envoyerMessage() async {
    final contenu = _controller.text.trim();
    if (contenu.isEmpty) return;
    final response = await http.post(
      getUri('/messages/envoyer'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({
        'expediteur_id': widget.monId,
        'destinataire_id': widget.destinataireId,
        'contenu': contenu,
      }),
    );
    if (response.statusCode == 200) {
      _controller.clear();
      fetchMessages();
    }
  }

  @override
  void initState() {
    super.initState();
    fetchMessages();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Chat avec ${widget.nomDest}'),
        backgroundColor: Colors.blueAccent,
      ),
      body: Column(
        children: [
          Expanded(
            child:
                loading
                    ? const Center(child: CircularProgressIndicator())
                    : ListView.builder(
                      reverse: false,
                      itemCount: messages.length,
                      itemBuilder: (context, index) {
                        final msg = messages[index];
                        final isMe = msg['expediteur_id'] == widget.monId;
                        return Align(
                          alignment:
                              isMe
                                  ? Alignment.centerRight
                                  : Alignment.centerLeft,
                          child: Container(
                            margin: const EdgeInsets.symmetric(
                              vertical: 3,
                              horizontal: 10,
                            ),
                            padding: const EdgeInsets.all(10),
                            decoration: BoxDecoration(
                              color: isMe ? Colors.blue[200] : Colors.grey[300],
                              borderRadius: BorderRadius.circular(10),
                            ),
                            child: Column(
                              crossAxisAlignment:
                                  isMe
                                      ? CrossAxisAlignment.end
                                      : CrossAxisAlignment.start,
                              children: [
                                Text(
                                  msg['contenu'],
                                  style: const TextStyle(fontSize: 16),
                                ),
                                const SizedBox(height: 2),
                                Text(
                                  msg['date_envoi'],
                                  style: TextStyle(
                                    fontSize: 10,
                                    color: Colors.grey[600],
                                  ),
                                ),
                              ],
                            ),
                          ),
                        );
                      },
                    ),
          ),
          Divider(height: 1),
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _controller,
                    decoration: const InputDecoration(
                      hintText: "Écrire un message...",
                    ),
                  ),
                ),
                IconButton(
                  icon: const Icon(Icons.send, color: Colors.blueAccent),
                  onPressed: envoyerMessage,
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
