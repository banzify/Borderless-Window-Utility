# Borderless-Window-Utility

Modifies window style to force most applications into a borderless windowed mode.  

# Usage

Install Python, probably from the [Microsoft Store](https://apps.microsoft.com/store/detail/python-310/9PJPW5LDXLZ5).

Checkout the code

Create a virtual environment by running `python -m venv .venv`.

Activate environment with `.venv\Scripts\activate`.

Update the requirements by running `pip install -r requirements.txt`.

Run `python main.py`.

Select an application in dropdown and click Borderless Window to remove the title bar, any borders, and the ability to resize the application with a border. Use the coordinates to determine where you want the window to be, and and adjust the resolution as desired. Some applications are fine adapting to non-traditional resolutions, but some will start to stretch.  
  
## Refresh  

Refreshes the list of visible windows in the window selection dropdown  
  
## Revert Changes  

Reverts the window to the original style. Falls back to the style the application had when the list of applications was last updated; Upon starting main.py or hitting the refresh button. If you hit the refresh button after making an application borderless windowed the revert button will not function  

# Profiles

Create an entry in `profiles.ini` for the game:

```
[Stationeers]
width=2560
height=1440
x=420
y=0
```

In this case we are recording video on a 21:9 3440x1440 monitor, so we want to force it to 16:9 and center it (offset by x=420).

If the window title contains 'Stationeers' the profile values will be used entered into the form.

# Notes

Created/Used on Windows 10.  
Windows 11 has not been tested.  
Will not function on any other operating system.

![image](https://user-images.githubusercontent.com/38366720/149036396-e7a4cc81-6004-4a3f-b5a1-d10007f587f7.png)


The real reason I made this:  
  
When games dont support the super ultrawide resolution and you have them fullscreen they fill in the unused space with black bars.
![image](https://user-images.githubusercontent.com/38366720/149245669-3457cb9e-6ec4-4fc9-a7ea-743400105b0a.png)

Putting the game a windowed state adds a titlebar which causes bottom of the window to be below the screen space. Some games don't allow you to resize these windows and you're forced to either have a piece of the window cut from the bottom or play at a lower resolution that fits within your vertical screen space.
![image](https://user-images.githubusercontent.com/38366720/149245709-f087ae6a-7ade-46b5-8c9c-899cb1d0f367.png)

I use the tool force a borderless windowed state that floats in the center of the screen (or wherever I want it to be)  for a cleaner look and the upside of not losing any of the game window below the monitor space.
![image](https://user-images.githubusercontent.com/38366720/149245765-e801bf91-091e-4f55-b271-0661e1b55fb9.png)
