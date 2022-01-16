# openCV

```c++
//命名窗口，设置窗口属性
cv::namedWindow("image test", CV_WINDOW_NORMAL);
//显示图片
cv::imshow("image test", frame);
//读取图片
frame = cv::imread(filePath);
//写入图片
std::vector<int> compression_params;
compression_params.push_back(CV_IMWRITE_PNG_COMPRESSION);
compression_params.push_back(6); // no loss compression 0~9为PNG格式的压缩系数 默认为3
cv::imwrite(filePath,frame, );
```

##### 画图形

```c++
//圆形
void cvCircle( CvArr* img, CvPoint center, int radius, CvScalar color,
               int thickness=1, int line_type=8, int shift=0 );
//椭圆
void ellipse(Mat& img, Point center,Size axes, double angle, double startAngle, double endAngle, const Scalar& color,int thickness=1, int lineType=8, int shift=0)
//矩形
void rectangle(Mat& img,Rect rec, const Scalar&color, intthickness=1, intlineType=8,intshift=0 )
//直线
void line(InputOutputArray img, Point pt1, Point pt2, const Scalar& color,
          int thickness = 1, int lineType = LINE_8, int shift = 0);
void cv::putText(
		cv::Mat& img, // 待绘制的图像
		const string& text, // 待绘制的文字
		cv::Point origin, // 文本框的左下角
		int fontFace, // 字体 (如cv::FONT_HERSHEY_PLAIN)
		double fontScale, // 尺寸因子，值越大文字越大
		cv::Scalar color, // 线条的颜色（RGB）
		int thickness = 1, // 线条宽度
		int lineType = 8, // 线型（4邻域或8邻域，默认8邻域）
		bool bottomLeftOrigin = false // true='origin at lower left'
	);
```

