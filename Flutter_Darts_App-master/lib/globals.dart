library flutter_video_tutorial.globals;

import 'dart:io';

import 'package:path/path.dart';
import 'package:path_provider/path_provider.dart';

String player1 = "";
String player2 = "";

String player = "";
String winner = "";

int score = 501;
int player1Score = score;
int player2Score = score;
int round = 1;
File emptyDartboardImage = null;
String outputImagePath = null;
String ip = '192.168.1.';
