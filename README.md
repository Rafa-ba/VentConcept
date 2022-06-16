<img src="https://github.com/Rafa-ba/VentConcept/blob/main/VentConcept_logo.png" alt="drawing" width="120"/>


# VentConcept
Simulation Tool for assessing Natural Ventilation strategies in the early stages of building design. VentConcept allows the user to test out different Natural Ventilation strategies and scenarios, to improve their architectural design based on the simulation results. The program was built with the idea of simplifying the simulation process to a maximum, making it intuitive also for users with no background in simulation.

## Description
VentConcept code is based on [Ladybug Tools](https://github.com/ladybug-tools). Other than Ladybug Tools, VentConcept has its own GUI. The GUI was done with [Kivy](https://kivy.org/#home). Simulations are run through [OpenStudio](https://openstudio.net/). Ladybug Tools libraries are slightly modified, especially due to pyinstaller incompatability of dynamicly imported packages (through importlib), a practice, commonly used in Ladybug Tools. Ladybug Tools Version 1.3.0 was used.

## Getting Started
Download and install OpenStudio Version 1.2.1 (higher versions lead to error in the air changes per hour plots under the results tab of VentConcept). OpenStudio 1.2.1 can be downloaded by clicking on the following link ([OpenStudio 1.2.1](https://github.com/openstudiocoalition/OpenStudioApplication/releases/download/v1.2.1/OpenStudioApplication-1.2.1+29888f9a87-Windows.exe)).
Download the VentConcept Installer _VentConcept_Installer.exe_ from the repository. Install the program, preferencably outside the Windows program directories (use the preset options of the installer).\
\
VentConcept is setup and ready to be used :)\
\
**Note that the text inside text fields of VentConcept must appear in black. If it is marked RED, it is not validated yet. Only by pressing the _enter_ key the text will be applied and turn BLACK again. Check the pdf files _VentConcept__User Instruction_, as it clarify this doubt in more detail and further doubts!**

## System Requirements
- Windows 10
- Full HD Display (1920x1080 pxs) or higher resolution - Make also sure that under the  _Settings -> Display -> Change the size of text, apps, and other items_  the scale is set to 100 % (in the case of FHD) or accordingly reduced in the case of higher resulutions. This is important to have all VentConcept items appearing correctly on the screen, as the scaling behavior of the current version is quite limited.

## License
AGPL, read the License Agreement

