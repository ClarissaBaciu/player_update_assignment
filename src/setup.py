from setuptools import setup, find_packages

setup(
    name="player_update_assignment",
    version="0.1",
    description='Tool to update thousands music players using an API',
    author='clarissa baciu',
    author_email='clarissa.baciu@mail.mcgill.ca',
    packages=find_packages('src'),
    install_requires=[
        "requests"
    ],
    package_dir={'': 'src'},
    package_data={'tool': ['tool/input_data.csv']},
    entry_points={
        'console_scripts': ['your-command=tool.player_update:main']
    },


)
