import 'dart:async';
import 'package:best_flutter_ui_templates/fitness_app_theme.dart';
import 'package:flutter/material.dart';
import 'package:firebase_database/firebase_database.dart';

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

  @override
  void initState() {
    super.initState();
    databaseRef = FirebaseDatabase.instance.ref();
    _initializeListener();
  }

  @override
  void dispose() {
    _databaseSubscription.cancel();
    super.dispose();
  }

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
          }
        }
      }
    }, onError: (error) {
      print('Error receiving data: $error');
    });
  }

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
