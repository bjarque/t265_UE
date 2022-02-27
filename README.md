# t265_UE
Intel Realsense t265 into Unreal Engine. Windows only.

Simple script that sends data into Unreal Engine through the JSON liveLink plugin. Works with both location and rotation. 

# Instructions
1. Install python 3.7.9, and remember too add it to PATH https://www.python.org/ftp/python/3.7.9/python-3.7.9-amd64.exe
2. do "pip install pyrealsense2" in CMD
3. Create a c++ project, and install JSON-Livelink Enhanced plugin into your project - https://github.com/clintonman/JSONLiveLink/tree/enhanced When its built, it can be copied to other non c++ projects in the same version. 
4. OR download precompiled plugin from this repository. Current versions are 4.26.2 and 4.27.0 and UE5EA, UE5Preview1
5. Configure livelink to recieve on localhost.

![image](https://user-images.githubusercontent.com/23232326/136547962-7b521660-e3d3-4b53-8ab5-6809187c0366.png)

6. Run script from repo with the command "py tracker.py", after you start it, it should show MHtrack in Livelink controller window. You can optinally add destination ips as   arguments to the command. (ex: "py tracker.py 127.0.0.1 10.0.0.2", would send to 2 destinations)

7. Add livelink component to your camera

![image](https://user-images.githubusercontent.com/23232326/136548300-f6686048-9b91-4e7f-9efd-17a724fe0d9e.png)

8. choose MHtrack as your "Subject representation"

![image](https://user-images.githubusercontent.com/23232326/136548328-ad5ef274-c035-4902-80c3-da6240c994ec.png)



Thats it! 




