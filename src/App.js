import React, { useEffect, useState } from "react";
import { Chessboard } from "react-chessboard";
import { db } from "./firebase";
import { doc, onSnapshot } from "firebase/firestore";
import { Chess } from "chess.js";
import './App.css';

function App() {
  const [game, setGame] = useState(new Chess());
  const [boardSize, setBoardSize] = useState(400); // taille par défaut du plateau

  useEffect(() => {
    console.log("Setting up Firestore subscription");
    const unsubscribe = onSnapshot(doc(db, "games", "game2"), (doc) => {
      const data = doc.data();
      if (data) {
        const chess = new Chess();
        data.moves.forEach(move => {
          // Apply only valid moves
          if (chess.move(move)) {
            chess.move(move);
          }
        });
        setGame(chess);
      }
    });

    return () => unsubscribe();
  }, []);

  const resetGame = async () => {
    const newGame = new Chess();
    await setDoc(doc(db, "games", "game2"), { moves: [] });
    setGame(newGame);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1 className="App-title">Chess Game</h1>
      </header>
      <div className="chessboard-container" style={{ width: `${boardSize}px`, height: `${boardSize}px` }}>
        <Chessboard
          position={game.fen()}
          allowDrag={() => false} // Désactiver le drag & drop
          allowDrop={() => false} // Désactiver le drag & drop
        />
      </div>
      <div>
        <label htmlFor="boardSize">Board Size: </label>
        <input
          id="boardSize"
          type="range"
          min="200"
          max="800"
          value={boardSize}
          onChange={(e) => setBoardSize(e.target.value)}
        />
      </div>
      <div>
        <button className="reset-button" onClick={resetGame}>Reset</button>
      </div>
    </div>
  );
}

export default App;
