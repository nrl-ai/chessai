mkdir -p training/datasets/chessai/COCO/train
mkdir -p training/datasets/chessai/COCO/val
cp data_preparation/data/train.json training/datasets/chessai/COCO/annotations/train.json
cp data_preparation/data/val.json training/datasets/chessai/COCO/annotations/val.json
cp -r data_preparation/data/combined_data/* training/datasets/chessai/COCO/train
cp -r data_preparation/data/combined_data/* training/datasets/chessai/COCO/val