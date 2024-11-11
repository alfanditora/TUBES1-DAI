import flet as ft
import time
import threading
import os
from MagicCube import MagicCube
from typing import List, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class VisualizerConfig:
    default_speed: float = 1.0
    min_speed: float = 0.1
    max_speed: float = 2.0
    speed_steps: int = 19
    cube_size: int = 200
    cell_size: int = 40
    spacing: int = 2

class Visualizer:
    def __init__(self, config: Optional[VisualizerConfig] = None):
        self.config = config or VisualizerConfig()
        self.list_of_magiccube: List[MagicCube] = []
        self.current_index: int = 0
        self.is_playing: bool = False
        self.is_reverse: bool = False
        self.speed: float = self.config.default_speed
        self.page: Optional[ft.Page] = None
        self.layer = None
        self.progress_slider = None
        self.play_button = None
        self.playback_button = None
        self.prev_button = None
        self.next_button = None
        self.reset_button = None
        self.iteration_information = None
        self.value_information = None
        self.speed_information = None
        self.file_path_text = None
        self.pick_files_dialog = None

    def load_file(self, filename: str) -> bool:
        try:
            self.show_loading_dialog("Loading file...")
            directory = ".\\save_file"
            filepath = os.path.join(directory, filename)

            with open(filepath, 'r') as file:
                content = file.read()
                states = content.strip().split(';')
                self.list_of_magiccube = []
                
                for state in states:
                    if state.strip():
                        cube = MagicCube()
                        rows = state.strip().split('\n')
                        for i, row in enumerate(rows):
                            numbers = [int(num) for num in row.strip().split()]
                            for j in range(cube.size):
                                for k in range(cube.size):
                                    cube.cube[i][j][k] = numbers[j * cube.size + k]
                        self.list_of_magiccube.append(MagicCube(cube.cube))

                self.current_index = 0
                self.is_playing = False
                self.is_reverse = False
                self.update_controls()
                self.hide_loading_dialog()
                return True

        except Exception as e:
            self.show_error_dialog(f"Error loading file: {str(e)}")
            return False

    def show_error_dialog(self, message: str) -> None:
        def close_dialog(e):
            dialog.open = False
            self.page.update()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Error"),
            content=ft.Text(message),
            actions=[ft.TextButton("OK", on_click=close_dialog)],
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def show_loading_dialog(self, message: str) -> None:
        def close_dialog(e):
            dialog.open = False
            self.page.update()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Loading"),
            content=ft.Column([
                ft.Text(message),
                ft.ProgressRing(),
            ]),
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def hide_loading_dialog(self) -> None:
        if self.page and self.page.dialog:
            self.page.dialog.open = False
            self.page.update()

    def update_controls(self) -> None:
        if not self.page:
            return

        self.play_button.disabled = not self.list_of_magiccube
        self.playback_button.disabled = not self.list_of_magiccube
        self.reset_button.disabled = not self.list_of_magiccube
        self.prev_button.disabled = self.current_index <= 0
        self.next_button.disabled = self.current_index >= len(self.list_of_magiccube) - 1
        self.progress_slider.disabled = not self.list_of_magiccube

        if self.list_of_magiccube:
            self.progress_slider.max = len(self.list_of_magiccube) - 1
            self.progress_slider.value = self.current_index

        for control in [self.play_button, self.playback_button, self.reset_button,
                       self.prev_button, self.next_button, self.progress_slider]:
            control.update()

    def pick_files_result(self, e: ft.FilePickerResultEvent) -> None:
        if e.files:
            file_path = e.files[0].path
            filename = os.path.basename(file_path)
            if self.load_file(filename):
                self.file_path_text.value = f"Loaded: {filename}"
                self.file_path_text.update()
                self.update_controls()

    def progress_changed(self, e) -> None:
        self.current_index = int(e.control.value)
        self.update_visualization(self.list_of_magiccube[self.current_index])

    def create_face(self, numbers: List[List[int]], offset_x: int, offset_y: int,
                   color: str) -> ft.Container:
        return ft.Container(
            width=self.config.cube_size,
            height=self.config.cube_size,
            left=offset_x,
            top=offset_y,
            border=ft.border.all(2, ft.colors.BLACK),
            bgcolor=color,
            content=ft.Column(
                spacing=self.config.spacing,
                controls=[
                    ft.Row(
                        spacing=self.config.spacing,
                        controls=[
                            ft.Container(
                                width=self.config.cell_size - self.config.spacing,
                                height=self.config.cell_size - self.config.spacing,
                                border=ft.border.all(1, ft.colors.BLACK),
                                content=ft.Text(
                                    str(numbers[i][j]),
                                    size=16,
                                    weight=ft.FontWeight.BOLD,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                alignment=ft.alignment.center,
                                bgcolor=ft.colors.WHITE10,
                            ) for j in range(5)
                        ],
                    ) for i in range(5)
                ]
            ),
        )

    def update_visualization(self, magic_cube: MagicCube) -> None:
        if not self.page:
            return

        layers = [[[magic_cube.cube[k][i][j] for j in range(5)]
                  for i in range(5)] for k in range(5)]
        cube_size = self.config.cube_size
        colors = [ft.colors.GREEN_50, ft.colors.ORANGE_50, ft.colors.RED_50,
                 ft.colors.PURPLE_50, ft.colors.YELLOW_50]

        faces = [self.create_face(layers[i], cube_size * i, 0, colors[i])
                for i in range(5)]

        self.layer.controls = faces
        self.iteration_information.value = f"Iteration: {self.current_index + 1}/{len(self.list_of_magiccube)}"
        self.value_information.value = f"Value: {magic_cube.value}"
        self.layer.update()
        self.iteration_information.update()
        self.value_information.update()
        self.update_controls()

    def play_sequence(self) -> None:
        while self.is_playing:
            time.sleep(self.speed)
            if self.is_reverse:
                if self.current_index > 0:
                    self.current_index -= 1
                    self.progress_slider.value = self.current_index
                    self.progress_slider.update()
                    self.update_visualization(self.list_of_magiccube[self.current_index])
                else:
                    self.is_playing = False
                    self.play_button.text = "Play Forward"
                    self.play_button.update()
            else:
                if self.current_index < len(self.list_of_magiccube) - 1:
                    self.current_index += 1
                    self.progress_slider.value = self.current_index
                    self.progress_slider.update()
                    self.update_visualization(self.list_of_magiccube[self.current_index])
                else:
                    self.is_playing = False
                    self.play_button.text = "Play Forward"
                    self.play_button.update()

    def setup_controls(self) -> None:
        self.play_button = ft.ElevatedButton(
            text="Play Forward",
            on_click=lambda _: self.play_button_clicked(),
            disabled=True
        )
        self.playback_button = ft.ElevatedButton(
            text="Play Backward",
            on_click=lambda _: self.playback_button_clicked(),
            disabled=True
        )
        self.reset_button = ft.ElevatedButton(
            text="Reset",
            on_click=lambda _: self.reset_button_clicked(),
            disabled=True
        )
        self.prev_button = ft.IconButton(
            icon=ft.icons.ARROW_BACK,
            on_click=lambda _: self.prev_button_clicked(),
            disabled=True
        )
        self.next_button = ft.IconButton(
            icon=ft.icons.ARROW_FORWARD,
            on_click=lambda _: self.next_button_clicked(),
            disabled=True
        )
        self.progress_slider = ft.Slider(
            min=0,
            max=0,
            value=0,
            divisions=None,
            label="{value}",
            on_change=self.progress_changed,
            disabled=True
        )

    def play_button_clicked(self) -> None:
        self.is_playing = not self.is_playing
        self.is_reverse = False
        self.play_button.text = "Pause" if self.is_playing else "Play Forward"
        self.play_button.update()
        if self.is_playing:
            threading.Thread(target=self.play_sequence, daemon=True).start()

    def playback_button_clicked(self) -> None:
        self.is_playing = not self.is_playing
        self.is_reverse = True
        self.playback_button.text = "Pause" if self.is_playing else "Play Backward"
        self.playback_button.update()
        if self.is_playing:
            threading.Thread(target=self.play_sequence, daemon=True).start()

    def next_button_clicked(self) -> None:
        if self.current_index < len(self.list_of_magiccube) - 1:
            self.current_index += 1
            self.update_visualization(self.list_of_magiccube[self.current_index])

    def prev_button_clicked(self) -> None:
        if self.current_index > 0:
            self.current_index -= 1
            self.update_visualization(self.list_of_magiccube[self.current_index])

    def reset_button_clicked(self) -> None:
        self.is_playing = False
        self.is_reverse = False
        self.current_index = 0
        self.play_button.text = "Play Forward"
        self.playback_button.text = "Play Backward"
        self.play_button.update()
        self.playback_button.update()
        self.progress_slider.value = 0
        self.progress_slider.update()
        self.update_visualization(self.list_of_magiccube[self.current_index])

    def speed_changed(self, e) -> None:
        self.speed = float(e.control.value)
        self.speed_information.value = f"Speed: {self.speed:.1f}s"
        self.speed_information.update()

    def setup_ui(self) -> None:
        self.pick_files_dialog = ft.FilePicker(on_result=self.pick_files_result)
        self.page.overlay.append(self.pick_files_dialog)

        title = ft.Text(
            "Magic Cube Sequence Visualization",
            size=24,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER
        )
        file_section = self.create_file_section()
        main_content = self.create_main_content()
        controls = self.create_controls_section()

        content = ft.Column(
            controls=[title, file_section, main_content, controls],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )
        self.page.add(content)

    def main(self, page: ft.Page) -> None:
        self.page = page
        self.page.title = "Magic Cube Sequence Visualization"
        self.page.padding = 50
        self.page.theme_mode = "light"

        self.setup_controls()
        self.setup_ui()

    def visualize(self) -> None:
        ft.app(target=self.main)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    visualizer = Visualizer()
    visualizer.visualize()