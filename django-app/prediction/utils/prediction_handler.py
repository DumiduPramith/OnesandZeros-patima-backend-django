import logging
import os

import cv2
import numpy as np
import tensorflow as tf
from django.apps import apps
from fontTools.ttx import process
from torch import dtype

from patima.utils.database_handler import DatabaseHandler
from prediction.utils.raw_image_handler import RawImageHandler
from prediction.utils.predicted_image_handler import PredictedImageHandler

if os.getenv('DJANGO_ENV') == 'dev':
    from matplotlib import pyplot as plt

logger = logging.getLogger(__name__)

class PredictionHandler(RawImageHandler, PredictedImageHandler):
    def __init__(self,usr_obj):
        RawImageHandler.__init__(self,user_obj=usr_obj)
        PredictedImageHandler.__init__(self,user_obj=usr_obj)
        self.segmentation_model = apps.get_app_config('prediction').segmentation_model
        self.new_generator = apps.get_app_config('prediction').new_generator
        self.__usr_obj = usr_obj

        self.__image_size = apps.get_app_config('prediction').prediction_config['image_size']
        self.__padding = apps.get_app_config('prediction').prediction_config['padding']

    def admin_retrieve_predictions_by_user_id(self, page_number=1):
        # Admin Panel - Retrieve all predictions by user id
        LIMIT = 10
        offset = (page_number - 1) * LIMIT
        sql = """
        SELECT i.image_id, i.input_image_path, i.created_at,i.predicted_image_path,it.tag_name
        FROM image i
        JOIN image_tags it ON it.image_id = i.image_id
        WHERE i.uploader_id = %s
        ORDER BY i.created_at DESC
        LIMIT %s OFFSET %s
        """
        params = (self._user_obj.id, LIMIT, offset)
        try:
            data = DatabaseHandler.run_select_query(sql, params)
            if data[0]['predicted_image_path'] is None:
                data[0]['predicted_image_path'] = '/static/predicted_images/error.png'
            return data
        except Exception as e:
            logger.error(f'Error occurred: {e}')
            return False

    def retrieve_predictions_by_user_id(self, page_number=1):
        # Retrieve all predictions by user id
        LIMIT = 10
        offset = (page_number - 1) * LIMIT
        sql = """
        SELECT i.image_id, i.input_image_path, i.created_at,i.predicted_image_path, it.tag_name
        FROM image i
        JOIN image_tags it ON it.image_id = i.image_id
        WHERE i.uploader_id = %s
        ORDER BY i.created_at DESC
        LIMIT %s OFFSET %s
        """
        params = (self._user_obj.id, LIMIT, offset)
        try:
            data = DatabaseHandler.run_select_query(sql, params)
            if data[0]['predicted_image_path'] is None:
                data[0]['predicted_image_path'] = '/static/predicted_images/error.png'
            return data
        except Exception as e:
            logger.error(f'Error occurred: {e}')
            return False

    def get_predicted_image(self):
        # Get last predicted image details
        sql = 'SELECT image_id, input_image_path,predicted_image_path,created_at FROM image WHERE image_id = %s '
        params = (self._image_id,)
        try:
            data = DatabaseHandler.run_select_query(sql, params)
            if data:
                if not data[0]['predicted_image_path']:
                    data[0]['predicted_image_path'] = '/static/predicted_images/error.png'
            return data[0]
        except Exception as e:
            logger.error(f'Error occurred: {e}')
            return False

    def save_locations(self,long,lat):
        # Save GPS locations
        sql = """
        INSERT INTO image_tags (image_id, tag_name)
        VALUES (%s, CONCAT(%s, ',',%s))
        """
        try:
            DatabaseHandler.run_insert_query(sql, (self._image_id, long,lat))
            return True
        except Exception as e:
            logger.error(f'Error occurred: {e}')
            return False

    def retrieve_nearby_predictions(self, prediction_id, page):
        # Retrieve nearby predictions based on GPS locations on given prediction_id
        LIMIT = 10
        OFFSET = (int(page) - 1) * LIMIT

        sql = """
        SELECT i.*
        FROM image_tags it1
        JOIN image_tags it2 ON 6371 * acos(
            cos(radians(SUBSTRING_INDEX(it1.tag_name, ',', 1))) *
            cos(radians(SUBSTRING_INDEX(it2.tag_name, ',', 1))) *
            cos(radians(SUBSTRING_INDEX(it2.tag_name, ',', -1)) - radians(SUBSTRING_INDEX(it1.tag_name, ',', -1))) +
            sin(radians(SUBSTRING_INDEX(it1.tag_name, ',', 1))) *
            sin(radians(SUBSTRING_INDEX(it2.tag_name, ',', 1)))
          ) <= 5
        JOIN image i ON it2.image_id = i.image_id
        WHERE it1.image_id =%s
        LIMIT %s OFFSET %s;
        """
        try:
            data = DatabaseHandler.run_select_query(sql, (prediction_id,LIMIT, OFFSET,))
        except Exception as e:
            logger.error(f'Error occurred: {e}')
            return False
        if data[0]['predicted_image_path'] is None:
            data[0]['predicted_image_path'] = '/static/predicted_images/error.png'
        return data

    def segment_image(self, input_image):
        # Convert TensorFlow tensor to NumPy array
        np_arr = tf.cast(input_image, tf.uint8).numpy()

        # convert RGB (tensorflow format) to BGR (opencv format)
        img = cv2.cvtColor(np_arr, cv2.COLOR_RGB2BGR)

        if img is None:
            logger.error('Could not decode the input image')
            return False

        H, W, _ = img.shape
        results = self.segmentation_model.predict(source=img, save=False, conf=0.25, verbose=False)

        for result in results:
            for mask in result.masks.data:
                mask = mask.cpu().numpy()
                mask_resized = cv2.resize(mask, (W, H))
                mask_resized = (mask_resized > 0.5).astype(np.uint8)

                # Apply the mask directly to the image
                segmented_image = cv2.bitwise_and(img, img, mask=mask_resized)

                # Keep the segmented image in the original coordinates
                return segmented_image

    @staticmethod
    def __post_processing(generated_image, segmented_image):
        segmented_image = segmented_image.numpy()[0] * 0.5 + 0.5
        generated_image = generated_image.numpy()

        # mask = (segmented_image == 1)
        tolerance = 1e-6
        mask = tf.reduce_all(tf.abs(segmented_image -1) < tolerance, axis=-1).numpy()
        mask = mask[..., None]

        masked_generated_image = generated_image * mask

        plt.figure(figsize=(12,6))

        plt.subplot(1, 3, 1)
        plt.title('Segmented Image')
        plt.imshow(segmented_image)
        plt.axis('off')

        plt.subplot(1, 3, 2)
        plt.title("Generated Image")
        plt.imshow(generated_image)
        plt.axis("off")

        # Display the masked part of the generated image
        plt.subplot(1, 3, 3)
        plt.title("Masked Generated Image")
        plt.imshow(masked_generated_image)
        plt.axis("off")

        plt.tight_layout()
        plt.show()


    def predict(self, input_image):
        # make prediction using the input image
        input_image.seek(0)
        image_bytes = input_image.read()
        input_tensor = tf.io.decode_image(image_bytes, channels=3, expand_animations=False)

        # Resize the image
        resized_image = self._resize(input_tensor)

        segmented_image = self.segment_image(resized_image)

        if segmented_image is False:
            return False

        segmented_image = cv2.cvtColor(segmented_image, cv2.COLOR_BGR2RGB)

        segmented_image = tf.cast(segmented_image, tf.float32)

        segmented_image = self._normalize(segmented_image)
        segmented_image = tf.expand_dims(segmented_image, 0)
        generated_image = self.new_generator(segmented_image, training=True)
        generated_image = generated_image[0] * 0.5 + 0.5

        # processed_image = self.__post_processing(generated_image, segmented_image)

        # processed_image = tf.squeeze(processed_image, axis=0)
        #
        if os.getenv('DJANGO_ENV') == 'dev':
            image_data = tf.image.decode_image(image_bytes, channels=3)
            image_data = tf.cast(image_data, tf.uint8)
            input_image_np = image_data._numpy()
            plt.subplot(1, 3, 1)
            plt.imshow(input_image_np)
            plt.title('Input Image')
            plt.subplot(1, 3, 2)
            # plt.imshow(generated_image)
            plt.imshow(segmented_image[0] * 0.5 + 0.5)
            plt.title('Segmented Image')
            plt.subplot(1, 3, 3)
            plt.imshow(generated_image)
            plt.title('Generated Image')
            plt.show()


        return generated_image
