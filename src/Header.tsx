import { Link } from "react-router-dom";
import { useState, useEffect, useRef } from "react";
import colors from "./colors";
import { ColorContext } from "./ColorContext";

export default function Header({ children }: { children: React.ReactNode }) {
  const headingRef = useRef<HTMLHeadingElement>(null);
  const [color, setColor] = useState(colors[0]);

  useEffect(() => {
    const changeColor = () => {
      setColor((prev) => {
        let newColor = prev;
        while (newColor === prev) {
          newColor = colors[Math.floor(Math.random() * colors.length)];
        }
        return newColor;
      });
    };

    const heading = headingRef.current;
    if (heading) {
      heading.addEventListener("animationiteration", changeColor);
      return () =>
        heading.removeEventListener("animationiteration", changeColor);
    }
  }, []);

  return (
    <ColorContext.Provider value={color}>
      <div className="workoutimgcontainer">
        <img
          className="workoutimg"
          src="https://images.unsplash.com/photo-1557330359-ffb0deed6163?q=80&w=2670&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
          alt="workout equipment"
        />
      </div>

      <div className="notgeneratedcontainer">
        <h1 ref={headingRef} style={{ color, textDecoration: `none` }}>
          Time for gains!
        </h1>
        <p className="greet">What would you like to do today?</p>
      </div>

      <Link to="/">
        <span className="home" style={{ color }}>
          Home
        </span>
      </Link>

      {children}
    </ColorContext.Provider>
  );
}
