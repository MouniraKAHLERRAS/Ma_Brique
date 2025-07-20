import 'package:flutter/material.dart';
import 'package:flutter_vector_icons/flutter_vector_icons.dart';
import 'package:try_1/ma_position.dart';
import 'package:try_1/mes_prets.dart';
import 'package:try_1/mes_remboursements_mip_cnas.dart';
import 'package:try_1/prestations_sociales.dart';
//import 'package:try_1/accueil_manager.dart';
import 'package:try_1/listing_collaborateurs.dart';
import 'package:try_1/droits_conge_collaborateurs.dart';
import 'package:try_1/formations_previsionnelles_collaborateurs.dart';
import 'package:try_1/assiduite_collaborateurs.dart';
import 'package:try_1/historique_suspension_collaborateurs.dart';
import 'package:try_1/apprentis_departement.dart';
import 'package:try_1/recherche_collaborateur.dart';
import 'package:try_1/etat_civil.dart';
import 'package:try_1/informations_generales.dart';
import 'package:try_1/anciennete_sonatrach.dart';
import 'package:try_1/experience_secteur.dart';
import 'package:try_1/experience_hors_secteur.dart';
import 'package:try_1/realisations_majeures.dart';
import 'package:try_1/medailles_gratifications.dart';
import 'package:try_1/sanctions_disciplinaires.dart';
import 'package:try_1/formation_base.dart';
import 'package:try_1/formations_complementaires.dart';
import 'package:try_1/formations_previsionnelles.dart';
import 'package:try_1/catalogue_exr.dart';
import 'package:try_1/elearning.dart';
import 'package:try_1/ma_retraite.dart';
//import 'package:try_1/conges.dart';
//import 'package:try_1/demandes.dart';
//import 'package:try_1/paie.dart';
//import 'package:try_1/sante.dart';
//import 'package:try_1/documents.dart';
import 'package:try_1/parametre.dart';
import 'package:try_1/main.dart';
import 'chatbot_page.dart';
import 'package:try_1/mes_inscriptions.dart';
import 'package:try_1/messagerie.dart';
import 'package:try_1/notifications_page.dart';
import 'package:try_1/recherche_employe.dart';
import 'package:try_1/news_notifications_widget.dart';
import 'chatbot_page_v2.dart';

class AcceuilPage extends StatelessWidget {
  final String nom;
  final String prenom;
  final int idEmploye;
  final bool isManager; // ✅ AJOUT

