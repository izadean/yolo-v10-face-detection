.PHONY: train inference clean

train_id=
image_path=
inference:
	@yolo detect predict model=runs/detect/train$(train_id)/weights/best.pt source=$(image_path)


epochs=5
train: data/processed
	@yolo settings datasets_dir=.
	@yolo train model=yolov10n.pt data=dataset.yaml epochs=$(epochs)

data/processed: data/interm
	@mkdir -p $@
	@python scripts/split_data.py $</images $</labels

data/interm:
	@mkdir -p $@/images $@/labels
	@sh scripts/prepare_fddb_dataset.sh $@/images $@/labels
	@sh scripts/prepare_miki_dataset.sh $@/images $@/labels
	@sh scripts/prepare_wider_face_dataset.sh $@/images $@/labels

clean:
	@rm -rf data/processed/
	@rm -rf data/interm/
	@rm -rf runs
	@rm -f *.pt

