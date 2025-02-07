from ultralytics import YOLO

if __name__ == "__main__":
    # Load a model
    model = YOLO(r"C:\workspace\github\PRfire\runs\classify\s1\weights\best.pt")  # load a pretrained model (recommended for training)

    # Train the model
    results = model.train(
        data=r"C:\Users\11386\Downloads\pdr2018",
        epochs=100,
        imgsz=640,
        patience=5,
        #batch=64,
        device="0",
        #workers=2,
        plots=True,
    )

