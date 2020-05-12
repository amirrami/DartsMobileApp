import 'package:flutter/material.dart';
import 'package:flutter_video_tutorial/routes/PreHomePage.dart';
import './routes/HomeScreen.dart';

main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(title: 'Welcome to Flutter', home: new PreHomeScreen());
  }
}
