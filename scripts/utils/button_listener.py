# Cody Tolene
# Apache License 2.0

import uasyncio
from utils.view_manager import switch_view


# Button listener process
async def buttonListenerProcess(
    views, galacticUnicorn, graphics, currentViewKey, currentViewTask
):
    view_keys = list(views.keys())

    buttonStates = {
        "A": False,
        "B": False,
        "C": False,
        "D": False,
        "VOLUME_UP": False,
        "VOLUME_DOWN": False,
        "BRIGHTNESS_UP": False,
        "BRIGHTNESS_DOWN": False,
        "SLEEP": False,
    }

    isDeviceOn = True
    previous_brightness = galacticUnicorn.get_brightness()
    previous_volume = 0.5  # Set initial volume to 0.5

    while True:
        if isDeviceOn:
            if galacticUnicorn.is_pressed(galacticUnicorn.SWITCH_A):
                if not buttonStates["A"]:
                    buttonStates["A"] = True
                    # Switch to the previous view
                    current_index = view_keys.index(currentViewKey)
                    currentViewKey = view_keys[(current_index - 1) % len(view_keys)]
                    currentViewTask = await switch_view(
                        views,
                        currentViewKey,
                        currentViewTask,
                        galacticUnicorn,
                        graphics,
                    )
            else:
                buttonStates["A"] = False

            if galacticUnicorn.is_pressed(galacticUnicorn.SWITCH_B):
                if not buttonStates["B"]:
                    buttonStates["B"] = True
                    # Switch to the next view
                    current_index = view_keys.index(currentViewKey)
                    currentViewKey = view_keys[(current_index + 1) % len(view_keys)]
                    currentViewTask = await switch_view(
                        views,
                        currentViewKey,
                        currentViewTask,
                        galacticUnicorn,
                        graphics,
                    )
            else:
                buttonStates["B"] = False

            if galacticUnicorn.is_pressed(galacticUnicorn.SWITCH_C):
                if not buttonStates["C"]:
                    buttonStates["C"] = True
                    # Handle SWITCH_C
            else:
                buttonStates["C"] = False

            if galacticUnicorn.is_pressed(galacticUnicorn.SWITCH_D):
                if not buttonStates["D"]:
                    buttonStates["D"] = True
                    # Handle SWITCH_D
            else:
                buttonStates["D"] = False

            if galacticUnicorn.is_pressed(galacticUnicorn.SWITCH_VOLUME_UP):
                if not buttonStates["VOLUME_UP"]:
                    buttonStates["VOLUME_UP"] = True
                    # Turn the volume up
                    previous_volume = min(previous_volume + 0.1, 1.0)
                    galacticUnicorn.set_volume(previous_volume)
            else:
                buttonStates["VOLUME_UP"] = False

            if galacticUnicorn.is_pressed(galacticUnicorn.SWITCH_VOLUME_DOWN):
                if not buttonStates["VOLUME_DOWN"]:
                    buttonStates["VOLUME_DOWN"] = True
                    # Turn the volume down
                    previous_volume = max(previous_volume - 0.1, 0.0)
                    galacticUnicorn.set_volume(previous_volume)
            else:
                buttonStates["VOLUME_DOWN"] = False

            if galacticUnicorn.is_pressed(galacticUnicorn.SWITCH_BRIGHTNESS_UP):
                if not buttonStates["BRIGHTNESS_UP"]:
                    buttonStates["BRIGHTNESS_UP"] = True
                    # Turn the brightness up
                    current_brightness = galacticUnicorn.get_brightness()
                    if current_brightness < 0.1:
                        new_brightness = 0.25
                    else:
                        new_brightness = min(current_brightness + 0.25, 1.0)
                    galacticUnicorn.set_brightness(new_brightness)
            else:
                buttonStates["BRIGHTNESS_UP"] = False

            if galacticUnicorn.is_pressed(galacticUnicorn.SWITCH_BRIGHTNESS_DOWN):
                if not buttonStates["BRIGHTNESS_DOWN"]:
                    buttonStates["BRIGHTNESS_DOWN"] = True
                    # Turn the brightness down
                    current_brightness = galacticUnicorn.get_brightness()
                    new_brightness = max(current_brightness - 0.25, 0.1)
                    galacticUnicorn.set_brightness(new_brightness)
            else:
                buttonStates["BRIGHTNESS_DOWN"] = False

        if galacticUnicorn.is_pressed(galacticUnicorn.SWITCH_SLEEP):
            if not buttonStates["SLEEP"]:
                buttonStates["SLEEP"] = True
                # Power on/off the device
                if isDeviceOn:
                    # Simulate power off by setting brightness and volume to 0
                    previous_brightness = galacticUnicorn.get_brightness()
                    galacticUnicorn.set_brightness(0)
                    galacticUnicorn.set_volume(0)
                    graphics.set_pen(graphics.create_pen(0, 0, 0))
                    graphics.clear()
                    galacticUnicorn.update(graphics)
                    isDeviceOn = False
                else:
                    # Simulate power on by restoring the previous brightness and volume
                    galacticUnicorn.set_brightness(previous_brightness)
                    galacticUnicorn.set_volume(previous_volume)
                    isDeviceOn = True
        else:
            buttonStates["SLEEP"] = False

        # Sleep for a short period to debounce button presses
        await uasyncio.sleep(0.1)
