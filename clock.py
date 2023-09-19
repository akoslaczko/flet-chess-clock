import flet as ft
import time
from datetime import timedelta
from helpers import format_timedelta


# The global refresh rate in seconds
REFRESH_RATE = 0.01

# Visual defaults
CLOCK_COLOR = ft.colors.BROWN_300
ACTIVE_COLOR = ft.colors.AMBER_100
DISABLED_COLOR = ft.colors.GREY_400


class ButtonControl(ft.UserControl):

    def __init__(self, init_time=1, on_click=None, *args, **kwargs):
        super(ButtonControl, self).__init__(*args, **kwargs)
        # Defining functional attributes
        self.press_count = 0
        self.time_remaining = timedelta(minutes=init_time)
        self.on_click=on_click
        # Defining visuals
        self.expand = True
        self.container = ft.Container(
            expand=True,
            bgcolor=self.button_color,
            border_radius=ft.border_radius.all(20),
            padding=20,
            on_click=self.on_click,
            content=ft.Column(
                expand=True,
                controls=[
                    ft.Row(
                        expand=True,
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            self.button_text,
                        ]
                    )
                ]
            )
        )
  
    @property
    def time_remaining_text(self):
        return format_timedelta(self.time_remaining)
    
    @property
    def time_remaining_color(self):
        if self.time_remaining <= timedelta(0):
            return ft.colors.RED
        else:
            return ft.colors.BLACK
        
    @property
    def is_flagged(self):
        if self.time_remaining <= timedelta(0):
            return True
        else:
            return False
        
    @property
    def button_text(self):
        return ft.Text(self.time_remaining_text, color=self.time_remaining_color, scale=5)

    @property
    def button_color(self):
        if self.disabled:
            return DISABLED_COLOR
        else:
            return ACTIVE_COLOR

    def build(self):
        return self.container

    def toggle_button(self):
        self.disabled = not self.disabled
        if self.disabled:
            self.press_count += 1
            self.container.bgcolor = DISABLED_COLOR
        else:
            self.container.bgcolor = ACTIVE_COLOR
        self.update()

    def refresh_time(self):
        if not self.disabled:
            self.time_remaining -= timedelta(seconds=REFRESH_RATE)
            self.container.content.controls[0].controls[0] = self.button_text  #Ez mocsok randa, de csak így frissül be a rohadék
        self.update()


class ClockControl(ft.UserControl):

    def __init__(self, *args, **kwargs):
        super(ClockControl, self).__init__(*args, **kwargs)
        # Defining functional attributes
        self.is_running = False
        # Instancing controls
        self.player_1_button = ButtonControl(
            disabled=True,
            on_click=self.switch_side,
        )
        self.player_2_button = ButtonControl(
            disabled=False,
            on_click=self.switch_side,
        )
        # Defining visuals
        self.expand = True
        self.container = ft.Container(
            expand=True,
            bgcolor=CLOCK_COLOR,
            border_radius=ft.border_radius.all(20),
            padding=20,
            content=ft.Row(
                expand=True,
                controls=[
                    self.player_1_button,
                    self.player_2_button,
                ]
            )
        )

    def build(self):
        return self.container
    
    def switch_side(self, e):
        # Only switch is neither player is flagged
        if sum([self.player_1_button.is_flagged, self.player_2_button.is_flagged]) == 0:
            self.player_1_button.toggle_button()
            self.player_2_button.toggle_button()
            # Start the clock if it's not running
            if not self.is_running:
                self.is_running = True
        self.update()

    def refresh(self):
        # Stop the clock if either player is flagged
        if self.player_1_button.is_flagged or self.player_2_button.is_flagged:
            self.is_running = False
        # Else recompute remaining times
        else:
            self.player_1_button.refresh_time()
            self.player_2_button.refresh_time()
        self.update()

def main(page: ft.Page):
    page.title = "FletChessClock"

    # create application instance
    clock = ClockControl()

    # add application's root control to the page
    page.add(clock)

    while True:
        time.sleep(REFRESH_RATE)
        if clock.is_running:
            clock.refresh()
        page.update()
    

ft.app(target=main)
