import cv2

print(cv2.__version__)

def stitch_images(imgs):

  stitchy = cv2.Stitcher.create()
  status, output = stitchy.stitch(imgs)

  if status != cv2.STITCHER_OK:
    print("Sorry, we can't stitch your images")
  else:
    print("Image Stitching Completed")
  # cv2.imwrite("./output_imgs/panorama.jpg", output)
  return output


def run_main(images):
    # img_num = 3
    # img_path = "./input_imgs/"
    # img_format = ".jpg"


    # imgs = []
    # image_paths = [ img_path + (str(i+1)+img_format) for i in range(img_num) ]
    #print(image_paths)
    # for i in range(len(image_paths)):
    #     imgs.append(cv2.imread(image_paths[i]))
    #     imgs[i]=cv2.resize(imgs[i],(0,0),fx=0.5,fy=0.5)
    for img in images:
      img=cv2.resize(img,(0,0),fx=0.5,fy=0.5)

    if(len(images) > 1):
        output = stitch_images(imgs=images)
        return output
    else:
        print("can't read images\n")