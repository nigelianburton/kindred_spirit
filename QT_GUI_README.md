# Kindred Spirit Calibration - Qt GUI

A visual interface for the Kindred Spirit ethical calibration tool. This Qt-based application presents 74 carefully crafted ethical dilemmas, each accompanied by two opposing perspectives from respected historical figures.

## Features

### 1. **Visual Progress Tracking**
   - Clear question numbering (e.g., "Question 1 of 74")
   - Progress bar showing completion percentage
   - Current question displayed prominently

### 2. **Dual Perspective Display**
   - Two-column layout showing opposing viewpoints
   - Each perspective includes:
     - Historical figure's name and years
     - Their role/credentials
     - A substantive quote representing their position
   - Clean, readable card-based design

### 3. **Interactive Answer System**
   - Large, clearly labeled Option A and Option B buttons
   - Visual feedback when option is selected (golden border)
   - Confidence level buttons (25%, 50%, 75%, 99%)
   - Confidence buttons disabled until you choose an option
   - Automatic advance when confidence is selected

### 4. **Summary View**
   - Complete list of all your responses
   - Shows choice and confidence level for each question
   - Save results to JSON file
   - Persistent record for training data generation

## Installation

1. **Install PyQt6**:
   ```bash
   pip install -r requirements_qt.txt
   ```

2. **Verify Installation**:
   ```bash
   python -c "import PyQt6; print('PyQt6 installed successfully')"
   ```

## Usage

Run the Qt GUI application:
```bash
python 1_calibrate_kindred_spirit_qt.py
```

### Workflow

1. **Read Both Perspectives**: Take time to understand both viewpoints
2. **Choose Your Answer**: Click Option A or Option B
3. **Select Confidence**: Choose how certain you are (25%, 50%, 75%, or 99%)
4. **Automatic Advance**: The next question loads immediately
5. **Review Results**: At the end, review all responses in the summary view
6. **Save**: Enter your name and save results to JSON

## Output Format

Results are saved as `{username}_kindred_spirit.json`:

```json
{
  "username": "your_name",
  "timestamp": "2026-01-31T10:30:00",
  "total_questions": 74,
  "responses": [
    {
      "question_id": "question_001",
      "question": "Corporate whistleblowing...",
      "choice": "A",
      "confidence": 75,
      "timestamp": "2026-01-31T10:31:15"
    }
  ]
}
```

## Design Philosophy

### Why Two Perspectives?

Rather than presenting questions as simple A/B choices, each question shows you respected historical figures who genuinely disagreed. This:

- **Validates both sides**: Shows that thoughtful people can reach different conclusions
- **Reduces bias**: Harder to dismiss a viewpoint when held by someone you respect
- **Encourages reflection**: Understanding both arguments leads to more authentic answers
- **Shows complexity**: Ethics isn't about "right answers" but about values

### Example Perspectives

**Question**: Should we protect whistleblowers who expose corporate wrongdoing?

**For** (Daniel Ellsberg, Pentagon Papers whistleblower):
> "There are certain secrets that are so important to expose that you must be willing to risk your career, your freedom, even your life."

**Against** (Edmund Burke, Irish statesman):
> "Order and stability require trust within institutions. When individuals take it upon themselves to violate oaths and confidences, they undermine the very foundations of civil society."

## UI Components

### Toolbar Section
- Question number and total count
- Full question text
- Progress bar with percentage

### Perspectives Section
- Left card: Option A with supporting perspective
- Right card: Option B with opposing perspective
- Scrollable for longer quotes
- Color-coded headers (blue for A, red for B)

### Answer Section
- Large Option A button (blue)
- Large Option B button (red)
- Four confidence buttons (25%, 50%, 75%, 99%)
- Gray when disabled, green when enabled
- Clear visual feedback on selection

### Summary Section
- Complete list of all responses
- Formatted as: "Q1: Option A (75% confident) - Question text"
- Save and Close buttons
- Export to JSON for next steps in pipeline

## Technical Details

- **Framework**: PyQt6
- **Python**: 3.8+
- **Data Source**: `questions_with_perspectives.json`
- **Output**: `{username}_kindred_spirit.json`
- **Window Size**: 1200x800 minimum (responsive)
- **Style**: Fusion theme with custom stylesheets

## Next Steps

After calibration:
1. Your responses are saved to JSON
2. Run `2_generate_training_data.py` to create training examples
3. Run `3_train_kindred_values.py` to fine-tune the model
4. Run `4_test_kindred_adapter.py` to test your personalized model

## Troubleshooting

### PyQt6 Import Errors
```bash
pip install --upgrade PyQt6
```

### Questions Not Loading
- Verify `questions_with_perspectives.json` exists in the same directory
- Check JSON file is valid (no syntax errors)

### Window Too Small
- Increase your screen resolution
- Or edit line with `setMinimumSize(1200, 800)` to smaller values

## Screenshots

*(The interface includes)*
- Clean, modern design with card-based layout
- Professional color scheme (blues, greens, neutrals)
- Clear typography and spacing
- Intuitive button states and feedback
- Smooth workflow from question to question

## Comparison to CLI Version

| Feature | CLI (`calibrate_kindred_spirit.py`) | Qt GUI (`1_calibrate_kindred_spirit_qt.py`) |
|---------|-------------------------------------|---------------------------------------------|
| Interface | Text-based terminal | Visual window |
| Perspectives | Not shown | Dual columns with quotes |
| Progress | Text only | Progress bar |
| Navigation | Type answers | Click buttons |
| Summary | Terminal output | Scrollable list |
| Best For | Servers, scripts | Desktop users |

## Philosophy

This tool is built on the belief that:
1. **Your values matter**: AI should reflect individual ethics, not corporate guidelines
2. **Complexity is real**: Most ethical questions have legitimate disagreement
3. **History teaches**: Studying how great minds disagreed enriches our own thinking
4. **Authenticity matters**: Quick, intuitive responses reveal true values better than deliberation

Take your time. Read both perspectives. Trust your gut. There are no "right" answers—only *your* answers.

---

*Part of the Kindred Spirit project: Building AI that reflects personal values through ethical calibration and LoRA fine-tuning.*
