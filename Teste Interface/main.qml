import QtQuick 1.0

Rectangle {
    width: 800
    height: column.height
    color: "white"
    border.color: "black"
    border.width: 2

    Column{
        id: column
        Image{
            id: home_button
            source: mouse_home.containsMouse ? "Images/Home_S.png" :"Images/Home.png"
            smooth: true
            MouseArea{
                id: mouse_home
                anchors.fill: parent
                hoverEnabled: true

            }
        }

        Image{
            id: mapping_button
            source: mouse_mapping.containsMouse ? "Images/Mapping_S.png" : "Images/Mapping.png"
            smooth: true
            MouseArea{
                id: mouse_mapping
                anchors.fill: parent
                hoverEnabled: true
                onClicked: mapping.visible = true
            }
        }

        Image{
            id: statistics_button
            source: mouse_statistics.containsMouse ? "Images/Statistics_S.png" : "Images/Statistics.png"
            smooth: true
            MouseArea{
                id: mouse_statistics
                anchors.fill: parent
                hoverEnabled: true

            }
        }

        Image{
            id: settings_button
            source: mouse_settings.containsMouse ? "Images/Settings_S.png" : "Images/Settings.png"
            smooth: true
            MouseArea{
                id: mouse_settings
                anchors.fill: parent
                hoverEnabled: true

            }
        }

        Image{
            id: about_button
            source: mouse_about.containsMouse ? "Images/About_S.png" : "Images/About.png"
            smooth: true
            MouseArea{
                id: mouse_about
                anchors.fill: parent
                hoverEnabled: true

            }
        }
    }

    Grid {
        id: mapping
        x: 176
        y: 0
        width: 624
        height: 425
        visible: false

        Rectangle{
            id: source_rect
            x: 100
            y: 100
            height: 20
            width: parent.width-100
            radius: 5
            border.color: "black"
            border.width: 2
            smooth: true

            TextEdit {
                property int margin: 3
                id: source
                x: margin
                y: margin
                height: parent.height-margin
                width: source_rect.width-margin
                text: qsTr("Text Edit")
                font.pixelSize: 12
            }
        }


    }


}
