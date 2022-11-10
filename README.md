# Screenshot-Plus

Screenshot tool with automation features made in Python.

## Dependencies

`screenshotplus.py` requires the use of `tkinter` and `pyautogui`.
`screenshotplus.exe` can be run without anything else installed.

## Help Guide

### Page Values

These values correspond to the location and dimensions of the page/screenshot.
This can currently only access the main monitor if using a multi-screen display.

#### Left Corner X & Y

The horizontal and vertical position of the top left corner of the page. 
These values can be set by the Quick Setup button at the bottom of the **Page Values** section. These are expected to be whole numbers.

#### Page Width & Height

How many pixels wide and tall the page is from the top left corner. These values can be set by the Quick Setup button at the bottom of the **Page Values** section. These are expected to be positive whole numbers.

#### Quick Setup (Page Values)

Easily set up the above page values by dragging a box over the desired area.
Right click cancels the setup.

### Between Screenshots

These values correspond to optional actions that can be automated between screenshots:
clicking on a given position or scrolling an amount.
Enable or disable them by clicking on each section's checkbox.
If both are checked, the click will happen before the scroll.
Clicking between screenshots is enabled by default.

#### Click X & Y
The horizontal and vertical position of the spot to click between screenshots. 
These values can be set by the **Quick Setup** button immediately below it. These are expected to be whole numbers.

#### Quick Setup (Between Screenshots)

Easily set up the above click coordinates by clicking on the desired position.
Right click cancels the setup.

#### Scroll X & Y

The amount of horizontal and vertical movement to scroll between screenshots. 
Scroll X can be positive to scroll right and negative to scroll left, but is currently unavailable on Windows.
Scroll Y can be positive to scroll down and negative to scroll up.
These are expected to be whole numbers.

#### Pause Time

The length of time (in seconds) waited after clicking or scrolling. This is expected to be a positive number.

### Save Location

This section describes where the screenshots will be saved. The save location can be changed with the **Change Folder** button. Screenshots will be saved as `n.png` where `n` is the page number.

### Number of Pages & Start Button

The number of pages entry is the number of screenshots the tool will take.
This is expected to be a whole number.
The **Start** button will hide the Screenshot Plus window and begin taking screenshots.
The tool can begin taking screenshots by pressing the `Enter` key as well.

