import React, { useState, useRef, useEffect } from 'react';

const MagicCubeVisualizer = () => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentFrame, setCurrentFrame] = useState(0);
  const [totalFrames, setTotalFrames] = useState(0);
  const [playbackSpeed, setPlaybackSpeed] = useState(1);
  const [stateData, setStateData] = useState(null);
  const animationRef = useRef(null);
  
  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    const reader = new FileReader();
    
    reader.onload = (e) => {
      try {
        const data = JSON.parse(e.target.result);
        setStateData(data);
        setTotalFrames(data.states.length);
        setCurrentFrame(0);
        setIsPlaying(false);
      } catch (error) {
        console.error('Error parsing file:', error);
      }
    };
    
    reader.readAsText(file);
  };

  useEffect(() => {
    let lastTime = 0;
    const frameInterval = (1000 / 30) / playbackSpeed;

    if (isPlaying && stateData) {
      const animate = (currentTime) => {
        if (!lastTime) lastTime = currentTime;
        
        const deltaTime = currentTime - lastTime;
        
        if (deltaTime >= frameInterval) {
          setCurrentFrame(prev => {
            if (prev >= totalFrames - 1) {
              setIsPlaying(false);
              return prev;
            }
            return prev + 1;
          });
          lastTime = currentTime;
        }
        
        animationRef.current = requestAnimationFrame(animate);
      };
      
      animationRef.current = requestAnimationFrame(animate);
    }
    
    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [isPlaying, totalFrames, stateData, playbackSpeed]);

  const renderCubeLayer = (layer, layerIndex) => (
    <div key={layerIndex} className="mb-4">
      <div className="text-sm font-semibold mb-1">Layer {layerIndex + 1}</div>
      {layer.map((row, rowIndex) => (
        <div key={rowIndex} className="flex">
          {row.map((value, colIndex) => (
            <div
              key={colIndex}
              className="w-12 h-12 border border-gray-300 flex items-center justify-center m-px bg-white"
            >
              {value}
            </div>
          ))}
        </div>
      ))}
    </div>
  );

  const renderCurrentState = () => {
    if (!stateData || !stateData.states[currentFrame]) {
      return <div className="text-gray-500">No data loaded</div>;
    }

    const currentState = stateData.states[currentFrame];
    
    return (
      <div className="flex flex-col items-center">
        <div className="mb-4 text-xl font-bold">
          Value: {currentState.value}/109
        </div>
        {currentState.cube.map((layer, i) => renderCubeLayer(layer, i))}
      </div>
    );
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="mb-6 flex justify-center">
        <label className="bg-blue-500 text-white px-4 py-2 rounded cursor-pointer hover:bg-blue-600">
          📁 Load Experiment
          <input
            type="file"
            onChange={handleFileUpload}
            accept=".json"
            className="hidden"
          />
        </label>
      </div>

      <div className="bg-gray-50 p-6 rounded-lg shadow-sm">
        {renderCurrentState()}
      </div>

      <div className="mt-6 flex items-center gap-4">
        <button
          onClick={() => setIsPlaying(!isPlaying)}
          className="px-4 py-2 bg-gray-100 rounded hover:bg-gray-200"
        >
          {isPlaying ? "⏸️" : "▶️"}
        </button>
        
        <button
          onClick={() => {
            setCurrentFrame(0);
            setIsPlaying(false);
          }}
          className="px-4 py-2 bg-gray-100 rounded hover:bg-gray-200"
        >
          🔄
        </button>

        <input
          type="range"
          min={0}
          max={Math.max(0, totalFrames - 1)}
          value={currentFrame}
          onChange={(e) => {
            setCurrentFrame(parseInt(e.target.value));
            if (isPlaying) setIsPlaying(false);
          }}
          className="flex-1"
        />

        <select
          value={playbackSpeed}
          onChange={(e) => setPlaybackSpeed(parseFloat(e.target.value))}
          className="px-3 py-2 border rounded"
        >
          <option value={0.5}>0.5x</option>
          <option value={1}>1x</option>
          <option value={2}>2x</option>
          <option value={4}>4x</option>
        </select>
      </div>

      <div className="mt-4 text-sm text-gray-600">
        Frame: {currentFrame + 1} / {totalFrames || 0}
      </div>
    </div>
  );
};

export default MagicCubeVisualizer;