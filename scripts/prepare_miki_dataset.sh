
images_dir=$1
labels_dir=$2
temporary_dir=temporary7852041981423

mkdir -p $temporary_dir "$images_dir" "$labels_dir"

curl -L "$ROBOFLOW_MIKI_URL" > $temporary_dir/miki.zip
unzip $temporary_dir/miki.zip -d $temporary_dir

mv $temporary_dir/train/images/* "$images_dir"
mv $temporary_dir/valid/images/* "$images_dir"
mv $temporary_dir/train/labels/* "$labels_dir"
mv $temporary_dir/valid/labels/* "$labels_dir"

rm -r $temporary_dir
