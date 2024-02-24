The authors collected and annotated a new **MJU-Waste Dataset** for waste object segmentation. It is the largest public benchmark available for waste object segmentation, with 1485 images for training, 248 for validation and 742 for testing. For each color image, the authors provide the co-registered depth image captured using an RGBD camera. We manually labeled each of the images. 

Note, similar **MJU-Waste Dataset** dataset is also available on the [DatasetNinja.com](https://datasetninja.com/):

- [TACO](https://datasetninja.com/taco)

## Motivation

Waste objects are ubiquitous in both indoor and outdoor settings, spanning household, office, and road environments. Consequently, it's imperative for vision-based intelligent robots to effectively locate and interact with them. However, the task of detecting and segmenting waste objects poses unique challenges compared to other objects. These items may be incomplete, damaged, or both, making their identification more complex. Often, their presence can only be inferred from contextual clues within the scene, such as their contrast against the background or their intended use.

Furthermore, accurately localizing waste objects is hindered by significant scale variations due to their diverse physical sizes and dynamic perspectives. The sheer volume of small objects exacerbates this challenge, making it difficult even for humans to precisely delineate their boundaries without zooming in for a closer look. Unlike robots, the human visual system possesses the ability to adjust attention across a wide or narrow visual field, enabling us to quickly grasp the scene's meaning and identify objects of interest. This capability allows us to focus on specific object regions for detailed examination and fine-grained delineation.

<img src="https://github.com/dataset-ninja/mju-waste/assets/120389559/812e271a-9db5-42b3-a0a3-3c5068795cb2" alt="image" width="600">

<span style="font-size: smaller; font-style: italic;">Example images from MJU-Waste and TACO datasets and their zoomed-in object regions. Detecting and localizing waste objects require both scene level and object level reasoning.</span>

## Dataset description



