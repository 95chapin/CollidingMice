/****************************************************************************
**
** Copyright (C) 2016 The Qt Company Ltd.
** Contact: https://www.qt.io/licensing/
**
** This file is part of the examples of the Qt Toolkit.
**
** $QT_BEGIN_LICENSE:BSD$
** Commercial License Usage
** Licensees holding valid commercial Qt licenses may use this file in
** accordance with the commercial license agreement provided with the
** Software or, alternatively, in accordance with the terms contained in
** a written agreement between you and The Qt Company. For licensing terms
** and conditions see https://www.qt.io/terms-conditions. For further
** information use the contact form at https://www.qt.io/contact-us.
**
** BSD License Usage
** Alternatively, you may use this file under the terms of the BSD license
** as follows:
**
** "Redistribution and use in source and binary forms, with or without
** modification, are permitted provided that the following conditions are
** met:
**   * Redistributions of source code must retain the above copyright
**     notice, this list of conditions and the following disclaimer.
**   * Redistributions in binary form must reproduce the above copyright
**     notice, this list of conditions and the following disclaimer in
**     the documentation and/or other materials provided with the
**     distribution.
**   * Neither the name of The Qt Company Ltd nor the names of its
**     contributors may be used to endorse or promote products derived
**     from this software without specific prior written permission.
**
**
** THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
** "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
** LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
** A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
** OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
** SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
** LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
** DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
** THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
** (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
** OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
**
** $QT_END_LICENSE$
**
****************************************************************************/

#include "aimouse.h"

#include <QGraphicsScene>
#include <QPainter>
#include <QRandomGenerator>
#include <QStyleOption>
#include <qmath.h>

#include <iostream>
using namespace std;

// basic file operations
//#include <iostream>
#include <fstream>
using namespace std;

// Reading a text file
#include <iostream>
//#include <fstream>
#include <string>
//using namespace std;

// For danger mice
#include <QGraphicsItem>
#include "mouse.h"

const qreal Pi = M_PI;
const qreal TwoPi = 2 * M_PI;

static qreal normalizeAngle(qreal angle)
{
    while (angle < 0)
        angle += TwoPi;
    while (angle > TwoPi)
        angle -= TwoPi;
    return angle;
}

//! [0]
AiMouse::AiMouse(const int numMice, const qreal tolerance, QGraphicsEllipseItem *goalPtr)
    : angle(0),
      speed(0),
      mouseEyeDirection(0),
      color(0, 0, 0),
      aiNumMice(numMice),
      goalTolerance(tolerance)

{
    AiAngleToMouse.clear();
    AiAngleToMouse.reserve(numMice);
    AiDistToMouse.clear();
    AiDistToMouse.reserve(numMice);
    collisionOccured = false;
    setRotation(0);
    done = false;       // If the round ends then this gets set to true (a collision occured or the AiMouse got to its destination)
    reward = 0.0;
    goalPtrAi = goalPtr;
//    QGraphicsEllipseItem(addEllipse(QRectF(goalX, goalY, goalTolerance*2, goalTolerance*2), QPen(Qt::black))) goal;
//    scene()->addEllipse(QRectF(goalX, goalY, goalTolerance*2, goalTolerance*2), QPen(Qt::black));
}

void AiMouse::initDangerMice(int numMice, QGraphicsScene *scene){
    std::uniform_int_distribution <int> dist(-300,300);
    for (int i = 0; i < numMice; ++i) {
        Mouse *mouse = new Mouse;
        dangerMice[i] = mouse;
        dangerMice[i]->setPos(dist(*QRandomGenerator::global()),
                              dist(*QRandomGenerator::global()));
        scene->addItem(mouse);
    } // end for (int i = 0; i < numMice
}

void AiMouse::reSetDangerMice(int numMice){
    for (int i = 0; i < numMice; ++i) {
        std::uniform_int_distribution <int> dist(-300,300);
        dangerMice[i]->setPos(dist(*QRandomGenerator::global()),
                              dist(*QRandomGenerator::global()));

        done = false;       // Reset to false to start a new round
    } // end for (int i = 0; i < numMice
}

void AiMouse::reSetAiMouse(int numMice){
    angle = 0;
    speed = 0;
    mouseEyeDirection = 0;
    aiNumMice = numMice;
    AiAngleToMouse.clear();
    AiAngleToMouse.reserve(numMice);
    AiDistToMouse.clear();
    AiDistToMouse.reserve(numMice);
    collisionOccured = false;
    setRotation(0);
    done = false;       // If the round ends then this gets set to true (a collision occured or the AiMouse got to its destination)
    reward = 0.0;
}

qreal AiMouse::updateSpeed(){
    return (-50 + QRandomGenerator::global()->bounded(100)) / 100.0;
}

