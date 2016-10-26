from distutils.core import setup


setup(
    name='micropython-chirp',
    py_modules=['chirp'],
    version="1.0",
    description="MicroPython library for interfacing with the Chirp Soil Moisture Sensor.",
    long_description="""\
This library lets you communicate with a Chirp soil moisture sensor.
""",
    author='Rob Berwick',
    author_email='rob.berwick@gmail.com',
    classifiers=[
        'Development Status :: 6 - Mature',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
