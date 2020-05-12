import 'dart:io';
import 'dart:ui';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import '../Alert.dart';
import 'TakePlayerShotPage.dart';
import '../globals.dart' as globals;
import '../rest_api.dart';

TextStyle _textStyle = TextStyle(fontSize: 20, color: Colors.white70);

Widget TakePictureScreen(BuildContext context) {
  return MaterialApp(
    home: MyHomePage(),
  );
}

class MyHomePage extends StatefulWidget {
  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  File _image;
  bool _isLoading = false;

  Future getImage() async {
    var image = await ImagePicker.pickImage(source: ImageSource.camera);
    globals.emptyDartboardImage = image;
    setState(() {
      _isLoading = true;
    });
    bool done = await ApiService.postEmptyDartBoard(image);
    setState(() {
      _isLoading = false;
    });
    if (done == false) {
      await showAlertDialog(context, "Error", "Please Try Again");
      _image = null;
      return;
    }
    print('DONE');
    print(done.toString());

    setState(() {
      _image = image;
    });
  }

  Future pickImage() async {
    var image = await ImagePicker.pickImage(source: ImageSource.gallery);
    globals.emptyDartboardImage = image;
    setState(() {
      _isLoading = true;
    });
    bool done = await ApiService.postEmptyDartBoard(image);
    setState(() {
      _isLoading = false;
    });
    print('DONE');
    print(done.toString());
    if (done == false) {
      await showAlertDialog(context, "Error", "Please Try Again");
      _image = null;
      return;
    }
    setState(() {
      _image = image;
    });
  }

  Widget _iconWidget() {
    return Expanded(
      flex: 2,
      child: _image == null
          ? Row(
              mainAxisAlignment: MainAxisAlignment.center,
              mainAxisSize: MainAxisSize.max,
              children: <Widget>[
                IconButton(
                  icon: Icon(
                    _image == null ? Icons.add_a_photo : Icons.done,
                    color: Colors.white70,
                  ),
                  onPressed: () {
                    getImage();
                  },
                  iconSize: 100,
                  alignment: Alignment.bottomCenter,
                ),
                IconButton(
                  icon: Icon(
                    _image == null ? Icons.photo : Icons.done,
                    color: Colors.white70,
                  ),
                  onPressed: () {
                    pickImage();
                  },
                  iconSize: 100,
                  alignment: Alignment.bottomCenter,
                ),
              ],
            )
          : IconButton(
              icon: Icon(
                Icons.done,
                color: Colors.white70,
              ),
              onPressed: null,
              iconSize: 100,
              alignment: Alignment.bottomCenter,
            ),
    );
  }

  Widget _buttonWidget() {
    return Opacity(
      opacity: _image == null ? 0.0 : 1.0,
      child: Container(
        margin: EdgeInsets.only(top: 20, bottom: 20),
        child: RaisedButton(
            padding:
                const EdgeInsets.only(right: 40, left: 40, top: 20, bottom: 20),
            color: Colors.transparent,
            child: Text(
              'NEXT',
              style: TextStyle(
                  fontSize: 20,
                  color: Colors.white70,
                  fontWeight: FontWeight.bold),
            ),
            shape: new RoundedRectangleBorder(
              borderRadius: new BorderRadius.circular(30.0),
              side: BorderSide(
                width: 2,
                color: Colors.white60,
              ),
            ),
            onPressed: _image == null
                ? null
                : () {
                    Navigator.of(context).pushReplacement(
                      MaterialPageRoute<void>(
                        builder: (BuildContext context) {
                          return TakePlayerShotScreen(context);
                        },
                      ),
                    );
                  }),
      ),
    );
  }

  Widget _textWidget() {
    return Container(
      margin: EdgeInsets.all(20),
      child: Text(
        _image == null
            ? 'Take Empty Dartboard Photo'
            : 'Image Taken Successfully',
        style: _textStyle,
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.only(top: 50),
      decoration: BoxDecoration(
          image: DecorationImage(
        image: AssetImage("assets/images/11.png"),
        fit: BoxFit.cover,
      )),
      child: Scaffold(
        backgroundColor: Colors.transparent,
        body: Column(
          children: <Widget>[
            Container(
              height: 60,
            ),
            _iconWidget(),
            _textWidget(),
            Opacity(
              opacity: _isLoading ? 1.0 : 0,
              child: CircularProgressIndicator(),
            ),
            Expanded(
                flex: 4,
                child: Container(
                  color: Colors.transparent,
                )),
            _buttonWidget(),
          ],
        ),
      ),
    );
  }
}
