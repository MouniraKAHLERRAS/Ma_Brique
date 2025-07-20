import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'config.dart';

class ChatbotPageV2 extends StatefulWidget {
  final int idEmploye;
  const ChatbotPageV2({super.key, required this.idEmploye});

  @override
  State<ChatbotPageV2> createState() => _ChatbotPageV2State();
}

class _ChatbotPageV2State extends State<ChatbotPageV2> {
  final TextEditingController _controller = TextEditingController();
  dynamic _reponse;
  bool _chargement = false;

  Future<void> _envoyer() async {
    final question = _controller.text.trim();
    if (question.isEmpty) return;

    setState(() {
      _chargement = true;
      _reponse = null;
    });

    final url = getUri('/api/ask');

    try {
      final response = await http.post(
        url,
        headers: {"Content-Type": "application/json"},
        body: jsonEncode({
          "question": question,
          "id_employe": widget.idEmploye,
        }),
      );

      final data = jsonDecode(response.body);
      final result = data["response"] ?? data["result"];

      setState(() => _reponse = result);
    } catch (e) {
      setState(() => _reponse = "⚠️ Erreur de connexion : $e");
    } finally {
      setState(() => _chargement = false);
    }
  }

  Widget _buildCard(Map<String, dynamic> row) {
    final keys = row.keys.toList();

    return Card(
      margin: const EdgeInsets.symmetric(vertical: 8),
      color: const Color(0xFFF1F8F4),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children:
              keys.map((key) {
                final value = row[key]?.toString() ?? '';
                return Padding(
                  padding: const EdgeInsets.symmetric(vertical: 6),
                  child: Row(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Icon(
                        Icons.label_important,
                        color: Color(0xFF3F9147),
                        size: 20,
                      ),
                      const SizedBox(width: 8),
                      Expanded(
                        child: Text(
                          "$key :\n$value",
                          style: const TextStyle(
                            fontSize: 15.5,
                            color: Colors.black87,
                          ),
                        ),
                      ),
                    ],
                  ),
                );
              }).toList(),
        ),
      ),
    );
  }

  Widget _buildResponseView() {
    if (_chargement) {
      return const Center(
        child: CircularProgressIndicator(color: Color(0xFF3F9147)),
      );
    }

    if (_reponse == null) return const SizedBox();

    if (_reponse is String) {
      return Text(_reponse, style: const TextStyle(fontSize: 16));
    }

    if (_reponse is Map<String, dynamic>) {
      return ListView(children: [_buildCard(_reponse)]);
    }

    if (_reponse is List) {
      return ListView.builder(
        itemCount: _reponse.length,
        itemBuilder: (context, index) {
          final item = _reponse[index];
          return _buildCard(item as Map<String, dynamic>);
        },
      );
    }

    return const Text("⚠️ Format de réponse inattendu");
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF0F4F2),
      appBar: AppBar(
        title: const Text("🤖 Assistant RH"),
        backgroundColor: const Color(0xFF3F9147),
      ),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(16),
            child: TextField(
              controller: _controller,
              decoration: InputDecoration(
                hintText: 'Pose ta question RH...',
                prefixIcon: const Icon(
                  Icons.question_answer,
                  color: Color(0xFF3F9147),
                ),
                filled: true,
                fillColor: Colors.white,
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                ),
              ),
              onSubmitted: (_) => _envoyer(),
            ),
          ),
          ElevatedButton.icon(
            onPressed: _envoyer,
            icon: const Icon(Icons.send),
            label: const Text("Envoyer"),
            style: ElevatedButton.styleFrom(
              backgroundColor: const Color(0xFF3F9147),
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(10),
              ),
            ),
          ),
          const SizedBox(height: 12),
          Expanded(
            child: Padding(
              padding: const EdgeInsets.all(10),
              child: _buildResponseView(),
            ),
          ),
        ],
      ),
    );
  }
}
