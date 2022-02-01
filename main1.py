import cv2 # library deteksi objek
from cvzone.HandTrackingModule import HandDetector # library cv zone untuk deteksi tangan
import pyfirmata #library penghubung ke arduino

cap = cv2.VideoCapture(0)
cap.set(3, 640) # seting ukuruan piksel
cap.set(4, 360)

if cap.isOpened() == False: # inisialisasi kamera bekerja tidaknya
    print("camera terbaca")
    exit()

detector = HandDetector(detectionCon=0.7) # variabel = memanggil fungsi deteksi tangan

counter_R, counter_S, counter_T = 0, 0, 0 # deklarasi variabel untuk switch
R_on, S_on, T_on  = False, False, False
valRST = [0, 0, 0] #variabel untuk menyimpan value tiap saklar

pinR, pinS, pinT = 10, 11, 12 #inisialisasi pin arduino nano
port = 'COM9' # inisialisasi COM
board = pyfirmata.Arduino(port) # inisialisasi arduino

while cap.isOpened():
    success, img = cap.read()
    img = detector.findHands(img) # variabel frame = deteksi tangan (output)
    lmlist, bboxHand = detector.findPosition(img) # variabel posisi tangan, menandai tangan = deteksi posisi tangan (output)

    if lmlist: # jika nilai posisi tangan
        x, y = 50, 50 # di posisi piksel x=50 y=50 akan membentuk sebuah kotak
        w, h = 120, 120 # membentuk kotak dengan bobot lebar dan tinggi x=120 y=120
        X, Y = 70, 100 # di posisi piksel x=50 y=50 akan membentuk sebuah tempat tulisan

        fx, fy = lmlist[8][0], lmlist [8][1] # deteksi jari telunjuk di index 8 dan disimpan di f(x)0, fy(1)
        posfinger = [fx, fy]
        #print(posfinger)
        cv2.circle(img, (fx, fy), 15, (180,200,0), cv2.FILLED) # membentuk lingkaran di ujung jari telunjuk(output, (posisi), ukuran lingkaran, (warna), fungsi waran full
       # cv2.putText(img, str(posfinger), (fx+10, fy-10), cv2.FONT_HERSHEY_PLAIN, 2, (255,180,0), 2) # ouput nilai posisi telunjuk di piksel berapa

        if x < fx < x+w-50 and y < fy < y+h-50: #jika telunjuk mendekati posisi piksel kotak saklar maka akan ganti kondisi lampu
            cv2.rectangle(img, (x, y), (w, h), (200, 200, 50), cv2.FILLED) # jeda proses perubahan kondisi
            counter_R += 1 #kondisi ketika telunjuk mengenai kotak maka akan berubah kondisi meskipusn sudah dilepas
            if counter_R == 1:
                R_on = not R_on
        else :
            counter_R = 0
            if R_on : # kondisi ketika nyala
                R_val = 1 #jika pakai relay ini kondisi aktif HIGH, jika pakai aktif low tinggal balik saja nilainya
                cv2.rectangle(img, (x, y), (w, h), (0, 200, 255), cv2.FILLED)
                cv2.putText(img, "1", (X, Y), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)
            else:
                R_val = 0 # kondisi ketika off
                cv2.rectangle(img, (x, y), (w, h), (150, 180, 150), cv2.FILLED)
                cv2.putText(img, "0", (X, Y), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)

        if x+180 < fx < x+w-50+180 and y < fy < y+h-50:
            cv2.rectangle(img, (x+180, y), (w+180, h), (200, 255, 0), cv2.FILLED)
            counter_S += 1
            if counter_S == 1:
                S_on = not S_on
        else :
            counter_S = 0
            if S_on :
                S_val = 1
                cv2.rectangle(img, (x+180, y), (w+180, h), (0, 0, 255), cv2.FILLED)
                cv2.putText(img, "1", (X+180, Y), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 3)
            else:
                S_val = 0
                cv2.rectangle(img, (x+180, y), (w+180, h), (150, 180, 150), cv2.FILLED)
                cv2.putText(img, "0", (X+180, Y), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 100), 3)

        if x+360 < fx < x+w-50+360 and y < fy < y+h-50:
            cv2.rectangle(img, (x+360, y), (w+360, h), (200, 255, 0), cv2.FILLED)
            counter_T += 1
            if counter_T == 1:
                T_on = not T_on
        else :
            counter_T = 0
            if T_on :
                T_val = 1
                cv2.rectangle(img, (x+360, y), (w+360, h), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, "1", (X+360, Y), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 3)
            else:
                T_val = 0
                cv2.rectangle(img, (x+360, y), (w+360, h), (150, 180, 150), cv2.FILLED)
                cv2.putText(img, "0", (X+360, Y), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 100), 3)

        # valRST[0] = R_val
        # valRST[1] = S_val
        # valRST[2] = T_val
        # print(valRST)

        board.digital[pinR].write(R_val) # kondisi menulis keputusan ke arduino
        board.digital[pinS].write(S_val)
        board.digital[pinT].write(T_val)

    cv2.imshow("output", img)
    cv2.waitKey(1)