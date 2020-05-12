import 'package:flutter/material.dart';
import './HomeScreen.dart';
import '../globals.dart' as globals;

class PreHomeScreen extends StatelessWidget {
  @override
  String ip = '192.168.1.';
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.only(top: 100),
      decoration: BoxDecoration(
          image: DecorationImage(
              image: AssetImage("assets/images/11.png"), fit: BoxFit.cover)),
      child: Scaffold(
        backgroundColor: Colors.transparent,
        appBar: AppBar(
          elevation: 0,
          backgroundColor: Colors.transparent,
          centerTitle: true,
        ),
        body: Column(
          children: <Widget>[
            Container(
              margin: EdgeInsets.all(50),
              child: TextField(
                style: TextStyle(color: Colors.white70, fontSize: 20),
                controller: TextEditingController()..text = ip,
                decoration: InputDecoration(
                    hintStyle: TextStyle(fontSize: 20, color: Colors.white24),
                    enabledBorder: OutlineInputBorder(
                      borderSide: BorderSide(color: Colors.white),
                    ),
                    disabledBorder: OutlineInputBorder(
                      borderSide: BorderSide(color: Colors.white),
                    ),
                    focusedBorder: OutlineInputBorder(
                      borderSide: BorderSide(color: Colors.white),
                    ),
                    hintText: 'IP'),
                onChanged: (text) {
                  ip = text;
                },
              ),
            ),
            RaisedButton(
                padding: const EdgeInsets.only(
                    right: 40, left: 40, top: 20, bottom: 20),
                color: Colors.transparent,
                child: Text(
                  'START',
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
                onPressed: () {
                  globals.ip = ip;
                  Navigator.of(context).pushReplacement(
                    MaterialPageRoute<void>(
                      builder: (BuildContext context) {
                        return HomeScreen();
                      },
                    ),
                  );
                }),
          ],
        ),
      ),
    );
  }
}
