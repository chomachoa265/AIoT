from flask import Flask, render_template, request, make_response, send_file, jsonify
from flask_cors import CORS
from flask_ngrok import run_with_ngrok

import os
import json
import pymysql
import numpy
import cv2
import random
from utils.stitch_grad_cam import gradCAM
from utils.stitcher import run_main
from utils.fileHandler import file2img, cropImage
from utils.auto_exposure import *

myserver ="localhost"
myuser="test123"
mypassword="test123"
mydb="aiotdb"

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'media')

@app.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    conn = pymysql.connect(host=myserver,user=myuser, passwd=mypassword, db=mydb)
    c = conn.cursor()
    c.execute("DELETE FROM repos WHERE repo_id={0}".format(id))
    conn.commit()
    c.close()
    conn.close()

    return "OK"

@app.route('/api', methods=['GET', 'POST'])
def api():
    repoName = request.form.get('repoName')
    files = request.files.getlist('file')

    conn = pymysql.connect(host=myserver,user=myuser, passwd=mypassword, db=mydb)
    c = conn.cursor()
    c.execute("INSERT INTO repos (name) VALUES ('{0}')".format(repoName))
    new_repo_id = conn.insert_id()
    input_dir_path = os.path.join(app.config['UPLOAD_FOLDER'], str(new_repo_id), 'source')
    os.makedirs(input_dir_path, exist_ok=True)
    images = []
    for idx, file in enumerate(files):
        img = file2img(file)
        images.append(img)
        cv2.imwrite(input_dir_path + '/{0}'.format(file.filename), img)
        c.execute("INSERT INTO images (repo_id, image_url, type) VALUES ({0}, '{1}', '{2}')".format(new_repo_id, file.filename, 'source'))


    output_dir_path = os.path.join(app.config['UPLOAD_FOLDER'], str(new_repo_id), 'results')
    os.makedirs(output_dir_path, exist_ok=True)
    # stitching images & upload to database
    resp = make_response()
    panorama = run_main(images)
    if panorama is not None:
        panorama = cropImage(panorama)
        panorama_path = output_dir_path + '/{0}'.format("panorama.jpg")
        enhanced_panorama_path = output_dir_path + '/{0}'.format("enhanced_panorama.jpg")
        grad_cam_panorama_path = output_dir_path + '/{0}'.format("grad_cam_panorama.jpg")
        cv2.imwrite(panorama_path, panorama)
        image = cv2.imread(panorama_path, 1)
        # enhanced_image = modify(image)
        enhanced_image = exCorrectTest(image)
        cv2.imwrite(enhanced_panorama_path, enhanced_image)

        image_r = image[:, :, 2].mean()
        image_g = image[:, :, 1].mean()
        image_b = image[:, :, 0].mean()
        image_l = image.mean()

        cam_image = gradCAM(enhanced_image)
        cv2.imwrite(grad_cam_panorama_path, cam_image)
        c.execute("INSERT INTO images (repo_id, image_url, type) VALUES ({0}, '{1}', '{2}')".format(new_repo_id, "panorama.jpg", 'results'))
        c.execute("INSERT INTO images (repo_id, image_url, type, image_r, image_g, image_b, lightness) VALUES ({0}, '{1}', '{2}', {3}, {4}, {5}, {6})".format(new_repo_id, "enhanced_panorama.jpg", 'results', image_r, image_g, image_b, image_l))
        c.execute("INSERT INTO images (repo_id, image_url, type) VALUES ({0}, '{1}', '{2}')".format(new_repo_id, "grad_cam_panorama.jpg", 'results'))

        conn.commit()
        c.close()
        conn.close()
        resp = jsonify({
            'status_text': "Processing Completed" 
        })
    else:
        resp = jsonify({
            "status_text": "Processing Failed (Can't stitch your images)"
        })

    return resp


@app.route('/repos')
def repos():
    conn = pymysql.connect(host=myserver,user=myuser, passwd=mypassword, db=mydb)
    # return dict type
    c = conn.cursor(pymysql.cursors.DictCursor) 
    c.execute("SELECT repos.repo_id, repos.name, COUNT(images.image_id) as `number_of_images` FROM `images` INNER JOIN `repos` ON repos.repo_id = images.repo_id GROUP BY repos.repo_id")
    info = c.fetchall()
    c.close()
    conn.close()
    resp = jsonify(info)
    return resp

