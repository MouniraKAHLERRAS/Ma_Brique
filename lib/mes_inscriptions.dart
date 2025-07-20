import 'package:flutter/material.dart';

class MesInscriptionsPage extends StatelessWidget {
  const MesInscriptionsPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Prestations Sociales'),
        backgroundColor: Color.fromARGB(255, 24, 101, 215),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              "Prestations servies par le service \"Social\" à la demande des employés",
              style: TextStyle(
                fontWeight: FontWeight.bold,
                fontSize: 18,
                color: Colors.teal,
              ),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 20),
            Table(
              border: TableBorder.all(color: Colors.grey),
              columnWidths: const {
                0: FlexColumnWidth(1.3),
                1: FlexColumnWidth(1.3),
                2: FlexColumnWidth(3),
                3: FlexColumnWidth(3),
              },
              children: [
                // En-tête large
                TableRow(
                  decoration: BoxDecoration(color: Colors.blue[50]),
                  children: [
                    TableCell(
                      child: Center(
                        child: Padding(
                          padding: EdgeInsets.symmetric(vertical: 8),
                          child: Text(
                            "Structure en charge",
                            style: TextStyle(fontWeight: FontWeight.bold),
                          ),
                        ),
                      ),
                    ),
                    TableCell(
                      child: Center(
                        child: Padding(
                          padding: EdgeInsets.symmetric(vertical: 8),
                          child: Text(
                            "",
                            style: TextStyle(fontWeight: FontWeight.bold),
                          ),
                        ),
                      ),
                    ),
                    TableCell(
                      child: Center(
                        child: Padding(
                          padding: EdgeInsets.symmetric(vertical: 8),
                          child: Text(
                            "Objet des prestations RH (je demande ; je m’informe)",
                            style: TextStyle(fontWeight: FontWeight.bold),
                            textAlign: TextAlign.center,
                          ),
                        ),
                      ),
                    ),
                    TableCell(
                      child: Center(
                        child: Padding(
                          padding: EdgeInsets.symmetric(vertical: 8),
                          child: Text(
                            "",
                            style: TextStyle(fontWeight: FontWeight.bold),
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
                // Sous-en-tête
                TableRow(
                  decoration: BoxDecoration(color: Colors.blue[100]),
                  children: [
                    TableCell(
                      child: Padding(
                        padding: EdgeInsets.all(8.0),
                        child: Text(
                          "Département",
                          style: TextStyle(fontWeight: FontWeight.bold),
                        ),
                      ),
                    ),
                    TableCell(
                      child: Padding(
                        padding: EdgeInsets.all(8.0),
                        child: Text(
                          "Service",
                          style: TextStyle(fontWeight: FontWeight.bold),
                        ),
                      ),
                    ),
                    TableCell(
                      child: Padding(
                        padding: EdgeInsets.all(8.0),
                        child: Text(
                          "Je demande mon/ma/un(e) :",
                          style: TextStyle(fontWeight: FontWeight.bold),
                        ),
                      ),
                    ),
                    TableCell(
                      child: Padding(
                        padding: EdgeInsets.all(8.0),
                        child: Text(
                          "Je m’informe sur mon/ma/mes :",
                          style: TextStyle(fontWeight: FontWeight.bold),
                        ),
                      ),
                    ),
                  ],
                ),
                // Ligne principale
                TableRow(
                  children: [
                    TableCell(
                      verticalAlignment: TableCellVerticalAlignment.top,
                      child: Padding(
                        padding: EdgeInsets.all(8.0),
                        child: Text("Gestion GRH"),
                      ),
                    ),
                    TableCell(
                      verticalAlignment: TableCellVerticalAlignment.top,
                      child: Padding(
                        padding: EdgeInsets.all(8.0),
                        child: Text("Service Social"),
                      ),
                    ),
                    TableCell(
                      verticalAlignment: TableCellVerticalAlignment.top,
                      child: Padding(
                        padding: EdgeInsets.all(8.0),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text("1- CMS:"),
                            Padding(
                              padding: const EdgeInsets.only(
                                left: 12.0,
                                top: 2,
                              ),
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Text(
                                    "• Un rendez-vous médical (se présenter auprès de l'assistante sociale muni de l'originale de la prescription médicale)",
                                  ),
                                  Text(
                                    "• Planning CMS région Boumerdès/Tizi Ouzou",
                                  ),
                                  Text(
                                    "• Cliniques conventionnées & médecins conventionnés installés dans le privé (Régions Boumerdès, Bouira, Tizi Ouzou & Alger)",
                                  ),
                                ],
                              ),
                            ),
                            SizedBox(height: 8),
                            Text("2- Dispositif Tiers Payant:"),
                            Padding(
                              padding: const EdgeInsets.only(
                                left: 12.0,
                                top: 2,
                              ),
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Text("• Prise en charge"),
                                  Text(
                                    "• Cliniques conventionnées (Région Boumerdès, Bouira, Tizi Ouzou & Territoire National + Détails des prestations par clinique)",
                                  ),
                                  Text(
                                    "• Activation et mise à jour des cartes CHIFA",
                                  ),
                                ],
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),
                    TableCell(
                      verticalAlignment: TableCellVerticalAlignment.top,
                      child: Padding(
                        padding: EdgeInsets.all(8.0),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text("1- Remboursement :"),
                            Padding(
                              padding: const EdgeInsets.only(
                                left: 12.0,
                                top: 2,
                              ),
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Text(
                                    "• Frais médicaux (consultable en ligne sur le site elhanna de la CNAS)",
                                  ),
                                  Text(
                                    "• Indemnités journalières (maladie, accident de travail, maternité) (consultable en ligne sur le site elhanna de la CNAS)",
                                  ),
                                  Text("• Prestations M.I.P"),
                                  Text("• Assurance groupe (AXA)"),
                                ],
                              ),
                            ),
                            SizedBox(height: 8),
                            Text("2- Dates des rendez-vous médicaux :"),
                            Padding(
                              padding: const EdgeInsets.only(
                                left: 12.0,
                                top: 2,
                              ),
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Text("• Médecine de soins"),
                                  Text(
                                    "• Médecine de travail (visite médicale annuelle et périodique)",
                                  ),
                                ],
                              ),
                            ),
                            SizedBox(height: 8),
                            Text("3- Programmes ASL (œuvres sociales) :"),
                            Padding(
                              padding: const EdgeInsets.only(
                                left: 12.0,
                                top: 2,
                              ),
                              child: Text(
                                "• Inscription jardin d’enfant, sport, culture & loisir, etc.",
                              ),
                            ),
                            SizedBox(height: 8),
                            Text(
                              "4- Liste des pièces à fournir pour prestations (CNAS, CNR, AXA, MIP, ASL) et les délais de rigueur",
                            ),
                          ],
                        ),
                      ),
                    ),
                  ],
                ),
              ],
            ),
            const SizedBox(height: 20),
            Card(
              margin: const EdgeInsets.symmetric(vertical: 10),
              color: Colors.blue[50],
              child: Padding(
                padding: const EdgeInsets.all(14.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      "Contact Siège :",
                      style: TextStyle(
                        fontWeight: FontWeight.bold,
                        color: Colors.blue[900],
                      ),
                    ),
                    Text("EXP-PERS-DGP-GRH-SOCIALES@Sonatrach.dz"),
                    SizedBox(height: 6),
                    Text(
                      "Contact HMD :",
                      style: TextStyle(
                        fontWeight: FontWeight.bold,
                        color: Colors.blue[900],
                      ),
                    ),
                    Text(
                      'Se rapprocher de "l\'activité sociale" au niveau de DOE',
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
