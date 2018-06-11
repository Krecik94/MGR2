import cv2
import numpy as np
import time
import sys

sys.setrecursionlimit(4000)


def is_stop_sign(img, upper, lower, left, right):
    height = lower - upper
    width = right - left

    if width == 0:
        return False

    if height / width <= 0.8 or height / width >= 1.2:
        return False

    inner_region_points = []
    found_inner_regions = []

    for i in range(upper, lower):
        for j in range(left, right):
            if (i, j) in inner_region_points:
                continue

            if img[i, j, 0] == 64:
                found_region = fill_region(img[upper:lower, left:right], i - upper, j - left, inner_region_points,
                                           found_inner_regions, [], 0, 64)
                if len(found_region) > width * height * 0.015 and len(found_region) > 3:
                    # print(len(found_region))
                    found_inner_regions.append(found_region)

    print('size %s' % (width * height))
    print('inner regions: %s' % len(found_inner_regions))
    M1 = calculateM1(img, upper, lower, left, right, 255)
    M7 = calculateM7(img, upper, lower, left, right, 255)
    print('M1: %s' % M1)
    print('M7: %s' % M7)

    if len(found_inner_regions) not in [6, 7, 8]:
        return False

    if M1 > 0.2277 or M1 < 0.1683:
        return False

    if M7 > 0.012 or M7 < 0.00833:
        return False

    # check letters
    if len(found_inner_regions) == 8:
        letter_regions = []
        for region in found_inner_regions:
            # Calculating bounding boxes
            inner_upper = min(region, key=lambda x: x[0])[0] + upper
            inner_lower = max(region, key=lambda x: x[0])[0] + upper
            inner_left = min(region, key=lambda x: x[1])[1] + left
            inner_right = max(region, key=lambda x: x[1])[1] + left

            # Checking if found segment is a stop sign

            img[inner_upper, inner_left:inner_right, 1] = 122
            img[inner_lower, inner_left:inner_right, 1] = 122
            img[inner_upper:inner_lower, inner_left, 1] = 122
            img[inner_upper:inner_lower, inner_right, 1] = 122
            img[inner_upper, inner_left:inner_right, 2] = 122
            img[inner_lower, inner_left:inner_right, 2] = 122
            img[inner_upper:inner_lower, inner_left, 2] = 122
            img[inner_upper:inner_lower, inner_right, 2] = 122
            img[inner_upper, inner_left:inner_right, 0] = 0
            img[inner_lower, inner_left:inner_right, 0] = 0
            img[inner_upper:inner_lower, inner_left, 0] = 0
            img[inner_upper:inner_lower, inner_right, 0] = 0

            if not (inner_upper in [upper, upper - 1, upper + 1]
                    or inner_lower in [lower, lower - 1, lower + 1]
                    or inner_left in [left, left - 1, left + 1]
                    or inner_right in [right, right - 1, right + 1]):
                letter_regions.append(region)
        print('letter regions: %s' % len(letter_regions))
        if len(letter_regions) == 4:
            # Sorting all points in region from left to right
            for region in letter_regions:
                region.sort(key=lambda x: x[1])

            # Sorting letters from left to right
            letter_regions.sort(key=lambda x: x[0][1])
            for region_number in range(4):
                inner_upper = min(letter_regions[region_number], key=lambda x: x[0])[0] + upper
                inner_lower = max(letter_regions[region_number], key=lambda x: x[0])[0] + upper
                inner_left = min(letter_regions[region_number], key=lambda x: x[1])[1] + left
                inner_right = max(letter_regions[region_number], key=lambda x: x[1])[1] + left

                M1 = calculateM1(img, inner_upper, inner_lower, inner_left, inner_right, 64)
                M7 = calculateM7(img, inner_upper, inner_lower, inner_left, inner_right, 64)

                if region_number == 0:
                    print('S M1: %s, M7: %s' % (M1, M7))
                    if M1 > 0.58 or M1 < 0.45:
                        return False
                    if M7 > 0.045 or M7 < 0.03:
                        return False

                if region_number == 1:
                    print('T M1: %s, M7: %s' % (M1, M7))
                    if M1 > 0.58 or M1 < 0.48:
                        return False
                    if M7 > 0.02 or M7 < 0.01:
                        return False

                if region_number == 2:
                    print('O M1: %s, M7: %s' % (M1, M7))
                    if M1 > 0.47 or M1 < 0.38:
                        return False
                    if M7 > 0.045 or M7 < 0.03:
                        return False

                if region_number == 3:
                    print('P M1: %s, M7: %s' % (M1, M7))
                    if M1 > 0.45 or M1 < 0.32:
                        return False
                    if M7 > 0.04 or M7 < 0.01:
                        return False

    return True


