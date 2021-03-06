
LibSPN
======

LibSPN is a library for learning and inference with Sum-Product Networks. LibSPN
is integrated with `TensorFlow <http://www.tensorflow.org>`_.

What are SPNs?
--------------

Sum-Product Networks (SPNs) are a probabilistic deep architecture with solid theoretical foundations, which demonstrated state-of-the-art performance in several domains. Yet, surprisingly, there are no mature, general-purpose SPN implementations that would serve as a platform for the community of machine learning researchers centered around SPNs. LibSPN is a new general-purpose Python library, which aims to become such a platform. The library is designed to make it straightforward and effortless to apply various SPN architectures to large-scale datasets and problems. The library achieves scalability and efficiency, thanks to a tight coupling with TensorFlow, a framework already used by a large community of researchers and developers in multiple domains.


Why LibSPN?
-----------

Several reasons:


* LibSPN is a general-purpose library with a generic interface and tools for generating SPN structure, making it easy to apply SPNs to any domain/problem
* LibSPN offers a simple Python interface for building or generating networks, learning, and inference, facilitating prototyping (e.g. in Jupyter) and enabling simple integration of SPNs with other software
* LibSPN is integrated with TensorFlow, making it possible to combine SPNs with other deep learning methods
* LibSPN uses concepts that should sound familiar to TensorFlow users (e.g. tensors, variables, feeding, queues, batching, TensorBoard etc.)
* LibSPN leverages the power of TensorFlow to efficiently perform parallel computations on (multiple) GPU devices
* LibSPN is extendable, making it easy to add custom operations and graph nodes

Features of LibSPN
------------------


* 
  Simple interface for manual creation of custom network architectures


  * Automatic SPN validity checking and scope calculation
  * Adding explicit latent variables to sums/mixtures
  * Weight sharing

* 
  Integration with TensorFlow


  * SPN graph is converted to TensorFlow graph realizing specific algorithms/computations
  * Inputs to the network come from TensorFlow feeds or any TensorFlow tensors

* 
  SPN structure generation and learning


  * Dense random SPN generator
  * Simple naive Bayes mixture model generator

* 
  Loading and saving of structure and weights of learned models

* 
  Simple interface for random data generation, data loading and batching


  * Random data sampling from Gaussian Mixtures
  * Using TensorFlow queues for data loading, shuffling and batching

* 
  Built-in visualizations


  * SPN graph structure visualization
  * Data/distribution visualizations

* 
  SPN Inference


  * SPN/MPN value calculation
  * Gradient calculation
  * Inferring MPE state

* 
  SPN Learning


  * Expectation Maximization
  * Gradient Descent

* 
  Other


  * Generating random sub-sets of all partitions of a set using repeated sampling or enumeration

Documentation
-------------

Installation instructions and complete documentation can be found at http://www.libspn.org

Papers using LibSPN
-------------------


*
  `Deep Convolutional Sum-Product Networks for Probabilistic Image Representations <https://arxiv.org/abs/1902.06155>`_ *Jos van de Wolfshaar, Andrzej Pronobis* (2019).
  Code can be found in the `this experimental branch <https://github.com/pronobis/libspn/tree/feature/convspn>`_ and the experiments are `reproduced here <https://github.com/pronobis/libspn/tree/feature/convspn/libspn/examples/convspn>`_

*
  `From Pixels to Buildings: End-to-end Probabilistic Deep Networks for Large-scale Semantic Mapping <https://arxiv.org/abs/1812.11866>`_, *Kaiyu Zheng, Andrzej Pronobis* (2018)

* `Learning Graph-Structured Sum-Product Networks for Probabilistic Semantic Maps <https://www.aaai.org/ocs/index.php/AAAI/AAAI18/paper/view/16923>`_ *Kaiyu Zheng, Andrzej Pronobis, Rajesh P. N. Rao* (2018)
* `Learning Deep Generative Spatial Models For Mobile Robots <https://ieeexplore.ieee.org/document/8202235/>`_ *Andrzej Pronobis, Rajesh P. N. Rao* (2017)
* `Learning Semantic Maps With Topological Reasoning <https://arxiv.org/abs/1709.08274>`_ *Kaiyu Zheng, Andrzej Pronobis, Rajesh P. N. Rao* (2017)
