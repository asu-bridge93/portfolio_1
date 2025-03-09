import joblib
import numpy as np
import os
from typing import Dict, List, Union, Any

class ModelWrapper:
    """AIモデルのラッパークラス"""

    def __init__(self, model_path: str = "app/models/trained_model.joblib"):
        # モデルを初期化をする
        self.model_path = model_path
        self._load_model()
    
    def _load_model(self):
        # 保存されたモデルを読み込む
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"モデルファイル {self.model_path} が見つかりません。")
        
        model_data = joblib.load(self.model_path)
        self.model = model_data['model']
        self.scaler = model_data['scaler']
        self.feature_names = model_data['feature_names']

    def predict(self, features: Dict[str, float]) -> Dict[str, Any]:
        # 入力特徴量からモデルの予測を行う
        # Args: features: 特徴量の辞書（特徴量名、数値）
        # Returns: 結果の辞書（予測結果、信頼度）

        input_features = []
        for feature in self.feature_names:
            if feature not in features:
                raise ValueError(f"特徴量'{feature}'が入力に含まれていません")
            input_features.append(features[feature])
        
        # 入力特徴量の配列化とスケーリング
        X = np.array([input_features])
        X_scaled = self.scaler.transform(X)

        # モデルの予測
        prediction = self.model.predict(X_scaled)[0]
        probabilities = self.model.predict_proba(X_scaled)[0]

        # 予測結果をconvert
        iris_classes = {0: 'setosa', 1: 'versicolor', 2: 'virginica'}
        predicted_class = iris_classes.get(prediction, str(prediction))

        # 結果をformat
        result = {
            'prediction': predicted_class,
            'prediction_id': int(prediction),
            'confidence': float(np.max(probabilities)),
            'probabilities': {
                iris_classes.get(i, str(i)): float(prob)
                for i, prob in enumerate(probabilities)
            }
        }

        return result
