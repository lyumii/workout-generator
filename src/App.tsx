import { useState, useEffect, useRef } from "react";

function App() {
  const greeting: string = "Name, please";
  const [displayText, setDisplayText] = useState<string>("");
  const [name, setName] = useState<string>("");
  const [dash, setDash] = useState<boolean>(false);
  const indexRef = useRef(-1);
  const intervalRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    if (indexRef.current >= greeting.length) return;
    const interval = setInterval(() => {
      indexRef.current += 1;
      setDisplayText((prev) => prev + greeting.charAt(indexRef.current));
    }, 400);
    return () => clearInterval(interval);
  }, [displayText]);

  useEffect(() => {
    if (displayText === "Name, please") {
      intervalRef.current = setInterval(() => {
        setDash((prev) => !prev);
      }, 400);
    }
    return () => clearInterval(intervalRef.current!);
  }, [displayText]);

  const handleFocus = () => {
    clearInterval(intervalRef.current!);
    setDash(false);
  };

  return (
    <>
      <h1>Welcome!</h1>
      <p>{displayText}</p>
      <input
        type="text"
        placeholder={dash ? "___" : " "}
        onChange={(e) => setName(e.target.value)}
        onFocus={handleFocus}
      />
      <button>Sign in {name}</button>
    </>
  );
}

export default App;
