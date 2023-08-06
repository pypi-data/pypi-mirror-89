
from high_vision.Segmentation.cdcl.inference_15parts_skeletons import run_image, run_video, run_camera
import numpy as np
import cv2
import os
from PIL import Image


class Pose_Estimation:
    
    """
    This is Pose-Estimation Class in High-Vision Library, it provides the support of State-Of-The-Art Models 
    like CDCL. After Instantiating this Class, you can set its properties and use pre-defined
    functions for performing segmentation Tasks out of the box.

        Use_CDCL()                                  # To Specify which Model to Use
        Detect_From_Image()                         # To Detect from Images
        Detect_From_Video()                         # To Detect from Videos

    """

    def __init__(self):
    
        self.model = None
        self.modelLoaded = False
        self.modelType = None  
    
    def Use_CDCL(self, weights_path:str = None):

        if weights_path is not None:
            if os.path.isfile(weights_path):
                self.weights_p = weights_path
            else:
                raise FileNotFoundError("Weights File Doesn't Exist at provided path.")
        else:
            pass
        
        self.modelLoaded = True
        self.modelType = 'cdcl'
    
    def Detect_From_Image(self, input_path:str, output_path:str):
        
        """[This Function is used to detect pose from Images.]
        
        Args:
            input_path: (str) [path to the input image with jpg/jpeg/png extension]
            output_path: (str) [path to save the output image with jpg/jpeg/png extension]
 
        Raises:
            RuntimeError: [If Model is not Loaded before using this Function]
            RuntimeError: [If any othre Model type is specified other than CDCL]
        """
        
        if self.modelLoaded != True:
            raise RuntimeError ('Before calling this function, you have to call Use_CDCL().')
              
                  
        if self.modelType == 'cdcl':

            _ = run_image(input_path, output_path, weights_path=self.weights_p)
        
        else:
            raise RuntimeError ('Invalid ModelType: Valid Type Is "CDCL"')

    def Detect_From_Video(self, input_path:str, output_path:str, fps:int = 25):
        
        """[This Function is used to detect pose from Videos.]
        
        Args:
            input_path: (str) [path to the input Video with mp4/avi extension]
            output_path: (str) [path to save the output Video with mp4/avi extension]
            fps: (int) [frames per second for video processing]
 
        Raises:
            RuntimeError: [If Model is not Loaded before using this Function]
            RuntimeError: [If any othre Model type is specified other than CDCL]
        """
    
        if self.modelLoaded != True:
            raise RuntimeError ('Before calling this function, you have to call Use_CDCL().')

        if self.modelType == 'cdcl':
            _ = run_video(input_path, output_path, fps, weights_path=self.weights_p)
        
        else:
            
            raise RuntimeError("Invalid ModelType: Valid Type is CDCL")
            
            
    def Detect_From_Camera(self, cam, output_path, show_boxes = False, fps:int = 25):
        
        """[This Function is used to detect pose from Live Camera Streams.]
        
        Args:
            input_path: (str) [path to the input Video with mp4/avi extension]
            output_path: (str) [path to save the output Video with mp4/avi extension]
            fps: (int) [frames per second for video processing]
 
        Raises:
            RuntimeError: [If Model is not Loaded before using this Function]
            RuntimeError: [If any othre Model type is specified other than CDCL]
        """
    
        if self.modelLoaded != True:
            raise RuntimeError ('Before calling this function, you have to call Use_CDCL().')

        if self.modelType == 'cdcl':
            _ = run_camera(cam, frames_per_second=fps, output_video_name=output_path, weights_path=self.weights_p)
        
        else:
            
            raise RuntimeError("Invalid ModelType: Valid Type is CDCL")