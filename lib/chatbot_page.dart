import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'config.dart';

class ChatbotPage extends StatefulWidget {
  final int idEmploye;
  const ChatbotPage({super.key, required this.idEmploye});

  @override
  State<ChatbotPage> createState() => _ChatbotPageState();
}

class _ChatbotPageState extends State<ChatbotPage> {
  final TextEditingController _controller = TextEditingController();
  final ScrollController _scrollController = ScrollController();
  bool _chargement = false;
  late int idEmploye;
  final List<Map<String, String>> _messages = []; // Historique (optionnel)

  @override
  void initState() {
    super.initState();
    idEmploye = widget.idEmploye;
  }

  Future<void> _envoyer() async {
    final question = _controller.text.trim();
    if (question.isEmpty) return;

    setState(() {
      _chargement = true;
    });

    final url = getUri("/question");

    try {
      final response = await http.post(
        url,
        headers: {"Content-Type": "application/json"},
        body: jsonEncode({"question": question, "id_employe": idEmploye}),
      );

      final data = jsonDecode(response.body);
      String reponse;
      bool isError = false;

      if (response.statusCode == 200) {
        reponse = _formatResponse(data["result"]);
      } else if (data["error"] != null) {
        reponse = "❌ ${data["error"]}";
        isError = true;
      } else {
        reponse = "❌ Erreur serveur : ${response.statusCode}";
        isError = true;
      }

      setState(() {
        _messages.add({
          "question": question,
          "reponse": reponse,
          "isError": isError.toString(),
        });
        _controller.clear();
        _chargement = false;
      });

      // Scroll to bottom after short delay
      Future.delayed(const Duration(milliseconds: 300), () {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: const Duration(milliseconds: 350),
          curve: Curves.easeOut,
        );
      });
    } catch (e) {
      setState(() {
        _messages.add({
          "question": question,
          "reponse": "⚠️ Erreur de connexion : $e",
          "isError": "true",
        });
        _chargement = false;
      });
    }
  }

  String _formatResponse(dynamic result) {
    // Si résultat est une liste de tuples : on fait un joli tableau
    if (result is List && result.isNotEmpty && result[0] is List) {
      String text = '';
      for (var row in result) {
        text += row.join(' | ') + '\n';
      }
      return text.trim();
    }
    return result.toString();
  }

  Widget _buildMessageCard(String question, String reponse, bool isError) {
    return Card(
      color: isError ? Colors.red[50] : Colors.indigo[50],
      elevation: 3,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
      margin: const EdgeInsets.symmetric(vertical: 8),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Icon(
              isError ? Icons.error_outline : Icons.smart_toy_rounded,
              color: isError ? Colors.red : Colors.indigo,
              size: 30,
            ),
            const SizedBox(width: 12),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  if (question.isNotEmpty)
                    Text(
                      'Vous : $question',
                      style: const TextStyle(
                        fontWeight: FontWeight.bold,
                        color: Colors.black87,
                      ),
                    ),
                  if (question.isNotEmpty) const SizedBox(height: 7),
                  // Affiche la réponse joliment (tableau si possible)
                  if (reponse.contains('|'))
                    _buildTable(reponse)
                  else
                    Text(
                      reponse,
                      style: TextStyle(
                        fontSize: 16,
                        color: isError ? Colors.red[900] : Colors.black,
                      ),
                    ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  // Affiche joliment les tableaux (pour les requêtes SQL tabulaires) avec un scroll horizontal
  Widget _buildTable(String formattedText) {
    final lines = formattedText.split('\n');
    if (lines.isEmpty) return const SizedBox();

    final rows =
        lines
            .map((line) => line.split('|').map((e) => e.trim()).toList())
            .toList();

    final int columnCount = rows
        .map((r) => r.length)
        .fold(0, (a, b) => a > b ? a : b);

    return SingleChildScrollView(
      scrollDirection: Axis.horizontal,
      child: DataTable(
        headingRowColor: MaterialStateProperty.all(Colors.indigo[100]),
        columns: List.generate(
          columnCount,
          (i) => DataColumn(
            label: Text(
              'Col${i + 1}',
              style: const TextStyle(fontWeight: FontWeight.bold),
            ),
          ),
        ),
        rows:
            rows
                .map(
                  (row) => DataRow(
                    cells: List.generate(
                      columnCount,
                      (i) => DataCell(Text(i < row.length ? row[i] : "")),
                    ),
                  ),
                )
                .toList(),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[100],
      appBar: AppBar(
        title: const Text("🤖 Assistant RH"),
        backgroundColor: Colors.indigo,
        elevation: 0,
      ),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [
            TextField(
              controller: _controller,
              decoration: InputDecoration(
                labelText: 'Pose ta question ici',
                prefixIcon: const Icon(Icons.chat_bubble_outline),
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                ),
                filled: true,
                fillColor: Colors.white,
              ),
              onSubmitted: (_) => _envoyer(),
            ),
            const SizedBox(height: 12),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton.icon(
                onPressed: _chargement ? null : _envoyer,
                icon: const Icon(Icons.send),
                label: const Text("Envoyer"),
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.indigo,
                  padding: const EdgeInsets.symmetric(vertical: 14),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(10),
                  ),
                  textStyle: const TextStyle(fontSize: 16),
                ),
              ),
            ),
            const SizedBox(height: 18),
            Expanded(
              child:
                  _chargement
                      ? const Center(child: CircularProgressIndicator())
                      : _messages.isEmpty
                      ? const Center(
                        child: Text("Posez votre question à l'assistant !"),
                      )
                      : ListView.builder(
                        controller: _scrollController,
                        itemCount: _messages.length,
                        itemBuilder: (context, i) {
                          final msg = _messages[i];
                          return _buildMessageCard(
                            msg["question"] ?? '',
                            msg["reponse"] ?? '',
                            msg["isError"] == "true",
                          );
                        },
                      ),
            ),
          ],
        ),
      ),
    );
  }
}
