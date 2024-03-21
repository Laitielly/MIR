import opensmile
import pandas as pd
import pickle
import re
import joblib
import os
import xgboost
class Emo_Classification:
    def __init__(self):
        self.model_path = os.getcwd() + '/' + 'model_59acc.joblib'
        self.scaler_path = os.getcwd() + '/' + 'scaler.joblib'
        self.features = None
        self.dict_classes = {0: 'злость', 1: 'скука', 2: 'спокойствие', 3: 'взволнованность',
                             4: 'радость', 5: 'удовлетворение', 6: 'печаль', 7: 'усталость'}
        with open(os.getcwd() +'/' + 'feature_cols', "rb") as fp:
            self.feature_cols = pickle.load(fp)

    def recognize_emotion(self, audio_path):
        self.extract_features(audio_path)
        self.features.set_index(pd.Series(0), inplace=True)
        scaler = joblib.load(self.scaler_path)
        self.features = self.features[scaler.feature_names_in_]
        self.features = pd.DataFrame(scaler.transform(self.features), columns=self.features.columns)
        self.features = self.features.iloc[:, self.feature_cols]
        model = joblib.load(self.model_path)
        return self.dict_classes[int(model.predict(self.features))]

    def extract_features(self, audio_path):
        smile = opensmile.Smile(
            feature_set = opensmile.FeatureSet.ComParE_2016,
            feature_level = opensmile.FeatureLevel.Functionals,
            num_workers = 4
        )
        self.features = pd.DataFrame(smile.process_file(audio_path))
        regex = re.compile(r"\[|\]|<", re.IGNORECASE)
        self.features.columns = [regex.sub("_", col) if any(x in str(col) for x in set(('[', ']', '<'))) else col for
                                  col in self.features.columns.values]