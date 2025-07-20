import 'package:flutter/material.dart';
import 'dart:convert';
import 'config.dart';
import 'package:http/http.dart' as http;

class ModifierMotDePassePage extends StatefulWidget {
  final int idEmploye;
  const ModifierMotDePassePage({super.key, required this.idEmploye});

  @override
  State<ModifierMotDePassePage> createState() => _ModifierMotDePassePageState();
}

class _ModifierMotDePassePageState extends State<ModifierMotDePassePage> {
  final _formKey = GlobalKey<FormState>();
  final TextEditingController ancienController = TextEditingController();
  final TextEditingController nouveauController = TextEditingController();
  final TextEditingController confirmerController = TextEditingController();

  bool loading = false;
  String? message;

  // Variables pour cacher/afficher le mot de passe
  bool _obscureOld = true;
  bool _obscureNew = true;
  bool _obscureConfirm = true;

  Future<void> modifierMotDePasse() async {
    setState(() {
      loading = true;
      message = null;
    });

    try {
      final response = await http.post(
        getUri('/modifier_mot_de_passe/${widget.idEmploye}'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          "ancien": ancienController.text.trim(),
          "nouveau": nouveauController.text.trim(),
        }),
      );

      final Map<String, dynamic>? data =
          response.body.isNotEmpty ? json.decode(response.body) : null;

      if (response.statusCode == 200) {
        setState(() {
          message = data?["message"] ?? "Mot de passe modifié avec succès.";
          loading = false;
        });
      } else {
        setState(() {
          message = data?["error"] ?? "Impossible de changer le mot de passe.";
          loading = false;
        });
      }
    } catch (e) {
      setState(() {
        message = "Erreur réseau : $e";
        loading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Modifier le mot de passe'),
        backgroundColor: Color.fromARGB(255, 24, 101, 215),
      ),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Form(
          key: _formKey,
          child: Column(
            children: [
              TextFormField(
                controller: ancienController,
                obscureText: _obscureOld,
                decoration: InputDecoration(
                  labelText: "Ancien mot de passe",
                  border: const OutlineInputBorder(),
                  suffixIcon: IconButton(
                    icon: Icon(
                      _obscureOld ? Icons.visibility_off : Icons.visibility,
                      color: Colors.deepPurple,
                    ),
                    onPressed: () {
                      setState(() {
                        _obscureOld = !_obscureOld;
                      });
                    },
                  ),
                ),
                validator:
                    (value) =>
                        value == null || value.isEmpty
                            ? "Champ obligatoire"
                            : null,
              ),
              const SizedBox(height: 16),
              TextFormField(
                controller: nouveauController,
                obscureText: _obscureNew,
                decoration: InputDecoration(
                  labelText: "Nouveau mot de passe",
                  border: const OutlineInputBorder(),
                  suffixIcon: IconButton(
                    icon: Icon(
                      _obscureNew ? Icons.visibility_off : Icons.visibility,
                      color: Colors.deepPurple,
                    ),
                    onPressed: () {
                      setState(() {
                        _obscureNew = !_obscureNew;
                      });
                    },
                  ),
                ),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return "Champ obligatoire";
                  }
                  if (value.length < 6) return "Au moins 6 caractères";
                  return null;
                },
              ),
              const SizedBox(height: 16),
              TextFormField(
                controller: confirmerController,
                obscureText: _obscureConfirm,
                decoration: InputDecoration(
                  labelText: "Confirmer nouveau mot de passe",
                  border: const OutlineInputBorder(),
                  suffixIcon: IconButton(
                    icon: Icon(
                      _obscureConfirm ? Icons.visibility_off : Icons.visibility,
                      color: Colors.deepPurple,
                    ),
                    onPressed: () {
                      setState(() {
                        _obscureConfirm = !_obscureConfirm;
                      });
                    },
                  ),
                ),
                validator: (value) {
                  if (value != nouveauController.text)
                    return "Les mots de passe ne correspondent pas";
                  return null;
                },
              ),
              const SizedBox(height: 20),
              loading
                  ? const CircularProgressIndicator()
                  : ElevatedButton(
                    onPressed: () {
                      if (_formKey.currentState!.validate()) {
                        modifierMotDePasse();
                      }
                    },
                    child: const Text("Modifier"),
                  ),
              if (message != null)
                Padding(
                  padding: const EdgeInsets.only(top: 16),
                  child: Text(
                    message!,
                    style: TextStyle(
                      color:
                          message!.contains("succès")
                              ? Colors.green
                              : Colors.red,
                    ),
                  ),
                ),
            ],
          ),
        ),
      ),
    );
  }
}
