The authors collected and annotated a new **MJU-Waste Dataset v1.0** for waste object segmentation. It is the largest public benchmark available for waste object segmentation, with 1485 images for training, 248 for validation and 742 for testing. For each color image, the authors provide the co-registered depth image captured using an RGBD camera. The authors manually labeled each of the images. 

Note, similar **MJU-Waste Dataset v1.0** dataset is also available on the [DatasetNinja.com](https://datasetninja.com/):

- [TACO](https://datasetninja.com/taco)

## Motivation

Waste objects are ubiquitous in both indoor and outdoor settings, spanning household, office, and road environments. Consequently, it's imperative for vision-based intelligent robots to effectively locate and interact with them. However, the task of detecting and segmenting waste objects poses unique challenges compared to other objects. These items may be incomplete, damaged, or both, making their identification more complex. Often, their presence can only be inferred from contextual clues within the scene, such as their contrast against the background or their intended use.

Furthermore, accurately localizing waste objects is hindered by significant scale variations due to their diverse physical sizes and dynamic perspectives. The sheer volume of small objects exacerbates this challenge, making it difficult even for humans to precisely delineate their boundaries without zooming in for a closer look. Unlike robots, the human visual system possesses the ability to adjust attention across a wide or narrow visual field, enabling us to quickly grasp the scene's meaning and identify objects of interest. This capability allows us to focus on specific object regions for detailed examination and fine-grained delineation.

<img src="https://github.com/dataset-ninja/mju-waste/assets/120389559/0c18de64-5157-468f-b013-ac42415b0dab" alt="image" width="800">

<span style="font-size: smaller; font-style: italic;">Example images from MJU-Waste and TACO datasets and their zoomed-in object regions. Detecting and localizing waste objects require both scene level and object level reasoning.</span>

## Dataset description

Given an input color image and optionally an additional depth image, the authors model outputs a pixelwise labeling map. They apply deep models at both the scene and the object levels. 

<img src="https://github.com/dataset-ninja/mju-waste/assets/120389559/b63c6ed2-df66-4b6b-9b08-bc9a41b89706" alt="image" width="800">

<span style="font-size: smaller; font-style: italic;">Overview of the proposed method. Given an input image, the authors approach the waste object segmentation problem at three levels: (i) scene-level parsing for an initial coarse segmentation, (ii) object-level parsing to recover fine details for each object region proposal, and (iii) pixel-level refinement based on color, depth, and spatial affinities. Together, joint inference at all these levels produces coherent final segmentation results.</span>

The dataset was curated by the authors through a process involving the collection of waste items from a university campus, subsequent transportation to a lab, and the capturing of images depicting individuals holding these waste items. All images within the dataset were acquired using a Microsoft Kinect RGBD camera. The current iteration of the dataset, known as MJU-Waste, comprises 2475 co-registered pairs of RGB and depth images.

To organize the dataset, the authors partitioned the images randomly into three subsets: a training set, a validation set, and a test set, consisting of 1485, 248, and 742 images, respectively. However, due to inherent limitations of the sensor, the depth frames may contain missing values, particularly at reflective surfaces, occlusion boundaries, and distant regions. To address this, a median filter is employed to fill in these missing values, ensuring the depth images maintain high quality. Furthermore, each image within the MJU-Waste dataset is meticulously annotated with a pixelwise mask delineating the waste objects present.

<img src="https://github.com/dataset-ninja/mju-waste/assets/120389559/21e85db0-cb68-48ae-b667-51b832383f34" alt="image" width="800">

<span style="font-size: smaller; font-style: italic;">Example color frames, ground-truth annotations, and depth frames from the MJU-Waste dataset. Ground-truth masks are shown in blue. Missing values in the raw depth frames are shown in white. These values are filled in with a median filter following.</span>



