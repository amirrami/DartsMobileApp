import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import '../globals.dart' as globals;
import 'StartGamePage.dart';

Widget FinishGameScreen(BuildContext context) {
  return Container(
      padding: const EdgeInsets.only(top: 20),
      decoration: BoxDecoration(
          color: Colors.white,
          image: DecorationImage(
              image: AssetImage("assets/images/source.gif"),
              fit: BoxFit.fitWidth)),
      child: Scaffold(
          backgroundColor: Colors.transparent,
          appBar: AppBar(
            centerTitle: true,
            title: Text(
              'The Winner is : ' + globals.player,
              style: TextStyle(fontSize: 30, color: Colors.black),
            ),
            backgroundColor: Colors.white,
          ),
          body: Container(
            margin: EdgeInsets.only(bottom: 50),
            child: Align(
              alignment: FractionalOffset.bottomCenter,
              child: RaisedButton(
                  padding: const EdgeInsets.only(
                      right: 40, left: 40, top: 20, bottom: 20),
                  color: Colors.white,
                  child: Text(
                    'START NEW GAME',
                    style: TextStyle(
                        fontSize: 20,
                        color: Colors.black,
                        fontWeight: FontWeight.bold),
                  ),
                  shape: new RoundedRectangleBorder(
                    borderRadius: new BorderRadius.circular(30.0),
                    side: BorderSide(
                      width: 2,
                      color: Colors.black,
                    ),
                  ),
                  onPressed: () {
                    globals.emptyDartboardImage = null;
                    globals.player1 = "";
                    globals.player2 = "";
                    globals.score = 501;
                    globals.player1Score = globals.score;
                    globals.player2Score = globals.score;
                    globals.round = 1;
                    Navigator.of(context).pushReplacement(
                      MaterialPageRoute<void>(
                        builder: (BuildContext context) {
                          return StartGamePage(context);
                        },
                      ),
                    );
                  }),
            ),
          )));
}
