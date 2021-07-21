from setuptools import setup

setup(name='sourdough',
      version='0.0.1',
      description='Package for creating and maintaining sourdough starters',
      author='Noa Dudai',
      author_email='nooninana@gmail.com',
      url='https://github.com/noadudai/sourdough',
      install_requires=[
          'SQLAlchemy==1.4.12',
          'Flask==1.1.2',
          'PyInquirer==1.0.3',
          'requests==2.25.1',

      ],
      )
