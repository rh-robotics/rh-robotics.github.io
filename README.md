# Rowland Hall Robotics, The Website!

This repository holds the code for our website. Nothing especially interesting is housed here.
It's just a regular bootstrap website that [Milo Banks](https://github.com/IsaccBarker) made to
show they were a better programmer than the Wix developers.

Content is written in CommonMark, and can be found in the `content` directory. It is then rendered
by [Marko](https://github.com/frostming/marko) and templated by [Jinja](https://jinja.palletsprojects.com/en/3.1.x/).
The `process/process.py` does all the heavy lifting, and reads minimal configuration data from
`website.yaml`. A GitHub action runs on each push which renders the website and pushes it to GitHub
pages for your browsing convenience.