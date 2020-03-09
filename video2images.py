import cv2 as cv
import os
import datetime as dt

'''
    This Library create frames from one or multiple videos in a folder. And export them i a folder named 
                                        outputData
    names as 00*.format, while format given from user.
'''


# -------------------------------------------------------------------------------------------------------------------- #

videoFileFormats = (".mov", ".MOV", ".qt", ".mp4", ".m4p", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".m2v", ".flv",
                    ".vob", ".ogg", ".ogv", ".gif", ".webm", ".mkv", ".drc", ".avi", ".wmv", ".qt", ".yuv", ".rm",
                    ".amv")


def video2img(path: str, exportPath: str, fps=0, scaleFps=1.0, nameIndex=0, imgFormat="jpg", diffFolder=False,
              restartNumbering=False):
    # Create a VideoCapture object and read from input file
    # If the input is the camera, pass -2 instead of the video file name
    print(str(dt.datetime.now()) + " : Video Open.... ")
    video = cv.VideoCapture(path)
    # Check if camera opened successfully
    if not video.isOpened():
        print(str(dt.datetime.now()) + " : Error opening video stream or file")
        return False, None
    print(str(dt.datetime.now()) + " : Success!\n")

    # Calculate fps
    if fps <= 0:
        print(str(dt.datetime.now()) + " : Calculate fps... ")
        (major_ver, minor_ver, subminor_ver) = cv.__version__.split('.')
        if int(major_ver) < 3:
            fps = video.get(cv.cv.CV_CAP_PROP_FPS)
            # print("Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps))
        else:
            fps = video.get(cv.CAP_PROP_FPS)
            # print("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))

    fps = int(round(fps * scaleFps, 1))
    success, frame = video.read()
    currFrameCounter = 0
    print(str(dt.datetime.now()) + " : fps = {0}\n".format(fps))
    print(str(dt.datetime.now()) + " : Export Frames")
    export_path = exportPath
    if diffFolder:
        if restartNumbering:
            nameIndex = 0
        videoName = os.path.basename(path)
        videoName = os.path.splitext(videoName)[0]
        export_path = export_path + videoName + "/"
        if not os.path.exists(export_path):
            os.makedirs(export_path)
    while success:
        if currFrameCounter % fps == 0:
            exportFilePath = export_path + "%03d." % nameIndex + imgFormat
            cv.imwrite(exportFilePath, frame)  # save frame as JPEG file
            print(str(dt.datetime.now()) + " : Export frame: %03d as " % nameIndex, exportFilePath)
            nameIndex += 1
        success, frame = video.read()
        currFrameCounter += 1

    # When everything done, release the video capture object
    video.release()
    # Closes all the frames
    cv.destroyAllWindows()
    return True, nameIndex


# -------------------------------------------------------------------------------------------------------------------- #

def videoINfolder2image(folderPath: str, exportPath: str, fps=0, scaleFps=1.0, imgFormat="jpg", diffFolder=False,
                        restartNumbering=False):
    videoFiles = []
    fileCounter = 0
    print(str(dt.datetime.now()) + " : Reading files in folder")
    for r, d, f in os.walk(folderPath):
        for file in f:
            for v_format in videoFileFormats:
                if v_format in file:
                    videoFiles.append(os.path.join(r, file))
                    fileCounter += 1
    videoFiles.sort()

    # print(videoFiles)  # for Debugging
    # print(fileCounter) # for Debugging

    frameIndex = 0
    for f in videoFiles:
        print("\n" + str(dt.datetime.now()) + " : Opening file %s" % f)
        success, frameIndex = video2img(f, exportPath, fps, scaleFps, frameIndex, imgFormat, diffFolder,
                                        restartNumbering)
