# ChessAI Training

## 1. Create conda environment

```shell
conda create -n chessai-training python=3.9 -y
```

```shell
conda activate chessai-training
```

```shell
cd dnn_models/training
pip install torch==2.0.1
pip install -e .
pip install tensorboard==2.12.0
```

## 2. Data preparation

```text
+ datasets
    + chessai
        + COCO
            + annotations
                - train.json
                - val.json
            - train
                - 000001.jpg
                - ...
            - val
                - 000001.jpg
                - ...
+ docs
+ exps
...
```

## 3. Training

- Light model:

```shell
export YOLOX_DATADIR=datasets/chessai
python tools/train.py -f exps/tfs_light.py
```

- Base model:

```shell
export YOLOX_DATADIR=datasets/chessai
python tools/train.py -f exps/tfs_base.py
```

Use `tmux` to run the training in the background.

## 4. Model export (to ONNX)

- Light model:

```shell
python tools/export_onnx.py -f exps/tfs_light.py -c YOLOX_outputs/tfs_light/best_ckpt.pth --output-name chessai-det-light.onnx
```

- Base model:

```shell
python tools/export_onnx.py -f exps/tfs_base.py -c YOLOX_outputs/tfs_base/best_ckpt.pth --output-name chessai-det-base.onnx
```


Copy `chessai-det-*.onnx` to `data/dnn`.
