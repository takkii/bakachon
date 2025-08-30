import cv2
import gc
import imutils
import os
import traceback
import tkinter as tk

from typing import Optional
from PIL import Image, ImageTk


def pull_down_a_shutter(face_picture, log_folder):
    try:
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()

            img = imutils.resize(frame, width=350)
            (h, w) = img.shape[:2]

            cv2.imshow("s=save q=exit alt+F4=close.", img)
            k: Optional[int] = cv2.waitKey(1) & 0xff

            if k == ord('s'):
                cv2.imwrite(face_picture, img)
                if os.path.isfile(face_picture):
                    pil_image = Image.open(face_picture)
                    w_size = int(pil_image.width)
                    h_size = int(pil_image.height)
                    root = tk.Tk()
                    root.title("Your Self picture image")
                    canvas = tk.Canvas(root, width=w_size, height=h_size)
                    canvas.pack()
                    tk_image = ImageTk.PhotoImage(
                        image=pil_image.resize((w_size, h_size)))
                    canvas.create_image(0, 0, anchor='nw', image=tk_image)
                    root.mainloop()
                else:
                    raise ValueError('No images saved')
            elif k == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    # TraceBack.
    except Exception:
        # Specify the folder to record the exception log.
        except_folder: Optional[str] = os.path.expanduser(log_folder)
        # Specify the file to log exception occurrences.
        except_f: Optional[str] = os.path.expanduser('~/' + log_folder +
                                                     '/d.log')

        # Load the dictionary.
        if os.path.isdir(os.path.expanduser(except_folder)):
            # Log writing process.
            with open(os.path.expanduser(except_f), 'a') as log_py:
                traceback.print_exc(file=log_py)

                # throw except.
                raise RuntimeError from None

        # Current directory Not Found.
        else:
            # Unique exception occurrence.
            raise ValueError("None, Please Check the Current directory.")
    finally:
        gc.collect()
