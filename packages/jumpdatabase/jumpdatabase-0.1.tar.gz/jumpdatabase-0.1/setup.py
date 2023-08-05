import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
  name = 'jumpdatabase',         # How you named your package folder (MyLib)
  packages = ['JumpDB'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='lgpl-3.0',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'minimal json local database',   # Give a short description about your library
  author = 'lagvidilo',                   # Type in your name
  author_email = 'informabox.contact@gmail.com',      # Type in your E-Mail
  url = 'https://gitlab.com/opensource-university/jumpdb',   # Provide either the link to your github or to your website
  keywords = ['DATABASE', 'JSON', 'LOCAL', 'MICRO'],   # Keywords that define your package best
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'Programming Language :: Python :: 3',      #Spe0cify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)