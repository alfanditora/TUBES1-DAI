# Magic Cube Local Search Solver

Implementation of various Local Search Algorithms to solve Magic Cube problem for IF3070 Artificial Intelligence course at ITB.

## Project Structure
```
TUBES1-DAI/
├── doc/
│   └── Tubes1_K01_Kelompok39.pdf          # Laporan tugas besar
├── save_file/          # Directory for saving experiment states
│   └── *.txt          # Saved states from different algorithms
├── src/
│   ├── MagicCube.py             # Core magic cube implementation
│   ├── main.py                  # Main program and menu interface
│   ├── genetic_algorithm.py     # Genetic Algorithm implementation
│   ├── simulated_annealing.py  # Simulated Annealing implementation
│   ├── random_restart.py       # Random Restart Hill Climbing
│   ├── sideways_move.py        # Sideways Move Hill Climbing
│   ├── steepest_ascent.py      # Steepest Ascent Hill Climbing
│   ├── stochastic.py           # Stochastic Hill Climbing
│   └── visualizer.py           # Visualization implementation using Flet
├── .gitignore
└── README.md
```

## Features
- Implementation of multiple Local Search algorithms:
  - Hill Climbing variants:
    - Steepest Ascent
    - Sideways Move
    - Stochastic
    - Random Restart
  - Simulated Annealing
  - Genetic Algorithm
- Interactive visualization with video player features:
  - Play/Pause
  - Forward/Backward playback
  - Speed control
  - Progress bar
  - State information display
- Experiment state saving and loading
- Comparative performance analysis
- Progress monitoring and visualization

## Requirements
1. Python Libraries:
```bash
pip install numpy matplotlib flet
```

## How to Run
1. Clone the repository:
```bash
git clone https://github.com/[username]/TUBES1-DAI.git
cd TUBES1-DAI
```

2. Run the main program:
```bash
python src/main.py
```

3. Menu Options:
- `1`: Start experiments with different algorithms
- `2`: Visualize saved experiment results
- `3`: Show help
- `4`: Exit program

## Algorithms
1. **Hill Climbing Variants**:
   - Steepest Ascent: Selects best neighbor
   - Sideways Move: Allows equal-value moves
   - Stochastic: Random neighbor selection
   - Random Restart: Multiple random starting points

2. **Simulated Annealing**:
   - Adaptive temperature scheduling
   - Dynamic reheat strategy
   - Multi-neighbor evaluation

3. **Genetic Algorithm**:
   - Configurable population size and iterations
   - Elite selection
   - Custom crossover and mutation operators

## Visualization Features
- Real-time cube state visualization
- Layer-by-layer view
- Playback controls
- State information display
- Progress tracking

## Contributors
- Habib Akhmad Al Farisi (18222029)	    
- Alfandito Rais Akbar (18222037)	  
- Winata Tristan (18222061) 
- Muhammad Rafi D. (18222069)  	   