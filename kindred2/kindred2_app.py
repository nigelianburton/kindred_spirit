#!/usr/bin/env python3
"""
Kindred2 - Ethical Model Manager (Standalone)
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from PyQt6.QtCore import Qt, QUrl, QTimer
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QListWidget, QListWidgetItem, QPushButton, QGroupBox, QMessageBox,
    QFileDialog, QFrame
)


FILE_SPECS: List[Tuple[str, str]] = [
    ("Question set", "questions_with_perspectives.json"),
    ("User answers", "user_answers.json"),
    ("Synthetic Q&A", "synthetic_qa.json"),
    ("Root model", "root_model.safetensors"),
    ("Finetuned model", "finetuned_model.safetensors"),
]


@dataclass
class Settings:
    models_root: Path


class SettingsStore:
    def __init__(self, settings_path: Path):
        self.settings_path = settings_path

    def load(self) -> Settings:
        if self.settings_path.exists():
            try:
                data = json.loads(self.settings_path.read_text(encoding="utf-8"))
                root = Path(data.get("models_root", "")).expanduser()
                if root:
                    return Settings(models_root=root)
            except Exception:
                pass
        default_root = Path.home() / "Documents" / "KindredModels"
        settings = Settings(models_root=default_root)
        self.save(settings)
        return settings

    def save(self, settings: Settings) -> None:
        self.settings_path.parent.mkdir(parents=True, exist_ok=True)
        self.settings_path.write_text(
            json.dumps({"models_root": str(settings.models_root)}, indent=2),
            encoding="utf-8"
        )


class ModelManager:
    def __init__(self, models_root: Path):
        self.models_root = models_root
        self.models_root.mkdir(parents=True, exist_ok=True)

    def list_models(self) -> List[str]:
        if not self.models_root.exists():
            return []
        return sorted([p.name for p in self.models_root.iterdir() if p.is_dir()])

    def get_model_path(self, model_name: str) -> Path:
        return self.models_root / model_name


class Kindred2Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kindred2 - Ethical Model Manager")
        self.setMinimumSize(1100, 700)

        self.settings_store = SettingsStore(Path(__file__).with_name("settings.json"))
        self.settings = self.settings_store.load()
        self.model_manager = ModelManager(self.settings.models_root)

        self.selected_model: Optional[str] = None
        self.status_labels: Dict[str, QLabel] = {}

        self.setup_ui()
        self.refresh_models()

    def setup_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)
        central.setLayout(main_layout)

        # Left: model list
        left_panel = QGroupBox("Ethical Models")
        left_layout = QVBoxLayout()
        left_panel.setLayout(left_layout)

        self.models_list = QListWidget()
        self.models_list.itemSelectionChanged.connect(self.on_model_selected)
        left_layout.addWidget(self.models_list)

        self.new_model_button = QPushButton("Create New Ethical Model")
        self.new_model_button.setEnabled(False)
        left_layout.addWidget(self.new_model_button)

        main_layout.addWidget(left_panel, 2)

        # Right: details + actions
        right_panel = QVBoxLayout()

        details_group = QGroupBox("Model Details")
        details_layout = QVBoxLayout()
        details_group.setLayout(details_layout)

        self.model_path_label = QLabel("No model selected")
        self.model_path_label.setWordWrap(True)
        details_layout.addWidget(self.model_path_label)

        status_frame = QFrame()
        status_frame.setStyleSheet("background-color: #2b2b2b; border-radius: 6px; padding: 8px;")
        status_layout = QVBoxLayout()
        status_layout.setSpacing(6)
        status_frame.setLayout(status_layout)

        for label, filename in FILE_SPECS:
            row = QLabel(f"{label}: {filename}")
            row.setStyleSheet("color: #ffffff;")
            status_layout.addWidget(row)
            self.status_labels[filename] = row

        details_layout.addWidget(status_frame)
        right_panel.addWidget(details_group)

        actions_group = QGroupBox("Actions")
        actions_layout = QVBoxLayout()
        actions_group.setLayout(actions_layout)

        self.change_questions_button = QPushButton("Change Questions")
        self.change_questions_button.clicked.connect(self.open_questions_file)
        actions_layout.addWidget(self.change_questions_button)

        self.reanswer_button = QPushButton("Reanswer Questions")
        self.reanswer_button.clicked.connect(self.run_reanswer)
        actions_layout.addWidget(self.reanswer_button)

        self.speculate_button = QPushButton("Speculate Responses (Disabled)")
        self.speculate_button.setEnabled(False)
        actions_layout.addWidget(self.speculate_button)

        self.build_synth_button = QPushButton("Build/Rebuild Synthetic Answers")
        self.build_synth_button.clicked.connect(self.build_synthetic_answers)
        actions_layout.addWidget(self.build_synth_button)

        self.run_tune_button = QPushButton("Run/Rerun Tune")
        self.run_tune_button.clicked.connect(self.run_tuning)
        actions_layout.addWidget(self.run_tune_button)

        self.summarize_button = QPushButton("Summarize Results")
        self.summarize_button.clicked.connect(self.summarize_results)
        actions_layout.addWidget(self.summarize_button)

        right_panel.addWidget(actions_group)
        right_panel.addStretch(1)

        right_widget = QWidget()
        right_widget.setLayout(right_panel)
        main_layout.addWidget(right_widget, 3)

        self.set_action_buttons_enabled(False)
        self.setup_menu()

    def setup_menu(self) -> None:
        menu = self.menuBar().addMenu("File")

        change_root_action = menu.addAction("Change Models Folder...")
        change_root_action.triggered.connect(self.change_models_root)

        export_action = menu.addAction("Export GGUF (Q4/Q6/Q8)...")
        export_action.triggered.connect(self.export_gguf)

        refresh_action = menu.addAction("Refresh")
        refresh_action.triggered.connect(self.refresh_models)

        exit_action = menu.addAction("Exit")
        exit_action.triggered.connect(self.close)

    def set_action_buttons_enabled(self, enabled: bool) -> None:
        self.change_questions_button.setEnabled(enabled)
        self.reanswer_button.setEnabled(enabled)
        self.build_synth_button.setEnabled(enabled)
        self.run_tune_button.setEnabled(enabled)
        self.summarize_button.setEnabled(enabled)

    def refresh_models(self) -> None:
        self.models_list.clear()
        models = self.model_manager.list_models()
        for model_name in models:
            item = QListWidgetItem(model_name)
            self.models_list.addItem(item)
        self.selected_model = None
        self.model_path_label.setText("No model selected")
        self.set_action_buttons_enabled(False)
        self.update_status(None)

    def on_model_selected(self) -> None:
        items = self.models_list.selectedItems()
        if not items:
            self.selected_model = None
            self.model_path_label.setText("No model selected")
            self.set_action_buttons_enabled(False)
            self.update_status(None)
            return
        self.selected_model = items[0].text()
        model_path = self.model_manager.get_model_path(self.selected_model)
        self.model_path_label.setText(str(model_path))
        self.set_action_buttons_enabled(True)
        self.update_status(model_path)

    def update_status(self, model_path: Optional[Path]) -> None:
        for _, filename in FILE_SPECS:
            label = self.status_labels[filename]
            if not model_path:
                label.setStyleSheet("color: #ffffff;")
                continue
            file_path = model_path / filename
            exists = file_path.exists() and file_path.is_file() and file_path.stat().st_size > 0
            color = "#8be28b" if exists else "#ffffff"
            label.setStyleSheet(f"color: {color};")

    def change_models_root(self) -> None:
        new_root = QFileDialog.getExistingDirectory(
            self,
            "Select Models Folder",
            str(self.settings.models_root)
        )
        if not new_root:
            return
        new_root_path = Path(new_root).expanduser()
        current_root = self.settings.models_root
        if new_root_path == current_root:
            return

        move_existing = False
        existing_models = self.model_manager.list_models()
        if existing_models:
            reply = QMessageBox.question(
                self,
                "Move Existing Models?",
                "Move existing model folders to the new location?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            move_existing = reply == QMessageBox.StandardButton.Yes

        new_root_path.mkdir(parents=True, exist_ok=True)

        if move_existing:
            for model_name in existing_models:
                src = current_root / model_name
                dst = new_root_path / model_name
                try:
                    if dst.exists():
                        QMessageBox.warning(
                            self,
                            "Move Skipped",
                            f"Destination already has {model_name}. Skipping move for this model."
                        )
                        continue
                    shutil.move(str(src), str(dst))
                except Exception as exc:
                    QMessageBox.warning(
                        self,
                        "Move Failed",
                        f"Failed to move {model_name}: {exc}"
                    )

        self.settings.models_root = new_root_path
        self.settings_store.save(self.settings)
        self.model_manager = ModelManager(self.settings.models_root)
        self.refresh_models()

    def get_selected_model_path(self) -> Optional[Path]:
        if not self.selected_model:
            return None
        return self.model_manager.get_model_path(self.selected_model)

    def open_questions_file(self) -> None:
        model_path = self.get_selected_model_path()
        if not model_path:
            return
        questions_path = model_path / "questions_with_perspectives.json"
        if not questions_path.exists():
            QMessageBox.warning(
                self,
                "Missing Questions",
                f"Questions file not found:\n{questions_path}"
            )
            return
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(questions_path)))

    def run_reanswer(self) -> None:
        model_path = self.get_selected_model_path()
        if not model_path:
            return
        questions_path = model_path / "questions_with_perspectives.json"
        output_path = model_path / "user_answers.json"
        if not questions_path.exists():
            QMessageBox.warning(
                self,
                "Missing Questions",
                f"Questions file not found:\n{questions_path}"
            )
            return

        script_path = Path(__file__).with_name("1_calibrate_kindred_spirit_qt.py")
        args = [
            sys.executable,
            str(script_path),
            "--questions", str(questions_path),
            "--output", str(output_path),
            "--title", f"Kindred2 Calibration - {self.selected_model}"
        ]
        try:
            subprocess.Popen(args, cwd=str(Path(__file__).parent))
        except Exception as exc:
            QMessageBox.critical(self, "Launch Failed", f"Failed to launch calibration:\n{exc}")

    def build_synthetic_answers(self) -> None:
        model_path = self.get_selected_model_path()
        if not model_path:
            return
        user_answers = model_path / "user_answers.json"
        if not user_answers.exists() or user_answers.stat().st_size == 0:
            QMessageBox.warning(
                self,
                "Missing User Answers",
                f"User answers not found:\n{user_answers}"
            )
            return
        output_path = model_path / "synthetic_qa.json"
        script_path = Path(__file__).with_name("synthetic_generate.py")
        args = [
            sys.executable,
            str(script_path),
            "--user-answers", str(user_answers),
            "--output", str(output_path),
        ]
        try:
            subprocess.Popen(args, cwd=str(Path(__file__).parent))
            QMessageBox.information(
                self,
                "Synthetic Generation Started",
                "Synthetic Q&A generation started in a new process."
            )
        except Exception as exc:
            QMessageBox.critical(self, "Build Failed", f"Failed to start synthetic generation:\n{exc}")

    def run_tuning(self) -> None:
        model_path = self.get_selected_model_path()
        if not model_path:
            return
        synthetic_path = model_path / "synthetic_qa.json"
        if not synthetic_path.exists() or synthetic_path.stat().st_size == 0:
            QMessageBox.warning(
                self,
                "Missing Synthetic Q&A",
                f"Synthetic Q&A not found:\n{synthetic_path}"
            )
            return

        script_path = Path(__file__).with_name("train_adapter.py")
        output_dir = model_path / "finetuned_adapter"
        args = [
            sys.executable,
            str(script_path),
            "--model-folder", str(model_path),
            "--output-dir", str(output_dir),
        ]
        try:
            subprocess.Popen(args, cwd=str(Path(__file__).parent))
            QMessageBox.information(
                self,
                "Training Started",
                "Training started in a new process."
            )
        except Exception as exc:
            QMessageBox.critical(self, "Training Failed", f"Failed to start training:\n{exc}")

    def summarize_results(self) -> None:
        model_path = self.get_selected_model_path()
        if not model_path:
            return
        user_answers = model_path / "user_answers.json"
        if not user_answers.exists() or user_answers.stat().st_size == 0:
            QMessageBox.warning(
                self,
                "Missing User Answers",
                f"User answers not found:\n{user_answers}"
            )
            return
        try:
            data = json.loads(user_answers.read_text(encoding="utf-8"))
            responses = data.get("responses", [])
            total = len(responses)
            counts = {"A": 0, "B": 0}
            for item in responses:
                choice = item.get("choice")
                if choice in counts:
                    counts[choice] += 1
            summary = (
                f"Total responses: {total}\n"
                f"Choice A: {counts['A']}\n"
                f"Choice B: {counts['B']}\n"
            )
            QMessageBox.information(self, "Summary", summary)
        except Exception as exc:
            QMessageBox.critical(self, "Summary Failed", f"Failed to summarize results:\n{exc}")

    def export_gguf(self) -> None:
        model_path = self.get_selected_model_path()
        if not model_path:
            QMessageBox.information(self, "No Model Selected", "Select an ethical model first.")
            return

        finetuned_adapter = model_path / "finetuned_adapter"
        if not finetuned_adapter.exists():
            QMessageBox.warning(
                self,
                "Missing Adapter",
                "No finetuned_adapter folder found. Run training first."
            )
            return

        msg = QMessageBox(self)
        msg.setWindowTitle("Export GGUF")
        msg.setText("Choose a GGUF quantization preset")
        q4_btn = msg.addButton("Q4 (small/fast)", QMessageBox.ButtonRole.AcceptRole)
        q6_btn = msg.addButton("Q6 (balanced)", QMessageBox.ButtonRole.AcceptRole)
        q8_btn = msg.addButton("Q8 (highest quality)", QMessageBox.ButtonRole.AcceptRole)
        msg.addButton("Cancel", QMessageBox.ButtonRole.RejectRole)
        msg.exec()

        clicked = msg.clickedButton()
        if clicked is None or clicked.text() == "Cancel":
            return

        quant = "Q4_K_M"
        if clicked == q6_btn:
            quant = "Q6_K"
        elif clicked == q8_btn:
            quant = "Q8_0"

        script_path = Path(__file__).with_name("convert_to_gguf.py")
        args = [
            sys.executable,
            str(script_path),
            "--model-folder", str(model_path),
            "--quant", quant,
        ]
        try:
            subprocess.Popen(args, cwd=str(Path(__file__).parent))
            QMessageBox.information(
                self,
                "Export Started",
                "GGUF export started in a new process."
            )
        except Exception as exc:
            QMessageBox.critical(self, "Export Failed", f"Failed to start export:\n{exc}")


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Kindred2 - Ethical Model Manager")
    parser.add_argument("--timeout", type=int, default=None, help="Auto-exit after N seconds")
    return parser.parse_args(argv)


def main() -> None:
    args = parse_args(sys.argv[1:])
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = Kindred2Window()
    window.show()

    if args.timeout is not None:
        QTimer.singleShot(max(0, args.timeout) * 1000, app.quit)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
