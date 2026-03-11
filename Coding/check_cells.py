import json

with open('phase3_neural_ode_model.ipynb', 'r') as f:
    nb = json.load(f)

cells = nb['cells']
print(f'Total cells: {len(cells)}\n')

# Check around cells 105-120
print("Cells 105-120:")
for i in range(104, min(120, len(cells))):
    cell = cells[i]
    if cell['cell_type'] == 'code':
        source = ''.join(cell.get('source', []))
        first_lines = source.split('\n')[:3]
        for line in first_lines:
            if 'SECTION 2' in line and 'CELL' in line:
                print(f"Cell {i+1}: {line.strip()}")
                break
            elif i+1 in [105, 106, 107, 108] and '# SECTION 21' in line:
                print(f"Cell {i+1}: {line.strip()}")
                break
