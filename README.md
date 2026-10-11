# Carrom Optimization

This project explores how likely a coin is to be potted on a carrom board using a multivariable model based on striker position, coin position, shot velocity, and shot angle. The results are stored as heatmaps in the `data/` folder.

## Viewing the heatmap data

The script `show_data.py` loads one of the saved score arrays from `data/` and displays it as a heatmap.

### 1. Install Python dependencies

From the repository root, install the required packages:

```bash
python -m pip install numpy matplotlib
```

### 2. Choose a velocity

The script looks for a file named:

```text
data/scores_vs{velocity}.npy
```

The available velocity values are multiples of 30 from 60 to 360:

```text
60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360
```

Open `show_data.py` and update this line:

```python
velocity = 300
```

For example, to view the 180 cm/s heatmap, change it to:

```python
velocity = 180
```

### 3. Run the script

From the repository root:

```bash
python show_data.py
```

This will display a heatmap where:

- x-axis = coin x-position (`x_c`, in cm)
- y-axis = coin y-position (`y_c`, in cm)
- color = score value
- title = `Score Heatmap for v_s = {velocity}`

### 4. What the script is doing

The script loads the NumPy array for the selected velocity:

```python
scores = np.load(f"data/scores_vs{velocity}.npy")
```

and then plots it using Matplotlib:

```python
plt.imshow(scores, cmap='inferno', interpolation='nearest', origin='lower', extent=extent)
plt.colorbar(label="Score")
plt.show()
```

If you want to inspect a different velocity, simply change `velocity` and rerun the script.

## Repository structure

- `main.py` — generates or analyzes the optimization data
- `show_data.py` — visualizes saved `.npy` score arrays
- `data/` — saved heatmap data files such as `scores_vs180.npy`
- `Research Paper (Latex)/` — LaTeX source for the paper

## Notes

- Make sure you run the script from the repository root so that the path `data/scores_vs{velocity}.npy` resolves correctly.
- If a file for your chosen velocity is missing, check that the corresponding `.npy` file exists in `data/`.
