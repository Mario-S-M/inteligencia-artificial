#include <stdio.h>
#include <opencv2/opencv.hpp>

using namespace cv;
using namespace std;

int main(){
	
	Mat a=imread("1baa.png", 0);
	//int aux[255]={0};
	int i, j;
	for(i=0; i<a.rows; i++ ){
		for(j=0; j<a.cols; j++){
			printf(" %d ", a.at<uchar>(i,j));
			}
		printf("\n");
		}
	//for(i=0; i<255; i++){
	//	printf("%d  = %d\n", i, aux[i]);
	//}
	
	imshow("Ejemplo", a);		
	waitKey(0);
	
	
	}
