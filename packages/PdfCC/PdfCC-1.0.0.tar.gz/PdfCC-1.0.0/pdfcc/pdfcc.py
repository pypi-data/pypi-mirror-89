"""pdfcc module contains the following modules.

- Pdf
- PdfCC
"""
import os
import argparse
from typing import List
import logging
from PIL import Image
from pdf2image import convert_from_path, exceptions
from file_wizard.file_manager import FileManager
from pdfcc.logger import initLogger


log: logging.Logger = initLogger()


class Pdf():
    """Pdf class is used to store the basic attributes of the desired output\
pdf such as pages, top margin, bottom margin, left margin, right margin.
    """
    __bottomMargin: int
    __topMargin: int
    __leftMargin: int
    __rightMargin: int
    __excludePages: List[int]

    def __init__(self):
        self.___topMargin = 0
        self.___leftMargin = 0
        self.___bottomMargin = -1
        self.___rightMargin = -1

    @property
    def ___topMargin(self) -> int:
        """The topMargin property is used to get the value of the topMargin

        Returns:
            int: topMargin
        """
        return self.__topMargin

    @___topMargin.setter
    def ___topMargin(self, topMargin: int):
        if topMargin < 0:
            log.error("The given value for top Margin is lesser than zero. "
                      "Using the default value for the top margin")
        else:
            self.__topMargin = topMargin

    @property
    def ___leftMargin(self) -> int:
        """The leftMargin property is used to get the value of the left \
            margin.

        Returns:
            int: leftMargin
        """
        return self.__leftMargin

    @___leftMargin.setter
    def ___leftMargin(self, leftMargin: int):
        if leftMargin < 0:
            log.error("The given value for left Margin is lesser than zero. "
                      "Using the default value for the left margin")
        else:
            self.__leftMargin = leftMargin

    @property
    def ___bottomMargin(self) -> int:
        """The bottomMargin property is used to get the value of the\
             bottomMargin

        Returns:
            int: bottomMargin
        """
        return self.__bottomMargin

    @___bottomMargin.setter
    def ___bottomMargin(self, bottomMargin: int):
        if bottomMargin != -1 and bottomMargin <= 0:
            log.error("The bottom margin should be set to -1 or should be "
                      "greater than 0. Using the default value for the bottom "
                      "margin")
        elif bottomMargin != -1 and bottomMargin <= self.___topMargin:
            log.error("The bottom margin should be  greater than top margin.")
        else:
            self.__bottomMargin = bottomMargin

    @property
    def ___rightMargin(self) -> int:
        """The rightMargin property is used to get the value of the rightMargin

        Returns:
            int: rightMargin
        """
        return self.__rightMargin

    @___rightMargin.setter
    def ___rightMargin(self, rightMargin: int):
        if rightMargin != -1 and rightMargin <= 0:
            log.error("The right margin should be set to -1 or should be "
                      "greater than 0. Using the default value for the right "
                      "margin")
        elif rightMargin != -1 and rightMargin <= self.___leftMargin:
            log.error("The right margin should be greater than left margin.")
        else:
            self.__rightMargin = rightMargin

    def setPageBoundary(self,
                        topMargin: int = 0,
                        bottomMargin: int = -1,
                        leftMargin: int = 0,
                        rightMargin: int = -1):
        """Sets the desired margin for the output pdf.

        Args:
            topMargin (int, optional):  Defaults to 0.
            bottomMargin (int, optional): Defaults to -1.
            leftMargin (int, optional):  Defaults to 0.
            rightMargin (int, optional):  Defaults to -1.
        """
        self.___topMargin = topMargin
        self.___bottomMargin = bottomMargin
        self.___leftMargin = leftMargin
        self.___rightMargin = rightMargin

    def getPageBoundary(self):
        """Sets the desired margin for the output pdf.

        Args:
            topMargin (int, optional):  Defaults to 0.
            bottomMargin (int, optional): Defaults to -1.
            leftMargin (int, optional):  Defaults to 0.
            rightMargin (int, optional):  Defaults to -1.
        """
        pageBoundary = {}
        pageBoundary["topMargin"] = self.___topMargin
        pageBoundary["bottomMargin"] = self.___bottomMargin
        pageBoundary["rightMargin"] = self.___rightMargin
        pageBoundary["leftMargin"] = self.___leftMargin
        return pageBoundary


