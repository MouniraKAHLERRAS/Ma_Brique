import 'package:flutter/material.dart';
import 'comprendre_retraite.dart';
import 'mes_demarches.dart';
import 'droits_devoirs.dart';
import 'documents_utiles.dart';

class ConditionRetraitePage extends StatelessWidget {
  const ConditionRetraitePage({super.key});

  @override
  Widget build(BuildContext context) {
    return DefaultTabController(
      length: 4,
      child: Scaffold(
        appBar: AppBar(
          title: const Text("Conditions & Modalités"),
          backgroundColor: Color.fromARGB(255, 24, 101, 215),
          bottom: const TabBar(
            labelColor: Colors.white,
            unselectedLabelColor: Colors.white70,
            indicatorColor: Colors.white,
            isScrollable: true,
            tabs: [
              Tab(text: "Comprendre la retraite"),
              Tab(text: "Mes démarches"),
              Tab(text: "Droits/devoirs"),
              Tab(text: "Documents utiles"),
            ],
          ),
        ),
        body: const TabBarView(
          children: [
            ComprendreRetraiteTab(),
            MesDemarchesTab(),
            DroitsDevoirsTab(),
            DocumentsUtilesTab(),
          ],
        ),
      ),
    );
  }
}
