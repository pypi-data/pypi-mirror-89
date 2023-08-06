# 使用办法:

    from FaceBagNet import FaceAnti
    import cv2
    FA = FaceAnti.FaceAnti()
    img = cv2.imread('1.jpg',1)
    score=FA.detect(img)
    print("is_live:%s"%(score))
