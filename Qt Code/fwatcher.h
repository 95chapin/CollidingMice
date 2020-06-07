#ifndef FWATCHER_H
#define FWATCHER_H

#include <QWidget>
#include <QMessageBox>
#include <iostream>
//#include <string>
using namespace std;

// For the file system
#include <string.h>
#include <filesystem>

// Find newest file
#include <chrono>
#include <filesystem>
#include <iostream>
namespace fs = std::experimental::filesystem;

class fWatcher : public QWidget
{
    Q_OBJECT

public:
    fWatcher(QWidget* parent= nullptr)
        :QWidget(parent){}

    ~fWatcher(){}

    string dirPath; // The directroy path that the getNewestFile() needs to seek through in propper format "//C:folder//"

    fs::path getNewestFile(){
        using namespace fs::v1;
        fs::directory_iterator iterator;
        //"C:\\Users\\willi\\Downloads\\CalPoly\\TestFolder"
        iterator = directory_iterator(dirPath);	// Path to folder being watched

        fs::path newestPath = iterator->path();             // INIT - The path of the newest file that is being sought (Last write time)
        auto newestTime = last_write_time(newestPath);      // INIT - The newest files write time
        auto currentTime = last_write_time(newestPath);     // INIT - The time of the file being considered
        std::time_t cftime;                                 // OUPUT - Used to ouput the time

        // Loop through the directory, compare the file times to each other to find the newest one
        for(const auto& file : iterator){
            currentTime = last_write_time(file);    // Set the current file's last write time

            // Check if the current file's last write time is newer than the newest file's write time
            if(currentTime > newestTime){
                newestPath = file.path();   // Set the current file's path as the newest file path
                newestTime = currentTime;   // Set the current file's write time as the newest write time
                cftime = decltype(currentTime)::clock::to_time_t(currentTime);  // Used to output the time
            }	// end if(currentTime > newestTime)
        } // end for(const auto& file : iterator)

        cftime = decltype(newestTime)::clock::to_time_t(newestTime);  			// Used to output the time
        std::cout << "Newest Path : " << newestPath << " Time : " << cftime;    // Output the newest path.

        return newestPath;
    }//  end getNewestFile()

public slots:
    void showModified(const QString& str)
    {
        Q_UNUSED(str)
        QMessageBox::

        QMessageBox::information(this,"Directory Modified", "Your Directory is modified");
//        cout << "folder modified: (" << str.toStdString() << ")" << endl;
//        cout << getNewestFile();
    } // end showModified()
};

#endif // FWATCHER_H

