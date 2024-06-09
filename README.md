# Wave Function Collapse Texture Generator

This Python script generates textures using the Wave Function Collapse algorithm. The configuration for the generation process is done through a `config.toml` file.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Example](#example)
- [License](#license)

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/wfc-texture-generator.git
    ```
2. Navigate to the project directory:
    ```sh
    cd wfc-texture-generator
    ```
3. (Optional) Create and activate a virtual environment:
    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```
4. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

Run the script with the following command:
```sh
python main.py
Ensure that config.toml is present in the same directory as the script.
```

### Configuration

The configuration file `config.toml` allows customization of various parameters. Below is the structure and explanation of each section in the configuration file.

### `[DEFAULT]`
- **NUMBER_OF_TILES**: Number of tiles to be used in the generation (default: 7).
- **WIDTH**: Width of the generated texture in tiles (default: 32).
- **HEIGHT**: Height of the generated texture in tiles (default: 32).
- **TILE_SIZE**: Size of each tile in pixels (default: 64).
- **BG_COLOR**: Background color for the texture (default: 0).
- **BORDER_MODE**: Mode for handling borders (default: 1).
- **IMAGE_PATH**: Path to save the final generated image (default: "final.jpg").

### `[NORTH_SOUTH]`
Defines the adjacency rules for tiles in the North-South direction.
- **row1** to **row7**: Lists of boolean values representing valid adjacencies.

### `[EAST_WEST]`
Defines the adjacency rules for tiles in the East-West direction.
- **row1** to **row7**: Lists of boolean values representing valid adjacencies.

### `[TILES]`
- **FOLDER**: Path to the folder containing tile images.
- **TILE_IMGS**: List of filenames for tile images.

## Example

An example `config.toml`:
```toml
[DEFAULT]
NUMBER_OF_TILES = 7
WIDTH = 32
HEIGHT = 32
TILE_SIZE = 64
BG_COLOR = 0
BORDER_MODE = 1
IMAGE_PATH = "final.jpg"

[NORTH_SOUTH]
row1 = [true, false, false, true, true, false, true]
row2 = [false, true, true, false, false, true, false]
row3 = [true, false, false, true, true, false, true]
row4 = [false, true, true, false, false, true, false]
row5 = [false, true, true, false, false, true, false]
row6 = [true, false, false, true, true, false, true]
row7 = [true, false, false, true, true, false, true]

[EAST_WEST]
row1 = [true, false, true, true, false, false, false]
row2 = [false, true, false, false, true, true, true]
row3 = [false, true, false, false, true, true, true]
row4 = [false, true, false, false, true, true, true]
row5 = [true, false, true, true, false, false, false]
row6 = [true, false, true, true, false, false, false]
row7 = [false, true, false, false, true, true, true]

[TILES]
FOLDER = "./ex_tiles"
TILE_IMGS = ["0.png", "1.png", "2.png", "3.png", "4.png", "5.png", "6.png"]
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
