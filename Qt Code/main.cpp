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

#include <QtWidgets>

#include <math.h>

#include "mouse.h"
#include "aimouse.h"
#include <QRandomGenerator>
#include <random>

#include <iostream>
using namespace std;

// File system watcher
#include <QFileSystemWatcher>
#include <QDebug>

#include "fwatcher.h"
#include <string.h>

static const int MouseCount = 0;
static const qreal tolerance = 60;
bool drawGoal = true;

//! [0]
int main(int argc, char **argv)
{
    QApplication app(argc, argv);
//! [0]
    // Set up File System watcher
    QFileSystemWatcher watcher;
    watcher.addPath("C:/Users/willi/Downloads/CalPoly/Spring_20/EE_509/Final_Project/dirwatch/py/pyout.txt");
//    fWatcher* fileWatch = new fWatcher;

//! [1]
    // Set up scene
    QGraphicsScene scene;
    scene.setSceneRect(-300, -300, 600, 600);

//    std::cout <<"Width  : " << scene.width() << "\n";
//    std::cout <<"Height : " << scene.height() << "\n";
//! [1] //! [2]
    scene.setItemIndexMethod(QGraphicsScene::NoIndex);
//! [2]

//! [3]
//    std::uniform_int_distribution <int> dist(-300,300);
//    for (int i = 0; i < MouseCount; ++i) {
//        Mouse *mouse = new Mouse;

//        mouse->setPos(dist(*QRandomGenerator::global()),
//                      dist(*QRandomGenerator::global()));
//        scene.addItem(mouse);
//    }


// Top left
//    Mouse *mouse1 = new Mouse;
//    mouse1->setPos(-300,-300);
//    scene.addItem(mouse1);

//    Mouse *mouse1 = new Mouse;
//    mouse1->setPos(0,0);
//    scene.addItem(mouse1);

//    Mouse *mouse2 = new Mouse;
//    mouse2->setPos(-100,-100);
//    scene.addItem(mouse2);

//    Mouse *mouse3 = new Mouse;
//    mouse3->setPos(100,-100);
//    scene.addItem(mouse3);

    // Top right
//    Mouse *mouse2 = new Mouse;
//    mouse2->setPos(300,-300);
//    scene.addItem(mouse2);

// Bottom right
//    Mouse *mouse3 = new Mouse;
//    mouse3->setPos(300,300);
//    scene.addItem(mouse3);

    // Bottom left
//    Mouse *mouse4 = new Mouse;
//    mouse4->setPos(-300,300);
//    scene.addItem(mouse4);
    std::uniform_int_distribution <int> dist(-250,250);
    qreal mainGoalX = dist(*QRandomGenerator::global());
    qreal mainGoalY = dist(*QRandomGenerator::global());
    QGraphicsEllipseItem *goal = new QGraphicsEllipseItem(QRectF(mainGoalX-tolerance, mainGoalY-tolerance, tolerance*2, tolerance*2));
    //    QGraphicsRectItem *rect = new QGraphicsRectItem(QRectF(goalX, goalY, 120*2, 120*2));

    if(drawGoal != true){
        goal = nullptr;
    }else{
        scene.addItem(goal);
    }


    // New mouse
    AiMouse *theAImouse = new AiMouse(MouseCount, tolerance, goal);
    theAImouse->initDangerMice(MouseCount, &scene);
    theAImouse->setPos(0,0);
    theAImouse->goalX = 0;
    theAImouse->goalY = 0;
    scene.addItem(theAImouse);




//    theAImouse->collisionOccured = scene.collidingItems(theAImouse).isEmpty();  // For the case that the mouse appears on top of another mouse

//! [3]

//! [4]
    QGraphicsView view(&scene);
    view.setRenderHint(QPainter::Antialiasing);
    view.setBackgroundBrush(QPixmap(":/images/cheese.jpg"));

//! [4] //! [5]
    view.setCacheMode(QGraphicsView::CacheBackground);
    view.setViewportUpdateMode(QGraphicsView::BoundingRectViewportUpdate);
    view.setDragMode(QGraphicsView::ScrollHandDrag);
//! [5] //! [6]
    view.setWindowTitle(QT_TRANSLATE_NOOP(QGraphicsView, "Colliding Mice"));
    view.resize(400, 300);
    view.show();



    //QTimer timer;
    QObject::connect(&watcher, SIGNAL(fileChanged(QString)), &scene, SLOT(advance()));
//    QObject::connect(&timer, SIGNAL(timeout()), &scene, SLOT(advance()));
    //timer.start(1000 / 33);

    return app.exec();


}
//! [6]
