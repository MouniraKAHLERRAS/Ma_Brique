import 'package:flutter/material.dart';

class ComprendreRetraiteTab extends StatelessWidget {
  const ComprendreRetraiteTab({super.key});
  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(20),
      child: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              "Comprendre la retraite\n",
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 16),
            // Schéma 1
            Center(child: Image.asset("assets/c1.png", width: 1000)),
            const SizedBox(height: 24),
            Divider(thickness: 2, color: Colors.grey),
            const SizedBox(height: 24),
            // Schéma 2
            Center(child: Image.asset("assets/c2.png", width: 300)),
            const SizedBox(height: 24),
            Divider(thickness: 2, color: Colors.grey),
            const SizedBox(height: 24),
            // Schéma 3
            Center(child: Image.asset("assets/c3.png", width: 300)),
            const SizedBox(height: 24),
            Divider(thickness: 2, color: Colors.grey),
            const SizedBox(height: 24),
            // Schéma 4
            Center(child: Image.asset("assets/c4.png", width: 300)),
            const SizedBox(height: 24),
            Divider(thickness: 2, color: Colors.grey),
            const SizedBox(height: 24),
            // Schéma 5
            Center(child: Image.asset("assets/c5.png", width: 300)),
            const SizedBox(height: 24),
            Divider(thickness: 2, color: Colors.grey),
            const SizedBox(height: 24),
          ],
        ),
      ),
    );
  }
}
