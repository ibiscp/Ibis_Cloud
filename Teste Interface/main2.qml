import QtQuick 1.0

Rectangle {
    width: 200
    height: 200
    color: "red"
    color.border: "black"

    Text {
        text: "Hello World"
        anchors.centerIn: parent
    }

    TextEdit {
        id: textEdit1
        x: 67
        y: 59
        width: 80
        height: 20
        text: qsTr("Text Edit")
        font.pixelSize: 12
    }


}
