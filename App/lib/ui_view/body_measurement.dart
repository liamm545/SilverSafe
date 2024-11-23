import 'dart:async';
import 'package:best_flutter_ui_templates/fitness_app_theme.dart';
import 'package:flutter/material.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart';
import 'package:firebase_database/firebase_database.dart';
import 'package:permission_handler/permission_handler.dart';

class BodyMeasurementView extends StatefulWidget {
  final AnimationController? animationController;
  final Animation<double>? animation;

  const BodyMeasurementView({Key? key, this.animationController, this.animation})
      : super(key: key);

  @override
  _BodyMeasurementViewState createState() => _BodyMeasurementViewState();
}

class _BodyMeasurementViewState extends State<BodyMeasurementView> with TickerProviderStateMixin {
  final List<String> logs = [];
  late DatabaseReference databaseRef;
  late StreamSubscription<DatabaseEvent> _databaseSubscription;
  late FlutterLocalNotificationsPlugin localNotifications;

  @override
  void initState() {
    super.initState();
    databaseRef = FirebaseDatabase.instance.ref();
    _initializeNotifications(); // Initialize notifications
    _initializeListener(); // Firebase listener
    Future.delayed(const Duration(seconds: 3), requestNotificationPermission); // 요청 알림 권한
  }

  @override
  void dispose() {
    _databaseSubscription.cancel();
    super.dispose();
  }

  /// 요청 알림 권한
  void requestNotificationPermission() async {
    if (await Permission.notification.isDenied) {
      await Permission.notification.request();
    }
  }

  /// 알림 초기화 및 채널 설정
  void _initializeNotifications() {
    localNotifications = FlutterLocalNotificationsPlugin();

    const androidSettings = AndroidInitializationSettings('@mipmap/ic_launcher');
    const iosSettings = DarwinInitializationSettings(
      requestAlertPermission: false,
      requestBadgePermission: false,
      requestSoundPermission: false,
    );

    const initializationSettings = InitializationSettings(
      android: androidSettings,
      iOS: iosSettings,
    );

    localNotifications.initialize(initializationSettings);

    const AndroidNotificationChannel channel = AndroidNotificationChannel(
      'danger_channel', // Channel ID
      'Danger Notifications', // Channel name
      description: 'This channel is used for danger alerts', // Channel description
      importance: Importance.high,
    );

    localNotifications
        .resolvePlatformSpecificImplementation<
        AndroidFlutterLocalNotificationsPlugin>()
        ?.createNotificationChannel(channel);
  }

  /// Firebase Realtime Database listener
  void _initializeListener() {
    _databaseSubscription = databaseRef.onChildChanged.listen((event) {
      final snapshot = event.snapshot;
      if (snapshot.exists && snapshot.value is bool) {
        final key = snapshot.key;
        final value = snapshot.value as bool;

        if (value) {
          if (key == 'walking') {
            _updateLog('walking');
          } else if (key == 'sitting') {
            _updateLog('sitting');
          } else if (key == 'jump') {
            _updateLog('jump');
          } else if (key == 'fall') {
            _updateLog('fall');
          } else if (key == 'standing') {
            _updateLog('standing');
          } else if (key == 'danger') {
            _updateLog('Danger detected!');
            // _showNotification(); // Show push notification
          }
        }
      }
    }, onError: (error) {
      print('Error receiving data: $error');
    });
  }

  /// 로그 업데이트
  void _updateLog(String state) {
    final currentTime = TimeOfDay.now();
    final logEntry = '${currentTime.format(context)} - $state';

    setState(() {
      logs.add(logEntry);
      if (logs.length > 20) {
        logs.removeAt(0);
      }
    });
  }

  /// 푸쉬 알림 표시
  Future<void> _showNotification() async {
    const androidDetails = AndroidNotificationDetails(
      'danger_channel', // Channel ID
      'Danger Notifications', // Channel Name
      channelDescription: 'Notifications for danger alerts',
      importance: Importance.high,
      priority: Priority.high,
    );

    const iosDetails = DarwinNotificationDetails(
      badgeNumber: 1,
    );

    const notificationDetails = NotificationDetails(
      android: androidDetails,
      iOS: iosDetails,
    );

    await localNotifications.show(
      0, // Notification ID
      'Danger Alert', // Notification Title
      'A dangerous situation has been detected.', // Notification Body
      notificationDetails,
    );
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: widget.animationController ?? AnimationController(vsync: this),
      builder: (BuildContext context, Widget? child) {
        return widget.animation == null
            ? SizedBox.shrink()
            : FadeTransition(
          opacity: widget.animation!,
          child: Transform(
            transform: Matrix4.translationValues(
                0.0, 30 * (1.0 - widget.animation!.value), 0.0),
            child: Padding(
              padding: const EdgeInsets.only(
                  left: 24, right: 24, top: 16, bottom: 18),
              child: Container(
                decoration: BoxDecoration(
                  color: Colors.white, // Use your theme color
                  borderRadius: BorderRadius.only(
                      topLeft: Radius.circular(8.0),
                      bottomLeft: Radius.circular(8.0),
                      bottomRight: Radius.circular(8.0),
                      topRight: Radius.circular(68.0)),
                  boxShadow: <BoxShadow>[
                    BoxShadow(
                        color: FitnessAppTheme.grey.withOpacity(0.2),
                        offset: Offset(1.1, 1.1),
                        blurRadius: 10.0),
                  ],
                ),
                child: Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Container(
                    height: 200, // Set a fixed height for the scrollable area
                    child: SingleChildScrollView(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: logs.map((log) => Text(log)).toList(),
                      ),
                    ),
                  ),
                ),
              ),
            ),
          ),
        );
      },
    );
  }
}