class PdfCC(Pdf):
    """PdfCC will help you to crop unnecessary boundaries from the pdf files.\
We are working on the additional functionalities.
    """
    def __init__(self, fileName, outputFileName):
        super().__init__()
        self.__fileName = fileName
        self.__outFileName = outputFileName
        self.__pageCount = 0

    def cropFile(self):
        """ Function to crop the pdf"""

        if not os.path.exists(self.__fileName):
            message = "File does not exist."
            log.error(message)
            return False
        fileManager = FileManager()
        temp = fileManager.mkdtemp(prefix="PDF-CC-")
        convertionStatus = self.__pdftoimage(temp)
        if convertionStatus is False:
            return convertionStatus

        imageList = []
        flag = False

        for i in range(0, self.__pageCount + 1):
            fileName = temp + os.path.split(self.__fileName)[1] + str(i)\
                 + ".png"
            image = Image.open(fileName)
            image = self.__cropImage(image)
            if flag:
                imageList.append(image)
            else:
                firstImage = image
                flag = True
            outputFilename = os.path.join(temp, os.path.split(
                self.__fileName)[1] + "out" + str(i) + ".png")
            print(outputFilename)
            image.save(outputFilename)
        firstImage.save(self.__outFileName, save_all=True,
                        append_images=imageList)
        fileManager.rmdtemp()
        return True

    def getCropBoundary(self, width, height):
        """
        Finds the actual page boundary after cropping, based on
        the user input and the actual dimension of the page,
        covering for any conflicts that can be handled easily enough.
        """
        pageBoundary = self.getPageBoundary()
        left = pageBoundary["leftMargin"]
        right = width - 1 if pageBoundary["rightMargin"] == -1\
            else min(pageBoundary["rightMargin"], width)
        top = pageBoundary["topMargin"]
        bottom = height - 1 if pageBoundary["bottomMargin"] == -1\
            else min(pageBoundary["bottomMargin"], height)
        return left, right, top, bottom

    def __cropImage(self, image):

        width, height = image.size
        left, right, top, bottom = self.getCropBoundary(
                                                        width,
                                                        height)
        if width < right or height < bottom:
            log.error("Cropping size greater than page size")
            return image
        croppedImage = image.crop((left, top, right, bottom))
        return croppedImage

    def __pdftoimage(self, temp):
        try:
            images = convert_from_path(self.__fileName)
        except exceptions.PDFPageCountError:
            log.exception("File type not recognised.")
            return False
        except exceptions.PDFInfoNotInstalledError:
            log.exception("File type not recognised.")
            return False

        for i, image in enumerate(images):
            fname = os.path.split(self.__fileName)[1] + str(i) + ".png"
            image.save(temp + fname, "PNG")
            self.__pageCount = i
        log.info("PDF successfully converted to png")
        return True


def main():
    """This is a CLI wrapper."""

    parser = argparse.ArgumentParser(
        description="PdfCC -- The ideal pdf size crop & compress.\nRemoves\
             unwanted info and compresses the pdf.")
    parser.add_argument("Path",
                        metavar="input_path",
                        type=str,
                        help="Path to the input pdf file.")
    parser.add_argument(
        "-L",
        nargs="?",
        dest="L",
        const=0,
        default=0,
        type=int,
        help="Specify the left limit",
    )
    parser.add_argument(
        "-R",
        nargs="?",
        dest="R",
        const=-1,
        default=-1,
        type=int,
        help="Specify the right limit",
    )
    parser.add_argument(
        "-T",
        nargs="?",
        dest="T",
        const=0,
        default=0,
        type=int,
        help="Specify the top limit",
    )
    parser.add_argument(
        "-B",
        nargs="?",
        dest="B",
        const=-1,
        default=-1,
        type=int,
        help="Specify the left limit",
    )
    parser.add_argument(
        "-o",
        nargs="?",
        metavar="output_path",
        dest="opath",
        default="output.pdf",
        help="Specify the output path (optional)",
    )
    args = parser.parse_args()

    pdfcropper = PdfCC(args.Path, args.opath)
    pdfcropper.setPageBoundary(args.L, args.R, args.T, args.B)
    pdfcropper.cropFile()
