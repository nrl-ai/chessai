import os
import zipfile
import pathlib
import argparse

def make_parser():
    parser = argparse.ArgumentParser("Create a submission")
    parser.add_argument(
        "--exp_dir",
        type=str,
        default="YOLOX_outputs/tfs_nano",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="submission.zip",
    )
    return parser

if __name__ == "__main__":
    parser = make_parser()
    args = parser.parse_args()
    
    if not os.path.exists(args.exp_dir):
        raise ValueError(f"Directory {args.exp_dir} does not exist!")

    log_dir = os.path.join(args.exp_dir, "tensorboard")
    if not os.path.exists(log_dir):
        raise ValueError(f"Directory {log_dir} does not exist! Please use tensorboard for logging.")
    
    best_ckpt = os.path.join(args.exp_dir, "best_ckpt.pth")
    if not os.path.exists(best_ckpt):
        raise ValueError(f"Model file {best_ckpt} does not exist!")
    
    output_file = args.output
    pathlib.Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "wb") as f:
        with zipfile.ZipFile(f, "w") as zipf:
            print(f"Zipping {best_ckpt} to {output_file}")
            zipf.write(best_ckpt, "best_ckpt.pth")
            print(f"Zipping {log_dir}")
            for root, dirs, files in os.walk(log_dir):
                for file in files:
                    print(f"    > {os.path.join(root, file)}")
                    zipf.write(os.path.join(root, file), os.path.join("tensorboard", file))
            
    print(f"Created submission file {output_file} successfully!")
    