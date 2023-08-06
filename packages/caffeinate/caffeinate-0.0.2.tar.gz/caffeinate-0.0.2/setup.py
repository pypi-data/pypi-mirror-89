from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        return f.read()

setup(
   name='caffeinate',
   version='0.0.2',
   author='Subash Poudyal',
   author_email='subash.poudyal8@gmail.com',
   packages=['caffeinate'],
   python_requires=">=3.6.3",
   url='https://github.com/subash774/Caffeinate',
   license='MIT',
   description="Don't let your computer go to sleep while you're busy training your model",
   long_description_content_type='text/markdown',
   long_description= readme(),
   install_requires=['pynput>=1.7.2'],
   zip_safe=False,
   entry_points={
        'console_scripts': [
            'awake=caffeinate.caffeinate:run',
        ]
    }
)