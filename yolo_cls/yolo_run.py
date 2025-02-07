from ultralytics import YOLO

if __name__ == "__main__":
    # Load a model
    model = YOLO(r"runs\classify\s1\weights\best.pt")  # load a pretrained model (recommended for training)

    model.eval()
    results = model(r"C:\Users\11386\Downloads\pdr2018\test\葡萄_褐斑病_严重\c12f4529-bda3-4091-964a-e47d6d1dd2a0___FAM_L.Blight 1362.JPG")  # predict on a single image
    
    print("神经网络分类模型结果(仅供参考):")
    for result in results:
        #print(result.names)
        probs = result.probs
        #print(probs.top5)
        #print(probs.top5conf)
        #result.show()
        
        for i,t in enumerate(probs.top5):
            #print(i,t,result.names[t],round(probs.top5conf[i].cpu().numpy() * 100,2))
            print(f"排名[{i+1}] {result.names[t]} 置信度{round(probs.top5conf[i].cpu().numpy() * 100,2)}%")