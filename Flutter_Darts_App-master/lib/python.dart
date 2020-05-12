import 'dart:io';
import './rest_api.dart';

getScore(File image) async {
  //score should use the python function
  int score = await ApiService.getScore(image);
  return score;
}
