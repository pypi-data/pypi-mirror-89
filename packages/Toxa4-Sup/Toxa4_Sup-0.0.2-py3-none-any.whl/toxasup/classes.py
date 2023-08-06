import pyowm.owm
from pyowm.utils.config import get_default_config
import cv2


class Corr:
    def __init__(self):
        pass
    def inputs(a):
        a_b = str(a).split()
        return a_b[0]
class Help:
    def __init__(self):
        pass
    def temo_po_name(place):
        config_dict = get_default_config()
        config_dict['language'] = 'ru'
        owm = pyowm.owm('c2a0e326bbada5bf04d2e515be62ca3c', config_dict)
        mgr = owm.weather_manager()
        observation = mgr.weather_at_place(place)
        weather = observation.weather

        temp = weather.temperature('celsius')['temp']
        status = weather.detailed_status
        ob = {'city': place, 'temp': temp, 'st': status}
        return ob
class Fotos:
    def viewImage(image, name_of_window):
        cv2.namedWindow(name_of_window, cv2.WINDOW_NORMAL)
        cv2.imshow(name_of_window, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def save_f_1(imge,ex_name):
        img = cv2.imread(imge)
        #cv2.imshow('zzz', img)
        cv2.waitKey(0)
        cv2.imwrite(ex_name+'.jpg', img)

    def info_2(imge):
        img = cv2.imread(imge)
        print('Высота: ' + str(img.shape[0]))
        print('Ширина: ' + str(img.shape[1]))
        print('Каналы: ' + str(img.shape[1]))
        print(f'Красный: {img[0, 2]}, Зеленый: {img[0, 1]}, Синий: {img[0, 0]}')

    def cadr_3(imge):
        img = cv2.imread(imge)
        cropp = img[10:500, 500:2000]
        Fotos.viewImage(cropp, 'Кадрирование')

    def roat_4(imge,gr):
        img = cv2.imread(imge)
        (h, w, d) = img.shape
        cen = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(cen, gr, 1.0)
        rot = cv2.warpAffine(img, M, (w, h))
        Fotos.viewImage(rot, 'Переворот')

    def umen_5(imge,raz_um):
        img = cv2.imread(imge)
        wi = int(img.shape[1] * raz_um / 100)
        hi = int(img.shape[0] * raz_um / 100)
        razmer = (wi, hi)
        res = cv2.resize(img, razmer, interpolation=cv2.INTER_AREA)
        if raz_um > 100:
            Fotos.viewImage(res, f'Плюс {raz_um}%')
        elif raz_um < 100:
            Fotos.viewImage(res, f'Минус {raz_um}%')
        else:
            Fotos.viewImage(res, f'Ничего не Изменилось')

    def clor_iz_6(imge):
        img = cv2.imread(imge)
        gray_i = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, tr_img = cv2.threshold(img, 127, 255, 0)
        Fotos.viewImage(gray_i, 'h')
        Fotos.viewImage(tr_img, 'w')

    def raz_7(imge):
        img = cv2.imread(imge)
        bl = cv2.GaussianBlur(img, (1, 1), 0)
        Fotos.viewImage(bl, 'raz')

    def wr_kw_8(imge):
        img = cv2.imread(imge)
        out = img.copy()
        x = int(img.shape[1])
        y = int(img.shape[0])
        cv2.rectangle(out, (600, 800), (y, x), (0, 255, 255), 10)
        Fotos.viewImage(out, 'Квадрат')

    def wr_lin_9(imge):
        img = cv2.imread(imge)
        out = img.copy()
        x = int(img.shape[1])
        y = int(img.shape[0])
        cv2.line(out, (600, 800), (y, x), (0, 255, 255), 10)
        Fotos.viewImage(out, 'Квадрат')

    def find_f_10(imge):
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        image = cv2.imread(imge)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(10, 10)
        )
        faces_detected = "Лиц обнаружено: " + format(len(faces))
        print(faces_detected)
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 255, 0), 2)
        Fotos.viewImage(image, faces_detected)



