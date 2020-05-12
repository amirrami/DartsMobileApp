import 'package:flutter/material.dart';
import './StartGamePage.dart';

class HomeScreen extends StatelessWidget {
  @override
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
        body: Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            RaisedButton(
                padding: const EdgeInsets.only(
                    right: 40, left: 40, top: 20, bottom: 20),
                color: Colors.transparent,
                child: Text(
                  'START GAME',
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
                  Navigator.of(context).pushReplacement(
                    MaterialPageRoute<void>(
                      // Add 20 lines from here...
                      builder: (BuildContext context) {
                        return StartGamePage(context);
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
