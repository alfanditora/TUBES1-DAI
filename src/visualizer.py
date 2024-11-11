import flet as ft
import time
import threading
import os
from MagicCube import MagicCube

class Visualizer:
    def __init__(self):
        self.list_of_magiccube = []
        self.current_index = 0
        self.is_playing = False
        self.is_reverse = False
        self.speed = 1.0
        self.page = None
        
    def load_file(self, filename):
        try:
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
                
                if self.page:
                    self.update_visualization(self.list_of_magiccube[0])
                    self.file_path_text.value = f"Loaded: {filename}"
                    self.file_path_text.update()

                    self.progress_slider.max = len(self.list_of_magiccube) - 1
                    self.progress_slider.value = 0
                    self.progress_slider.disabled = False
                    self.progress_slider.update()
                
                return True
                        
        except FileNotFoundError:
            if self.page:
                self.show_error_dialog(f"File {filename} not found")
            return False
        except Exception as e:
            if self.page:
                self.show_error_dialog(f"Error occurred: {str(e)}")
            return False

    def show_error_dialog(self, message):
        def close_dialog(e):
            dialog.open = False
            self.page.update()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Error"),
            content=ft.Text(message),
            actions=[
                ft.TextButton("OK", on_click=close_dialog),
            ],
        )

        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def pick_files_result(self, e: ft.FilePickerResultEvent):
        if e.files:
            file_path = e.files[0].path
            filename = os.path.basename(file_path)
            success = self.load_file(filename)
            
            if success:
                self.play_button.disabled = False
                self.playback_button.disabled = False
                self.reset_button.disabled = False
                self.prev_button.disabled = self.current_index <= 0
                self.next_button.disabled = self.current_index >= len(self.list_of_magiccube) - 1
                self.progress_slider.disabled = False
                
                self.play_button.update()
                self.playback_button.update()
                self.reset_button.update()
                self.prev_button.update()
                self.next_button.update()
                self.progress_slider.update()
    
    def progress_changed(self, e):
        self.current_index = int(e.control.value)
        self.update_visualization(self.list_of_magiccube[self.current_index])

    def create_face(self, numbers, offset_x, offset_y, color, cube_size=200):
        cell_size = cube_size / 5 
        spacing = 2
        
        face = ft.Container(
            width=cube_size,
            height=cube_size,
            left=offset_x,
            top=offset_y,
            border=ft.border.all(2, ft.colors.BLACK),
            bgcolor=color,
            content=ft.Column(
                spacing=spacing,
                controls=[
                    ft.Row(
                        spacing=spacing,
                        controls=[
                            ft.Container(
                                width=cell_size - spacing,
                                height=cell_size - spacing,
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
        return face

    def update_visualization(self, magic_cube):
        if not self.page:
            return
            
        # Layer state
        layers = [
            [[magic_cube.cube[k][i][j] for j in range(5)] for i in range(5)]
            for k in range(5)
        ]
        
        # position
        cube_size = 200
        mid_x = cube_size
        
        # Create faces with different colors
        colors = [ft.colors.GREEN_50, ft.colors.ORANGE_50, ft.colors.RED_50, 
                 ft.colors.PURPLE_50, ft.colors.YELLOW_50]
        
        faces = [
            self.create_face(layers[i], mid_x * i, 0, colors[i])
            for i in range(5)
        ]

        # Update layer
        self.layer.controls = faces
        
        # Update iteration information
        self.iteration_information.value = f"Iteration: {self.current_index + 1}/{len(self.list_of_magiccube)}"
        self.iteration_information.update()
        
        # Update value information
        self.value_information.value = f"Value: {magic_cube.value}"
        self.value_information.update()

        # Update nav button
        self.prev_button.disabled = self.current_index <= 0
        self.next_button.disabled = self.current_index >= len(self.list_of_magiccube) - 1
        self.prev_button.update()
        self.next_button.update()
        
        self.layer.update()

    def play_sequence(self):
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

    def play_button_clicked(self, e):
        self.is_playing = not self.is_playing
        self.is_reverse = False
        e.control.text = "Pause" if self.is_playing else "Play Forward"
        e.control.update()
        
        if self.is_playing:
            threading.Thread(target=self.play_sequence, daemon=True).start()

    def playback_button_clicked(self, e):
        self.is_playing = not self.is_playing
        self.is_reverse = True
        e.control.text = "Pause" if self.is_playing else "Play Backward"
        e.control.update()
        
        if self.is_playing:
            threading.Thread(target=self.play_sequence, daemon=True).start()

    def next_button_clicked(self, e):
        if self.current_index < len(self.list_of_magiccube) - 1:
            self.current_index += 1
            self.update_visualization(self.list_of_magiccube[self.current_index])

    def prev_button_clicked(self, e):
        if self.current_index > 0:
            self.current_index -= 1
            self.update_visualization(self.list_of_magiccube[self.current_index])

    def reset_button_clicked(self, e):
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

    def speed_changed(self, e):
        self.speed = float(e.control.value)
        self.speed_information.value = f"Speed: {self.speed:.1f}s"
        self.speed_information.update()

    def main(self, page: ft.Page):
        self.page = page
        page.title = "Magic Cube Sequence Visualization"
        page.padding = 50
        page.theme_mode = "light"
        
        self.pick_files_dialog = ft.FilePicker(
            on_result=self.pick_files_result
        )
        
        self.file_path_text = ft.Text(
            "No file loaded",
            size=14,
            color=ft.colors.GREY_700
        )
        
        load_file_button = ft.ElevatedButton(
            "Load File",
            icon=ft.icons.UPLOAD_FILE,
            on_click=lambda _: self.pick_files_dialog.pick_files(
                allow_multiple=False,
                allowed_extensions=["txt"]
            )
        )
        
        file_section = ft.Row(
            controls=[
                load_file_button,
                self.file_path_text
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
        
        page.overlay.append(self.pick_files_dialog)
        
        title = ft.Text(
            "Magic Cube Sequence Visualization",
            size=24,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER
        )
        
        # Info
        self.iteration_information = ft.Text(
            f"Iteration: 0/0",
            size=16,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
        )
        
        self.value_information = ft.Text(
            f"Value: 0",
            size=16,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
        )
        
        # Layer
        self.layer = ft.Stack(
            width=200 * 5,
            height=200,
        )
        
        # Progress slider
        self.progress_slider = ft.Slider(
            min=0,
            max=0,
            value=0,
            divisions=None,
            label="{value}",
            on_change=self.progress_changed,
            disabled=True
        )
        
        progress_container = ft.Container(
            content=self.progress_slider,
            padding=ft.padding.symmetric(horizontal=20),
            width=600
        )
        
        # Nav button
        self.prev_button = ft.IconButton(
            icon=ft.icons.ARROW_BACK,
            on_click=self.prev_button_clicked,
            disabled=True
        )
        
        self.next_button = ft.IconButton(
            icon=ft.icons.ARROW_FORWARD,
            on_click=self.next_button_clicked,
            disabled=True
        )
        
        self.play_button = ft.ElevatedButton(
            text="Play Forward",
            on_click=self.play_button_clicked,
            disabled=True
        )
        
        self.playback_button = ft.ElevatedButton(
            text="Play Backward",
            on_click=self.playback_button_clicked,
            disabled=True
        )
        
        self.reset_button = ft.ElevatedButton(
            text="Reset",
            on_click=self.reset_button_clicked,
            disabled=True
        )
        
        self.speed_information = ft.Text(f" Playing Speed: {self.speed:.1f}s")
        speed_slider = ft.Slider(
            min=0.1,
            max=2.0,
            value=self.speed,
            divisions=19,
            label="{value}s",
            on_change=self.speed_changed
        )
        
        navigation = ft.Row(
            controls=[
                self.prev_button,
                self.next_button,
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
        
        controls = ft.Row(
            controls=[
                self.playback_button,
                self.play_button,
                self.reset_button,
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
        
        anim_speed = ft.Row(
            controls=[
                speed_slider,
                self.speed_information
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
        
        layer_information = ft.Row(
            controls=[
                ft.Text("Layer 1", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.GREEN),
                ft.Text("Layer 2", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.ORANGE),
                ft.Text("Layer 3", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.RED),
                ft.Text("Layer 4", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.PURPLE),
                ft.Text("Layer 5", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.YELLOW_600),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20
        )
        
        content = ft.Column(
            controls=[
                title,
                file_section,
                self.iteration_information,
                self.value_information,
                self.layer,
                progress_container,
                navigation,
                controls,
                anim_speed,
                layer_information,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )
        
        page.add(content)

    def visualize(self):
        ft.app(target=self.main)