// int index is temporary
qreal AiMouse::updateAngle(int index){
    qreal angleToMouse = AiAngleToMouse.at(index);
    qreal offset = 0;
    if (angleToMouse >= 0 && angleToMouse < Pi / 2) { // If in quadrant 1
        // Rotate right
        offset = 0.5;
    } else if (angleToMouse <= TwoPi && angleToMouse > (TwoPi - Pi / 2)) { // If in quadrant 4
        // Rotate left
        offset = -0.5;
    }

    return offset;

}
//! [0]

//! [1]
QRectF AiMouse::boundingRect() const
{
    qreal adjust = 0.5;
    return QRectF(-18 - adjust, -22 - adjust,
                  36 + adjust, 60 + adjust);
}
//! [1]

//! [2]
QPainterPath AiMouse::shape() const
{
    QPainterPath path;
    path.addRect(-10, -20, 20, 40);
    return path;
}
//! [2]

//! [3]
void AiMouse::paint(QPainter *painter, const QStyleOptionGraphicsItem *, QWidget *)
{
    // Body
    painter->setBrush(color);
    painter->drawEllipse(-10, -20, 20, 40);

    // Eyes
    painter->setBrush(Qt::white);
    painter->drawEllipse(-10, -17, 8, 8);
    painter->drawEllipse(2, -17, 8, 8);

    // Nose
    painter->setBrush(Qt::black);
    painter->drawEllipse(QRectF(-2, -22, 4, 4));

    // Pupils
    painter->drawEllipse(QRectF(-8.0 + mouseEyeDirection, -17, 4, 4));
    painter->drawEllipse(QRectF(4.0 + mouseEyeDirection, -17, 4, 4));

    // Ears
    painter->setBrush(scene()->collidingItems(this).isEmpty() ? Qt::darkYellow : Qt::red);
    painter->drawEllipse(-17, -12, 16, 16);
    painter->drawEllipse(1, -12, 16, 16);

    // Tail
    QPainterPath path(QPointF(0, 20));
    path.cubicTo(-5, 22, -5, 22, 0, 25);
    path.cubicTo(5, 27, 5, 32, 0, 30);
    path.cubicTo(-5, 32, -5, 42, 0, 35);
    painter->setBrush(Qt::NoBrush);
    painter->drawPath(path);
}
//! [3]

