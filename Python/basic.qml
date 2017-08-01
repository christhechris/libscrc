import QtQuick 2.0
import QtQuick.Controls 1.0
import QtQuick.Window 2.0

Rectangle {
    id:root
    width: 1230; height: 768
    color: "lightgray"

    GroupBox {
        id: groupBoxConfigure
        x: 19
        y: 15
        width: 1203
        height: 61
        title: qsTr("Configure")

        Text {
            id: text1
            x: 0; y: 11
            width: 94; height: 16
            text: qsTr("Host IP Address")
            font.pixelSize: 18
        }

        Text {
            id: text2
            x: 268
            y: 11
            width: 94
            height: 16
            text: qsTr("PassWord")
            font.pixelSize: 18
        }

        TextField {
            id: textFieldHostIP
            x: 127
            y: 10
            text: "https://10.194.152.11"
            placeholderText: qsTr("Text Field")
        }

        TextField {
            id: textFieldPwd
            x: 352
            y: 10
            text: "admin"
            echoMode: 2
            placeholderText: qsTr("Text Field")
        }

        Button {
            id: buttonLogin
            x: 922
            y: 6
            width: 75
            height: 31
            text: qsTr("Login")
            onClicked: {
                buttonStart.enabled = conn.login(textFieldHostIP.text, textFieldPwd.text)
            }

        }

        Button {
            id: buttonStart
            x: 1017
            y: 6
            width: 75
            height: 31
            text: qsTr("Start(&S)")
            enabled: false
            onClicked: {
                textAreaResult.text = conn.start()
            }
        }

        Button {
            id: buttonExit
            x: 1105
            y: 6
            width: 75
            height: 31
            text: qsTr("Exit(&Q)")
            onClicked: {
                conn.exit()
            }
        }

        Text {
            id: text3
            x: 510
            y: 12
            width: 94
            height: 16
            text: qsTr("New Itmes")
            font.pixelSize: 18
        }

        ComboBox {
            id: comboBox
            x: 606
            y: 6
            width: 125
            height: 31
            model: [ "5","10","20","30","40","50"]
            currentIndex:2
            onCurrentIndexChanged:{
                conn.comboBox(currentText)
            }
        }


    }

    GroupBox {
        id: groupBoxResult
        x: 19
        y: 91
        width: 1203
        height: 655
        title: qsTr("Result")

        TextArea {
            id: textAreaResult
            x: 0
            y: 1
            width: 1182
            height: 631
            text: ""
            font.weight: Font.Normal
            font.pixelSize: 8
            font.family: "Courier"
            readOnly: true
        }


    }

}
