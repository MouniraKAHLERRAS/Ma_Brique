import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'config.dart';

class NotificationsPage extends StatefulWidget {
  final int idEmploye;
  const NotificationsPage({super.key, required this.idEmploye});

  @override
  State<NotificationsPage> createState() => _NotificationsPageState();
}

class _NotificationsPageState extends State<NotificationsPage> {
  List notifications = [];
  bool isLoading = true;

  @override
  void initState() {
    super.initState();
    fetchNotifications();
  }

  Future<void> fetchNotifications() async {
    setState(() => isLoading = true);
    final url = getUri('/notifications/${widget.idEmploye}');
    final res = await http.get(url);
    if (res.statusCode == 200) {
      setState(() {
        notifications = json.decode(res.body);
        isLoading = false;
      });
    } else {
      setState(() {
        notifications = [];
        isLoading = false;
      });
    }
  }

  Future<void> markAsRead(int idNotif) async {
    await http.post(getUri('/notifications/lire/$idNotif'));
    fetchNotifications();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Notifications'),
        backgroundColor: Colors.blue[700],
      ),
      body:
          isLoading
              ? const Center(child: CircularProgressIndicator())
              : notifications.isEmpty
              ? const Center(child: Text("Aucune notification."))
              : ListView.builder(
                itemCount: notifications.length,
                itemBuilder: (context, i) {
                  final notif = notifications[i];
                  return Card(
                    color: notif["est_lue"] ? Colors.white : Colors.blue[50],
                    elevation: notif["est_lue"] ? 1 : 3,
                    child: ListTile(
                      leading:
                          notif["est_lue"]
                              ? const Icon(Icons.notifications)
                              : const Icon(
                                Icons.notifications_active,
                                color: Colors.blue,
                              ),
                      title: Text(
                        notif["titre"] ?? "Notification",
                        style: TextStyle(
                          fontWeight:
                              notif["est_lue"]
                                  ? FontWeight.normal
                                  : FontWeight.bold,
                        ),
                      ),
                      subtitle: Text(
                        "${notif["description"] ?? ""}\n${notif["date"] ?? ""}",
                      ),
                      isThreeLine: true,
                      trailing:
                          notif["document"] != null && notif["document"] != ""
                              ? IconButton(
                                icon: const Icon(Icons.attachment),
                                onPressed: () {
                                  // Ici tu pourrais ouvrir le document avec url_launcher ou autre
                                  ScaffoldMessenger.of(context).showSnackBar(
                                    SnackBar(
                                      content: Text(
                                        'Ouverture du document pas encore implémentée',
                                      ),
                                    ),
                                  );
                                },
                              )
                              : null,
                      onTap: () {
                        if (!notif["est_lue"]) {
                          markAsRead(notif["id_notification"]);
                        }
                      },
                    ),
                  );
                },
              ),
    );
  }
}
