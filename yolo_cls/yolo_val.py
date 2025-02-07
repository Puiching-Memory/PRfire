from ultralytics import YOLO

if __name__ == "__main__":
    # Load a model
    model = YOLO(r"C:\workspace\github\PRfire\runs\classify\s1\weights\best.pt")  # load a pretrained model (recommended for training)

    
    metrics = model.val(data=r"C:/Users/11386/Downloads/pdr2018")
    print(metrics)
