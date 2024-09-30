import React, { useState } from 'react';
import axios from '../axiosConfig';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
  Tooltip,
  Legend,
  Title,
} from 'chart.js';
import type { ChartOptions } from 'chart.js';

ChartJS.register(
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
  Tooltip,
  Legend,
  Title
);

interface PriceData {
  dates: string[];
  prices: number[];
}

interface PredictionResponse {
  prediction: PriceData;
  historical: PriceData;
  error?: string;
}

const ModelTrainer: React.FC = () => {
  const [isTraining, setIsTraining] = useState(false);
  const [predictions, setPredictions] = useState<PriceData | null>(null);
  const [historical, setHistorical] = useState<PriceData | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleTrainModel = async () => {
    setIsTraining(true);
    setError(null);
    try {
      const response = await axios.post('/train/');
      console.log(response.data);
      alert('Model trained successfully!');
    } catch (err) {
      console.error(err);
      setError('An error occurred while training the model.');
    } finally {
      setIsTraining(false);
    }
  };

  const handlePredict = async () => {
    setError(null);
    try {
      const response = await axios.get<PredictionResponse>('/predict/', {
        params: { days: 30 },
      });

      console.log('Predict response data:', response.data);

      if (response.data.error) {
        setError(response.data.error);
        return;
      }

      setPredictions(response.data.prediction);
      setHistorical(response.data.historical);
    } catch (err) {
      console.error(err);
      setError('An error occurred while fetching predictions.');
    }
  };

  const historicalPrices = historical?.prices.map(Number) || [];
  const historicalDates = historical?.dates || [];
  const predictionPrices = predictions?.prices.map(Number) || [];
  const predictionDates = predictions?.dates || [];

  // Prepare datasets with clear separation
  const data = {
    labels: [...historicalDates, ...predictionDates],
    datasets: [
      {
        label: 'Dados Históricos',
        data: historicalPrices,
        borderColor: 'rgb(59, 130, 246)', // Tailwind blue-500
        backgroundColor: 'rgba(59, 130, 246, 0.2)', // Lower opacity
        borderWidth: 1, // Thinner line
        pointRadius: 1, // No points to keep the line clean
        fill: false,
      },
      {
        label: 'Previsões',
        data: new Array(historicalPrices.length).fill(null).concat(predictionPrices),
        borderColor: 'rgb(34, 197, 94)', // Tailwind green-500
        backgroundColor: 'rgba(34, 197, 94, 0.2)', // Lower opacity
        borderWidth: 1, // Slightly thicker line to emphasize predictions
        pointRadius: 1, // Add small points for prediction
        pointBackgroundColor: 'rgb(34, 197, 94)',
        pointBorderWidth: 1,
        fill: false,
      },
    ],
  };
  

  const options: ChartOptions<'line'> = {
    responsive: true,
    maintainAspectRatio: false,
    interaction: {
      mode: 'index',
      intersect: false,
    },
    plugins: {
      legend: {
        position: 'top',
        labels: {
          font: {
            size: 14,
          },
        },
      },
      title: {
        display: true,
        text: 'BTC-USD Preços Históricos e Previsões',
        font: {
          size: 20,
        },
      },
      tooltip: {
        mode: 'index',
        intersect: false,
      },
    },
    scales: {
      x: {
        title: {
          display: true,
          text: 'Data',
          font: {
            size: 16,
          },
        },
        ticks: {
          maxRotation: 45,
          minRotation: 45,
          maxTicksLimit: 10, // Adjust as needed
        },
        grid: {
          display: false,
        },
      },
      y: {
        title: {
          display: true,
          text: 'Preço (USD)',
          font: {
            size: 16,
          },
        },
        ticks: {
          callback: function (value) {
            return '$' + value.toLocaleString();
          },
        },
        grid: {
          color: 'rgba(200, 200, 200, 0.2)',
        },
      },
    },
  };

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Navbar */}
      <nav className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <div className="text-xl font-semibold text-gray-800">
            CryptoPredictor
          </div>
          <div>
            <a href="#" className="text-gray-800 hover:text-blue-500 mx-4">
              Home
            </a>
            <a href="#" className="text-gray-800 hover:text-blue-500 mx-4">
              Sobre
            </a>
            <a href="#" className="text-gray-800 hover:text-blue-500 mx-4">
              Contato
            </a>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="w-screen mx-auto p-6">
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-3xl font-bold mb-4 text-center">
            Predição de Preço BTC-USD 
          </h2>

          <div className="flex justify-center space-x-4 mb-6">
            <button
              onClick={handleTrainModel}
              className={`px-6 py-2 rounded ${
                isTraining ? 'bg-gray-400 cursor-not-allowed' : 'bg-blue-500 hover:bg-blue-600'
              } text-white font-semibold`}
              disabled={isTraining}
            >
              {isTraining ? 'Treinando...' : 'Treinar Modelo'}
            </button>

            <button
              onClick={handlePredict}
              className="px-6 py-2 bg-green-500 hover:bg-green-600 rounded text-white font-semibold"
            >
              Predição
            </button>
          </div>

          {error && <p className="text-red-500 mb-4 text-center">{error}</p>}

          {(historicalPrices.length > 0 || predictionPrices.length > 0) ? (
            <>
              <div className="w-full h-96">
                <Line data={data} options={options} />
              </div>

              {/* Prediction Card */}
              {predictionPrices.length > 0 && (
                <div className="mt-8">
                  <h3 className="text-xl font-semibold mb-4 text-center">
                    Valores Previstos
                  </h3>
                  <div className="bg-gray-100 p-4 rounded-lg shadow">
                    <table className="min-w-full table-auto">
                      <thead>
                        <tr className="bg-gray-200">
                          <th className="px-4 py-2 text-left text-gray-600 font-medium">Date</th>
                          <th className="px-4 py-2 text-left text-gray-600 font-medium"> Preço Previsto (USD)</th>
                        </tr>
                      </thead>
                      <tbody>
                        {predictionDates.map((date, index) => (
                          <tr key={index} className="border-b">
                            <td className="px-4 py-2 text-gray-700">{date}</td>
                            <td className="px-4 py-2 text-gray-700">${predictionPrices[index].toFixed(2)}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}
            </>
          ) : (
            <p className="text-center text-gray-600">
              Clique Prever para gerar o gráfico e as previsões.
            </p>
          )}
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-white shadow mt-10">
        <div className="max-w-7xl mx-auto px-4 py-6 text-center text-gray-600">
          &copy; {new Date().getFullYear()} Ólin Costa
        </div>
      </footer>
    </div>
  );
};

export default ModelTrainer;
