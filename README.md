# wegc-moderation
---

## Important Note on Image Files (Case Sensitivity)

GitHub Codespaces runs in a **Linux environment**, which is strictly **case-sensitive** regarding file paths (unlike Windows or macOS).

* **Issue:** Images may fail to load due to discrepencies between the system the student built their web app on and the Linux environment provided by Codespaces.

  
# Student Flask Applications Preview

This repository hosts Flask applications for multiple learners (`Learner A` through `Learner F` for external moderation). It is configured to run entirely inside **GitHub Codespaces** without requiring any local VS Code setup or file downloads.

---

## How to Launch the Apps in GitHub Codespaces

1. **Open Codespaces:**
   * Click the green **`<> Code`** button at the top right of this repository page.
   * Select the **Codespaces** tab.
   * Click **Create codespace on main**.
   *(Alternatively, go directly to `https://github.com/ksenek/wegc-moderation/codespaces`)*

2. **Wait for Setup:**
   * Allow 1–2 minutes for the cloud environment to finish loading and pre-install dependencies.

3. **Select a Student Application:**
   * Once loaded, an interactive menu will automatically open in the integrated terminal at the bottom of the screen:
     ```text
     ==========================================
         Select a Student's Flask App to Run   
     ==========================================
     1) Learner A/
     2) Learner B/
     3) Learner C/
     4) Learner D/
     5) Learner E/
     6) Learner F/
     ...
     Enter the number of the student app to launch: 
     ```
   * Type the number corresponding to the student whose project you wish to view and press **Enter**.

4. **View the Live App:**
   * Codespaces will automatically detect the running server on port `5000` and open a preview window in a new browser tab.

---

## How to Switch Between Student Apps
To view a different student's application without restarting the Codespace:

1. Click into the integrated terminal at the bottom.
2. Press `Ctrl + C` on your keyboard to stop the currently running server.
3. Type the following command and press **Enter**:
   ```bash
   ./run_app.sh

## Troubleshooting
The Interactive Terminal Menu Did Not Open Automatically
Solution: If the menu didn't pop up in the terminal when the environment loaded, open the integrated terminal (Ctrl + ~ or Cmd + ~) and start the script manually:
./run_app.sh

If Permission Denied: Run this command to make the script executable, then run it again: 
chmod +x run_app.sh && ./run_app.sh

Type the following command and press **Enter**: 
```bash
   ./run_app.sh
