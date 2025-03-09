from setuptools import find_packages, setup ## for consdering init as package
from typing import List

''' The `setup.py` file is essential for packaging, dependency management, 
    versioning, and easy installation of your ML project. It ensures reproducibility,
    simplifies distribution, and enables script execution. 🚀 '''

def get_requirements()-> list[str]:

    '''this fuction will return list of requirement'''
    req_list:List[str] = []
    try:
        with open('requirement.txt', 'r') as file:
            ## read lines from requirement file 
            lines = file.readlines()
            ## process each line , ignore space and -e.
            for i in lines :
                requirements = i.strip()
                if requirements and requirements != '-e .':
                    req_list.append(requirements)
    
    except Exception as e :
        print("my requirement.txt is not found")

    return req_list


setup(
    author = 'Dabgar Shreyash',
    version= '0.0.1',
    name = 'Network Security System',
    author_email='dabgarshreyash199@gmail.com',
    packages=find_packages(),
    requires_to_install=get_requirements()

)

