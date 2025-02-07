import os
import shutil
import json

if __name__ == "__main__":
    train_path = r"C:\Users\11386\Downloads\ai_challenger_pdr2018_trainingset_20181023\AgriculturalDisease_trainingset"
    test_path = r"C:\Users\11386\Downloads\ai_challenger_pdr2018_validationset_20181023\AgriculturalDisease_validationset"
    save_path = r"C:\Users\11386\Downloads\pdr2018\test"

    cls_book = {
        0: "苹果_健康",
        1: "苹果_黑星病_一般",
        2: "苹果_黑星病_严重",
        3: "苹果_灰斑病",
        4: "苹果_雪松锈病_一般",
        5: "苹果_雪松锈病_严重",
        6: "樱桃_健康",
        7: "樱桃_白粉病_一般",
        8: "樱桃_白粉病_严重",
        9: "玉米_健康",
        10: "玉米_灰斑病_一般",
        11: "玉米_灰斑病_严重",
        12: "玉米_锈病_一般",
        13: "玉米_锈病_严重",
        14: "玉米_叶斑病_一般",
        15: "玉米_叶斑病_严重",
        16: "玉米_花叶病毒病",
        17: "葡萄_健康",
        18: "葡萄_黑腐病_一般",
        19: "葡萄_黑腐病_严重",
        20: "葡萄_轮斑病_一般",
        21: "葡萄_轮斑病_严重",
        22: "葡萄_褐斑病_一般",
        23: "葡萄_褐斑病_严重",
        24: "柑桔_健康",
        25: "柑桔_黄龙病_一般",
        26: "柑桔_黄龙病_严重",
        27: "桃_健康",
        28: "桃_疮痂病_一般",
        29: "桃_疮痂病_严重",
        30: "辣椒_健康",
        31: "辣椒_疮痂病_一般",
        32: "辣椒_疮痂病_严重",
        33: "马铃薯_健康",
        34: "马铃薯_早疫病_一般",
        35: "马铃薯_早疫病_严重",
        36: "马铃薯_晚疫病_一般",
        37: "马铃薯_晚疫病_严重",
        38: "草莓_健康",
        39: "草莓_叶枯病_一般",
        40: "草莓_叶枯病_严重",
        41: "番茄_健康",
        42: "番茄_白粉病_一般",
        43: "番茄_白粉病_严重",
        44: "番茄_疮痂病_一般",
        45: "番茄_疮痂病_严重",
        46: "番茄_早疫病_一般",
        47: "番茄_早疫病_严重",
        48: "番茄_晚疫病_一般",
        49: "番茄_晚疫病_严重",
        50: "番茄_叶霉病_一般",
        51: "番茄_叶霉病_严重",
        52: "番茄_斑点病_一般",
        53: "番茄_斑点病_严重",
        54: "番茄_斑枯病_一般",
        55: "番茄_斑枯病_严重",
        56: "番茄_红蜘蛛损伤_一般",
        57: "番茄_红蜘蛛损伤_严重",
        58: "番茄_黄化曲叶病毒病_一般",
        59: "番茄_黄化曲叶病毒病_严重",
        60: "番茄_花叶病毒病",
    }

    with open(test_path + r"\AgriculturalDisease_validation_annotations.json", "r") as f:
        data = json.load(f)
    # [{'disease_class': 1, 'image_id': '62fd8bf4d53a1b94fbac16738406f10b.jpg'},{},...]
    for obj in data:
        cls_name = cls_book[obj["disease_class"]]
        image_id = obj["image_id"]
        print(cls_name, image_id)
        print(f"{test_path}\images\{image_id}")
        if not os.path.exists(f"{save_path}\{cls_name}"):
            os.makedirs(f"{save_path}\{cls_name}")  # 创建多级目录
        shutil.copy2(
            f"{test_path}\images\{image_id}", f"{save_path}\{cls_name}\{image_id}"
        )
