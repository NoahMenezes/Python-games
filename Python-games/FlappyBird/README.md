# Flappy Bird Game 🐦

A beautifully designed Flappy Bird clone built with Pygame featuring smooth gameplay, stunning UI, and score tracking.

## Features ✨

- **Amazing Game UI**: Beautiful sky gradient background, animated clouds, and detailed ground
- **Custom Bird Design**: Yellow bird with eye, beak, and outline details
- **Realistic Pipes**: Green pipes with caps and detailed borders
- **Score System**: Real-time score tracking in the top right corner
- **High Score Tracking**: Keeps track of your best score across sessions
- **Menu System**: 
  - Start screen with title and instructions
  - Game over screen with final score and restart button
- **Smooth Controls**: Click or press SPACE to make the bird flap
- **Collision Detection**: Accurate collision with pipes, ground, and ceiling

## Installation 📦

1. Make sure you have Python installed (Python 3.6 or higher)
2. Install Pygame:
```
pip install pygame
```

## How to Play 🎮

1. Run the game:
```
python flappy_bird.py
```

2. **Controls**:
   - Press `SPACE` or `LEFT CLICK` to make the bird flap
   - The bird will fall due to gravity
   - Navigate through the pipes without hitting them
   - Each pipe you pass awards 1 point

3. **Objective**:
   - Get the highest score possible by passing through as many pipes as you can
   - Avoid hitting the pipes, ground, or ceiling
   - Beat your high score!

## Game Mechanics 🎯

- **Scoring**: You earn 1 point for each pipe successfully passed
- **Difficulty**: Pipes spawn at random heights with consistent gaps
- **Physics**: Realistic gravity and jump mechanics
- **Speed**: Constant pipe movement speed for fair gameplay

## UI Elements 🎨

- **Sky Gradient Background**: Beautiful blue gradient sky
- **Animated Clouds**: Static clouds for atmosphere
- **Ground**: Textured ground with grass details
- **Score Display**: Always visible in top right corner
- **Menu Overlay**: Semi-transparent overlays for menus
- **Buttons**: Golden hover-effect buttons

## Tips 💡

- Time your clicks carefully - don't spam!
- Watch the pipe spacing and plan your flaps
- Stay calm and maintain rhythm
- The bird falls faster than it rises, so plan accordingly

## Customization 🛠️

You can easily customize the game by modifying these constants in `flappy_bird.py`:

- `SCREEN_WIDTH` / `SCREEN_HEIGHT`: Change window size
- `FPS`: Adjust game speed
- `gravity`: Make the bird fall faster/slower
- `pipe.gap`: Adjust difficulty by changing pipe gap size
- Colors: Modify any of the color constants

## Credits 👨‍💻

Built with Python and Pygame
Original Flappy Bird concept by Dong Nguyen

## License 📄

Free to use and modify for personal and educational purposes.

Enjoy the game! 🎮🐦