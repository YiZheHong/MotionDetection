## Object Detection in Videos

This is a simple program that can help user to capture the moving objects occured in the videos and output them as PNG files with duplicates removed.

## Installation
Download the project from github

Create a python environment with
``` bash
conda create -n env1 python=3.7.11 numpy=1.20.3 
```
Install the necesarry python pacakges with
``` bash
pip install opencv-python
pip install imutils==0.5.4
```

## Run
Cd to the directory where you store this program, change the hyperparamters in method.py and

``` bash
python main.py
```



## Example Usage
One frame from a video

![Test Image 1](./images/pic9.png)

Output produced by the program

![Test Image 2](./images/0.png)

![Test Image 3](./images/1.png)



