# TODO: Fill out this file with information about your package

# HINT: Go back to the object-oriented programming lesson "Putting Code on PyPi" and "Exercise: Upload to PyPi"

# HINT: Here is an example of a setup.py file
# https://packaging.python.org/tutorials/packaging-projects/
# TODO:用你的包的信息填充这个文件
#提示:回到面向对象编程课“把代码放到PyPi上”和“练习:上传到PyPi上”
#提示:这是一个setup.py文件的例子
# https://packaging.python.org/tutorials/packaging-projects/

from setuptools import setup

setup(name='appleliu_distributions',
      version='0.11',
      description='Gaussian distributions',
      packages=['distributions'],
      zip_safe=False)