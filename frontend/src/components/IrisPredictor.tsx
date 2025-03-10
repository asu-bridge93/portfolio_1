import React, { useState } from "react";
import { predictIris } from "../api";
import "./IrisPredictor.css";  // スタイルを追加
import iris from "../images/iris.png"

const IrisPredictor: React.FC = () => {
  const [features, setFeatures] = useState<number[]>([5.1, 3.5, 1.4, 0.2]); // 初期値
  const [prediction, setPrediction] = useState<string | null>(null);
  const [isPredicting, setIsPredicting] = useState<boolean>(false); // 予測中フラグ

  const handleChange = (index: number, value: string) => {
    const newFeatures = [...features];
    newFeatures[index] = parseFloat(value) || 0;
    setFeatures(newFeatures);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsPredicting(true); // 予測開始時にローディング状態にする
    try {
      const result = await predictIris(features);
      setPrediction(result.prediction);
    } catch (error) {
      setPrediction("Error in prediction");
    } finally {
      setIsPredicting(false); // 予測が終わったらローディング解除
    }
  };

  const featureNames = ["Sepal Length", "Sepal Width", "Petal Length", "Petal Width"];

  return (
    <div className="predictor-container">
      <h2 className="header">Iris Species Predictor</h2>
      
      {/* あやめの画像を横に並べる */}
      <div className="image-gallery">
        <img src={iris} alt="Iris 2" />
      </div>

      <form className="predictor-form" onSubmit={handleSubmit}>
        {features.map((value, index) => (
          <div key={index} className="form-group">
            <div className="feature-label">
              <b>{featureNames[index]}:</b>
            </div>
            <input
              className="slider"
              type="range"
              min="0"
              max="10"
              step="0.1"
              value={value}
              onChange={(e) => handleChange(index, e.target.value)}
            />
            <div className="slider-value"><b>{value.toFixed(1)}</b></div>
          </div>
        ))}
        <button className="submit-btn" type="submit" disabled={isPredicting}>
          {isPredicting ? "Predicting..." : "Predict"}
        </button>
      </form>

      {prediction && <h3 className="prediction-result">Prediction: {prediction}</h3>}
    </div>
  );
};

export default IrisPredictor;