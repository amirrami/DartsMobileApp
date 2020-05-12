import 'package:flutter/material.dart';
import '../Alert.dart';
import './CaptureScreen.dart';
import '../globals.dart' as globals;

Widget StartGamePage(BuildContext context) {
  final _biggerFont = const TextStyle(fontSize: 20.0, color: Colors.white70);

  Widget _inputText(String player) {
    String hint = '';
    if (player == "Score    : ") {
      hint = '501';
    } else {
      hint = 'Player Name';
    }
    return Container(
      margin: EdgeInsets.only(left: 10),
      child: TextField(
        style: TextStyle(color: Colors.white70, fontSize: 20),
        decoration: InputDecoration(
            hintStyle: TextStyle(fontSize: 20, color: Colors.white24),
            focusedBorder: UnderlineInputBorder(
              borderSide: BorderSide(color: Colors.white),
            ),
            hintText: hint),
        onChanged: (text) {
          if (player == "Player 1 : ") {
            globals.player1 = text;
            globals.player = globals.player1;
          } else if (player == "Player 2 : ") {
            globals.player2 = text;
          } else if (player == "Score    : ") {
            print("TRY PARSE = " + int.tryParse(text).toString());
            globals.score = int.tryParse(text);
            if (globals.score == null) {
              globals.score = 501;
            }
            print("SCORE = " + globals.score.toString());
            globals.player1Score = globals.score;
            globals.player2Score = globals.score;
          }
        },
      ),
    );
  }

  Widget _row(String player) {
    return Container(
        margin: EdgeInsets.only(
          left: 50.0,
          right: 50,
        ),
        child: Row(
          children: <Widget>[
            Text(
              player,
              style: _biggerFont,
            ),
            Expanded(
              child: _inputText(player),
            )
          ],
        ));
  }

  return Container(
    padding: const EdgeInsets.only(top: 20),
    decoration: BoxDecoration(
        image: DecorationImage(
            image: AssetImage("assets/images/11.png"), fit: BoxFit.cover)),
    child: Scaffold(
      backgroundColor: Colors.transparent,
      body: Center(
        child: Column(children: <Widget>[
          Container(
            color: Colors.transparent,
            height: 50,
          ),
          Expanded(
            flex: 1,
            child: _row("Player 1 : "),
          ),
          Expanded(
            flex: 1,
            child: _row("Player 2 : "),
          ),
          Expanded(
            flex: 1,
            child: _row("Score    : "),
          ),
          Container(
            margin: EdgeInsets.only(top: 20),
            child: RaisedButton(
                padding: const EdgeInsets.only(
                    right: 40, left: 40, top: 20, bottom: 20),
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
                onPressed: () {
                  print(globals.player1 +
                      " " +
                      globals.player2 +
                      " " +
                      globals.score.toString());
                  if (globals.player1 == '' || globals.player1 == null) {
                    showAlertDialog(
                        context, "Player1 Name !", "Please Enter Player1 Name");
                    return;
                  } else if (globals.player2 == '' || globals.player2 == null) {
                    showAlertDialog(
                        context, "Player2 Name !", "Please Enter Player2 Name");
                    return;
                  } else if (globals.score == null) {
                    //SHOW ALERT
                    showAlertDialog(context, "Score !", "Please Enter Score");
                    return;
                  }
                  Navigator.of(context).push(
                    MaterialPageRoute<void>(
                      builder: (BuildContext context) {
                        return TakePictureScreen(context);
                      },
                    ),
                  );
                }),
          ),
          Expanded(
            flex: 4,
            child: Container(),
          ),
        ]),
      ),
    ),
  );
}
