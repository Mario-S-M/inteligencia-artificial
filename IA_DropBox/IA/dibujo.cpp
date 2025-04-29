#include <stdio.h>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>


using namespace cv;
using namespace std;

int main (){
	
	Mat ejemplo = imread("1.png", 0);
	Mat ejemplo2 = Mat(ejemplo.rows, ejemplo.cols, CV_8UC1, Scalar(159) );
	Mat ejemplo3 = Mat(ejemplo.rows/2, ejemplo.cols/2, CV_8UC1, Scalar(255));
	int i,j;
	for(i=0; i<ejemplo.rows/2; i++)
		for(j=0; j<ejemplo.cols/2; j++)
			ejemplo3.at<uchar>(i,j)=ejemplo.at<uchar>(i,j)> 150  ?255:0;
	
	imshow("Ejemplo ", ejemplo );
	imshow("Ejemplo2 ", ejemplo2 );
		imshow("Ejemplo3 ", ejemplo3 );

	waitKey(0);
	return 0;
	}
