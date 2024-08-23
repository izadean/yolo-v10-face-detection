
images_dir=$1
labels_dir=$2
temporary_dir=temporary4823704q247089

mkdir -p "$images_dir" "$labels_dir" $temporary_dir

gdown 15hGDLhsx8bLgLcIRD5DhYt5iBxnjNF1M -O $temporary_dir/1.zip
gdown 1GUCogbp16PMGa39thoMMeWxp7Rp5oM8Q -O $temporary_dir/2.zip

unzip -d $temporary_dir $temporary_dir/1.zip
unzip -d $temporary_dir $temporary_dir/2.zip

curl http://shuoyang1213.me/WIDERFACE/support/bbx_annotation/wider_face_split.zip > $temporary_dir/anns.zip
unzip $temporary_dir/anns.zip -d $temporary_dir/anns

mv $temporary_dir/WIDER_*/images/*/*.jpg "$images_dir"

python scripts/wider_face_to_yolo.py $temporary_dir/anns/wider_face_split/wider_face_train_bbx_gt.txt "$labels_dir" "$images_dir"
python scripts/wider_face_to_yolo.py $temporary_dir/anns/wider_face_split/wider_face_val_bbx_gt.txt "$labels_dir" "$images_dir"

rm -r $temporary_dir
