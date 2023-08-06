import QtQuick 2.7
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.3
import org.kde.kirigami 2.5 as Kirigami

Kirigami.Page {
    title: qsTr("Welcome to MyGNUHeath")
    ColumnLayout {
        anchors.fill: parent
        Image {
            Layout.fillWidth: true
            Layout.fillHeight: true
            fillMode: Image.PreserveAspectFit
            source: "../images/my-gnu-health.png"
            MouseArea {
                anchors.fill: parent
                onClicked: pageStack.replace(Qt.resolvedUrl("PageLogin.qml"))
            }
        }

        Button {
            Layout.alignment: Qt.AlignHCenter
            text: qsTr("Start")
            onClicked: pageStack.replace(Qt.resolvedUrl("PageLogin.qml"))
        }
    }
}
