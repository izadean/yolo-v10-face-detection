# YOLOv10 Face Detection

## **Project Definition**: ML project for training YOLO-v10 model for human faces detection task

## **Start Training**: 
1. Fill `ROBOFLOW_FDDB_URL` & `ROBOFLOW_MIKI_URL` with valid urls from the website
2. Run in the terminal `make train [epochs=number_of_epochs(default: 5)]`

## **Inference on an Image**: 
1. Copy the path of the target image
2. Run in the terminal `make inference image_path=your_image_path [train_id=your_experiment_id_in_saves_folder(default: blank)]`