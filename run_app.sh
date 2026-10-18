#!/bin/bash

# Find all student directories matching the pattern "student_*"
students=(student_*/)

# Check if any student directories exist
if [ ${#students[@]} -eq 0 ] || [ ! -d "${students[0]}" ]; then
    echo "No student directories found starting with 'student_'!"
    exit 1
fi

echo "=========================================="
echo "    Select a Student's Flask App to Run   "
echo "=========================================="

# Display menu options
PS3="Enter the number of the student app to launch: "
select dir in "${students[@]}"; do
    if [ -n "$dir" ]; then
        # Remove trailing slash for cleaner output
        student_name="${dir%/}"
        echo ""
        echo "--> Launching app for: $student_name"
        echo "--> Directory: $dir"
        
        cd "$dir" || exit 1
        
        # Install dependencies if requirements.txt exists
        if [ -f "requirements.txt" ]; then
            echo "--> Installing dependencies..."
            pip install -q -r requirements.txt
        fi
        
        # Detect entry file (defaults to app.py or main.py)
        APP_FILE="app.py"
        if [ ! -f "app.py" ] && [ -f "main.py" ]; then
            APP_FILE="main.py"
        fi

        echo "--> Starting Flask server ($APP_FILE) on http://0.0.0.0:5000..."
        echo "=========================================="
        
        # Run Flask using host 0.0.0.0 for Codespaces port forwarding
        flask --app "${APP_FILE%.py}" run --host=0.0.0.0 --port=5000
        break
    else
        echo "Invalid choice. Please enter a valid number."
    fi
done
