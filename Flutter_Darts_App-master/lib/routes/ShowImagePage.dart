import 'dart:io';

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:path/path.dart';
import 'package:path_provider/path_provider.dart';

import '../globals.dart' as globals;

Widget ShowImagePage(BuildContext context, _image) {
  void goBack() {
    Navigator.of(context).pop();
  }

  Future<String> getFile() async {
    return join(
      // Store the picture in the temp directory.
      // Find the temp directory using the `path_provider` plugin.
      (await getTemporaryDirectory()).path,
      'outputImage.jpg',
    );
  }

  return MaterialApp(
    theme: ThemeData.dark(),
    home: Scaffold(
      body: Center(
        child: Image.file(File(globals.outputImagePath)),
      ),
      floatingActionButton:
          FloatingActionButton(child: Icon(Icons.backspace), onPressed: goBack),
      floatingActionButtonLocation: FloatingActionButtonLocation.endFloat,
    ),
  );
}
