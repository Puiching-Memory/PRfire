from ultralytics import YOLO

if __name__ == "__main__":

    # Initialize the YOLO model
    model = YOLO("yolo11m-cls.pt")

    # Define search space
    # search_space = {
    #     "lr0": (1e-5, 1e-1),
    #     "degrees": (0.0, 45.0),
    # }

    model.tune(
        data=r"C:\Users\11386\Downloads\pdr2018",
        epochs=5,
        iterations=50,
        optimizer="AdamW",
        # space=search_space,
        plots=True,
        save=True,
        val=True,
        cache="disk",
    )