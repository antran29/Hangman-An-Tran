# Hangman-An-Tran

List of Changes Made to the Code:
Added Difficulty Selection at the Start:

Implemented a difficulty_screen() function.
Player can choose between Easy (5 mistakes allowed) and Hard (3 mistakes allowed) modes.

Adjusted Mistake Limits:

Easy Mode: Reduced from 9 mistakes to 5.
Hard Mode: Reduced from 6 mistakes to 3.

Restart or Quit Option After Winning or Losing:

Implemented a display_message() function that shows "You WON!" or "You LOST!" with Restart and Quit buttons.
Clicking Restart starts a new game, and Quit exits the game.

Improved Button UI:

Green for Restart, Red for Quit.
Green for Easy Mode, Red for Hard Mode.

Optimized Code Structure:

Ensured letter visibility resets when restarting.
Refactored drawing and event-handling functions for cleaner execution.
