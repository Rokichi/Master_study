# 手順　

## 下準備
split.pyでデータを分割
cd pytorch-CycleGAN-and-pix2pix
python datasets/make_dataset_aligned.py --dataset-path datasets

## 学習
python train.py --dataroot datasets --name fog_dog --model pix2pix --batch_size 64 --gpu_ids 0 --checkpoints_dir checkpoints --direction BtoA --n_epochs 500 --n_epochs_decay 100

## Test
python test.py --dataroot datasets --name fog_dog_white --model pix2pix --gpu_ids 0 --checkpoints_dir checkpoints --direction BtoA --results_dir checkpoints_result_white_550 --epoch 550
# download CXR
gsutil -m cp -r ."gs://mimic-cxr-2.0.0.physionet.org/files/p10" .

