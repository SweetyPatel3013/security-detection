# API configuration
web_app_port = 8080

# Path where the API will save files
data_dir = './resources/data'
feature_dir = './resources/features'

# Models implemented: TF or DLIB
face_recognition_type = 'DLIB'

# Face mask detection config
mask_prototxt_path = './resources/maskdetector/deploy.prototxt'
mask_weights_path = './resources/maskdetector/res10_300x300_ssd_iter_140000.caffemodel'
mask_model_path = './resources/maskdetector/mask_detector.model'
