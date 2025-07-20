import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'config.dart';
import 'notifications_page.dart'; // Ajoute cette ligne si besoin !

class NewsNotificationsWidget extends StatefulWidget {
  final int idEmploye;
  const NewsNotificationsWidget({Key? key, required this.idEmploye})
    : super(key: key);

  @override
  State<NewsNotificationsWidget> createState() =>
      _NewsNotificationsWidgetState();
}

class _NewsNotificationsWidgetState extends State<NewsNotificationsWidget> {
  List notifs = [];
  bool loading = true;

  @override
  void initState() {
    super.initState();
    fetchNotifications();
  }

  Future<void> fetchNotifications() async {
    setState(() {
      loading = true;
    });
    final url = getUri('/notifications/dernieres/${widget.idEmploye}');
    final response = await http.get(url);
    if (response.statusCode == 200) {
      setState(() {
        notifs = json.decode(response.body);
        loading = false;
      });
    } else {
      setState(() {
        notifs = [];
        loading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 20),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            'News EXR',
            style: TextStyle(
              fontSize: 20,
              fontWeight: FontWeight.bold,
              color: Color.fromARGB(255, 57, 126, 247),
            ),
          ),
          const SizedBox(height: 10),
          Card(
            elevation: 3,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(10),
            ),
            child: Padding(
              padding: const EdgeInsets.all(15),
              child:
                  loading
                      ? const Center(child: CircularProgressIndicator())
                      : notifs.isEmpty
                      ? const Text("Aucune nouvelle notification.")
                      : Column(
                        children: [
                          for (var notif in notifs) ...[
                            ListTile(
                              leading: const Icon(Icons.notifications),
                              title: Text(
                                notif['titre'] ?? '',
                                style: TextStyle(
                                  fontWeight:
                                      notif['est_lue'] == false
                                          ? FontWeight.bold
                                          : FontWeight.normal,
                                  color:
                                      notif['est_lue'] == false
                                          ? Colors.blue
                                          : null,
                                ),
                              ),
                              subtitle: Text(
                                notif['description'] ?? '',
                                maxLines: 2,
                                overflow: TextOverflow.ellipsis,
                              ),
                              trailing: Text(
                                notif['date'] ?? '',
                                style: TextStyle(
                                  fontSize: 12,
                                  color: Colors.grey[600],
                                ),
                              ),
                              onTap: () {
                                // Navigue vers la page NotificationsPage à l'appui
                                Navigator.push(
                                  context,
                                  MaterialPageRoute(
                                    builder:
                                        (context) => NotificationsPage(
                                          idEmploye: widget.idEmploye,
                                        ),
                                  ),
                                );
                              },
                            ),
                            const Divider(),
                          ],
                        ],
                      ),
            ),
          ),
        ],
      ),
    );
  }
}
