# ChessAI - Chinese Chess Game Analyzer

ChessAI is a groundbreaking tool that brings together computer vision, chess algorithms, and advanced analytics to revolutionize the Chinese Chess analytics landscape. With ChessAI, you don't need expensive electronic boards to analyze your games. Simply use your regular board, set up a camera to capture the position, and let ChessAI do the rest.

- Main source code: `chesssai`.
- Deep Learning / Data Preparation: `dnn_models/data_preparation` - Currenly only support for Chinese Chess (XiangQi), [contact me](https://aicurious.io/contact) for the license and the source code of the data preparation tool.
- Deep Learning / Training: `dnn_models/training`.

## 2. Environment setup

- Clone this repository.

```bash
git clone https://github.com/vietanhdev/chessai --recursive
```

- Python >= 3.9.

```bash
pip install -r requirements.txt
```

Or using `Conda`:

```bash
conda create -n chessai python=3.9
conda activate chessai
pip install -r requirements.txt
```

## 3. Build chess engine

- This project uses [godogpaw](https://github.com/hmgle/godogpaw) as the chess engine.
- Install [Go](https://go.dev/doc/install).
- Build the engine.

```bash
cd godogpaw
go build
```

- Copy the executable file (`godogpaw*`) to the [./data/engines](./data/engines) folder.

## 4. Usage

```bash
ENGINE_PATH="data/engines/godogpaw-macos-arm" python main.py
```

Replace `ENGINE_PATH` with the path to the chess engine executable file.

- Press `ESC` to quit.
- Press `m` to get move from chess engine.

## 5. Data preparation & Training

This project uses computer vision and deep learning to detect chess pieces and chess board position.

**AI flow for chess detection:**

![AI flow for chess detection](./docs/images/ai_flow.png)

- Go to [dnn_models](./dnn_models) folder and follow the instructions in the `README.md` file.

## 6. References

- This project was initially built for [Hackster's OpenCV AI Competition 2023](https://www.hackster.io/contests/opencv-ai-competition-2023). Hackster Project: [ChessAI - Chinese Chess Game Analyzer](https://www.hackster.io/vietanhdev/chessai-chinese-chess-game-analyzer-4be768).
- Object detection model (for chess pieces) is based on [YOLOX](https://github.com/Megvii-BaseDetection/YOLOX).
