import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from lightgbm import LGBMClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os
import warnings

warnings.filterwarnings("ignore")

DATA_PATH = "model_training/data/Loan_default.csv"
MODEL_PATH = "app/model/loan_default_model.joblib"

def load_and_preprocess_data(data_path=DATA_PATH):
    """データセットを読み込み、前処理を行う"""
    print(f"データを読み込んでいます: {data_path}")
    
    try:
        data = pd.read_csv(data_path)
        print(f"データの形状: {data.shape}")
        
        # カテゴリカル変数のエンコーディング
        le = LabelEncoder()
        obj_col = ['HasCoSigner', 'LoanPurpose', 'HasDependents', 'HasMortgage', 
                   'MaritalStatus', 'EmploymentType', 'Education']
        
        for col in obj_col:
            data[col] = le.fit_transform(data[col])
        
        # 不要なカラムの削除
        if 'LoanID' in data.columns:
            data = data.drop(['LoanID'], axis=1)
        
        print("データの前処理が完了しました。")
        return data
    
    except Exception as e:
        print(f"データの読み込みまたは前処理中にエラーが発生しました: {e}")
        raise

def create_model(data):
    """モデルを作成し、訓練する関数"""
    # 特徴量とターゲットに分割
    X = data.drop('Default', axis=1)
    y = data['Default']
    
    print(f"特徴量の数: {X.shape[1]}")
    print(f"クラス分布: \n{y.value_counts(normalize=True)}")
    
    # TrainとTestに分割
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    print(f"訓練データサイズ: {X_train.shape}, テストデータサイズ: {X_test.shape}")
    
    # LightGBMモデルの作成と訓練
    model = LGBMClassifier(random_state=42)
    print("モデルをトレーニングしています...")
    model.fit(X_train, y_train)
    
    # モデルの評価
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    
    print(f"モデルの精度: {accuracy:.4f}")
    print("分類レポート:")
    print(report)
    
    # 特徴量の重要度を表示
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("特徴量の重要度:")
    print(feature_importance.head(10))
    
    # モデル及び前処理オブジェクトの保存
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump({
        'model': model,
        'feature_names': X.columns.tolist()
    }, MODEL_PATH)
    
    print(f"モデルを {MODEL_PATH} に保存しました")
    return model

if __name__ == "__main__":
    # データディレクトリの作成
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    
    # データの読み込みと前処理
    data = load_and_preprocess_data()
    
    # モデルの作成と訓練
    model = create_model(data)