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

## Task Assigned

| Nama Mahasiswa | NIM | No | Tugas yang dikerjakan |
|----------------|-----|---|-----------------------|
| Habib Akhmad Al Farisi | 18222029 | 1 | Membuat implementasi algoritma genetic algorithm dan melakukan eksperimen pada genetic algorithm |
|  | | 2 | Melakukan analisis perbandingan, hasilnya berupa laporan analisis perbandingan pada dokumen |
| Alfandito Rais Akbar | 18222037 | 1 | Membuat implementasi magic cube, steepest ascent sideways move, stochastic, dan visualizer 'video player' dan melakukan eksperimen pada steepest ascent sideways move, dan stochastic |
|  | | 2 | Mengerjakan objective function dan implementasi algoritma magic cube, steepest ascent sideways move, stochastic, dan visualizer 'video player' pada dokumen |
| Winata Tristan | 18222061 | 1 | Membuat implementasi algoritma Random Restart Hill Climbing dan melakukan eksperimen pada Random Restart Hill Climbing |
|  | | 2 | Mengerjakan implementasi algoritma random restart pada dokumen |
| Muhammad Rafi Dhiyaulhaq | 18222069 | 1 | Membuat deskripsi persoalan, membuat implementasi algoritma simulated annealing, hasil eksperimen simulated annealing, kesimpulan, dan saran pada dokumen |
|  | | 2 | Membuat algoritma dan visualisasi untuk simulated annealing, membuat struktur project, membuat video player dalam js, membuat main.py, memperbaiki file yang sudah dibuat (MagicCube, genetic_algorithm, visualizer), dan README |