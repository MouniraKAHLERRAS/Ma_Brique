import 'package:flutter/material.dart';

class DroitsDevoirsTab extends StatelessWidget {
  const DroitsDevoirsTab({super.key});

  Widget sectionTitle(String text) => Padding(
    padding: const EdgeInsets.symmetric(vertical: 10),
    child: Text(
      text,
      style: const TextStyle(
        fontWeight: FontWeight.bold,
        fontSize: 18,
        color: Colors.blue,
      ),
    ),
  );

  Widget subtitle(String text) => Padding(
    padding: const EdgeInsets.only(top: 10, bottom: 4),
    child: Text(
      text,
      style: const TextStyle(
        fontWeight: FontWeight.bold,
        fontSize: 16,
        color: Color.fromARGB(255, 37, 0, 150),
      ),
    ),
  );

  Widget bulletList(List<String> items) => Container(
    margin: const EdgeInsets.symmetric(vertical: 8),
    padding: const EdgeInsets.all(12),
    decoration: BoxDecoration(
      color: Colors.blue[50], // Bleu clair
      borderRadius: BorderRadius.circular(10),
      border: Border.all(
        color: const Color.fromARGB(255, 37, 0, 150), // Bleu foncé
        width: 2,
      ),
    ),
    child: Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children:
          items
              .map(
                (e) => Padding(
                  padding: const EdgeInsets.symmetric(vertical: 2),
                  child: Text(
                    "• $e",
                    style: const TextStyle(fontSize: 15, color: Colors.black87),
                  ),
                ),
              )
              .toList(),
    ),
  );

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(20),
      child: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            sectionTitle("Mes droits"),
            subtitle("Avant ma mise à la retraite"),
            bulletList([
              "Pré-notification CNR.",
              "Dépôt du dossier de retraite, par le service social, au pères de la CNR.",
              "Décision de cessation de la relation de travail pour mise à la retraite.",
              "Certificat de travail.",
              "Solde de tout compte (STC) (qui comprend notamment les montants dus au titre de l'IC/IZCV et l'AFC (cf. circulaire n°4.06.1 et n°08.02), ainsi que l'octroi éventuel de la gratification médaille (cf. circulaire n°7.08.1)( veuillez consulter le {lien}))",
              "Notification, contre accusé de réception, de la note d'information relative à la couverture Assurance groupe Décès, Invalidité et Maladies Redoutées",
            ]),
            subtitle("Une fois à la retraite"),
            bulletList([
              "Badge Retraité (remis par ASL)",
              "Continuer de bénéficier des œuvres sociales de la Société, conformément aux dispositions régissant les prestations en matière des Œuvres Sociales + CNAS",
              "Cadeaux retraités (somme d'argent, en guise de présent) dont le montant est arrêté par la Commission Supérieure des Œuvres Sociales",
              "Invitation aux festivités (anniversaire de la création de SONATRACH : 24 février, 1er mai, 5 juillet, 1er novembre) – un groupe (par roulement) de retraités",
              "Être rappelé, sous contrat (prestation de services) : pour accomplir une mission déterminée, dispenser des cours ou encadrer le personnel nouvellement recruté durant la période d’induction",
            ]),
            const SizedBox(height: 30),
            sectionTitle("Mes devoirs"),
            subtitle("Avant ma mise à la retraite"),
            bulletList([
              "Préparation et/ou formation du remplaçant",
              "Transfert progressive de tous les dossiers selon un échéancier à définir avant le départ à la retraite",
              "Apurement de la situation administrative et financière, notamment :",
              " Apurement des reliquats de congé (annuel ou de récupération):",
              " Solder les prêts accordés (social, véhicule, logement, construction) ou via STC",
              "Restitution des équipements professionnels et autres qui sont mis à ma disposition dans le cadre de l’activité professionnelle, notamment : les outils, micro-ordinateur, téléphone, carte professionnelle, matériel et documentation utilisés dans le cadre de l’exercice de mes fonctions.",
            ]),
            subtitle("Une fois à la retraite"),
            bulletList([
              "Déposer le dossier « Badge Retraité » auprès de ASL",
              "Déposer le dossier « MIP » + Badge Retraité MIP :",
              "Le membre adhérent ayant déjà la qualité de membre actif est appelé à fournir le dossier afin d’assurer la continuité de son adhésion (pour lui-même et ses ayants droits) en contre partie de cotisation.",
              "Déposer le dossier « Assurance Groupe » :",
              "Le retraité souhaitant bénéficier de cette couverture est appelé à signer un contrat avec l’assureur et à s’acquitter de la prime d’assurance y afférente, au profit de l’assureur.",
              "Le retraité bénéficiera des mêmes avantages et conditions de couverture (montant prime et garanties).",
              "Déposer le dossier « Tiers payant » :",
              "Le retraité souhaitant continuer de bénéficier du dispositif tiers payant est appelé à fournir un dossier à ASL et verser la contribution.",
            ]),
          ],
        ),
      ),
    );
  }
}
