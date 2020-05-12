import 'package:flutter/material.dart';

showAlertDialog(BuildContext context, String title, String message) {
  // set up the button
  Widget okButton = FlatButton(
    child: Text("OK"),
    onPressed: () {
      Navigator.of(context, rootNavigator: true).pop(false);
    },
  );

  // set up the AlertDialog
  AlertDialog alert = AlertDialog(
    title: Text(title),
    content: Text(message),
    backgroundColor: Colors.white,
    shape: RoundedRectangleBorder(borderRadius: new BorderRadius.circular(15)),
    actions: [
      okButton,
    ],
  );

  showAlert(BuildContext context, String title, String message) {}

  // show the dialog
  showDialog(
    context: context,
    builder: (BuildContext context) {
      return alert;
    },
  );
}
