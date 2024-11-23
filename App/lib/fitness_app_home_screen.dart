import 'package:best_flutter_ui_templates/models/tabIcon_data.dart';
import 'package:best_flutter_ui_templates/training/training_screen.dart';
import 'package:flutter/material.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart';
import 'bottom_navigation_view/bottom_bar_view.dart';
import 'fitness_app_theme.dart';
import 'my_diary/my_diary_screen.dart';
import 'information/information_screen.dart';
import 'ui_view/body_measurement.dart';
import 'package:firebase_core/firebase_core.dart';
import 'firebase_options.dart';
import 'package:firebase_database/firebase_database.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primarySwatch: Colors.blue,
        textTheme: FitnessAppTheme.textTheme,
        platform: TargetPlatform.iOS,
      ),
      home: FitnessAppHomeScreen(),
    );
  }
}

class FitnessAppHomeScreen extends StatefulWidget {
  @override
  _FitnessAppHomeScreenState createState() => _FitnessAppHomeScreenState();
}

class _FitnessAppHomeScreenState extends State<FitnessAppHomeScreen>
    with TickerProviderStateMixin {
  AnimationController? animationController;
  late FlutterLocalNotificationsPlugin localNotifications;
  List<TabIconData> tabIconsList = TabIconData.tabIconsList;
  Widget tabBody = Container(
    color: FitnessAppTheme.background,
  );

  @override
  void initState() {
    super.initState();
    tabIconsList.forEach((TabIconData tab) {
      tab.isSelected = false;
    });
    tabIconsList[0].isSelected = true;

    animationController = AnimationController(
        duration: const Duration(milliseconds: 600), vsync: this);
    tabBody = MyDiaryScreen(animationController: animationController);

    _initializeNotifications(); // Local notifications 초기화
    _subscribeToFirebaseDatabase(); // Firebase 데이터베이스 구독
  }

  @override
  void dispose() {
    animationController?.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      color: FitnessAppTheme.background,
      child: Scaffold(
        backgroundColor: Colors.transparent,
        body: FutureBuilder<bool>(
          future: getData(),
          builder: (BuildContext context, AsyncSnapshot<bool> snapshot) {
            if (!snapshot.hasData) {
              return const SizedBox();
            } else {
              return Stack(
                children: <Widget>[
                  tabBody,
                  bottomBar(),
                ],
              );
            }
          },
        ),
      ),
    );
  }

  Future<bool> getData() async {
    await Future<dynamic>.delayed(const Duration(milliseconds: 200));
    return true;
  }

  Widget bottomBar() {
    return Column(
      children: <Widget>[
        const Expanded(
          child: SizedBox(),
        ),
        BottomBarView(
          tabIconsList: tabIconsList,
          addClick: () {},
          changeIndex: (int index) {
            if (index == 0) {
              animationController?.reverse().then<dynamic>((data) {
                if (!mounted) {
                  return;
                }
                setState(() {
                  tabBody =
                      MyDiaryScreen(animationController: animationController);
                });
              });
            } else if (index == 3) { // 개인정보
              animationController?.reverse().then<dynamic>((data) {
                if (!mounted) {
                  return;
                }
                setState(() {
                  tabBody =
                      InformationScreen(animationController: animationController);
                });
              });
            }
          },
        ),
      ],
    );
  }

  // Local notifications 초기화
  void _initializeNotifications() {
    localNotifications = FlutterLocalNotificationsPlugin();

    const androidSettings = AndroidInitializationSettings('@mipmap/ic_launcher');
    const initializationSettings = InitializationSettings(
      android: androidSettings,
    );

    localNotifications.initialize(initializationSettings);
  }

  // Firebase 데이터베이스에서 danger 값을 구독
  void _subscribeToFirebaseDatabase() {
    final databaseReference = FirebaseDatabase.instance.ref('danger');

    databaseReference.onValue.listen((event) {
      final dangerValue = event.snapshot.value as bool?;

      if (dangerValue == true) {
        _showNotification(); // danger 값이 true일 때 알림 표시
      }
    });
  }

  // 푸쉬 알림 표시
  Future<void> _showNotification() async {
    const androidDetails = AndroidNotificationDetails(
      'danger_channel', // 채널 ID
      'Danger Notifications', // 채널 이름
      channelDescription: 'Notifications for danger alerts',
      importance: Importance.high,
      priority: Priority.high,
    );

    const notificationDetails = NotificationDetails(
      android: androidDetails,
    );

    await localNotifications.show(
      0, // 알림 ID
      'Danger Alert', // 알림 제목
      'Danger Detected! Please Check', // 알림 내용
      notificationDetails,
    );
  }
}