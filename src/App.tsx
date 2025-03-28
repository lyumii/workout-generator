import BrowseWorkoutHistory from "./BrowseWorkoutHistory";
import ChoiceButtons from "./ChoiceButtons";
import GenerateWorkout from "./GenerateWorkout";
import Header from "./Header";
import colors from "./colors";
import { useState, useEffect, useRef } from "react";
import { Route, Routes } from "react-router-dom";

function App() {
  const headingRef = useRef<HTMLHeadingElement>(null);
  const [color, setColor] = useState(colors[0]);

  useEffect(() => {
    const changeColor = () => {
      setColor(colors[Math.floor(Math.random() * colors.length)]);
    };

    const heading = headingRef.current;
    if (heading) {
      heading.addEventListener("animationiteration", changeColor);
      return () =>
        heading.removeEventListener("animationiteration", changeColor);
    }
  }, []);

  return (
    <main className="main">
      <Header color={color} headingRef={headingRef} />
      <Routes>
        <Route
          path="/"
          element={
            <>
              <ChoiceButtons color={color} />
            </>
          }
        />
        <Route path="/browse" element={<BrowseWorkoutHistory />} />
        <Route path="/generated" element={<GenerateWorkout />} />
      </Routes>
    </main>
  );
}

export default App;
