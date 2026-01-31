#!/usr/bin/env python3
"""
Kindred Spirit Calibration - Qt GUI

A visual interface to discover your actual values through 74 calibration questions,
each presented with two historical perspectives showing genuine philosophical disagreement.

Features:
- Progress bar showing current question and overall progress
- Two-column view showing opposing perspectives with quotes
- Yes/No selection with confidence levels (25%, 50%, 75%, 99%)
- Summary view of all responses at completion

Outputs: {username}_kindred_spirit.json
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QProgressBar, QTextEdit, QListWidget,
    QListWidgetItem, QFrame, QScrollArea, QButtonGroup, QMessageBox
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon


class CalibrationQuestion:
    """Represents a single calibration question with perspectives"""
    def __init__(self, data: Dict):
        self.id = data['id']
        self.phase = data['phase']
        self.question = data['question']
        self.option_a = data['option_a']
        self.option_b = data['option_b']
        self.perspective_for = data['perspective_for']
        self.perspective_against = data['perspective_against']


class UserResponse:
    """Stores user's response to a question"""
    def __init__(self, question_id: str, question_text: str, 
                 choice: str, confidence: int):
        self.question_id = question_id
        self.question_text = question_text
        self.choice = choice  # 'A' or 'B'
        self.confidence = confidence  # 25, 50, 75, or 99
        self.timestamp = datetime.now().isoformat()


class PerspectiveCard(QFrame):
    """A card displaying one perspective with person, quote, and source"""
    def __init__(self, perspective: Dict, option_label: str, option_text: str):
        super().__init__()
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Raised)
        self.setLineWidth(2)
        self.setup_ui(perspective, option_label, option_text)
    
    def setup_ui(self, perspective: Dict, option_label: str, option_text: str):
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Option label and text
        option_header = QLabel(f"<b>{option_label}: {option_text}</b>")
        option_header.setWordWrap(True)
        option_header.setStyleSheet("color: #2C5AA0; font-size: 14pt;")
        layout.addWidget(option_header)
        
        # Person name and details
        person = perspective['person']
        years = perspective['years']
        role = perspective['role']
        
        person_label = QLabel(f"<b>{person}</b> ({years})")
        person_label.setStyleSheet("font-size: 12pt; color: #1a1a1a;")
        layout.addWidget(person_label)
        
        role_label = QLabel(role)
        role_label.setStyleSheet("font-size: 10pt; color: #555555; font-style: italic;")
        role_label.setWordWrap(True)
        layout.addWidget(role_label)
        
        # Quote
        quote_text = QTextEdit()
        quote_text.setReadOnly(True)
        quote_text.setPlainText(f'"{perspective["quote"]}"')
        quote_text.setStyleSheet("""
            QTextEdit {
                background-color: #f5f5f5;
                border: 1px solid #cccccc;
                border-radius: 5px;
                padding: 10px;
                font-size: 11pt;
                color: #333333;
            }
        """)
        quote_text.setMinimumHeight(150)
        quote_text.setMaximumHeight(300)
        layout.addWidget(quote_text)
        
        layout.addStretch()
        self.setLayout(layout)


