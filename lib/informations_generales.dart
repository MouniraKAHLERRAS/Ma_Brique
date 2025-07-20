import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'config.dart';

class InformationsGeneralesPage extends StatefulWidget {
  final int idEmploye;
  const InformationsGeneralesPage({super.key, required this.idEmploye});

  @override
  State<InformationsGeneralesPage> createState() =>
      _InformationsGeneralesPageState();
}

class _InformationsGeneralesPageState extends State<InformationsGeneralesPage> {
  Map<String, dynamic>? infos;
  bool loading = true;
  bool modifInProgress = false;

  @override
  void initState() {
    super.initState();
    fetchInfos();
  }

  Future<void> fetchInfos() async {
    setState(() {
      loading = true;
    });
    try {
      final response = await http.get(
        getUri('/infos_generales/${widget.idEmploye}'),
      );
      if (!mounted) return;
      if (response.statusCode == 200) {
        setState(() {
          infos = json.decode(response.body);
          loading = false;
        });
      } else {
        setState(() => loading = false);
      }
    } catch (e) {
      if (!mounted) return;
      setState(() => loading = false);
    }
  }

  // Fonction pour modifier la visibilité
  Future<void> modifierVisibilite({
    bool? emailPublic,
    bool? telephonePublic,
  }) async {
    if (infos == null) return;
    setState(() {
      modifInProgress = true;
    });
    final res = await http.post(
      getUri('/employe/modifier_visibilite'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({
        'id_employe': widget.idEmploye,
        'email_public': emailPublic ?? infos!['email_public'],
        'telephone_public': telephonePublic ?? infos!['telephone_public'],
      }),
    );
    if (res.statusCode == 200) {
      setState(() {
        if (emailPublic != null) infos!['email_public'] = emailPublic;
        if (telephonePublic != null)
          infos!['telephone_public'] = telephonePublic;
      });
    }
    setState(() {
      modifInProgress = false;
    });
  }

  Widget buildInfoRow(String label, String value, {Widget? action}) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Row(
        children: [
          Expanded(
            flex: 4,
            child: Text(
              "$label :",
              style: const TextStyle(fontWeight: FontWeight.bold),
            ),
          ),
          Expanded(flex: 5, child: Text(value)),
          if (action != null) action,
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Informations Générales'),
        backgroundColor: const Color.fromARGB(255, 24, 101, 215),
      ),
      body:
          loading
              ? const Center(child: CircularProgressIndicator())
              : infos == null
              ? const Center(child: Text("Aucune information trouvée."))
              : Padding(
                padding: const EdgeInsets.all(20),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    buildInfoRow("Nom", infos!['nom'] ?? ''),
                    buildInfoRow("Prénom", infos!['prenom'] ?? ''),
                    // ---- EMAIL avec œil ----
                    buildInfoRow(
                      "Email",
                      infos!['email'] ?? '',
                      action: IconButton(
                        icon: Icon(
                          infos!['email_public'] == true
                              ? Icons.visibility
                              : Icons.visibility_off,
                          color:
                              infos!['email_public'] == true
                                  ? Colors.green
                                  : Colors.red,
                        ),
                        tooltip:
                            infos!['email_public'] == true
                                ? "Email public (cliquez pour masquer)"
                                : "Email privé (cliquez pour afficher)",
                        onPressed:
                            modifInProgress
                                ? null
                                : () async {
                                  await modifierVisibilite(
                                    emailPublic:
                                        !(infos!['email_public'] ?? true),
                                  );
                                },
                      ),
                    ),
                    // ---- Téléphone avec œil ----
                    buildInfoRow(
                      "Téléphone",
                      infos!['numero_telephone'] ?? '',
                      action: IconButton(
                        icon: Icon(
                          infos!['telephone_public'] == true
                              ? Icons.visibility
                              : Icons.visibility_off,
                          color:
                              infos!['telephone_public'] == true
                                  ? Colors.green
                                  : Colors.red,
                        ),
                        tooltip:
                            infos!['telephone_public'] == true
                                ? "Téléphone public (cliquez pour masquer)"
                                : "Téléphone privé (cliquez pour afficher)",
                        onPressed:
                            modifInProgress
                                ? null
                                : () async {
                                  await modifierVisibilite(
                                    telephonePublic:
                                        !(infos!['telephone_public'] ?? true),
                                  );
                                },
                      ),
                    ),
                    const Divider(),
                    buildInfoRow("Poste", infos!['poste'] ?? ''),
                    buildInfoRow("Service", infos!['service'] ?? ''),
                    buildInfoRow("Niveau", "${infos!['niveau'] ?? ''}"),
                    buildInfoRow("Échelle", "${infos!['echelle'] ?? ''}"),
                    buildInfoRow("Direction", infos!['direction'] ?? ''),
                    const Divider(),
                    buildInfoRow("Structure", infos!['structure'] ?? ''),
                    buildInfoRow(
                      "Classification",
                      infos!['classification'] ?? '',
                    ),
                    buildInfoRow(
                      "Début carrière",
                      infos!['debut_carriere'] ?? '',
                    ),
                  ],
                ),
              ),
    );
  }
}
