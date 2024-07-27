# Cody Tolene
# Apache License 2.0

import uasyncio
from utils.view_manager import switch_view


# Button listener process
async def buttonListenerProcess(
    views, galacticUnicorn, graphics, currentViewKey, currentViewTask
):
    buttonAState = False
    buttonBState = False
    buttonCState = False
    buttonDState = False
    volumeUpState = False
    volumeDownState = False
    brightnessUpState = False
    brightnessDownState = False
    sleepState = False

    view_keys = list(views.keys())

    while True:
        # Check if button A is pressed
        if galacticUnicorn.is_pressed(galacticUnicorn.SWITCH_A):
            if not buttonAState:
                buttonAState = True
                # Handle button A press if needed
        else:
            buttonAState = False

        # Check if button B is pressed
        if galacticUnicorn.is_pressed(galacticUnicorn.SWITCH_B):
            if not buttonBState:
                buttonBState = True
                # Handle button B press if needed
        else:
            buttonBState = False

        # Check if button C is pressed
        if galacticUnicorn.is_pressed(galacticUnicorn.SWITCH_C):
            if not buttonCState:
                buttonCState = True
                # Handle button C press if needed
        else:
            buttonCState = False

        # Check if button D is pressed
        if galacticUnicorn.is_pressed(galacticUnicorn.SWITCH_D):
            if not buttonDState:
                buttonDState = True
                # Handle button D press if needed
        else:
            buttonDState = False

        # Check if volume up is pressed
        if galacticUnicorn.is_pressed(galacticUnicorn.SWITCH_VOLUME_UP):
            if not volumeUpState:
                volumeUpState = True
                # Handle volume up press if needed
        else:
            volumeUpState = False

        # Check if volume down is pressed
        if galacticUnicorn.is_pressed(galacticUnicorn.SWITCH_VOLUME_DOWN):
            if not volumeDownState:
                volumeDownState = True
                # Handle volume down press if needed
        else:
            volumeDownState = False

        # Check if brightness up is pressed
        if galacticUnicorn.is_pressed(galacticUnicorn.SWITCH_BRIGHTNESS_UP):
            if not brightnessUpState:
                brightnessUpState = True
                current_index = view_keys.index(currentViewKey)
                currentViewKey = view_keys[(current_index - 1) % len(view_keys)]
                currentViewTask = await switch_view(
                    views, currentViewKey, currentViewTask, galacticUnicorn, graphics
                )
        else:
            brightnessUpState = False

        # Check if brightness down is pressed
        if galacticUnicorn.is_pressed(galacticUnicorn.SWITCH_BRIGHTNESS_DOWN):
            if not brightnessDownState:
                brightnessDownState = True
                current_index = view_keys.index(currentViewKey)
                currentViewKey = view_keys[(current_index + 1) % len(view_keys)]
                currentViewTask = await switch_view(
                    views, currentViewKey, currentViewTask, galacticUnicorn, graphics
                )
        else:
            brightnessDownState = False

        # Check if sleep is pressed
        if galacticUnicorn.is_pressed(galacticUnicorn.SWITCH_SLEEP):
            if not sleepState:
                sleepState = True
                # Handle sleep press if needed
        else:
            sleepState = False

        # Sleep for a short period to debounce button presses
        await uasyncio.sleep(0.1)
