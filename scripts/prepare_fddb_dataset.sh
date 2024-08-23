
images_dir=$1
labels_dir=$2
temporary_dir=temporary092481948158971897

mkdir -p "$images_dir" "$labels_dir" $temporary_dir

curl -L "$ROBOFLOW_FDDB_URL" > $temporary_dir/fddb.zip
unzip $temporary_dir/fddb.zip -d $temporary_dir

mv $temporary_dir/train/images/* "$images_dir"
mv $temporary_dir/valid/images/* "$images_dir"
mv $temporary_dir/train/labels/* "$labels_dir"
mv $temporary_dir/valid/labels/* "$labels_dir"

rm -r $temporary_dir
