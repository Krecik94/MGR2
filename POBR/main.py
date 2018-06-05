import cv2
import numpy as np
import time
import sys

sys.setrecursionlimit(2000)


def is_stop_sign(img, upper, lower, left, right):
    height = lower - upper
    width = right - left

    if width ==0:
        return False

    if height / width <=0.8 or height / width >= 1.2:
        return False

    inner_region_points = []
    found_inner_regions = []

    for i in range(upper,lower):
        for j in range(left,right):
            if (i, j) in inner_region_points:
                continue

            if img[i, j, 0] == 64:
                found_region = fill_region(img[upper:lower, left:right], i-upper, j-left, inner_region_points, found_inner_regions, [], 0, 64)
                if len(found_region) > width*height*0.015 and len(found_region) >3:
                    print (len(found_region))
                    found_inner_regions.append(found_region)

    print(width*height)
    print('inner regions: %s'%len(found_inner_regions))
    if len(found_inner_regions) not in [6, 7,8]:
        return False

    return True


def fill_region(img, i, j, analysed_points, found_regions, current_region, depth_counter, value):
    depth_counter += 1
    if (i, j) in analysed_points:
        # print('hit')
        return current_region
    # print(depth_counter)
    analysed_points.append((i, j))

    if img[i, j, 0] == value:
        current_region.append((i, j))
        if i > 1:
            fill_region(img, i - 1, j, analysed_points, found_regions, current_region, depth_counter, value)
        if i < (len(img) - 2):
            fill_region(img, i + 1, j, analysed_points, found_regions, current_region, depth_counter, value)
        if j > 1:
            fill_region(img, i, j - 1, analysed_points, found_regions, current_region, depth_counter, value)
        if j < (len(img[0]) - 2):
            fill_region(img, i, j + 1, analysed_points, found_regions, current_region, depth_counter, value)

    return current_region


def main():
    img = cv2.imread('images\\5.jpg')
    # hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # for i in range(len(hsv_image)):
    #     for j in range(len(hsv_image[0])):
    #         if (hsv_image[i][j][0] in range(160, 200)):
    #             hsv_image[i][j][0] = 160
    #             hsv_image[i][j][1] = 0
    #             hsv_image[i][j][2] = 255
    #         else:
    #             hsv_image[i][j][0] = 0
    #             hsv_image[i][j][1] = 0
    #             hsv_image[i][j][2] = 0

    for i in range(len(img)):
        for j in range(len(img[0])):
            if (img[i][j][2] > 170 and img[i][j][0] < 180 and img[i][j][1] < 180):
                img[i][j][0] = 255
                img[i][j][1] = 255
                img[i][j][2] = 255
            else:
                img[i][j][0] = 64
                img[i][j][1] = 64
                img[i][j][2] = 64

    found_upper = None
    # Calculating upper bound
    for i in range(len(img)):
        if list(img[i, 0:, 0]).count(255) > len(img) / 7:
            found_upper = i
            break

    found_lower = None
    for i in reversed(range(len(img))):
        if list(img[i, 0:, 0]).count(255) > len(img) / 7:
            found_lower = i
            break

    found_left = None
    for i in range(len(img[0])):
        if list(img[0:, i, 0]).count(255) > len(img[0]) / 7:
            print(list(img[i, 0:, 0]).count(255))
            found_left = i
            break

    found_right = None
    for i in reversed(range(len(img[0]))):
        if list(img[0:, i, 0]).count(255) > len(img[0]) / 7:
            print(list(img[i, 0:, 0]).count(255))
            found_right = i
            break

    # img[found_upper, 0:, 0] = 255
    # img[found_lower, 0:, 0] = 255
    # img[0:, found_left, 0] = 255
    # img[0:, found_right, 0] = 255

    # getting regions

    analysed_points = []
    found_regions = []

    for i in range(len(img)):
        for j in range(len(img[0])):
            if (i, j) in analysed_points:
                continue

            if img[i, j, 0] == 255:
                found_region = fill_region(img, i, j, analysed_points, found_regions, [], 0, 255)
                if len(found_region) > 10:
                    found_regions.append(found_region)

    print(len(found_regions))

    for region in found_regions:
        upper = min(region, key=lambda x: x[0])[0]
        lower = max(region, key=lambda x: x[0])[0]
        left = min(region, key=lambda x: x[1])[1]
        right = max(region, key=lambda x: x[1])[1]

        if is_stop_sign(img, upper, lower, left, right):
            img[upper, left:right, 1] = 255
            img[lower, left:right, 1] = 255
            img[upper:lower, left, 1] = 255
            img[upper:lower, right, 1] = 255
        else:
            img[upper, left:right, 2] = 255
            img[lower, left:right, 2] = 255
            img[upper:lower, left, 2] = 255
            img[upper:lower, right, 2] = 255

    print(len(img))
    print(len(img[0]))

    # hsv_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
