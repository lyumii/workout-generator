import { useState } from "react";
import { usePulseColor } from "./ColorContext";
import { useNavigate } from "react-router-dom";

export default function ChoiceButtons() {
  const navigate = useNavigate();
  const [prompt, setPrompt] = useState("");
  const color = usePulseColor();

  const sendGenerateRequest = async (
    event: React.FormEvent<HTMLFormElement>
  ) => {
    event.preventDefault();
    try {
      const res = await fetch("http://localhost:5000/generate-workout", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt }),
      });
      if (!res.ok) {
        throw new Error(`failed to send prompt`);
      }
      const data = await res.json();
      navigate("/generated", {
        state: {
          workouts: data,
          prompt: prompt,
        },
      });
    } catch (error) {
      console.log(`smth went wrong`, error);
    }
  };

  return (
    <div className="notgeneratedcontainer">
      <form onSubmit={sendGenerateRequest}>
        <input
          type="text"
          onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
            setPrompt(e.target.value)
          }
        />
        <button type="submit" style={{ backgroundColor: color }}>
          Ask for a workout
        </button>
        <p className="orparagraph"> • or • </p>
        <button
          onClick={(e) => {
            e.preventDefault();
            navigate("/browse");
          }}
          style={{ backgroundColor: color }}
        >
          Browse workout history
        </button>
      </form>
    </div>
  );
}
