import face_recognition
import sqlite3
import os
from PIL import Image

# SQLite DB 연결
conn = sqlite3.connect('./our_faces.db')
cursor = conn.cursor()

# 데이터베이스에서 이름과 얼굴 벡터 조회
cursor.execute('SELECT name, encoding FROM faces')
rows = cursor.fetchall()

# 결과 출력
for row in rows:
    name, encoding = row
    print(f"Name: {name}, Encoding: {encoding}")

# 얼굴 이미지에서 특징 벡터를 추출하고 데이터베이스에 저장하는 함수
def save_face_encoding(image_path, name):
    # 얼굴 이미지 불러오기
    image = face_recognition.load_image_file(image_path)
    
    # 얼굴 특징 벡터 추출 (이미지에서 첫 번째 얼굴)
    face_encoding = face_recognition.face_encodings(image)
    
    if face_encoding:  # 얼굴이 존재하면
        face_encoding = face_encoding[0]  # 첫 번째 얼굴 벡터만 사용
        
        # 데이터베이스에 얼굴 벡터 저장
        cursor.execute("INSERT INTO faces (name, encoding) VALUES (?, ?)", 
                       (name, face_encoding.tobytes()))  # BLOB으로 저장
        conn.commit()
        print(f"Saved {name}'s face encoding to the database.")
    else:
        print(f"No face found in the image for {name}.")
        
        
# 이미지 폴더에서 사람들의 얼굴 벡터 저장
# def save_all_faces_from_folder(folder_path):
#     for filename in os.listdir(folder_path):
#         if filename.endswith(".jpg") or filename.endswith(".png"):
#             image_path = os.path.join(folder_path, filename)
#             name = os.path.splitext(filename)[0]  # 파일명에서 이름 추출
#             save_face_encoding(image_path, name)


# 새로운 사람의 얼굴 벡터 추가 함수
def add_new_person(image_path, name):
    print(f"Adding {name} to the database...")
    save_face_encoding(image_path, name)

# 새로운 사람 추가
# 이미지 파일 경로와 이름을 전달
folder_path = './face_images/new_person.jpg'  # 새로운 사람의 얼굴 이미지 경로
new_name = 'New Person'  # 새로운 사람의 이름

# 새로운 사람 추가
add_new_person(folder_path, new_name)

# 연결 종료
conn.close()
