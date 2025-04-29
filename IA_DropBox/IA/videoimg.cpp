#include "opencv2/opencv.hpp"
#include "opencv2/core/core.hpp"
#include <opencv2/highgui/highgui.hpp>
#include <stdio.h>
#include <iostream>

//g++ -Wall %f -o %e `pkg-config --cflags --libs opencv`
//g++ -Wall videoimg.cpp -o chonavideo `pkg-config --cflags --libs opencv`

//mogrify resize 10x10 *.jpg

using namespace cv;
using namespace std;
int main()
{
    VideoCapture cap("/home/likcos/video/1.webm");
   // VideoCapture cap(0);

	String a;
	  
	int i=0, j=0, w=0;	
    for(;;)
    {
	   Mat frame;	
        cap >> frame; 
        Mat aux;
        //Mat tam=Mat(frame.rows/30, frame.cols/30, CV_8UC3, Scalar(0,0,0));
 		/*for(i=0; i<frame.rows; i++)
			for(j=0; j<frame.cols; j++)
				tam.at<Vec3b>(i/30,j/30)=frame.at<Vec3b>(i,j); 
		*/
		resize(frame, aux, Size(10,10));
		imshow("test",aux);
		//imshow("original",frame);
		imwrite(to_string(w)+".jpg", aux);
		if(waitKey(50) == 0) break;
		w++;
    }
    waitKey(0);
    return 0;
}
