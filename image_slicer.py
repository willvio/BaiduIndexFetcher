# -*- coding: utf-8 -*-

import numpy
from PIL import Image
from scipy.misc import imsave


class ImageSlicer:

    TEMP_BINARY_IMAGE_PREFIX = 'bi_'
    TEMP_CROPPED_IMAGE_PREFIX = 'crop_'

    def __init__(self, working_dir):
        self.working_dir = working_dir

    # 横切
    @staticmethod
    def __horizontal_cut(digit_array):  # 找到两个端点
        row_sums = []
        for i in range(0, len(digit_array[0])):
            row_sums.append(sum(digit_array[:, i]))

        start = 0
        end = 0
        for i in range(len(row_sums) - 1):
            if row_sums[i] == 0 and row_sums[i + 1] != 0:  # 中间有0可能产生干扰
                start = i + 1
            elif row_sums[i] != 0 and row_sums[i + 1] == 0:
                end = i + 1
        return start, end

    @staticmethod
    def __binarize_image(working_dir, image_file_name, output_file_prefix, threshold=200):
        """Binarize an image."""
        image_file = Image.open(working_dir + image_file_name)
        image = image_file.convert('L')  # convert image to monochrome
        image_array = numpy.array(image)
        bi_image = ImageSlicer.__binarize_array(image_array, threshold)
        imsave(working_dir + output_file_prefix + image_file_name, bi_image)
        return bi_image

    @staticmethod
    def __binarize_array(numpy_array, threshold):
        """Binarize a numpy array."""
        for i in range(len(numpy_array)):
            for j in range(len(numpy_array[0])):
                if numpy_array[i][j] > threshold:
                    numpy_array[i][j] = 255
                else:
                    numpy_array[i][j] = 0
        return numpy_array

    @staticmethod
    def __search_colon(sarray, spos, epos):
        colon = []
        for i in range(len(spos)):
            total_pixel = 0
            if epos[i] - spos[i] == 1 and sarray[spos[i]] == 2:  # 如果只有1列且含两个像素
                for t in range(spos[i]-5, epos[i]+5):
                    total_pixel = total_pixel + sarray[t]
                if total_pixel == 2:  # 这一列的前后三列为空白
                    colon.append(i)
            if epos[i] - spos[i] == 2 and sarray[spos[i]] <=2 and sarray[spos[i]+1] <=2:  # 如果有两列且每列最多两像素
                for t in range(spos[i]-3, epos[i]+3):
                    total_pixel = total_pixel + sarray[t]
                if total_pixel == sarray[spos[i]] + sarray[spos[i]+1]:  # 这两列前后三列为空白
                    colon.append(i)
        return colon

    def pretreatment(self, image_file):

        image_array = ImageSlicer.__binarize_image(self.working_dir,
                                                   image_file,
                                                   ImageSlicer.TEMP_BINARY_IMAGE_PREFIX)
        im1 = numpy.where(image_array > 128, 1, 0)  # binarized array
        # im1 = im1.transpose()
        #
        # # 先纵切 start_pos, end_pos列表分别是一个个的切割起点和终点
        # column_sums = []
        # start_pos = []
        # end_pos = []
        # colon = []
        # for i in range(0, len(im1)):
        #     column_sums.append(sum(im1[i]))
        #
        # if column_sums[0] != 0:
        #     start_pos.append(0)
        # for i in range(len(column_sums) - 1):
        #     if column_sums[i] == 0 and column_sums[i + 1] != 0:
        #         start_pos.append(i + 1)
        #     elif column_sums[i] != 0 and column_sums[i + 1] == 0:
        #         end_pos.append(i + 1)

        # 截取下来的图片数字前面都以冒号开始，冒号在图片中占2个像素（图片中可能会有其他的逗号或者什么也占2个像素）
        # for i in range(0, len(start_pos)):
        #     if end_pos[i]-start_pos[i] == 2:
        #         colon.append(i)

        start_pos = []
        end_pos = []
        column_sums = numpy.sum(im1, axis=0)
        for i in range(column_sums.shape[0] -1):
            if column_sums[i] == 0 and column_sums[i+1] != 0:
                start_pos.append(i+1)
            if column_sums[i] != 0 and column_sums[i+1] == 0:
                end_pos.append(i+1)
        colon = ImageSlicer.__search_colon(column_sums, start_pos, end_pos)
        image = Image.open(self.working_dir + ImageSlicer.TEMP_BINARY_IMAGE_PREFIX + image_file)
        digits = []
        for i in range(colon[0]+1, len(start_pos)):   # d中可能不止一个数字，因此要判断下
            if 4 < end_pos[i] - start_pos[i] < 8:  # 排除其他的干扰，数字都在4-8个像素之间
                try:
                    x_start = start_pos[i]
                    x_end = end_pos[i]
                    y_start, y_end = self.__horizontal_cut(im1.transpose()[x_start:x_end])
                    ima2 = image.crop((x_start, y_start, x_end, y_end))
                    digits.append(ima2)
                except Exception as ex:
                    print(ex)
        return digits
