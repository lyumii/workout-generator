import { useState, useEffect, useRef } from "react";
import GenerateWorkout from "./GenerateWorkout";

function App() {
  const colors = [
    "#F5A623",
    "#FFD166",
    "#06D6A0",
    "#4ECDC4",
    "#C3E88D",
    "#FF6B6B",
    "#F78FB3",
    "#A29BFE",
    "#8C9EFF",
    "#67D5FF",
  ];

  const greeting: string = "Name, please";
  const [displayText, setDisplayText] = useState<string>("");
  const [name, setName] = useState<string>("");
  const [dash, setDash] = useState<boolean>(false);
  const [generate, setGenerate] = useState(false);
  const [color, setColor] = useState(colors[0]);

  const indexRef = useRef(-1);
  const intervalRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const headingRef = useRef<HTMLHeadingElement>(null);

  useEffect(() => {
    if (indexRef.current >= greeting.length) return;
    const interval = setInterval(() => {
      indexRef.current += 1;
      setDisplayText((prev) => prev + greeting.charAt(indexRef.current));
    }, 200);
    return () => clearInterval(interval);
  }, [displayText]);

  useEffect(() => {
    if (displayText === "Name, please") {
      intervalRef.current = setInterval(() => {
        setDash((prev) => !prev);
      }, 200);
    }
    return () => clearInterval(intervalRef.current!);
  }, [displayText]);

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

  const handleFocus = () => {
    clearInterval(intervalRef.current!);
    setDash(false);
  };

  return (
    <>
      {!generate && (
        <div className="notgeneratedcontainer">
          <div className="welcomecontainer">
            <div className="workoutimgcontainer">
              <img
                className="workoutimg"
                src="https://images.unsplash.com/photo-1557330359-ffb0deed6163?q=80&w=2670&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
                alt="workout equipment"
              />
            </div>
            <h1 ref={headingRef} style={{ color }}>
              Welcome!
            </h1>
            <p className="greet">{displayText}</p>
          </div>
          <form onSubmit={() => setGenerate(true)}>
            <input
              type="text"
              placeholder={dash ? "___" : " "}
              onChange={(e) => setName(e.target.value)}
              onFocus={handleFocus}
            />
            <button type="submit" style={{ backgroundColor: color }}>
              Sign in
            </button>
          </form>
        </div>
      )}
      {generate && <GenerateWorkout name={name} />}
    </>
  );
}

export default App;
