# Training for DNN models

## 1. Data preparation

- Currenly only support for Chinese Chess (XiangQi), [contact me](https://aicurious.io/contact) for the license and the source code of the data preparation folder.
- Go to `data_preparation` folder and follow the instructions in the README.md file.
- Copy the generated data to `training/datasets/chessai` folder.

```bash
cd dnn_models
mkdir -p training/datasets/chessai/COCO/train
mkdir -p training/datasets/chessai/COCO/val
cp data_preparation/data/train.json training/datasets/chessai/COCO/annotations/train.json
cp data_preparation/data/val.json training/datasets/chessai/COCO/annotations/val.json
cp -r data_preparation/data/combined_data/* training/datasets/chessai/COCO/train
cp -r data_preparation/data/combined_data/* training/datasets/chessai/COCO/val
```

## 2. Training

- Follow the instructions in the README.md file in `training` folder.
