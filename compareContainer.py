from collections import defaultdict
import cv2
import numpy as np

class compareContainer:
     def __init__(self,simlarityThreshold,detectMode):
          self.container = defaultdict(list)
          self.total_num_pic = 0
          self.pure_num_pic = 0
          self.duplicatesRemoved = []
          self.simlarityThreshold = simlarityThreshold
          self.detector = cv2.AKAZE_create()
          self.detectMode = detectMode

     def add(self,size,object):
          self.container[size].append(object)
          self.total_num_pic +=1

     def remove_duplicate(self):
          for size in self.container:
               for pic in self.container[size]:
                    # cv2.imshow('Frame', pic)
                    # cv2.waitKey()
                    containedDuplicate = False
                    sim =0
                    for index, ComparePic in enumerate(self.duplicatesRemoved):
                         if pic.shape[0]!=0 and ComparePic.shape[0] != 0 and pic.shape[1]!=0 and ComparePic.shape[1] != 0:
                              picGray = cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY)
                              ComparePicGray = cv2.cvtColor(ComparePic, cv2.COLOR_BGR2GRAY)
                              if self.detectMode == 1:
                                   sim = self.featureSim(picGray,ComparePicGray)
                                   if sim < self.simlarityThreshold: #higher, stricter
                                        containedDuplicate = True
                                        break
                              else:
                                   sim = self.calSim(pic,ComparePic)
                                   if sim >self.simlarityThreshold:# lower, stricter
                                        containedDuplicate = True
                                        break
                    if not containedDuplicate:
                         if pic.shape[0] != 0 and pic.shape[1] != 0:
                              self.pure_num_pic +=1
                              self.duplicatesRemoved.append(pic)

     def calSim(self,input1, input2, dim=(500, 500)):
          try:
               input1 = cv2.resize(input1, dim, interpolation=cv2.INTER_AREA)
               input2 = cv2.resize(input2, dim, interpolation=cv2.INTER_AREA)
          except:
               print()
          if input1.shape == input2.shape:
               errorL2 = cv2.norm(input1, input2, cv2.NORM_L2)
               if input1.shape[0] * input2.shape[1] != 0:
                    similarity = 1 - errorL2 / (input1.shape[0] * input2.shape[1])
                    return similarity
          return 0
     def featureSim(self,input1, input2, dim=(500, 500)):
          ret=0
          try:
               input1 = cv2.resize(input1, dim, interpolation=cv2.INTER_AREA)
               input2 = cv2.resize(input2, dim, interpolation=cv2.INTER_AREA)
          except:
               print()
          bf = cv2.BFMatcher(cv2.NORM_HAMMING)
          (target_kp, target_des) = self.detector.detectAndCompute(input1, None)
          if input1.shape == input2.shape:
               try:
                    (comparing_kp, comparing_des) = self.detector.detectAndCompute(input2, None)
                    matches = bf.match(target_des, comparing_des)
                    dist = [m.distance for m in matches]
                    if len(dist) ==0:
                         return 0
                    ret = sum(dist) / len(dist)
                    return ret
               except:
                    ret = 1000000
          return ret
     def isSame(self,input1,input2):
          if input1.shape == input2.shape:
               difference = cv2.subtract(input1, input2)
               b, g, r = cv2.split(difference)
               if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
                    return True
          return False
     def compareSize(self,input1,input2):
          area1 = input1.shape[0]*input1.shape[1]
          area2 = input2.shape[0] * input2.shape[1]
          if area1 > area2:
              return input1,input2
          return input2, input1
     def largeContainsmall(self,largePic, smallPic):
          im = np.atleast_3d(largePic)
          tpl = np.atleast_3d(smallPic)
          H, W, D = im.shape[:3]
          h, w = tpl.shape[:2]

          # Integral image and template sum per channel
          sat = im.cumsum(1).cumsum(0)
          tplsum = np.array([tpl[:, :, i].sum() for i in range(D)])

          # Calculate lookup table for all the possible windows
          iA, iB, iC, iD = sat[:-h, :-w], sat[:-h, w:], sat[h:, :-w], sat[h:, w:]
          lookup = iD - iB - iC + iA
          # Possible matches
          possible_match = np.where(np.logical_and.reduce([lookup[..., i] == tplsum[i] for i in range(D)]))

          # Find exact match
          for y, x in zip(*possible_match):
               if np.all(im[y + 1:y + h + 1, x + 1:x + w + 1] == tpl):
                    return True
          return False

          # raise Exception("Image not found")
