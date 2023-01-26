from setuptools import setup

package_name = 'my_package'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='nourhanabdulazeem',
    maintainer_email='nourhanabdulazeem@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
	entry_points={
        'console_scripts': [
                'controller = my_package.controller:main',
                'timer = my_package.timer:main',
                'happy_face = my_package.happy_face:main',
        ],
	},
)