def calculate_M(img, upper, lower, left, right, p, q, color):
    M = 0
    center = calculateCenter(img, upper, lower, left, right, color)
    for i in range(upper, lower):
        for j in range(left, right):
            if img[i, j, 0] == color:
                M = M + np.power(i - center[0], p) * np.power(j - center[1], q)
    return M


def calculateM1(img, upper, lower, left, right, color):
    return ((float(calculate_M(img, upper, lower, left, right, 2, 0, color)) +
             float(calculate_M(img, upper, lower, left, right, 0, 2, color))) /
            np.power(float(calculate_m(img, upper, lower, left, right, 0, 0, color)), 2))


def calculateM7(img, upper, lower, left, right, color):
    return ((float(calculate_M(img, upper, lower, left, right, 2, 0, color)) *
             float(calculate_M(img, upper, lower, left, right, 0, 2, color)) -
             np.power(float(calculate_M(img, upper, lower, left, right, 1, 1, color)), 2)) /
            np.power(float(calculate_m(img, upper, lower, left, right, 0, 0, color)), 4))


def calculateCenter(img, upper, lower, left, right, color):
    center = []
    center.append(
        calculate_m(img, upper, lower, left, right, 1, 0, color) / calculate_m(img, upper, lower, left, right, 0, 0,
                                                                               color))
    center.append(
        calculate_m(img, upper, lower, left, right, 0, 1, color) / calculate_m(img, upper, lower, left, right, 0, 0,
                                                                               color))
    return center


def calculate_m(img, upper, lower, left, right, p, q, color):
    m = 0
    for i in range(upper, lower):
        for j in range(left, right):
            if img[i, j, 0] == color:
                m = m + np.power(i, p) * np.power(j, q)
    return m


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
    img = cv2.imread('images\\quadruple.jpg')
    img = cv2.resize(img, (200, int(len(img) / len(img[0]) * 200)))
    hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # for i in range(len(hsv_image)):
    #     for j in range(len(hsv_image[0])):
    #         if (hsv_image[i][j][0] in range(177, 180)) or (hsv_image[i][j][0] in range(0, 3)):
    #             hsv_image[i][j][0] = 160
    #             hsv_image[i][j][1] = 0
    #             hsv_image[i][j][2] = 255
    #         else:
    #             hsv_image[i][j][0] = 0
    #             hsv_image[i][j][1] = 0
    #             hsv_image[i][j][2] = 0

    # Detecting red
    for i in range(len(img)):
        for j in range(len(img[0])):
            if (img[i][j][2] > 160 and img[i][j][0] < 180 and img[i][j][1] < 180):
                img[i][j][0] = 255
                img[i][j][1] = 255
                img[i][j][2] = 255
            else:
                img[i][j][0] = 64
                img[i][j][1] = 64
                img[i][j][2] = 64

    # img[found_upper, 0:, 0] = 255
    # img[found_lower, 0:, 0] = 255
    # img[0:, found_left, 0] = 255
    # img[0:, found_right, 0] = 255

    # getting regions

    analysed_points = []
    found_regions = []

    # Segmenting
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
        # Calculating bounding boxes
        upper = min(region, key=lambda x: x[0])[0]
        lower = max(region, key=lambda x: x[0])[0]
        left = min(region, key=lambda x: x[1])[1]
        right = max(region, key=lambda x: x[1])[1]

        # Checking if found segment is a stop sign
        if is_stop_sign(img, upper, lower, left, right):
            img[upper, left:right, 1] = 255
            img[lower, left:right, 1] = 255
            img[upper:lower, left, 1] = 255
            img[upper:lower, right, 1] = 255
            img[upper, left:right, 2] = 0
            img[lower, left:right, 2] = 0
            img[upper:lower, left, 2] = 0
            img[upper:lower, right, 2] = 0
            img[upper, left:right, 0] = 0
            img[lower, left:right, 0] = 0
            img[upper:lower, left, 0] = 0
            img[upper:lower, right, 0] = 0
        else:
            img[upper, left:right, 2] = 255
            img[lower, left:right, 2] = 255
            img[upper:lower, left, 2] = 255
            img[upper:lower, right, 2] = 255
            img[upper, left:right, 0] = 0
            img[lower, left:right, 0] = 0
            img[upper:lower, left, 0] = 0
            img[upper:lower, right, 0] = 0
            img[upper, left:right, 1] = 0
            img[lower, left:right, 1] = 0
            img[upper:lower, left, 1] = 0
            img[upper:lower, right, 1] = 0

    print(len(img))
    print(len(img[0]))

    # hsv_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)

    cv2.imwrite('images\\quadruple_solved.jpg', img)
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
