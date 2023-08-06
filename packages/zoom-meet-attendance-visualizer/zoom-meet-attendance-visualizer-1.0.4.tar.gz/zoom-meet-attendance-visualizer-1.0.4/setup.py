from pathlib import Path

import setuptools

setuptools.setup(
    name="zoom-meet-attendance-visualizer",
    version="1.0.4",
    description="Manage and visualize data collected using extension zoom_meet_attendance",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/mahbd/zoom_meet_attendance_visualizer",
    author="Mahmudul Alam",
    author_email="mahmudula2000@gmail.com",
    install_requires=["matplotlib", "seaborn", "numpy"],
    packages=setuptools.find_packages(exclude=['venv']),
)