//! [4]
void AiMouse::advance(int step)
{
    if (!step)
        return;

    // **************************   Update scene from NN decision    **************************

    // Read in pyout file for inputs // Read pyout
    string line;
    ifstream myfile ("C:/Users/willi/Downloads/CalPoly/Spring_20/EE_509/Final_Project/dirwatch/py/pyout.txt");
    int dataFromPy[2];
    if(myfile.is_open())
    {
        int i = 0;
        while(myfile >> line){
            if(line == "restart"){
//                scene()->clear();
                reSetDangerMice(aiNumMice);
                reSetAiMouse(aiNumMice);

                if (goalPtrAi != nullptr){
                    std::uniform_int_distribution <int> dist(-250,250);
                    AiMouse::setPos(0,0);
                    goalX = dist(*QRandomGenerator::global());
                    goalY = dist(*QRandomGenerator::global());
                    scene()->removeItem(goalPtrAi);
                    QGraphicsEllipseItem *goalPtr = new QGraphicsEllipseItem(QRectF(goalX-goalTolerance, goalY-goalTolerance, goalTolerance*2, goalTolerance*2));
                    goalPtrAi = goalPtr;
                    scene()->addItem(goalPtrAi);
//                    scene()->goalPtrAi->setPos(goalX-goalTolerance,goalY-goalTolerance);
                }

            } else if (line == "end"){
                return;
            } else {
                dataFromPy[i] = std::stoi(line);
                i = i + 1;
            } // end if(line == "restart") if else else
        }// end while(myfile >> line)
    }// end if(myfile.is_open())

    angle += normalizeAngle(qreal(dataFromPy[0])*(3.14/180.0));
    speed = 0.8; //dataFromPy[1];

    qreal dx = ::sin(angle) * 10;   // Replace this with return of NN
    mouseEyeDirection = (qAbs(dx / 5) < 1) ? 0 : dx / 5;


    setRotation(rotation() + dx);
    setPos(mapToParent(0, -(3 + sin(speed) * 3)));
    collisionOccured = ! scene()->collidingItems(this).isEmpty(); // Update if a collision occured based on the mouse movement

    //cout << collisionOccured << "\n";
    prevDistToGoal = distToGoal;    // Set the previous distance to determine if the AiMouse got closer or further to the goal

    QLineF lineToGoalPos(QPointF(0, 0), mapFromScene(goalX, goalY)); // 300, 300 bottom right corner // 0 0 center
    distToGoal = lineToGoalPos.length();    // Update the distance the mouse is from the goal position
    qreal angleToCenter = std::atan2(lineToGoalPos.dy(), lineToGoalPos.dx());
    angleToGoal = normalizeAngle((Pi - angleToCenter) + Pi / 2);



    // *********** Calculate the reward based on the previous decision ***********
    // If a collision occured or the AiMouse got to its destination, then end the round
    reward = 0.0;
    if(collisionOccured){
        reward = -1.0;  // Set the punishment
        if(distToGoal <= goalTolerance+50){
           reward = 10.0;
        }
        done = true;    // End the round
    } else if(distToGoal <= goalTolerance+50) {
        reward = 10.0;    // Set the reward
        done = true;    // End the round
    }else if (distToGoal > 800){
        reward = -1.0;     // Reset the reward
        done = true;        // End the round
    }else{
        reward = 0.0;     // Reset the reward
        done = false;

        // Calculate the reward from the previous decision
        if((prevDistToGoal - distToGoal) > 0){
            reward += 0.02;
        }else if((prevDistToGoal - distToGoal) < 0){
            reward -= 0.05;
        }
    }
    // **************************    End update scene from NN decision    **************************



//! [4]
    // Go towards goal location
//! [5]

//! [5] //! [6]
//! [6]

    // Try not to crash with any other mice
//! [7]
//!

    const QList<QGraphicsItem *> dangerMice = scene()->items(QPolygonF()
                                                       << mapToScene(0, 0)
                                                       << mapToScene(-100, -100)
                                                       << mapToScene(100, -100));
    AiAngleToMouse.clear();             // Clear the old angles
    AiAngleToMouse.reserve(aiNumMice);  // Allocate space for the new angles
    AiDistToMouse.clear();              // Clear the old distances
    AiDistToMouse.reserve(aiNumMice);   // Allocate space for the new distances
    int index = -1;
//    cout << "Danger Mice Size: " << dangerMice.size() << "\n";
//    cout << "Danger Mice Count: " << dangerMice.count() << "\n";
    foreach (QGraphicsItem *item, dangerMice) {
        if (item == this){
            continue;
        }else if(item == goalPtrAi){
            continue;
        }

        index = index + 1;
        QLineF lineToMouse(QPointF(0, 0), mapFromItem(item, 0, 0));
        qreal angleToMouse = std::atan2(lineToMouse.dy(), lineToMouse.dx());
        angleToMouse = normalizeAngle((Pi - angleToMouse) + Pi / 2);
        AiAngleToMouse.append(angleToMouse);            // Append angle to vector
        AiDistToMouse.append(lineToMouse.length());     // Append the distance the mouse is from the danger mice
//        std::cout << "Return Angle " << updateAngle(index) << "\n";


//! [7] //! [8]

//! [8] //! [9]
    } // End foreach (QGraphicsItem *item, dangerMice)
        // For every mouse that was not spotted, set the identifier to -1
        int numDangerMice = AiAngleToMouse.size();
//        cout << "Num Danger: " << numDangerMice << "\n";
        for (int i = numDangerMice; i < aiNumMice; i++) {
          AiAngleToMouse.append(-1.0);       // Fill the non-spotted mice with arbitrary identifier (-1.0)
          AiDistToMouse.append(-1.0);        // Fill the non-spotted mice with arbitrary identifier (-1.0)
        }// End for (i = numDangerMice ...
//! [9]

//! [10]

//! [10]

//! [11]
   // Pass in angles of all danger mice and angle to goal
    // Pass in collision occured boolean
    // NN pass in
//    QVariant PythonQt

    // ******************************** Output to NN **************************************

    // Send signal to python by writing to the Qt output file
    ofstream myNewfile;
    myNewfile.open ("C:\\Users\\willi\\Downloads\\CalPoly\\Spring_20\\EE_509\\Final_Project\\dirwatch\\qt\\qtout.txt");
    myNewfile << distToGoal << "\n" << angleToGoal << "\n";   // Write the first three inputs of the NN to the file

        // Write the distances and angles between danger mice to the output file
        for(int i = 0; i < AiDistToMouse.size(); i++){

            myNewfile << AiDistToMouse.at(i)   << "\n";    // Write the distance of the danger mouse to the output file
            myNewfile << AiAngleToMouse.at(i)  << "\n";    // Write the angle    of the danger mouse to the output file
        } // end for(int i = 0; i < numDangerMice

    myNewfile << reward << "\n" + to_string(done); // Write the reward and if the round ended
    myNewfile.close();
    // ******************************** End Output to NN **************************************

    // wait for a return signal to continue
    // Normalize the return angle

}
//! [11]