class QuestionView(QWidget):
    """Main view for displaying a question with perspectives and answer options"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_question: Optional[CalibrationQuestion] = None
        self.selected_choice: Optional[str] = None
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Toolbar: Question number, text, and progress bar
        toolbar = QFrame()
        toolbar.setFrameStyle(QFrame.Shape.StyledPanel)
        toolbar.setStyleSheet("background-color: #f0f0f0; border-radius: 8px;")
        toolbar_layout = QVBoxLayout()
        toolbar_layout.setContentsMargins(15, 15, 15, 15)
        
        # Question number
        self.question_number_label = QLabel("Question 1 of 74")
        self.question_number_label.setStyleSheet("font-size: 11pt; font-weight: bold; color: #555555;")
        toolbar_layout.addWidget(self.question_number_label)
        
        # Question text
        self.question_label = QLabel()
        self.question_label.setWordWrap(True)
        self.question_label.setStyleSheet("font-size: 14pt; font-weight: bold; color: #1a1a1a; padding: 5px 0;")
        toolbar_layout.addWidget(self.question_label)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(74)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #cccccc;
                border-radius: 5px;
                text-align: center;
                height: 25px;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                border-radius: 3px;
            }
        """)
        toolbar_layout.addWidget(self.progress_bar)
        
        toolbar.setLayout(toolbar_layout)
        layout.addWidget(toolbar)
        
        # Perspectives row (two columns)
        perspectives_container = QWidget()
        perspectives_layout = QHBoxLayout()
        perspectives_layout.setSpacing(15)
        
        # Left perspective (perspective_for / Option A)
        self.left_card = QFrame()
        self.left_card.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Raised)
        perspectives_layout.addWidget(self.left_card)
        
        # Right perspective (perspective_against / Option B)
        self.right_card = QFrame()
        self.right_card.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Raised)
        perspectives_layout.addWidget(self.right_card)
        
        perspectives_container.setLayout(perspectives_layout)
        
        # Wrap perspectives in scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidget(perspectives_container)
        scroll_area.setWidgetResizable(True)
        scroll_area.setMinimumHeight(400)
        layout.addWidget(scroll_area, stretch=1)
        
        # Answer buttons section
        answer_frame = QFrame()
        answer_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        answer_frame.setStyleSheet("background-color: #fafafa; border-radius: 8px;")
        answer_layout = QVBoxLayout()
        answer_layout.setContentsMargins(15, 15, 15, 15)
        answer_layout.setSpacing(15)
        
        # Yes/No buttons
        choice_label = QLabel("<b>Your Answer:</b>")
        choice_label.setStyleSheet("font-size: 12pt;")
        answer_layout.addWidget(choice_label)
        
        choice_buttons_layout = QHBoxLayout()
        choice_buttons_layout.setSpacing(15)
        
        self.button_group = QButtonGroup()
        
        self.choice_a_button = QPushButton()
        self.choice_a_button.setCheckable(True)
        self.choice_a_button.setMinimumHeight(50)
        self.choice_a_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border-radius: 8px;
                font-size: 12pt;
                font-weight: bold;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:checked {
                background-color: #0D47A1;
                border: 3px solid #FFD700;
            }
        """)
        self.choice_a_button.clicked.connect(lambda: self.on_choice_selected('A'))
        self.button_group.addButton(self.choice_a_button)
        choice_buttons_layout.addWidget(self.choice_a_button)
        
        self.choice_b_button = QPushButton()
        self.choice_b_button.setCheckable(True)
        self.choice_b_button.setMinimumHeight(50)
        self.choice_b_button.setStyleSheet("""
            QPushButton {
                background-color: #FF5722;
                color: white;
                border-radius: 8px;
                font-size: 12pt;
                font-weight: bold;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #E64A19;
            }
            QPushButton:checked {
                background-color: #BF360C;
                border: 3px solid #FFD700;
            }
        """)
        self.choice_b_button.clicked.connect(lambda: self.on_choice_selected('B'))
        self.button_group.addButton(self.choice_b_button)
        choice_buttons_layout.addWidget(self.choice_b_button)
        
        answer_layout.addLayout(choice_buttons_layout)
        
        # Confidence buttons
        confidence_label = QLabel("<b>Confidence Level:</b>")
        confidence_label.setStyleSheet("font-size: 12pt;")
        answer_layout.addWidget(confidence_label)
        
        confidence_layout = QHBoxLayout()
        confidence_layout.setSpacing(10)
        
        self.confidence_buttons = []
        for confidence in [25, 50, 75, 99]:
            btn = QPushButton(f"{confidence}%")
            btn.setMinimumHeight(45)
            btn.setEnabled(False)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #9E9E9E;
                    color: white;
                    border-radius: 8px;
                    font-size: 11pt;
                    font-weight: bold;
                }
                QPushButton:enabled {
                    background-color: #4CAF50;
                }
                QPushButton:enabled:hover {
                    background-color: #45a049;
                }
                QPushButton:enabled:pressed {
                    background-color: #2E7D32;
                }
            """)
            btn.clicked.connect(lambda checked, c=confidence: self.on_confidence_selected(c))
            confidence_layout.addWidget(btn)
            self.confidence_buttons.append(btn)
        
        answer_layout.addLayout(confidence_layout)
        answer_frame.setLayout(answer_layout)
        layout.addWidget(answer_frame)
        
        self.setLayout(layout)
    
    def load_question(self, question: CalibrationQuestion, question_num: int, total: int):
        """Load and display a question"""
        self.current_question = question
        self.selected_choice = None
        
        # Update toolbar
        self.question_number_label.setText(f"Question {question_num} of {total}")
        self.question_label.setText(question.question)
        self.progress_bar.setValue(question_num - 1)
        
        # Update choice buttons text
        self.choice_a_button.setText(f"A: {question.option_a}")
        self.choice_b_button.setText(f"B: {question.option_b}")
        self.choice_a_button.setChecked(False)
        self.choice_b_button.setChecked(False)
        
        # Disable confidence buttons
        for btn in self.confidence_buttons:
            btn.setEnabled(False)
        
        # Update perspective cards
        self.update_perspective_cards()
    
    def update_perspective_cards(self):
        """Update the perspective cards with new data"""
        if not self.current_question:
            return
        
        # Clear old cards
        left_card = PerspectiveCard(
            self.current_question.perspective_for,
            "Option A",
            self.current_question.option_a
        )
        right_card = PerspectiveCard(
            self.current_question.perspective_against,
            "Option B",
            self.current_question.option_b
        )
        
        # Replace cards
        parent_layout = self.left_card.parent().layout()
        parent_layout.replaceWidget(self.left_card, left_card)
        parent_layout.replaceWidget(self.right_card, right_card)
        
        self.left_card.deleteLater()
        self.right_card.deleteLater()
        self.left_card = left_card
        self.right_card = right_card
    
    def on_choice_selected(self, choice: str):
        """Handle choice selection"""
        self.selected_choice = choice
        # Enable confidence buttons
        for btn in self.confidence_buttons:
            btn.setEnabled(True)
    
    def on_confidence_selected(self, confidence: int):
        """Handle confidence selection - triggers advance to next question"""
        if self.selected_choice and self.current_question:
            response = UserResponse(
                self.current_question.id,
                self.current_question.question,
                self.selected_choice,
                confidence
            )
            # Emit signal to parent
            self.parent().on_answer_submitted(response)