  const AcceuilPage({
    super.key,
    required this.nom,
    required this.prenom,
    required this.idEmploye,
    required this.isManager, // ✅ AJOUT
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[50],
      appBar: AppBar(
        title: Row(
          children: [
            Image.asset('assets/avatar.png', height: 30),
            const SizedBox(width: 10),
            const Text('MA BRIQUE', style: TextStyle(fontSize: 18)),
          ],
        ),
        backgroundColor: const Color.fromARGB(255, 24, 101, 215),
        elevation: 0,
        /* actions: [
          IconButton(icon: const Icon(Icons.notifications), onPressed: () {}),
          IconButton(icon: const Icon(Icons.person), onPressed: () {}),
        ],*/
      ),
      drawer: _buildDrawer(context),
      body: SingleChildScrollView(
        child: Column(
          children: [
            // Header
            Container(
              padding: const EdgeInsets.all(20),
              decoration: const BoxDecoration(
                gradient: LinearGradient(
                  colors: [
                    Color.fromARGB(255, 65, 77, 211),
                    Color.fromARGB(255, 65, 77, 211),
                  ],
                  begin: Alignment.topLeft,
                  end: Alignment.bottomRight,
                ),
                borderRadius: BorderRadius.only(
                  bottomLeft: Radius.circular(20),
                  bottomRight: Radius.circular(20),
                ),
              ),
              child: Row(
                children: [
                  const CircleAvatar(
                    radius: 25,
                    backgroundImage: AssetImage('assets/user_placeholder.png'),
                  ),
                  const SizedBox(width: 15),
                  Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'Bienvenue : $nom $prenom',

                        style: TextStyle(
                          color: Colors.white,
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      Text(
                        'Direction Data Management',
                        style: TextStyle(
                          color: Colors.green[100],
                          fontSize: 14,
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            ),
            // Ce que je dois savoir
            Padding(
              padding: const EdgeInsets.all(20),
              child: Card(
                elevation: 4,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(10),
                ),
                child: Padding(
                  padding: const EdgeInsets.all(15),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.center,
                    children: [
                      Text(
                        'Ce que je dois savoir',
                        style: TextStyle(
                          fontSize: 20,
                          fontWeight: FontWeight.bold,
                          color: const Color.fromARGB(255, 36, 49, 190),
                        ),
                      ),
                      const SizedBox(height: 10),
                      Center(
                        child: Text(
                          'Bienvenue $nom $prenom sur votre espace RH ! Ici, vous pouvez consulter toutes vos informations (carrière, congés, formations…), contacter et rechercher vos collaborateurs, ajuster la visibilité de vos données et obtenir facilement les renseignements souhaités via l\'assistant virtuel. Recevez aussi en temps réel les notifications sur l\'état de vos demandes, sans avoir à vous déplacer.',
                          style: TextStyle(
                            fontSize: 15,
                            color: Color.fromARGB(255, 0, 0, 0),
                            height: 2,
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),
            // Menu
            Padding(
              padding: const EdgeInsets.all(20),
              child: GridView.count(
                shrinkWrap: true,
                physics: const NeverScrollableScrollPhysics(),
                crossAxisCount: 3,
                childAspectRatio: 1.0,
                mainAxisSpacing: 15,
                crossAxisSpacing: 15,
                children: [
                  _buildMenuCard(
                    context,
                    icon: Icons.admin_panel_settings,
                    title: 'Espace ADM',
                    color: Colors.purple,
                    onTap: () {
                      showModalBottomSheet(
                        context: context,
                        shape: const RoundedRectangleBorder(
                          borderRadius: BorderRadius.vertical(
                            top: Radius.circular(20),
                          ),
                        ),
                        builder: (context) {
                          return Column(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              const SizedBox(height: 15),
                              const Text(
                                'Espace ADM',
                                style: TextStyle(
                                  fontSize: 20,
                                  fontWeight: FontWeight.bold,
                                  color: Colors.purple,
                                ),
                              ),
                              const SizedBox(height: 10),
                              const Divider(thickness: 2),
                              ListTile(
                                leading: const Icon(
                                  Icons.my_location,
                                  color: Colors.blue,
                                ),
                                title: const Text('Ma Position'),
                                onTap: () {
                                  Navigator.pop(
                                    context,
                                  ); // Fermer le bottom sheet
                                  Navigator.push(
                                    context,
                                    MaterialPageRoute(
                                      builder:
                                          (context) => MaPositionPage(
                                            idEmploye: idEmploye,
                                          ),
                                    ),
                                  );
                                },
                              ),
                              ListTile(
                                leading: const Icon(
                                  Icons.account_balance_wallet,
                                  color: Colors.green,
                                ),
                                title: const Text('Mes Prêts'),
                                onTap: () {
                                  Navigator.pop(
                                    context,
                                  ); // Fermer le bottom sheet
                                  Navigator.push(
                                    context,
                                    MaterialPageRoute(
                                      builder:
                                          (context) => MesPretsPage(
                                            idEmploye: idEmploye,
                                          ),
                                    ),
                                  );
                                },
                              ),
                              ListTile(
                                leading: const Icon(
                                  Icons.badge,
                                  color: Colors.orange,
                                ),
                                title: const Text('Mon État Civil'),
                                onTap: () {
                                  Navigator.pop(context);
                                  Navigator.push(
                                    context,
                                    MaterialPageRoute(
                                      builder:
                                          (context) => MonEtatCivilPage(
                                            idEmploye: idEmploye,
                                          ),
                                    ),
                                  );
                                },
                              ),
                            ],
                          );
                        },
                      );
                    },
                  ),
                  _buildMenuCard(
                    context,
                    icon: Icons.message,
                    title: 'Messagerie',
                    color: Colors.blueAccent,
                    onTap: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder:
                              (context) => MessageriePage(idEmploye: idEmploye),
                        ),
                      );
                    },
                  ),

                  _buildMenuCard(
                    context,
                    icon: FontAwesome.briefcase,
                    title: 'Carrière',
                    color: Colors.orange,
                    onTap: () {
                      showModalBottomSheet(
                        context: context,
                        shape: const RoundedRectangleBorder(
                          borderRadius: BorderRadius.vertical(
                            top: Radius.circular(20),
                          ),
                        ),
                        builder: (context) {
                          return SingleChildScrollView(
                            child: Column(
                              mainAxisSize: MainAxisSize.min,
                              children: [
                                const SizedBox(height: 15),
                                const Text(
                                  'Carrière',
                                  style: TextStyle(
                                    fontSize: 20,
                                    fontWeight: FontWeight.bold,
                                    color: Colors.orangeAccent,
                                  ),
                                ),
                                const SizedBox(height: 10),
                                const Divider(thickness: 2),
                                ListTile(
                                  leading: const Icon(
                                    Icons.info,
                                    color: Colors.blue,
                                  ),
                                  title: const Text('Informations Générales'),
                                  onTap: () {
                                    Navigator.pop(
                                      context,
                                    ); // Ferme le bottom sheet
                                    Navigator.push(
                                      context,
                                      MaterialPageRoute(
                                        builder:
                                            (context) =>
                                                InformationsGeneralesPage(
                                                  idEmploye: idEmploye,
                                                ),
                                      ),
                                    );
                                  },
                                ),
                                ListTile(
                                  leading: const Icon(
                                    Icons.timeline,
                                    color: Colors.green,
                                  ),
                                  title: const Text('Mon Ancienneté SONATRACH'),
                                  onTap: () {
                                    Navigator.pop(context);
                                    Navigator.push(
                                      context,
                                      MaterialPageRoute(
                                        builder:
                                            (context) =>
                                                AncienneteSonatrachPage(
                                                  idEmploye: idEmploye,
                                                ),
                                      ),
                                    );
                                  },
                                ),

                                ListTile(
                                  leading: const Icon(
                                    Icons.work,
                                    color: Colors.teal,
                                  ),
                                  title: const Text('Mon Expérience Secteur'),
                                  onTap: () {
                                    Navigator.pop(context);
                                    Navigator.push(
                                      context,
                                      MaterialPageRoute(
                                        builder:
                                            (context) => ExperienceSecteurPage(
                                              idEmploye: idEmploye,
                                            ),
                                      ),
                                    );
                                  },
                                ),
                                ListTile(
                                  leading: const Icon(
                                    Icons.public,
                                    color: Colors.orange,
                                  ),
                                  title: const Text(
                                    'Mon Expérience Hors Secteur',
                                  ),
                                  onTap: () {
                                    Navigator.pop(context);
                                    Navigator.push(
                                      context,
                                      MaterialPageRoute(
                                        builder:
                                            (context) =>
                                                ExperienceHorsSecteurPage(
                                                  idEmploye: idEmploye,
                                                ),
                                      ),
                                    );
                                  },
                                ),
                                ListTile(
                                  leading: const Icon(
                                    Icons.star,
                                    color: Colors.purple,
                                  ),
                                  title: const Text(
                                    'Mes Réalisations Majeures',
                                  ),
                                  onTap: () {
                                    Navigator.pop(context);
                                    Navigator.push(
                                      context,
                                      MaterialPageRoute(
                                        builder:
                                            (context) =>
                                                RealisationMajeuresPage(
                                                  idEmploye: idEmploye,
                                                ),
                                      ),
                                    );
                                  },
                                ),

                                ListTile(
                                  leading: const Icon(
                                    Icons.emoji_events,
                                    color: Colors.red,
                                  ),
                                  title: const Text(
                                    'Mes Médailles / Gratifications',
                                  ),
                                  onTap: () {
                                    Navigator.pop(context);
                                    Navigator.push(
                                      context,
                                      MaterialPageRoute(
                                        builder:
                                            (context) =>
                                                const MedaillesGratificationsPage(),
                                      ),
                                    );
                                  },
                                ),
                                ListTile(
                                  leading: const Icon(
                                    Icons.gavel,
                                    color: Colors.brown,
                                  ),
                                  title: const Text('Sanctions Disciplinaires'),
                                  onTap: () {
                                    Navigator.pop(context);
                                    Navigator.push(
                                      context,
                                      MaterialPageRoute(
                                        builder:
                                            (context) =>
                                                SanctionsDisciplinairesPage(
                                                  idEmploye: idEmploye,
                                                ),
                                      ),
                                    );
                                  },
                                ),
                              ],
                            ),
                          );
                        },
                      );
                    },
                  ),
                  _buildMenuCard(
                    context,
                    icon: FontAwesome.graduation_cap,
                    title: 'Formation',
                    color: Colors.green,
                    onTap: () {
                      showModalBottomSheet(
                        context: context,
                        shape: const RoundedRectangleBorder(
                          borderRadius: BorderRadius.vertical(
                            top: Radius.circular(20),
                          ),
                        ),
                        builder: (context) {
                          return SingleChildScrollView(
                            child: Column(
                              mainAxisSize: MainAxisSize.min,
                              children: [
                                const SizedBox(height: 15),
                                const Text(
                                  'Formation',
                                  style: TextStyle(
                                    fontSize: 20,
                                    fontWeight: FontWeight.bold,
                                    color: Colors.green,
                                  ),
                                ),
                                const SizedBox(height: 10),
                                const Divider(thickness: 2),
                                ListTile(
                                  leading: const Icon(
                                    Icons.school,
                                    color: Colors.blue,
                                  ),
                                  title: const Text(
                                    'Ma formation de base / Diplômes',
                                  ),
                                  onTap: () {
                                    Navigator.pop(context);
                                    Navigator.push(
                                      context,
                                      MaterialPageRoute(
                                        builder:
                                            (context) => FormationBasePage(
                                              idEmploye: idEmploye,
                                            ),
                                      ),
                                    );
                                  },
                                ),

                                ListTile(
                                  leading: const Icon(
                                    Icons.book,
                                    color: Colors.green,
                                  ),
                                  title: const Text(
                                    'Mes formations complémentaires',
                                  ),
                                  onTap: () {
                                    Navigator.pop(context);
                                    Navigator.push(
                                      context,
                                      MaterialPageRoute(
                                        builder:
                                            (context) =>
                                                FormationsComplementairesPage(
                                                  idEmploye: idEmploye,
                                                ),
                                      ),
                                    );
                                  },
                                ),
                                ListTile(
                                  leading: const Icon(
                                    Icons.calendar_today,
                                    color: Colors.teal,
                                  ),
                                  title: const Text(
                                    'Mes formations prévisionnelles',
                                  ),
                                  onTap: () {
                                    Navigator.pop(context);
                                    Navigator.push(
                                      context,
                                      MaterialPageRoute(
                                        builder:
                                            (context) =>
                                                FormationsPrevisionnellesPage(
                                                  idEmploye: idEmploye,
                                                ),
                                      ),
                                    );
                                  },
                                ),
                                ListTile(
                                  leading: const Icon(
                                    Icons.menu_book,
                                    color: Colors.orange,
                                  ),
                                  title: const Text(
                                    'Catalogue bibliothèque EXR',
                                  ),
                                  onTap: () {
                                    Navigator.pop(context);
                                    Navigator.push(
                                      context,
                                      MaterialPageRoute(
                                        builder:
                                            (context) =>
                                                const CatalogueExrPage(),
                                      ),
                                    );
                                  },
                                ),
                                ListTile(
                                  leading: const Icon(
                                    Icons.laptop_mac,
                                    color: Colors.purple,
                                  ),
                                  title: const Text('E-learning'),
                                  onTap: () {
                                    Navigator.pop(context);
                                    Navigator.push(
                                      context,
                                      MaterialPageRoute(
                                        builder:
                                            (context) => const ELearningPage(),
                                      ),
                                    );
                                  },
                                ),
                              ],
                            ),
                          );
                        },
                      );
                    },
                  ),
                  _buildMenuCard(
                    context,
                    icon: FontAwesome.users,
                    title: 'Social',
                    color: Colors.red,
                    onTap: () {
                      showModalBottomSheet(
                        context: context,
                        shape: const RoundedRectangleBorder(
                          borderRadius: BorderRadius.vertical(
                            top: Radius.circular(20),
                          ),
                        ),
                        builder: (context) {
                          return SingleChildScrollView(
                            child: Column(
                              mainAxisSize: MainAxisSize.min,
                              children: [
                                const SizedBox(height: 15),
                                const Text(
                                  'Social',
                                  style: TextStyle(
                                    fontSize: 20,
                                    fontWeight: FontWeight.bold,
                                    color: Colors.red,
                                  ),
                                ),
                                const SizedBox(height: 10),
                                const Divider(thickness: 2),
                                ListTile(
                                  leading: const Icon(
                                    Icons.monetization_on,
                                    color: Colors.blue,
                                  ),
                                  title: const Text(
                                    'Mes remboursements MIP/CNAS',
                                  ),
                                  onTap: () {
                                    Navigator.pop(context); // fermer le popup
                                    Navigator.push(
                                      context,
                                      MaterialPageRoute(
                                        builder:
                                            (context) =>
                                                MesRemboursementsMipCnasPage(
                                                  idEmploye: idEmploye,
                                                ),
                                      ),
                                    );
                                  },
                                ),
                                ListTile(
                                  leading: const Icon(
                                    Icons.volunteer_activism,
                                    color: Colors.green,
                                  ),
                                  title: const Text('Mes Inscriptions'),
                                  onTap: () {
                                    Navigator.pop(
                                      context,
                                    ); // Fermer le bottom sheet
                                    Navigator.push(
                                      context,
                                      MaterialPageRoute(
                                        builder:
                                            (context) =>
                                                PrestationsSocialesPage(
                                                  idEmploye: idEmploye,
                                                ),
                                      ),
                                    );
                                  },
                                ),
                                ListTile(
                                  leading: const Icon(
                                    Icons.emoji_people,
                                    color: Colors.orange,
                                  ),
                                  title: const Text(
                                    'Prestations Sociales',
                                  ), // Correction typo ici
                                  onTap: () {
                                    Navigator.pop(context);
                                    Navigator.push(
                                      context,
                                      MaterialPageRoute(
                                        builder:
                                            (context) => MesInscriptionsPage(),
                                      ),
                                    );
                                  },
                                ),
                                // ---- AJOUT DU BOUTON "Ma Retraite" ----
                                ListTile(
                                  leading: const Icon(
                                    Icons.hourglass_bottom,
                                    color: Colors.purple,
                                  ),
                                  title: const Text('Ma Retraite'),
                                  onTap: () {
                                    Navigator.pop(context);
                                    Navigator.push(
                                      context,
                                      MaterialPageRoute(
                                        builder:
                                            (context) => MaRetraitePage(
                                              idEmploye: idEmploye,
                                            ),
                                      ),
                                    );
                                  },
                                ),
                              ],
                            ),
                          );
                        },
                      );
                    },
                  ),

                  if (isManager)
                    _buildMenuCard(
                      context,
                      icon: Icons.manage_accounts,
                      title: 'Manager',
                      color: Colors.teal,
                      onTap: () {
                        showModalBottomSheet(
                          context: context,
                          shape: const RoundedRectangleBorder(
                            borderRadius: BorderRadius.vertical(
                              top: Radius.circular(10),
                            ),
                          ),
                          builder: (context) {
                            return SingleChildScrollView(
                              child: Column(
                                mainAxisSize: MainAxisSize.min,
                                children: [
                                  const SizedBox(height: 15),
                                  const Text(
                                    'Manager',
                                    style: TextStyle(
                                      fontSize: 20,
                                      fontWeight: FontWeight.bold,
                                      color: Colors.teal,
                                    ),
                                  ),
                                  const SizedBox(height: 10),
                                  const Divider(thickness: 2),

                                  // === Retiré le ListTile "Accueil Manager" ici ===
                                  ListTile(
                                    leading: const Icon(
                                      Icons.people,
                                      color: Colors.green,
                                    ),
                                    title: const Text('Listing Collaborateurs'),
                                    onTap: () {
                                      Navigator.pop(context);
                                      Navigator.push(
                                        context,
                                        MaterialPageRoute(
                                          builder:
                                              (context) =>
                                                  ListingCollaborateursPage(
                                                    idEmploye: idEmploye,
                                                  ),
                                        ),
                                      );
                                    },
                                  ),
                                  ListTile(
                                    leading: const Icon(
                                      Icons.beach_access,
                                      color: Colors.orange,
                                    ),
                                    title: const Text(
                                      'Droits à congé Collaborateurs',
                                    ),
                                    onTap: () {
                                      Navigator.pop(context);
                                      Navigator.push(
                                        context,
                                        MaterialPageRoute(
                                          builder:
                                              (context) =>
                                                  DroitsCongeCollaborateursPage(
                                                    idEmploye: idEmploye,
                                                  ),
                                        ),
                                      );
                                    },
                                  ),
                                  ListTile(
                                    leading: const Icon(
                                      Icons.school,
                                      color: Colors.purple,
                                    ),
                                    title: const Text(
                                      'Formations prévisionnelles Collaborateurs',
                                    ),
                                    onTap: () {
                                      Navigator.pop(context);
                                      Navigator.push(
                                        context,
                                        MaterialPageRoute(
                                          builder:
                                              (context) =>
                                                  FormationsPrevisionnellesCollaborateursPage(
                                                    idEmploye: idEmploye,
                                                  ),
                                        ),
                                      );
                                    },
                                  ),
                                  ListTile(
                                    leading: const Icon(
                                      Icons.check_circle,
                                      color: Colors.teal,
                                    ),
                                    title: const Text(
                                      'Assiduité Collaborateurs',
                                    ),
                                    onTap: () {
                                      Navigator.pop(context);
                                      Navigator.push(
                                        context,
                                        MaterialPageRoute(
                                          builder:
                                              (context) =>
                                                  AssiduiteCollaborateursPage(
                                                    idManager: idEmploye,
                                                  ),
                                        ),
                                      );
                                    },
                                  ),
                                  ListTile(
                                    leading: const Icon(
                                      Icons.timelapse,
                                      color: Colors.red,
                                    ),
                                    title: const Text(
                                      'Historique Suspension Collaborateurs',
                                    ),
                                    onTap: () {
                                      Navigator.pop(context);
                                      Navigator.push(
                                        context,
                                        MaterialPageRoute(
                                          builder:
                                              (context) =>
                                                  HistoriqueSuspensionCollaborateursPage(
                                                    idEmploye: idEmploye,
                                                  ),
                                        ),
                                      );
                                    },
                                  ),
                                  ListTile(
                                    leading: const Icon(
                                      Icons.school_outlined,
                                      color: Colors.indigo,
                                    ),
                                    title: const Text('Apprentis Département'),
                                    onTap: () {
                                      Navigator.pop(context);
                                      Navigator.push(
                                        context,
                                        MaterialPageRoute(
                                          builder:
                                              (context) =>
                                                  const ApprentisDepartementPage(),
                                        ),
                                      );
                                    },
                                  ),
                                  ListTile(
                                    leading: const Icon(
                                      Icons.search,
                                      color: Colors.deepOrange,
                                    ),
                                    title: const Text(
                                      'Recherche d\'un Collaborateur',
                                    ),
                                    onTap: () {
                                      Navigator.pop(context);
                                      Navigator.push(
                                        context,
                                        MaterialPageRoute(
                                          builder:
                                              (context) =>
                                                  RechercheCollaborateurPage(
                                                    idManager: idEmploye,
                                                  ),
                                        ),
                                      );
                                    },
                                  ),
                                ],
                              ),
                            );
                          },
                        );
                      },
                    ),
                ],
              ),
            ),
            // News EXR
            NewsNotificationsWidget(idEmploye: idEmploye),
            // Demande en ligne
          ],
        ),
      ),
    );
  }

  // Modifiez le drawer comme suit
  Widget _buildDrawer(BuildContext context) {
    return Drawer(
      child: ListView(
        padding: EdgeInsets.zero,
        children: [
          DrawerHeader(
            decoration: const BoxDecoration(
              color: Color.fromARGB(255, 44, 109, 207),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Image.asset('assets/avatar.png', height: 40),
                const SizedBox(height: 10),
                const Text(
                  'Accès rapide',
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ],
            ),
          ),
          // Version originale
          ListTile(
            leading: const Icon(Icons.chat, color: Colors.blue),
            title: const Text('Assistant Virtuel (payant)'),
            onTap: () {
              Navigator.pop(context);
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => ChatbotPage(idEmploye: idEmploye),
                ),
              );
            },
          ),
          // Nouvelle version
          ListTile(
            leading: const Icon(Icons.chat, color: Colors.green),
            title: const Text('Assistant Virtuel (gratuit)'),
            onTap: () {
              Navigator.pop(context);
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => ChatbotPageV2(idEmploye: idEmploye),
                ),
              );
            },
          ),
          const Divider(),
          _buildDrawerItem(context, Icons.search, 'Rechercher'),
          _buildDrawerItem(context, Icons.notifications, 'Notifications'),
          const Divider(),
          _buildDrawerItem(context, Icons.settings, 'Paramètre'),
          _buildDrawerItem(context, Icons.exit_to_app, 'Déconnexion'),
        ],
      ),
    );
  }

  Widget _buildDrawerItem(BuildContext context, IconData icon, String title) {
    return ListTile(
      leading: Icon(icon, color: const Color.fromARGB(255, 57, 101, 213)),
      title: Text(
        title,
        style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w500),
      ),
      onTap: () {
        Navigator.pop(context); // Fermer le drawer
        if (title == 'Votre Assistant Virtuelle') {
          Navigator.push(
            context,
            MaterialPageRoute(
              builder:
                  (context) => ChatbotPage(idEmploye: idEmploye), // ✅ ICI aussi
            ),
          );
        } else if (title == 'Notifications') {
          Navigator.push(
            context,
            MaterialPageRoute(
              builder: (context) => NotificationsPage(idEmploye: idEmploye),
            ),
          );
        }
        if (title == 'Rechercher') {
          Navigator.push(
            context,
            MaterialPageRoute(
              builder: (context) => const RechercheEmployePage(),
            ),
          );
        } else if (title == 'Paramètre') {
          Navigator.push(
            context,
            MaterialPageRoute(
              builder: (context) => ParametrePage(idEmploye: idEmploye),
            ),
          );
        } else if (title == 'Déconnexion') {
          showDialog(
            context: context,
            builder: (BuildContext context) {
              return AlertDialog(
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(15),
                ),
                title: Row(
                  children: const [
                    Icon(Icons.logout, color: Colors.red),
                    SizedBox(width: 10),
                    Text('Déconnexion'),
                  ],
                ),
                content: const Text(
                  'Êtes-vous sûr de vouloir vous déconnecter ?',
                  style: TextStyle(fontSize: 16),
                ),
                actionsPadding: const EdgeInsets.only(bottom: 10, right: 10),
                actions: [
                  TextButton(
                    style: TextButton.styleFrom(
                      foregroundColor: Colors.grey[700],
                      textStyle: const TextStyle(fontWeight: FontWeight.bold),
                    ),
                    child: const Text('Annuler'),
                    onPressed: () {
                      Navigator.of(context).pop(); // Fermer le popup
                    },
                  ),
                  ElevatedButton.icon(
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.red,
                      foregroundColor: Colors.white,
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(10),
                      ),
                    ),
                    icon: const Icon(Icons.logout),
                    label: const Text('Déconnecter'),
                    onPressed: () {
                      Navigator.of(context).pop(); // Fermer le popup
                      Navigator.pushReplacement(
                        context,
                        MaterialPageRoute(
                          builder: (context) => const LoginPage(),
                        ),
                      );
                    },
                  ),
                ],
              );
            },
          );
        }
      },
    );
  }

  Widget _buildMenuCard(
    BuildContext context, {
    required IconData icon,
    required String title,
    required Color color,
    required VoidCallback onTap,
  }) {
    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15)),
      child: InkWell(
        borderRadius: BorderRadius.circular(15),
        onTap: onTap,
        child: Padding(
          padding: const EdgeInsets.all(10),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(icon, size: 30, color: color),
              const SizedBox(height: 10),
              Text(
                title,
                textAlign: TextAlign.center,
                style: TextStyle(
                  fontSize: 12,
                  fontWeight: FontWeight.bold,
                  color: Colors.grey[800],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
