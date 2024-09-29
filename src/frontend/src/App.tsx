// src/App.tsx

import React from 'react';
import ModelTrainer from './components/ModelTrainer';

const App: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <ModelTrainer />
    </div>
  );
};

export default App;