class SummaryView(QWidget):
    """View for displaying all responses at the end"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("<h2>Calibration Complete!</h2>")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Summary text
        summary_text = QLabel(
            "Here's a summary of your responses. Your calibration data has been saved."
        )
        summary_text.setWordWrap(True)
        summary_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        summary_text.setStyleSheet("font-size: 11pt; color: #555555; margin-bottom: 10px;")
        layout.addWidget(summary_text)
        
        # List of responses
        self.response_list = QListWidget()
        self.response_list.setStyleSheet("""
            QListWidget {
                border: 2px solid #cccccc;
                border-radius: 8px;
                font-size: 10pt;
                padding: 5px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #eeeeee;
            }
            QListWidget::item:hover {
                background-color: #f0f0f0;
            }
        """)
        layout.addWidget(self.response_list)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.save_button = QPushButton("Save Results")
        self.save_button.setMinimumHeight(40)
        self.save_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 8px;
                font-size: 12pt;
                font-weight: bold;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        button_layout.addWidget(self.save_button)
        
        self.close_button = QPushButton("Close")
        self.close_button.setMinimumHeight(40)
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: #555555;
                color: white;
                border-radius: 8px;
                font-size: 12pt;
                font-weight: bold;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #444444;
            }
        """)
        button_layout.addWidget(self.close_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def load_responses(self, responses: List[UserResponse]):
        """Load responses into the list"""
        self.response_list.clear()
        for i, response in enumerate(responses, 1):
            choice_text = "Option A" if response.choice == 'A' else "Option B"
            item_text = f"Q{i}: {choice_text} ({response.confidence}% confident) - {response.question_text}"
            self.response_list.addItem(item_text)


class CalibrationWindow(QMainWindow):
    """Main application window"""
    def __init__(self):
        super().__init__()
        self.questions: List[CalibrationQuestion] = []
        self.responses: List[UserResponse] = []
        self.current_question_index = 0
        
        self.setup_ui()
        self.load_questions()
        self.show_next_question()
    
    def setup_ui(self):
        """Setup the main window"""
        self.setWindowTitle("Kindred Spirit Calibration")
        self.setMinimumSize(1200, 800)
        
        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Main layout
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.central_widget.setLayout(self.main_layout)
        
        # Question view
        self.question_view = QuestionView(self)
        self.main_layout.addWidget(self.question_view)
        
        # Summary view (initially hidden)
        self.summary_view = SummaryView(self)
        self.summary_view.save_button.clicked.connect(self.save_results)
        self.summary_view.close_button.clicked.connect(self.close)
        self.summary_view.hide()
    
    def load_questions(self):
        """Load questions from JSON file"""
        json_path = Path(__file__).parent / "questions_with_perspectives.json"
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for q_data in data['calibration_questions']:
                    self.questions.append(CalibrationQuestion(q_data))
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error Loading Questions",
                f"Failed to load questions from {json_path}:\n{str(e)}"
            )
            sys.exit(1)
    
    def show_next_question(self):
        """Display the next question"""
        if self.current_question_index < len(self.questions):
            question = self.questions[self.current_question_index]
            self.question_view.load_question(
                question,
                self.current_question_index + 1,
                len(self.questions)
            )
        else:
            self.show_summary()
    
    def on_answer_submitted(self, response: UserResponse):
        """Handle answer submission"""
        self.responses.append(response)
        self.current_question_index += 1
        self.show_next_question()
    
    def show_summary(self):
        """Show the summary view"""
        # Remove question view and show summary
        self.question_view.hide()
        self.main_layout.removeWidget(self.question_view)
        
        self.summary_view.load_responses(self.responses)
        self.main_layout.addWidget(self.summary_view)
        self.summary_view.show()
        
        # Update progress bar to 100%
        self.question_view.progress_bar.setValue(len(self.questions))
    
    def save_results(self):
        """Save results to JSON file"""
        # Ask for username
        from PyQt6.QtWidgets import QInputDialog
        username, ok = QInputDialog.getText(
            self,
            "Save Results",
            "Enter your name/identifier:"
        )
        
        if not ok or not username:
            username = "anonymous"
        
        # Prepare output data
        output_data = {
            "username": username,
            "timestamp": datetime.now().isoformat(),
            "total_questions": len(self.questions),
            "responses": [
                {
                    "question_id": r.question_id,
                    "question": r.question_text,
                    "choice": r.choice,
                    "confidence": r.confidence,
                    "timestamp": r.timestamp
                }
                for r in self.responses
            ]
        }
        
        # Save to file
        output_path = Path(__file__).parent / f"{username}_kindred_spirit.json"
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            
            QMessageBox.information(
                self,
                "Success",
                f"Results saved to:\n{output_path}"
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error Saving Results",
                f"Failed to save results:\n{str(e)}"
            )


def main():
    """Main entry point"""
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show main window
    window = CalibrationWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