@app.route('/chartData/<int:id>')
def chartData(id):
    conn = pymysql.connect(host=myserver,user=myuser, passwd=mypassword, db=mydb)
    # return dict type
    c = conn.cursor(pymysql.cursors.DictCursor) 
    c.execute("SELECT images.image_r, images.image_g, images.image_b, images.lightness FROM `images` INNER JOIN `repos` ON repos.repo_id = images.repo_id AND images.lightness > 0 AND repos.repo_id = {0} GROUP BY repos.repo_id;".format(id))
    info = c.fetchall()
    c.close()
    conn.close()
    resp = jsonify(info)
    return resp

@app.route('/dashboardData')
def dashboardData():
    conn = pymysql.connect(host=myserver,user=myuser, passwd=mypassword, db=mydb)
    # return dict type
    c = conn.cursor(pymysql.cursors.DictCursor) 
    c.execute("SELECT AVG(number_of_images) as avg_images FROM (SELECT COUNT(image_id) as number_of_images FROM `images` GROUP BY repo_id) as alias;")
    # c.execute("SELECT images.lightness FROM `images` INNER JOIN `repos` ON repos.repo_id = images.repo_id AND images.lightness > 0 AND repos.repo_id = {0} GROUP BY repos.repo_id;".format(id))
    avg_images_dict = c.fetchone()
    c.execute("SELECT SUM(downloads_count) as total_downloads, COUNT(repo_id) as total_repos FROM repos")
    total_repos_dict = c.fetchone()
    c.execute("SELECT AVG(lightness) as avg_lightness FROM images WHERE lightness > 0")
    avg_lightness_dict = c.fetchone()

    info = {
        'avg_images': avg_images_dict['avg_images'],
        'total_repos': total_repos_dict['total_repos'],
        'avg_lightness': avg_lightness_dict['avg_lightness'],
        'total_downloads': total_repos_dict['total_downloads']
    }

    c.close()
    conn.close()
    resp = jsonify(info)
    return resp

@app.route('/dashboardChartData')
def dashboardChartData():
    conn = pymysql.connect(host=myserver,user=myuser, passwd=mypassword, db=mydb)
    # return dict type
    c = conn.cursor(pymysql.cursors.DictCursor) 
    c.execute("SELECT AVG(image_r) as avg_r, AVG(image_g) as avg_g, AVG(image_b) as avg_b, AVG(lightness) as avg_lightness FROM images WHERE lightness > 0;")
    colorInfo = c.fetchone()
    c.close()
    conn.close()
    resp = jsonify(colorInfo)
    return resp



@app.route('/downloads/<path:repoID>')
def downloads(repoID):
    conn = pymysql.connect(host=myserver,user=myuser, passwd=mypassword, db=mydb)
    # return dict type
    c = conn.cursor(pymysql.cursors.DictCursor) 
    c.execute("SELECT downloads_count FROM repos WHERE repo_id = {0};".format(repoID))
    currCount = c.fetchone()['downloads_count']
    c.execute("UPDATE repos SET downloads_count = {0} WHERE repo_id = {1};".format(currCount+1, repoID))
    conn.commit()

    c.close()
    conn.close()
    from zipfile import ZipFile
    import glob
    path = "./media/{0}/results/*".format(repoID)
    file_list = glob.glob(path)
    file_name = "./media/{0}/results/results_{0}.zip".format(repoID)
    
    if os.path.exists(file_name):
        return send_file(file_name)
    else:
        with ZipFile(file_name, 'w') as zip:
            for file in file_list:
                zip.write(file, arcname=os.path.basename(file))
            zip.close()
            return send_file(file_name)

@app.route('/media/<path:repoID>/<path:type>/<path:filename>')
def media(repoID, type, filename):
    return send_file("./media/{0}/{1}/{2}".format(repoID, type, filename))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)


    