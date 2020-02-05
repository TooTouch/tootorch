# tootorch

Implemetation XAI in Computer Vision (Pytorch)

# Requirements

```
torch
opencv-python
pillow
h5py
tqdm
```

# Installation
```bash
pip install tootorch
```

# Interpretable Methods
**Attribution Methods**
- Vanilla Backpropagation (VBP) [[Notebook](https://github.com/Tootouch/WhiteBox-Part1/blob/master/notebook/%5BAttribution%5D%20-%20Vanilla%20Backpropagation%20%26%20Ensemble.ipynb)]
- Input x Backpropagation (IB) [[Notebook](https://github.com/Tootouch/WhiteBox-Part1/blob/master/notebook/%5BAttribution%5D%20-%20Input%20x%20Backpropagation%20%26%20Ensemble.ipynb)]
- DeconvNet [5] [[Notebook](https://github.com/Tootouch/WhiteBox-Part1/blob/master/notebook/%5BAttribution%5D%20-%20DeconvNet%20%26%20Ensemble.ipynb)]
- Guided Backpropagation (GB) [6] [[Notebook](https://github.com/Tootouch/WhiteBox-Part1/blob/master/notebook/%5BAttribution%5D%20-%20Guided%20Backpropagation%20%26%20Ensemble.ipynb)]
- Integrated Gradients (IG) [7] [[Notebook](https://github.com/Tootouch/WhiteBox-Part1/blob/master/notebook/%5BAttribution%5D%20-%20Integrated%20Gradients%20%26%20Ensemble.ipynb)]
- Grad-CAM (GC) [8] [[Notebook](https://github.com/Tootouch/WhiteBox-Part1/blob/master/notebook/%5BAttribution%5D%20-%20GradCAM%20%26%20Ensemble.ipynb)]
- Guided Grad-CAM (GB-GC) [8] [[Notebook](https://github.com/Tootouch/WhiteBox-Part1/blob/master/notebook/%5BAttribution%5D%20-%20Guided-GradCAM%20%26%20Ensemble.ipynb)]

**Ensemble Methods**
- SmoothGrad (SG) [9]
- SmoothGrad-Squared (SG-SQ) [10]
- SmoothGrad-VAR (SG-VAR) [10]

# Evaluation 
- Coherence
- Selectivity
- Remove and Retrain (ROAR) [10]
- Keep and Retrain (KAR) [10]

# Reference
- [1] Wang, F., Jiang, M., Qian, C., Yang, S., Li, C., Zhang, H., ... & Tang, X. (2017). Residual attention network for image classification. In Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (pp. 3156-3164). [[Paper](https://arxiv.org/abs/1704.06904)]

- [2] Zhou, B., Khosla, A., Lapedriza, A., Oliva, A., & Torralba, A. (2016). Learning deep features for discriminative localization. In Proceedings of the IEEE conference on computer vision and pattern recognition (pp. 2921-2929). [[Paper](https://arxiv.org/abs/1512.04150)]

- [3] Woo, S., Park, J., Lee, J. Y., & So Kweon, I. (2018). Cbam: Convolutional block attention module. In Proceedings of the European Conference on Computer Vision (ECCV) (pp. 3-19). [[Paper](https://arxiv.org/abs/1807.06521)]

- [4] Rodríguez, P., Gonfaus, J. M., Cucurull, G., XavierRoca, F., & Gonzalez, J. (2018). Attend and rectify: a gated attention mechanism for fine-grained recovery. In Proceedings of the European Conference on Computer Vision (ECCV) (pp. 349-364). [[Paper](https://arxiv.org/abs/1807.07320)]

- [5] Zeiler, M. D., & Fergus, R. (2014, September). Visualizing and understanding convolutional networks. In European conference on computer vision (pp. 818-833). Springer, Cham. [[Paper](https://arxiv.org/abs/1311.2901)] [[Korean version](https://datanetworkanalysis.github.io/2019/10/27/deconvnet)]

- [6] Springenberg, J. T., Dosovitskiy, A., Brox, T., & Riedmiller, M. (2014). Striving for simplicity: The all convolutional net. arXiv preprint arXiv:1412.6806. [[Paper](https://arxiv.org/abs/1412.6806)]

- [7] Sundararajan, M., Taly, A., & Yan, Q. (2017, August). Axiomatic attribution for deep networks. In Proceedings of the 34th International Conference on Machine Learning-Volume 70 (pp. 3319-3328). JMLR. org. [[Paper](https://arxiv.org/pdf/1703.01365.pdf)]

- [8] Selvaraju, R. R., Cogswell, M., Das, A., Vedantam, R., Parikh, D., & Batra, D. (2017). Grad-cam: Visual explanations from deep networks via gradient-based localization. In Proceedings of the IEEE International Conference on Computer Vision (pp. 618-626). [[Paper](https://arxiv.org/abs/1610.02391)] [[Korean version](https://www.notion.so/tootouch/Grad-CAM-Visual-Explanations-from-Deep-Networks-via-Gradient-based-Localization-504a3f7a58fd4c3eafdc26258befd643)]

- [9] Smilkov, D., Thorat, N., Kim, B., Viégas, F., & Wattenberg, M. (2017). Smoothgrad: removing noise by adding noise. arXiv preprint arXiv:1706.03825. [[Paper](
https://arxiv.org/abs/1706.03825)] [[Korean version](https://datanetworkanalysis.github.io/2019/10/22/smoothgrad)]

- [10] Hooker, S., Erhan, D., Kindermans, P. J., & Kim, B. (2018). Evaluating feature importance estimates. arXiv preprint arXiv:1806.10758. [[Paper](https://arxiv.org/abs/1806.10758)] [[Korean version](https://datanetworkanalysis.github.io/2019/11/13/roar_kar)]
