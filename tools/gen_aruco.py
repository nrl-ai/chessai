import cv2


def generate_single_marker(aruco_dict):
    marker_size = int(input("Enter the marker size: "))
    marker_id = int(input("Enter the marker ID: "))
    marker_img = cv2.aruco.generateImageMarker(aruco_dict, marker_id, marker_size)
    cv2.imwrite("marker_{}.png".format(marker_id), marker_img)
    marker_img = cv2.imread("marker_{}.png".format(marker_id))
    print("Dimensions:", marker_img.shape)


def generate_bulk_markers(aruco_dict):
    marker_size = int(input("Enter the marker size: "))
    num_markers = int(input("Enter the number of markers to generate: "))
    marker_imgs = []
    for marker_id in range(num_markers):
        marker_img = cv2.aruco.generateImageMarker(aruco_dict, marker_id, marker_size)

        cv2.imwrite("marker_{}.png".format(marker_id), marker_img)
        marker_imgs.append(cv2.imread("marker_{}.png".format(marker_id)))


def main():
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
    user_input = input(
        "Press '1' to generate a single marker or " "'2' to generate markers in bulk: "
    )
    if user_input == "1":
        generate_single_marker(aruco_dict)
    elif user_input == "2":
        generate_bulk_markers(aruco_dict)
    else:
        print("Invalid input. Please try again.")


if __name__ == "__main__":
    main()
