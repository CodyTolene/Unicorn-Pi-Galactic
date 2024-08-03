# Cody Tolene
# Apache License 2.0

import uasyncio
import json


class ViewManager:
    def __init__(self, view_index_file="/current_view.json"):
        self.view_index_file = view_index_file
        self.current_view_key = self.load_current_view_index()

    def save_current_view_index(self, key):
        with open(self.view_index_file, "w") as f:
            json.dump({"current_view_key": key}, f)

    def load_current_view_index(self):
        try:
            with open(self.view_index_file, "r") as f:
                data = json.load(f)
                return data.get("current_view_key", "Rainbow")
        except OSError:
            return "Rainbow"

    async def switch_view(
        self, views, current_view_task, galactic_unicorn, graphics, sound_service
    ):
        if current_view_task:
            current_view_task.cancel()
            try:
                await current_view_task
            except uasyncio.CancelledError:
                pass

        # Clear the screen
        graphics.set_pen(0)  # Black
        graphics.clear()
        galactic_unicorn.update(graphics)
        self.save_current_view_index(self.current_view_key)
        current_view_task = uasyncio.create_task(
            views[self.current_view_key](galactic_unicorn, graphics, sound_service)
        )
        return current_view_task
