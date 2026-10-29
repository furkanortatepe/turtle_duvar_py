from setuptools import find_packages, setup

package_name = 'turtle_duvar_py'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Furkan Ortatepe',
    maintainer_email='furkanortatepe31@gmail.com',
    description='Turtlesim duvardan kacan kaplumbaga ROS 2 paketi',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'duvardan_kacan = turtle_duvar_py.duvardan_kacan:main',
        ],
    },
)
