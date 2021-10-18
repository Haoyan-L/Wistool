from wx.tools.img2py import img2py
import os, sys
import img


# --------------------------------------------------------------------------------------------------------------------------------
# Class: Img2Python
# --------------------------------------------------------------------------------------------------------------------------------
def forderprocess():
    listext = ('.png', '.ico', '.icon', '.gif')
    apppath, appfilename = os.path.split(os.path.abspath(sys.argv[0]))
    pyfile = apppath + '\img.py'

    if os.path.isdir(apppath):

        for name in os.listdir(apppath):
            (x, ext) = os.path.splitext(name)

            if ext in listext:
                img = os.path.join(apppath, name)
                if os.path.isfile(pyfile):
                    ret = img2py(img, pyfile, append=True)
                else:
                    ret = img2py(img, pyfile, append=True)


if __name__ == '__main__':
    forderprocess()