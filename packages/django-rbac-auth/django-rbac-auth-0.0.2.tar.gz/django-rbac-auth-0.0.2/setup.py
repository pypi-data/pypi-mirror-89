import os
from setuptools import setup, find_packages


version = '0.0.2'

readme_file = os.path.join(os.path.dirname(__file__), 'README.rst')
with open(readme_file) as f:
    long_description = f.read()

setup(
    name='django-rbac-auth',
    version=version,
    python_requires='>=3.5',
    author='xiaoyaogege',
    author_email='249768447@qq.com',
    description="A role-based access control(RBAC) practice via Django.",
    long_description=long_description,
    url='https://github.com/XIAOYAOGEGE666/django-rbac-auth',
    zip_safe=False,
    packages=find_packages(),
    include_package_data=True,
    license='BSD',
    install_requires=["Django>=2.2"],
)
