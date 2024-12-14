# Genetic MIDI Evolution Project

This project uses a genetic algorithm to evolve new MIDI tracks from an input MIDI file. The algorithm applies crossover and mutation operations to generate new tracks and selects the best tracks based on a rating function.

## Project Structure

This document provides an overview of the project's directory structure and files.

```
ProjectRoot/
|—— __pycache__/
|—— .vscode/
|     —— settings.json
|—— debug_files/
|     —— crossover1.mid
|     —— crossover2.mid
|     —— desirable.txt
|     —— home_riff.mid
|     —— input.mid
|     —— intermediate.txt
|     —— intermediate2.txt
|     —— mutated_track.txt
|     —— output.mid
|     —— track
|     —— track2
|—— make_riffs/
|     —— dead_memories_riff.py
|     —— home_riff.py
|     —— hutch_cup_riff.py
|     —— ...
|—— midi_files/
|     —— ...
|—— reference_codes/
|     —— ...
|—— a.py
|—— crossover.py
|—— format_conversion.py
|—— Genetic.py
|—— Genetic_Final.py
|—— main.py
|—— main2.py
|—— mutator.py
|—— old_crossover.py
|—— old.py
|—— raters.py
|—— slow_down_alone.py
|—— song_ratings.csv
|—— test_mutators.py
|—— test.mid
```

## How to Run

1. **Install Dependencies**: Ensure you have the required dependencies installed. You can install them using pip:
    ```sh
    pip install mido
    ```

2. **Run the Genetic Algorithm**: Execute the [`main.py`](main.py) file to start the genetic algorithm.
    ```sh
    python Genetic_Final.py
    ```

3. **Output**: The evolved MIDI tracks will be saved in the specified output directory (default is `./midi_files/`). The best-evolved track will be saved as `evolved.mid`.

## What to See

- **Midi Files Directory**: Check the `./midi_files/` directory for the evolved MIDI tracks.
- **Best Track**: The best-evolved track will be saved as `evolved_song.mid` in the output directory.
- **Logs**: The console will display logs for each generation, including the top score and the progress of the algorithm.

## Code Explanation

### Genetic Algorithm

The genetic algorithm is implemented in the [`genetic_algorithm`](Genetic_Final.py) function in [`Genetic_Final.py`](Genetic_Final.py). It performs the following steps:

1. **Initialization**: Reads the input MIDI file and generates the initial population of tracks.
2. **Evaluation**: Rates each track in the population using the [`rate_a_song`](Final_Rater.py) function.
3. **Selection**: Retains the top-rated tracks.
4. **Crossover and Mutation**: Applies crossover and mutation operations to generate new tracks.
5. **Iteration**: Repeats the evaluation, selection, crossover, and mutation steps for a specified number of generations.
6. **Output**: Saves the best-evolved track from the final generation.

### Key Functions

- **[`genetic_algorithm`](Genetic_Final.py)**: Main function to run the genetic algorithm.
- **[`Mutate`](Genetic_Final.py)**: Applies mutation to a track.
- **[`Crossover`](Genetic_Final.py)**: Applies crossover to two tracks.
- **[`rate_a_song`](Genetic_Final.py)**: Rates a MIDI track.
- **[`save_modified_midi`](Genetic_Final.py)**: Saves a modified MIDI track.
- **[`delete_output_files_directory`](Genetic_Final.py)**: Deletes the specified directory and its contents.

### Example Usage

```python
from Genetic import genetic_algorithm

input_song_path = 'path/to/input.mid'
output_dir = './output_files/'
best_track = genetic_algorithm(input_song_path, output_dir=output_dir)
print(f"Best evolved track saved at: {best_track}")
```
# How to Run MIDI Files

MIDI files are versatile and can be played on multiple platforms using different software. Follow the instructions below based on your operating system.

---

## On Windows  
MIDI files can be run on **Windows Media Player** just like any other song format.  
To play a MIDI file:  
1. Locate the MIDI file on your computer.  
2. Double-click the file, and it will open and play in Windows Media Player.  

If Windows Media Player is not set as the default program, right-click the file, select **Open With**, and choose **Windows Media Player**.

---

## On Linux  
You can play MIDI files using **TiMidity**, a powerful software synthesizer available on Linux.

### Steps to Play MIDI Files with TiMidity:
1. **Install TiMidity** using your package manager:  
   For Debian/Ubuntu-based systems, run:  
   ```bash
   sudo apt-get install timidity
   ```

2. **Play the MIDI File**:  
   Use the following command to play the file:  
   ```bash
   timidity filename.mid
   ```
   Replace `filename.mid` with the name of your MIDI file.

3. **Output**:  
   TiMidity will play the file directly in the terminal or the default sound output.



