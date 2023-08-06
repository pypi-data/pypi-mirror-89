from setuptools import setup, find_packages

setup(
      name = 'high_vision',
      version = 0.1,
      description = 'A Python Library for Computer Vision tasks like Object Detection, Segmentation, Pose Estimation etc',
      url = "https://github.com/fahima10/high-vision",
      author = "Adeel Intizar",
      packages = find_packages(),
      package_data = {'': ['config']},
      python_requires='>=3.5, <4',
      install_requires = [
          "tensorflow", 
          'keras',
          'opencv-python',
          'numpy',
          'pillow',
          'matplotlib',
          'pandas',
          'scikit-learn',
          'progressbar2',
          'scipy',
          'h5py',
	  'imgaug',
	  'scikit-image',
	  'labelme2coco',
	  'configobj',
	  ],
     
      )