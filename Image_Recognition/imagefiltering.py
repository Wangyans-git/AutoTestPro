#!C:\wys\AutoTestProjects
# -*- coding: utf-8 -*-
# @Time    : 
# @Author  :yansheng.wang 
# @File    : 
# @Description : 识别异常图片
import os
import shutil

import cv2
from PIL import Image
from skimage.metrics import structural_similarity as ssim

from log.get_log import GetLog


class FilterHandle:
    def __init__(self):
        # 脚本日志
        self.get_log = GetLog(f"log\\log.log")
        # 设置截图保存路径
        self.video_path = f'video'  # 原视频路径
        self.output_folder_path = f'all_image_frames'  # 分帧后的图片
        self.crop_output_folder_path = f'crop_image'  # 截取处理后的图片
        self.error_image_path = f"error_image"  # 出错的图片

    # 使用结构相似性
    def calculate(self, image1_path):
        try:
            """
                这里的文件名需要和crop_image下的第一张图片名一样，需要和第一张做对比，也就是正常状态的图
            """
            image2_path = f'crop_image\\crop_frame_0000.jpg'  # 正确图片
            image1 = cv2.imread(image1_path, cv2.IMREAD_GRAYSCALE)
            image2 = cv2.imread(image2_path, cv2.IMREAD_GRAYSCALE)
            score, _ = ssim(image1, image2, full=True)
            # print(score)
            return score
        except Exception as e:
            print(e)

    # 遍历图片并输出结果
    def Output_similarity_results(self,similar_value):
        try:
            n = 0
            for file in os.listdir(self.crop_output_folder_path):
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
                    file_path = os.path.join(self.crop_output_folder_path, file)
                    print(f'对比图片: {file_path}')
                    # 输出相似率
                    image1 = f'{file_path}'
                    # image.save("p2.png", image)  # 或'home.png'，目前只支持png 和 jpg格式的图像
                    # 输出相似率
                    result = self.calculate(image1)
                    print("相似度：", result)
                    if result > similar_value:
                        print("该图片没有异常")
                    else:
                        n += 1
                        print(f"发现异常图片:{file_path}")
                        image = Image.open(file_path)
                        save_path = self.error_image_path
                        file_name = os.path.basename(file_path)
                        image.save(save_path + '\\' + file_name)
                    print()
                    # time.sleep(2)
        except Exception as e:
            print("杀掉后台后异常报错：", e)
            print(
                "查看一下“calculate”方法，这里的文件名需要和crop_image下的第一张图片名一样，需要和第一张做对比，也就是正常状态的图：")

    # 裁剪图片
    def crop_image(self, image_path, start_x, start_y, width, height):
        # 读取图像
        image = cv2.imread(image_path)

        if image is None:
            print("Error: Unable to load image.")
            return

        # 获取图像的尺寸
        img_height, img_width = image.shape[:2]

        # 确保裁剪区域在图像范围内
        end_x = min(start_x + width, img_width)
        end_y = min(start_y + height, img_height)

        # 裁剪图像
        cropped_image = image[start_y:end_y, start_x:end_x]
        return cropped_image

    # 保存裁剪后的图像
    def save_crop_image(self, start_x, start_y, width, height):
        n = 0
        print("图片裁剪中..")
        for file in os.listdir(self.output_folder_path):
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
                n += 1
                file_path = os.path.join(self.output_folder_path, file)
                cropped_image = test.crop_image(file_path, start_x, start_y, width, height)
                if cropped_image is not None:
                    # 显示裁剪后的图像
                    cv2.waitKey(1)
                    cv2.destroyAllWindows()
                    # 保存裁剪后的图像
                    cv2.imwrite(f'crop_image\\crop_{file}', cropped_image)
        print("图片裁剪完成")

    # 视频分帧
    def video_framing(self):
        # 确保输出文件夹存在
        if not os.path.exists(self.output_folder_path):
            os.makedirs(self.output_folder_path)
        # 打开视频文件
        files = os.listdir(self.video_path)  # 获取目录下所有文件和文件夹的列表
        frame_count = 0  # 张数
        frame_num = 0  # 序号
        for file in files:
            print('['+file+']',"分帧中..")
            cap = cv2.VideoCapture(self.video_path+'\\'+file)
            while True:
                ret, frame = cap.read()
                # 如果无法读取帧，退出循环
                if not ret:
                    break
                # 保存当前帧为图像文件
                frame_filename = os.path.join(self.output_folder_path, f'frame_{frame_num:04d}.jpg')
                if frame_count % 10 == 0:
                    cv2.imwrite(frame_filename, frame)
                    frame_num += 1
                frame_count += 1
            # 释放资源
            cap.release()
            cv2.destroyAllWindows()
            print('['+file+']',"分帧完成")

    def delete_files_in_directory(self):
        # 检查目录是否存在
        directory_list = [self.error_image_path, self.crop_output_folder_path,self.output_folder_path]
        for directory_path in directory_list:
            if not os.path.exists(directory_path):
                print(f"目录 {directory_path} 不存在")
                return
            # 遍历目录下的所有文件和子目录
            for filename in os.listdir(directory_path):
                file_path = os.path.join(directory_path, filename)
                try:
                    # 如果是文件，删除文件
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                        print(f"文件 {file_path} 已删除")
                    # 如果是目录，递归删除目录
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                        print(f"目录 {file_path} 已删除")
                except Exception as e:
                    print(f"删除文件 {file_path} 失败: {e}")


if __name__ == '__main__':
    test = FilterHandle()

    ########
    # test.delete_files_in_directory()  # 删除上一次的图片目录中图片，不同视频时使用
    ########
    like_value = 0.98    # 大于这个值为正常图片
    start_x, start_y = 160, 660  # 需要截取图片的左上角坐标 (x, y)，使用win画图工具获取
    width, height = 140, 250  # 需要截取图片的宽度和高度
    test.video_framing()  # 视频分帧
    # test.save_crop_image(start_x, start_y, width, height)  # 图片裁剪
    # test.Output_similarity_results(like_value)  # 对比图片相似度
