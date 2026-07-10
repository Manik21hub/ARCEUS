from setuptools import setup, find_packages

setup(
    name="arceus-assistant",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "SpeechRecognition",
        "pyttsx3",
        "pyaudio",
        "google-generativeai",
        "python-dotenv"
    ],
    entry_points={
        'console_scripts': [
            'arceus=main:run_arceus',  # Maps the terminal command 'arceus' to your run_arceus function
        ],
    },
)