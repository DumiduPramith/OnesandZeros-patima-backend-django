def load_segmentation_model():
    import tensorflow as tf

    import os

    def unet_model_modified(input_size=(256, 256, 1)):
        inputs = tf.keras.layers.Input(input_size)

        # Encoder
        conv1 = tf.keras.layers.Conv2D(64, 3, activation='relu', padding='same')(inputs)
        conv1 = tf.keras.layers.Conv2D(64, 3, activation='relu', padding='same')(conv1)
        pool1 = tf.keras.layers.MaxPooling2D(pool_size=(2, 2))(conv1)

        conv2 = tf.keras.layers.Conv2D(128, 3, activation='relu', padding='same')(pool1)
        conv2 = tf.keras.layers.Conv2D(128, 3, activation='relu', padding='same')(conv2)
        pool2 = tf.keras.layers.MaxPooling2D(pool_size=(2, 2))(conv2)

        conv3 = tf.keras.layers.Conv2D(256, 3, activation='relu', padding='same')(pool2)
        conv3 = tf.keras.layers.Conv2D(256, 3, activation='relu', padding='same')(conv3)
        pool3 = tf.keras.layers.MaxPooling2D(pool_size=(2, 2))(conv3)

        conv4 = tf.keras.layers.Conv2D(512, 3, activation='relu', padding='same')(pool3)
        conv4 = tf.keras.layers.Conv2D(512, 3, activation='relu', padding='same')(conv4)
        pool4 = tf.keras.layers.MaxPooling2D(pool_size=(2, 2))(conv4)

        conv5 = tf.keras.layers.Conv2D(1024, 3, activation='relu', padding='same')(pool4)
        conv5 = tf.keras.layers.Conv2D(1024, 3, activation='relu', padding='same')(conv5)

        # Decoder
        up6 = tf.keras.layers.Conv2DTranspose(512, 2, strides=(2, 2), padding='same')(conv5)
        merge6 = tf.keras.layers.concatenate([conv4, up6], axis=3)
        conv6 = tf.keras.layers.Conv2D(512, 3, activation='relu', padding='same')(merge6)
        conv6 = tf.keras.layers.Conv2D(512, 3, activation='relu', padding='same')(conv6)

        up7 = tf.keras.layers.Conv2DTranspose(256, 2, strides=(2, 2), padding='same')(conv6)
        merge7 = tf.keras.layers.concatenate([conv3, up7], axis=3)
        conv7 = tf.keras.layers.Conv2D(256, 3, activation='relu', padding='same')(merge7)
        conv7 = tf.keras.layers.Conv2D(256, 3, activation='relu', padding='same')(conv7)

        up8 = tf.keras.layers.Conv2DTranspose(128, 2, strides=(2, 2), padding='same')(conv7)
        merge8 = tf.keras.layers.concatenate([conv2, up8], axis=3)
        conv8 = tf.keras.layers.Conv2D(128, 3, activation='relu', padding='same')(merge8)
        conv8 = tf.keras.layers.Conv2D(128, 3, activation='relu', padding='same')(conv8)

        up9 = tf.keras.layers.Conv2DTranspose(64, 2, strides=(2, 2), padding='same')(conv8)
        merge9 = tf.keras.layers.concatenate([conv1, up9], axis=3)
        conv9 = tf.keras.layers.Conv2D(64, 3, activation='relu', padding='same')(merge9)
        conv9 = tf.keras.layers.Conv2D(64, 3, activation='relu', padding='same')(conv9)

        conv10 = tf.keras.layers.Conv2D(1, 1, activation='sigmoid')(conv9)

        model = tf.keras.models.Model(inputs=inputs, outputs=conv10)
        return model

    model = unet_model_modified()
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4), loss='binary_crossentropy',
                  metrics=['accuracy'])
    model_path = os.path.join('prediction','ml_models','segmentation')
    seg_model_path = os.path.join(model_path, 'unet_best_model_2.keras')
    model = tf.keras.models.load_model(seg_model_path)
    return model