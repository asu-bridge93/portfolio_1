import pandas as pd  # データ操作・分析のためのライブラリ
import numpy as np  # 数値計算を効率化するライブラリ

# 機械学習のためのライブラリ
from sklearn.model_selection import train_test_split  # データを学習用・テスト用に分割
from sklearn.preprocessing import StandardScaler  # 特徴量を標準化（平均0、分散1に変換）
from sklearn.ensemble import RandomForestClassifier  # ランダムフォレスト分類器
from sklearn.metrics import accuracy_score, classification_report  # モデルの評価指標

# モデルの保存・管理に使用
import joblib  # 学習済みモデルの保存と読み込み
import os  # ファイル操作（フォルダ作成・パス管理）

DATA_PATH = "model_training/data/dataset.csv"

def load_data():
    """データセットを読み込み、特徴量のカラム名を変更して保存する"""
    from sklearn.datasets import load_iris
    iris = load_iris()

    # カラム名のスペースと括弧をアンダースコアに変換
    feature_names = [name.replace(" ", "_").replace("(", "").replace(")", "")[:-3] for name in iris['feature_names']]
    
    # DataFrame 作成
    data = pd.DataFrame(data=np.c_[iris['data'], iris['target']], columns=feature_names + ['target'])

    # ディレクトリ作成 & CSV 保存
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    data.to_csv(DATA_PATH, index=False)
    
    print(f"データを{DATA_PATH}に保存しました。")
    return data

MODEL_PATH = "app/models/trained_model.joblib" # appディレクトリについては後ほど作成します。

def create_model(data):
    """モデルを作成し、訓練する関数"""
    # 特徴量とターゲットに分割
    X = data.drop('target', axis=1)
    y = data['target']

    # TrainとTestに分割
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # 特徴量のスケーリング
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    x_test_scaled = scaler.transform(X_test)

    # モデルの作成と訓練
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)

    # モデルの評価
    y_pred = model.predict(x_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)

    print(f"モデルの精度: {accuracy:.4f}")
    print("分類レポート:")
    print(report)

    # モデル及び前処理オブジェクトの保存
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump({
        'model': model,
        'scaler': scaler,
        'feature_names': X.columns.tolist()
    }, MODEL_PATH)

    print(f"モデルを {MODEL_PATH} に保存しました")
    return model, scaler

if __name__ == "__main__":
    data = load_data()
    create_model(data)