# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yodf']

package_data = \
{'': ['*'], 'yodf': ['.pytest_cache/*', '.pytest_cache/v/cache/*']}

install_requires = \
['numpy>=1.19.4,<2.0.0']

setup_kwargs = {
    'name': 'yodf',
    'version': '1.0.2',
    'description': "'Hello, World!' Forward Mode Autdiff library with Tensorflow 1.15 like interface.",
    'long_description': '## A \'Hello, World!\' forward mode autodiff library.\nThis library with around 500 lines of code is meant as an illustration of how forward mode autodiff can possibly be implemented. \nIt lets you compute the value and the derivative of a function where function is expressed as a computational flow using the primitives\nprovided by the library. Interface of the library is very similar to Tensorflow 1.15. All the samples provided in *examples* folder \ncan very well be run if you do **import tensorflow as tf** as opposed to **import yodf as tf** \n\n### Installation\n**pip install yodf** will install the library. Only dependency it has is *numpy*.\nSamples provided in examples folder also have dependency on *matplotlib*.\n\n### Basic usage\n\nBelow code computes the value and the derivative of the function **x^2** as x=5.0  \n```\nimport yodf as tf\nx = tf.Variable(5.0)\ncost = x**2\nwith tf.Session() as s:\n    # global_variables_initializer API added just so as to\n\t# resemble Tensorflow, it hardly does anything\n    s.run(tf.global_variables_initializer())\n    s.run(cost)\nprint(x.value, cost.value, cost.gradient)\n```\n\n### Basic gradient descent example\nBelow code computes optima of the function **x^2** along with the value at which optima occurs starting with x=5.0  \n```\nimport yodf as tf\nx = tf.Variable(5.0)\ncost = x**2\ntrain = tf.train.GradientDescentOptimizer(learning_rate=0.2).minimize(cost)\nwith tf.Session() as s:\n    s.run(tf.global_variables_initializer())\n    for _ in range(50):\n        _, cost_final, x_final = s.run([train, x, cost])\nprint(f"Minima: {cost_final:.10f} x at minima: {x_final:.10f}")\n```\n\n## How does it work?\nIt has a class called *Tensor* with *Variable* and *_Constant* as classes derived from it. Tensor has a value and a gradient.\nGradient of a constant is 0 and that of a variable is 1 which is as good as saying d(x)/dx.  \nA tensor can also represent an operation and a tensor representating an operation gets created using a convenient function call.\n```\nimport numpy as np\nimport yodf as tf\nx = tf.Variable(np.array([[1,1],[2,2]]))\nop_sin = tf.sin(x)\nprint(op_sin)\n```\nWould print **<yod.Tensor type=TensorType.INT, shape=(2, 2), operation=\'sin\'>**  \nYou typically pass a tensor to run method of *Session* class which ends up evaluating the tensor along with its derivative.\nExecute method of tensor just knows how to compute derivative of basic arithmatic operations, power function and some of the \ntranscendental functions like sin, cos, log, exp. It also knows how to compute derivative when matrix multiplication operation is \ninvolved. By applying the chain rule repeatedly to these operations, derivative of an arbitrary function \n(represented as a tensor) gets computed automatically. *run* method simply builds post order traversal tree of the tensor passed to it and evaluates all the nodes in\nthe tree. *GradientDescentOptimizer* simply updates the value of the variable based on the gradient of the cost tensor passed to \nits minimize function.  \nWhen there are multiple independent variables whose partial derivates needs to be computed, gradient of all but one variable \nwhose partial derivative is being computed are set to 0 during computational flow path. This is handled by *GradientDescentOptimizer*.\n\n## Limitiation of forward mode autodiff\nThough with forward mode autodiff, derivative of a function with one independent variables gets computed during forward pass itself and \nno backward pass is needed as is the case with reverse mode autodiff (generalized backpropagation), with multiple indepdent variables \n(say weights in a neural network), as many passes are needed as number of indepdent variables. So as can be seen in sample \nhttps://github.com/yogimogi/yodf/blob/master/examples/example3_linear_regression.ipynb, time needed by gradient descent linearly\nincreases with increase in degree of polynomial you are trying to fit.  \nExecution times will become prohibitively high when trying to fit \na model with large number of weights which is typically case with deep neural networks.',
    'author': 'Yogesh Ketkar',
    'author_email': 'yogimogi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/yogimogi/yodf',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
