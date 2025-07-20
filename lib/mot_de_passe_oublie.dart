import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'config.dart';

class MotDePasseOubliePage extends StatefulWidget {
  const MotDePasseOubliePage({super.key});

  @override
  State<MotDePasseOubliePage> createState() => _MotDePasseOubliePageState();
}

class _MotDePasseOubliePageState extends State<MotDePasseOubliePage> {
  final TextEditingController _emailController = TextEditingController();
  final TextEditingController _codeController = TextEditingController();
  final TextEditingController _newPasswordController = TextEditingController();

  bool _codeEnvoye = false;
  bool _isLoading = false;

  Future<void> _envoyerCode() async {
    setState(() => _isLoading = true);
    final response = await http.post(
      getUri('/demander_code_reset'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'email': _emailController.text.trim()}),
    );
    setState(() => _isLoading = false);
    final data = jsonDecode(response.body);
    if (response.statusCode == 200) {
      setState(() => _codeEnvoye = true);
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(const SnackBar(content: Text('Code envoyé par email !')));
    } else {
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(SnackBar(content: Text(data['error'] ?? "Erreur !")));
    }
  }

  Future<void> _changerMotDePasse() async {
    setState(() => _isLoading = true);
    final response = await http.post(
      getUri('/reset_mot_de_passe'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'email': _emailController.text.trim(),
        'code': _codeController.text.trim(),
        'nouveau_mdp': _newPasswordController.text.trim(),
      }),
    );
    setState(() => _isLoading = false);
    final data = jsonDecode(response.body);
    if (response.statusCode == 200) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Mot de passe mis à jour !')),
      );
      Navigator.pop(context); // Retour à la connexion
    } else {
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(SnackBar(content: Text(data['error'] ?? "Erreur !")));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Réinitialisation du mot de passe'),
        backgroundColor: const Color.fromARGB(255, 24, 101, 215),
      ),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [
            if (!_codeEnvoye) ...[
              const Text(
                'Entrez votre email, vous recevrez un code par email.',
                style: TextStyle(fontSize: 16),
              ),
              const SizedBox(height: 20),
              TextField(
                controller: _emailController,
                keyboardType: TextInputType.emailAddress,
                decoration: const InputDecoration(
                  labelText: 'Adresse email',
                  prefixIcon: Icon(Icons.email),
                ),
              ),
              const SizedBox(height: 30),
              ElevatedButton(
                onPressed: _isLoading ? null : _envoyerCode,
                child:
                    _isLoading
                        ? const CircularProgressIndicator()
                        : const Text('Envoyer le code'),
              ),
            ],
            if (_codeEnvoye) ...[
              const Text(
                'Un code a été envoyé à votre email. Entrez-le puis choisissez un nouveau mot de passe.',
                style: TextStyle(fontSize: 16),
              ),
              const SizedBox(height: 20),
              TextField(
                controller: _codeController,
                keyboardType: TextInputType.number,
                decoration: const InputDecoration(
                  labelText: 'Code de vérification',
                  prefixIcon: Icon(Icons.lock),
                ),
              ),
              const SizedBox(height: 16),
              TextField(
                controller: _newPasswordController,
                obscureText: true,
                decoration: const InputDecoration(
                  labelText: 'Nouveau mot de passe',
                  prefixIcon: Icon(Icons.password),
                ),
              ),
              const SizedBox(height: 30),
              ElevatedButton(
                onPressed: _isLoading ? null : _changerMotDePasse,
                child:
                    _isLoading
                        ? const CircularProgressIndicator()
                        : const Text('Changer le mot de passe'),
              ),
            ],
          ],
        ),
      ),
    );
  }
}
