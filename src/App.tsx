import { useState, useEffect, useRef } from "react";
import GenerateWorkout from "./GenerateWorkout";

function App() {
  const greeting: string = "Name, please";
  const [displayText, setDisplayText] = useState<string>("");
  const [name, setName] = useState<string>("");
  const [dash, setDash] = useState<boolean>(false);
  const [generate, setGenerate] = useState(false);
  const indexRef = useRef(-1);
  const intervalRef = useRef<ReturnType<typeof setTimeout> | null>(null);

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

  const handleFocus = () => {
    clearInterval(intervalRef.current!);
    setDash(false);
  };

  return (
    <>
      {!generate && (
        <div>
          <h1>Welcome!</h1>
          <p>{displayText}</p>
          <form onSubmit={() => setGenerate(true)}>
            <input
              type="text"
              placeholder={dash ? "___" : " "}
              onChange={(e) => setName(e.target.value)}
              onFocus={handleFocus}
            />
            <button type="submit">Sign in</button>
          </form>
        </div>
      )}
      {generate && <GenerateWorkout name={name} />}
    </>
  );
}

export default App;
