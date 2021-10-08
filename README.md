# t265_UE
Intel Realsense t265 into Unreal Engine. Windows only, and Livelink plugin is 4.26.2 only at the moment. Might recompile it for different versions if you want.

Simple script that sends data into Unreal Engine through the JSON liveLink plugin. Can be configured to send to another IP as well.

# Instructions
1. Install the SDK from Intel https://www.intelrealsense.com/sdk-2/
2. Install JSON-Livelink Enhanced plugin into your project - https://github.com/clintonman/JSONLiveLink/tree/enhanced
3. Configure livelink to recieve on localhost.

![image](https://user-images.githubusercontent.com/23232326/136547962-7b521660-e3d3-4b53-8ab5-6809187c0366.png)

4. Install python 3.7.9, and remember too add it to PATH https://www.python.org/ftp/python/3.7.9/python-3.7.9-amd64.exe
5. do "pip install pyrealsense2" in CMD
6. And run with "py tracker.py"

7. Add livelink component to your camera

![image](https://user-images.githubusercontent.com/23232326/136548300-f6686048-9b91-4e7f-9efd-17a724fe0d9e.png)

8. choose MHtrack as your "Subject representation"

![image](https://user-images.githubusercontent.com/23232326/136548328-ad5ef274-c035-4902-80c3-da6240c994ec.png)



Thats it! 




