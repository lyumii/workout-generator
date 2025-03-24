import BrowseWorkouts from "./BrowseWorkouts";
import ChoiceButtons from "./ChoiceButtons";
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
    <Routes>
      <Route
        path="/"
        element={
          <>
            <Header color={color} headingRef={headingRef} />
            <ChoiceButtons color={color} />
          </>
        }
      />
      <Route path="/browse" element={<BrowseWorkouts />} />
    </Routes>
  );
}

export default App;
