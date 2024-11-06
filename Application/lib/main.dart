import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:firebase_core/firebase_core.dart';
import 'firebase_options.dart';
import 'package:firebase_database/firebase_database.dart';
import 'package:flutter_mjpeg/flutter_mjpeg.dart';
import 'package:http/http.dart' as http;

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
      title: 'Silver Safe App',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: MyHomePage(),
    );
  }
}

class MyHomePage extends HookWidget {
  @override
  Widget build(BuildContext context) {
    final isRunning = useState(true);
    final logs = useState<List<String>>([]);
    final fallCount = useState<int>(0);
    final imageUrl = useState<String>('');
    final isImageInitialized = useState<bool>(false);

    final databaseRef = FirebaseDatabase.instance.ref();
    final imageStreamUrl = 'http://10.221.153.52:5001/video_feed'; // MJPEG 스트림 URL

    // Update logs function
    void _updateLog(String state) {
      final currentTime = TimeOfDay.now();
      final logEntry = '${currentTime.format(context)} - $state';

      logs.value = [...logs.value, logEntry];
      if (logs.value.length > 20) {
        logs.value.removeAt(0);
      }
    }

    useEffect(() {
      void _fetchImageUrl() async {
        try {
          final response = await http.get(Uri.parse('http://10.221.153.52:5002/'));
          if (response.statusCode == 200) {
            imageUrl.value = 'http://10.221.153.52:5002/video_feed';
            isImageInitialized.value = true;
          } else {
            print('Failed to load image URL: ${response.statusCode}');
          }
        } catch (e) {
          print('Error fetching image URL: $e');
        }
      }

      _fetchImageUrl();

      final listener = databaseRef.onValue.listen((event) {
        final snapshot = event.snapshot;

        if (snapshot.exists && snapshot.value is Map) {
          final data = snapshot.value as Map<dynamic, dynamic>;

          data.forEach((key, value) {
            if (value is bool) {
              if (key == 'fall') {
                if (value) {
                  fallCount.value++;
                  _updateLog('fall');
                }
              } else if (key == 'walking') {
                if (value) {
                  _updateLog('walking');
                }
              } else if (key == 'sitting') {
                if (value) {
                  _updateLog('sitting');
                }
              } else if (key == 'jump') {
                if (value) {
                  _updateLog('jump');
                }
              }
            }
          });
        }
      }, onError: (error) {
        print('Error receiving data: $error');
      });

      return () => listener.cancel();
    }, []);

    return Scaffold(
      appBar: AppBar(
        title: Text('Silver Safe'),
        centerTitle: true,
      ),
      body: Column(
        children: [
          Divider(
            color: Colors.grey,
            height: 1,
            thickness: 1,
          ),
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                // Left button
                Expanded(
                  child: Container(
                    width: 150,
                    height: 150,
                    color: Colors.amber,
                    child: Column(
                      children: [
                        Expanded(
                          child: SingleChildScrollView(
                            child: Column(
                              children: logs.value.map((log) => Text(log)).toList(),
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
                SizedBox(width: 16),

                // Right button
                Container(
                  width: 150,
                  height: 150,
                  color: Colors.amber,
                  child: Center(
                    child: Text(
                      '${fallCount.value}',
                      textAlign: TextAlign.center,
                      style: TextStyle(
                        color: Colors.black,
                        fontSize: 30,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                ),
              ],
            ),
          ),
          Divider(
            color: Colors.grey,
            height: 1,
            thickness: 3,
          ),
          Expanded(
            child: isImageInitialized.value
                ? Mjpeg(
              isLive: isRunning.value,
              error: (context, error, stack) {
                print(error);
                print(stack);
                return Text(error.toString(), style: TextStyle(color: Colors.red));
              },
              stream: imageUrl.value,
            )
                : Center(child: CircularProgressIndicator()),
          ),
        ],
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          isRunning.value = !isRunning.value;
        },
        child: Icon(isRunning.value ? Icons.pause : Icons.play_arrow),
      ),
    );
  }
}
